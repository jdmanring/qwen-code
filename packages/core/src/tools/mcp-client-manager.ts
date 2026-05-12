/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import type { Config, MCPServerConfig } from '../config/config.js';
import { isSdkMcpServerConfig } from '../config/config.js';
import type { ToolRegistry } from './tool-registry.js';
import {
  McpClient,
  MCPDiscoveryState,
  MCPServerStatus,
  populateMcpServerCommand,
  removeMCPServerStatus,
} from './mcp-client.js';
import type { SendSdkMcpMessage } from './mcp-client.js';
import { getErrorMessage } from '../utils/errors.js';
import { createDebugLogger } from '../utils/debugLogger.js';
import { recordStartupEvent } from '../utils/startupEventSink.js';
import type { EventEmitter } from 'node:events';
import type { ReadResourceResult } from '@modelcontextprotocol/sdk/types.js';

const debugLogger = createDebugLogger('MCP');
export const RUNTIME_MCP_IF_ABSENT_CONFIG_FLAG = '__qwenRuntimeMcpIfAbsent';

/**
 * Configuration for MCP health monitoring
 */
export interface MCPHealthMonitorConfig {
  /** Health check interval in milliseconds (default: 30000ms) */
  checkIntervalMs: number;
  /** Number of consecutive failures before marking as disconnected (default: 3) */
  maxConsecutiveFailures: number;
  /** Enable automatic reconnection (default: true) */
  autoReconnect: boolean;
  /** Delay before reconnection attempt in milliseconds (default: 5000ms) */
  reconnectDelayMs: number;
}

const DEFAULT_HEALTH_CONFIG: MCPHealthMonitorConfig = {
  checkIntervalMs: 30000, // 30 seconds
  maxConsecutiveFailures: 3,
  autoReconnect: true,
  reconnectDelayMs: 5000, // 5 seconds
};

/**
 * Manages the lifecycle of multiple MCP clients, including local child processes.
 * This class is responsible for starting, stopping, and discovering tools from
 * a collection of MCP servers defined in the configuration.
 */
export class McpClientManager {
  private clients: Map<string, McpClient> = new Map();
  private readonly toolRegistry: ToolRegistry;
  private readonly cliConfig: Config;
  private discoveryState: MCPDiscoveryState = MCPDiscoveryState.NOT_STARTED;
  private readonly eventEmitter?: EventEmitter;
  private readonly sendSdkMcpMessage?: SendSdkMcpMessage;
  private healthConfig: MCPHealthMonitorConfig;
  private healthCheckTimers: Map<string, NodeJS.Timeout> = new Map();
  private consecutiveFailures: Map<string, number> = new Map();
  private isReconnecting: Map<string, boolean> = new Map();
  private serverDiscoveryPromises: Map<string, Promise<void>> = new Map();

  /**
   * Per connected server, the single-session "connected config key" of the
   * config it was last connected with — see {@link singleSessionConnectedKeyOf}.
   * Single-session path only; pool mode tracks transport identity via
   * `pooledConnections[].id` and its own `desiredIds` diff.
   * Lets `discoverAllMcpToolsIncremental` detect an in-place config change to an
   * already-connected server and reconnect it, instead of leaving it on the
   * stale config. Unlike the transport-only `connectionIdOf`, this key also
   * covers the discovery-time filters (trust / includeTools / excludeTools) so
   * editing those re-applies them. Set on successful connect; cleared on every
   * teardown path so a stale key can't mask a later change.
   */
  private readonly connectedConfigKeys = new Map<string, string>();

  /**
   * Budget bookkeeping. Slots are reserved synchronously by server name
   * inside the discovery loop BEFORE any `await client.connect()`, so
   * `Promise.all(discoveryPromises)` cannot interleave a second connect
   * past the cap. `enforce` mode refuses past the cap; `warn` mode
   * over-reserves so accounting reflects the configured set; `off`
   * doesn't reserve at all.
   */
  private readonly reservedSlots = new Set<string>();
  private readonly clientBudget?: number;
  private readonly budgetMode: McpBudgetMode;
  /**
   * names whose
   * slot was freshly reserved (not `'already_held'`) by an
   * in-flight `discoverMcpToolsForServerInternal` call. Read by
   * `runWithDiscoveryTimeout`'s timeout handler to decide whether
   * to release the slot on hard timeout — fresh reservations
   * release (server never connected, slot shouldn't permanently
   * block other servers); `'already_held'` reconnects keep their
   * slot (operator's previously-healthy server shouldn't be
   * permanently demoted by a transient timeout).
   *
   * Lifetime: `add` after `tryReserveSlot` returns `'reserved'`
   * with the `.has` guard, `delete` in success / catch / finally
   * cleanup. Idempotent — multiple deletes are no-ops.
   */
  private readonly freshReservations = new Set<string>();
  /**
   * Servers refused during the most recent `discoverAllMcpTools*` pass.
   * Reset at the start of each pass; survives between passes so a
   * snapshot taken between discoveries still shows the last set of
   * refusals to operators.
   */
  private lastRefusedServerNames: string[] = [];
  /**
   * transport family (`stdio`/`http`/...) resolved for each
   * entry in `lastRefusedServerNames`, captured at refusal time. The
   * `'refused_batch'` event payload includes the per-server transport
   * so dashboards can break down "which kind of servers got refused"
   * without re-walking config.
   *
   * Lifetime mirrors `lastRefusedServerNames`: reset at the start of
   * each `discoverAllMcpTools*` pass + on `stop()` + on
   * `dropRefusalEntry` (operator removed/disconnected the server).
   * NOT cleared on `emitRefusedBatchIfAny` — the snapshot-visible
   * refusal state survives between passes per the contract,
   * so a snapshot taken between passes still reports the last
   * refusal set with correct transport metadata. The push-event
   * idempotency invariant is held by the separate
   * `pendingRefusalNames` queue, not by clearing this map.
   */
  private lastRefusedTransports = new Map<string, McpTransportKind>();
  /**
   * queue of refusal names NOT YET emitted as a push event.
   * `lastRefusedServerNames` is the snapshot-visible state and MUST
   * survive between passes (contract). The push-event path
   * needs separate accounting so a length-1 batch fired by a single-
   * server / readResource refusal doesn't get re-emitted by the
   * bulk-pass end-of-pass call. `refuseAndLog` adds to both;
   * `emitRefusedBatchIfAny` drains and clears this set without
   * touching `lastRefusedServerNames`. Empty whenever there are no
   * unsent refusals, regardless of pass.
   */
  private pendingRefusalNames = new Set<string>();
  /**
   * hysteresis state for `'budget_warning'` events. `true`
   * means "next 75% upward crossing fires"; `false` means "warning
   * already fired, waiting for ratio to drop below 37.5% to re-arm".
   * Stays `true` permanently in `off` mode (the state machine
   * short-circuits before touching it). Initial value `true` so the
   * first crossing during a session always fires.
   */
  private warnArmed = true;
  /**
   * re-entrant counter that
   * tracks whether a bulk discovery pass is currently in flight.
   * Incremented on entry to `discoverAllMcpTools` /
   * `discoverAllMcpToolsIncremental`; decremented in the matching
   * `finally`. While > 0, `emitRefusedBatchIfAny` short-circuits so
   * per-server refusals queue up; the bulk pass's own end-of-pass
   * call (which runs AFTER `bulkPassDepth--`) drains the queue once
   * as a coalesced batch — preserving the documented "one batch per
   * pass" contract regardless of which inner code path enqueued the
   * refusals (`discoverMcpToolsForServerInternal` from incremental,
   * inline `refuseAndLog` from legacy bulk).
   *
   * Counter rather than boolean to defend against re-entry (a future
   * code path that nests bulk passes — e.g. a discovery hook that
   * itself triggers reload — wouldn't accidentally clear the flag
   * mid-outer-pass).
   */
  private bulkPassDepth = 0;
  /**
   * optional callback set at construction time OR via
   * `setOnBudgetEvent` after construction. When non-`null` and
   * `budgetMode !== 'off'`, the manager fires it on every threshold
   * crossing or non-empty refusal batch. Decouples core from ACP
   * wire types; `acpAgent.newSessionConfig` provides the adapter
   * that translates events into `connection.extNotification`.
   *
   * The setter exists because the production construction path
   * (`ToolRegistry` constructor → `loadCliConfig`) doesn't expose a
   * hook to thread the callback through. acpAgent registers the
   * callback after `loadCliConfig` returns but BEFORE
   * `config.initialize()` fires the first discovery — so no events
   * are missed.
   */
  private onBudgetEvent?: (event: McpBudgetEvent) => void;

  /**
   * when present, non-SDK MCP server discovery
   * delegates to the workspace-shared pool instead of spawning a
   * per-session `McpClient`. Tracked here so `disconnectServer` /
   * `stop` can `release` the pool reference cleanly without leaking
   * refs (the pool's drain timer kicks in when refs hit zero).
   *
   * SDK MCP servers (`isSdkMcpServerConfig`) always bypass the pool
   * — the `sendSdkMcpMessage` callback is per-session by design and
   * the pool's transport is workspace-level. Per-server gating in
   * `discoverMcpToolsForServer` keeps the legacy path for SDK MCP.
   */
  private readonly pool?: import('./mcp-transport-pool.js').McpTransportPool;
  private readonly pooledConnections = new Map<
    string,
    import('./mcp-pool-entry.js').PooledConnection
  >();
  /**
   * re-entrancy guard
   * for `discoverAllMcpToolsViaPool`. Two passes interleaving (full
   * + incremental, or two incrementals) could see
   * `pooledConnections.has(name) === false` simultaneously and both
   * call `pool.acquire`, with the second `set(name, conn2)` silently
   * overwriting the first → conn1 leaks (refcount never reaches 0,
   * drain timer never fires). The mutex serializes passes; a second
   * caller awaits the same promise and sees the resolved state.
   */
  private discoveryInFlight?: Promise<void>;

  /**
   * set true by
   * `stop()` when its 5s shutdown-grace timer wins the race against
   * `discoveryInFlight`. The in-flight discovery pass checks this
   * flag before calling `pooledConnections.set(...)` so a late-
   * resolving `pool.acquire` (whose 30s default timeout exceeds the
   * shutdown cap) doesn't orphan an entry by re-populating the Map
   * after `releaseAllPooledConnections` cleared it.
   */
  private stopTimedOut = false;

  constructor(
    config: Config,
    toolRegistry: ToolRegistry,
    eventEmitter?: EventEmitter,
    sendSdkMcpMessage?: SendSdkMcpMessage,
    healthConfig?: Partial<MCPHealthMonitorConfig>,
  ) {
    this.cliConfig = config;
    this.toolRegistry = toolRegistry;

    this.eventEmitter = eventEmitter;
    this.sendSdkMcpMessage = sendSdkMcpMessage;
    this.healthConfig = { ...DEFAULT_HEALTH_CONFIG, ...healthConfig };
  }

  /**
   * Initiates the tool discovery process for all configured MCP servers.
   * It connects to each server, discovers its available tools, and registers
   * them with the `ToolRegistry`.
   */
  async discoverAllMcpTools(cliConfig: Config): Promise<void> {
    if (!cliConfig.isTrustedFolder()) {
      return;
    }
    await this.stop();

    const servers = populateMcpServerCommand(
      this.cliConfig.getMcpServers() || {},
      this.cliConfig.getMcpServerCommand(),
    );

    this.discoveryState = MCPDiscoveryState.IN_PROGRESS;

    this.eventEmitter?.emit('mcp-client-update', this.clients);
    const discoveryPromises = Object.entries(servers).map(
      async ([name, config]) => {
        // Skip disabled servers
        if (cliConfig.isMcpServerDisabled(name)) {
          debugLogger.debug(`Skipping disabled MCP server: ${name}`);
          return;
        }

        // For SDK MCP servers, pass the sendSdkMcpMessage callback
        const sdkCallback = isSdkMcpServerConfig(config)
          ? this.sendSdkMcpMessage
          : undefined;

        const client = new McpClient(
          name,
          config,
          this.toolRegistry,
          this.cliConfig.getPromptRegistry(),
          this.cliConfig.getWorkspaceContext(),
          this.cliConfig.getDebugMode(),
          sdkCallback,
        );
        this.clients.set(name, client);

        this.eventEmitter?.emit('mcp-client-update', this.clients);
        try {
          await client.connect();
          await client.discover(cliConfig);
          this.eventEmitter?.emit('mcp-client-update', this.clients);
          try {
            await client.connect();
            await client.discover(cliConfig);
            // Record the fingerprint of the config this client connected with
            // so a later `discoverAllMcpToolsIncremental` can detect an
            // in-place config change. The single-session reconcile guard
            // skips a still-connected server whose fingerprint is `undefined`,
            // so a bulk connect (this path is reached via legacy blocking boot
            // + extension reload) that omitted this would silently drop a
            // subsequent edit — same invariant the per-server path upholds.
            this.connectedConfigKeys.set(
              name,
              this.singleSessionConnectedKeyOf(name, config),
            );
            this.eventEmitter?.emit('mcp-client-update', this.clients);
          } catch (error) {
            // zombie slot leak.
            // `tryReserveSlot(name)` reserved a slot above. If `connect()`
            // throws, the slot would stay reserved forever and the client
            // entry would stay in `this.clients` in a never-CONNECTED
            // state, blocking other servers in `enforce` mode until a
            // full discovery restart. Release both so the budget cap
            // reflects actual usable capacity.
            //
            // Slot bookkeeping in this bulk path is partially redundant
            // with `await this.stop()` at the top of
            // `discoverAllMcpTools` (line ~320) — the next bulk run
            // wipes `reservedSlots` regardless. But the SAME catch
            // ALSO needs to handle the transport (see below): the
            // client object held by `clients.delete(name)` only had
            // its tracking reference removed, not its underlying
            // transport closed. Leaving the orphan transport alive
            // would leak the stdio child / WebSocket / HTTP socket
            // for the rest of the process — `stop()` can't clean it
            // because we just removed it from the map.
            //
            // The per-server reconnect path
            // (`discoverMcpToolsForServerInternal`) keeps the slot
            // when `weReservedSlot === false` so health-monitor retry
            // doesn't have to compete for capacity — different
            // lifecycle, different contract. Bulk path always releases
            // because every server is "fresh" here (preceded by
            // stop()).
            //
            // also
            // call `await client.disconnect()` BEFORE dropping the
            // reference. R7 #3 fixed the analogous leak in the
            // per-server path; this is the bulk-path mirror. Errors
            // intentionally swallowed (we're already in a discovery-
            // failure catch; double-throwing would lose the original
            // error context).
            try {
              await client.disconnect();
            } catch {
              // best-effort transport cleanup
            }
            this.releaseSlotName(name);
            this.clients.delete(name);
            this.eventEmitter?.emit('mcp-client-update', this.clients);
            // Log the error but don't let a single failed server stop the others
            debugLogger.error(
              `Error during discovery for server '${name}': ${getErrorMessage(
                error,
              )}`,
            );
          }
        },
      );

    await Promise.all(discoveryPromises);
    this.discoveryState = MCPDiscoveryState.COMPLETED;
  }

  /**
   * Connects to a single MCP server and discovers its tools/prompts.
   * The connected client is tracked so it can be closed by {@link stop}.
   *
   * This is primarily used for on-demand re-discovery flows (e.g. after OAuth).
   */
  async discoverMcpToolsForServer(
    serverName: string,
    cliConfig: Config,
  ): Promise<void> {
    const inProgressDiscovery = this.serverDiscoveryPromises.get(serverName);
    if (inProgressDiscovery) {
      await inProgressDiscovery;
      return;
    }

    const discoveryPromise = this.discoverMcpToolsForServerInternal(
      serverName,
      cliConfig,
    );
    this.serverDiscoveryPromises.set(serverName, discoveryPromise);

    try {
      await discoveryPromise;
    } finally {
      if (this.serverDiscoveryPromises.get(serverName) === discoveryPromise) {
        this.serverDiscoveryPromises.delete(serverName);
      }
    }
  }

  private async discoverMcpToolsForServerInternal(
    serverName: string,
    cliConfig: Config,
  ): Promise<void> {
    const servers = populateMcpServerCommand(
      this.cliConfig.getMcpServers() || {},
      this.cliConfig.getMcpServerCommand(),
    );
    const serverConfig = servers[serverName];
    if (!serverConfig) {
      return;
    }

    this.stopHealthCheck(serverName);

    // Ensure we don't leak an existing connection for this server.
    const existingClient = this.clients.get(serverName);
    if (existingClient) {
      try {
        await existingClient.disconnect();
      } catch (error) {
        debugLogger.error(
          `Error stopping client '${serverName}': ${getErrorMessage(error)}`,
        );
      } finally {
        this.clients.delete(serverName);
        // Purge the OLD config's tools/prompts before rediscovery. `discover()`
        // only adds/overwrites by name and never purges, and `disconnect()`
        // doesn't touch the registries — so when this path reconnects a server
        // whose config CHANGED (the incremental fingerprint-diff branch), any
        // tool the new config drops or renames would otherwise linger,
        // selectable by the model but bound to the now-closed client. Clearing
        // here also keeps the failure path clean (a rediscovery that throws
        // leaves no stale entries behind). Mirrors `removeServer` /
        // `addRuntimeMcpServer`'s replace branch. Same-config reconnects
        // (`/mcp reconnect`, health monitor, OAuth) simply re-register the
        // identical set immediately after.
        this.purgeServerRegistries(serverName);
        this.eventEmitter?.emit('mcp-client-update', this.clients);
      }
    }

    // For SDK MCP servers, pass the sendSdkMcpMessage callback.
    const sdkCallback = isSdkMcpServerConfig(serverConfig)
      ? this.sendSdkMcpMessage
      : undefined;

    const client = new McpClient(
      serverName,
      serverConfig,
      this.toolRegistry,
      this.cliConfig.getPromptRegistry(),
      this.cliConfig.getWorkspaceContext(),
      this.cliConfig.getDebugMode(),
      sdkCallback,
    );

    this.clients.set(serverName, client);
    this.eventEmitter?.emit('mcp-client-update', this.clients);

    try {
      await client.connect();
      await client.discover(cliConfig);
      // Record the connected-config key of the config this client is now
      // connected with, so the incremental reconcile can detect a later
      // in-place config change and reconnect (mirrors the pool path's `conn.id`
      // tracking, plus the discovery filters — see singleSessionConnectedKeyOf).
      this.connectedConfigKeys.set(
        serverName,
        this.singleSessionConnectedKeyOf(serverName, serverConfig),
      );
      // a server that
      // was refused at a previous discovery pass and is now
      // successfully (re)connected via this path (e.g. `/mcp
      // reconnect`, health-monitor retry after another server was
      // removed) leaves a stale entry in `lastRefusedServerNames`.
      // The snapshot would then report `error / disabledReason:
      // 'budget'` for a CONNECTED server until the next discovery
      // pass clears the per-pass log. Clear it here so post-success
      // snapshots immediately reflect reality. Mirrors the same
      // pattern in `readResource`'s late-reserve branch.
      this.dropRefusalEntry(serverName);
      // fix #4: hysteresis is driven inline by
      // `tryReserveSlot` (upward) and `releaseSlotName` (downward).
      // The standalone `evaluateBudgetState` that used to live here
      // is now redundant — the reservation that opened this branch
      // already fired the warning if it crossed 75%.
    } catch (error) {
      // two-mode
      // cleanup for connect failure, matching the `readResource`
      // R2 C3 fix pattern:
      //
      //   - `weReservedSlot === true` (this call freshly took a
      //     slot for a brand-new server): RELEASE the slot + drop
      //     the client. The server never successfully held a slot
      //     and shouldn't permanently block another server in
      //     `enforce` mode. Operator can re-add it later; the next
      //     `discoverAllMcpToolsIncremental` pass will re-reserve
      //     if capacity is available.
      //   - `weReservedSlot === false` (reconnect against an
      //     `'already_held'` slot — e.g. health-monitor retry,
      //     `/mcp reconnect` against a stable-but-momentarily-flaky
      //     server): KEEP the slot. The original successful connect
      //     established operator intent + capacity reservation; a
      //     transient reconnect hiccup shouldn't lose that.
      //
      // Corrected here: align with
      // `discoverAllMcpTools` (bulk) catch and `readResource`
      // (lazy spawn) catch. All three paths now use the same
      // weReserved-driven cleanup.
      if (weReservedSlot) {
        // transport
        // leak — when `connect()` succeeded (transport established)
        // but `discover()` later threw, deleting the client without
        // calling `disconnect()` left the stdio child process /
        // socket alive until Node exits. Best-effort disconnect
        // here closes the transport before dropping our reference.
        // Errors from disconnect are intentionally swallowed
        // (we're already in a discovery-failure catch; double-
        // throwing would lose the original error context).
        try {
          await client.disconnect();
        } catch {
          // best-effort transport cleanup
        }
        this.releaseSlotName(serverName);
        this.clients.delete(serverName);
        this.connectedConfigKeys.delete(serverName);
      }
      // Log the error but don't throw: callers expect best-effort discovery.
      debugLogger.error(
        `Error during discovery for server '${serverName}': ${getErrorMessage(
          error,
        )}`,
      );
    } finally {
      this.startHealthCheck(serverName);
      this.eventEmitter?.emit('mcp-client-update', this.clients);
    }
  }

  /**
   * pool-mode discovery. Iterates configured
   * servers and calls `pool.acquire(name, cfg, sessionId, toolReg,
   * promptReg)` for each non-disabled server. Pool internally:
   *   - Returns the existing PoolEntry if same fingerprint already
   *     spawned for this workspace (other sessions sharing it)
   *   - Spawns a new entry otherwise (deduped via spawnInFlight)
   *   - For SDK MCP / non-pooled HTTP: routes to
   *     `createUnpooledConnection` (per-session McpClient with the
   *     supplied session registries)
   *   - On attach: synchronously applies tool/prompt snapshots into
   *     the supplied session registries via `SessionMcpView`
   *
   * Per-session reconnect / health monitoring / budget enforcement
   * lives inside the pool, NOT in this manager — `this.reservedSlots`
   * / `this.healthCheckTimers` etc. stay empty in pool mode (they're
   * still allocated for legacy mode coexistence).
   *
   * Pre-pool path's `await this.stop()` releases EVERYTHING; here we
   * only need to drop the manager's own pool refs because cross-
   * session pool entries still belong to the pool.
   */
  private discoverAllMcpToolsViaPool(cliConfig: Config): Promise<void> {
    // Re-entrancy guard : if a pass is in flight, return the
    // same promise so the caller awaits the in-flight resolution
    // instead of triggering a parallel pass that races on
    // `pooledConnections`. Cleanup runs in `.finally` so the next
    // call (after this pass completes) starts fresh.
    if (this.discoveryInFlight) return this.discoveryInFlight;
    this.discoveryInFlight = this.runDiscoverAllMcpToolsViaPool(
      cliConfig,
    ).finally(() => {
      this.discoveryInFlight = undefined;
    });
    return this.discoveryInFlight;
  }

  private async runDiscoverAllMcpToolsViaPool(
    cliConfig: Config,
  ): Promise<void> {
    if (!this.pool) return; // unreachable; caller already gates
    // reset the
    // shutdown-timeout flag at the START of every discovery pass. The
    // flag is sticky — it persists across `stop()` calls until
    // explicitly reset. Without this reset, a manager that survived
    // one timed-out shutdown (e.g., a slow MCP server during SIGTERM
    // exceeding the 5s grace cap) would then enter every subsequent
    // discovery pass with the guard already true, silently calling
    // `conn.release()` and skipping `pooledConnections.set(...)` for
    // every server — the manager would appear to discover servers but
    // none would be reachable for subsequent tool calls. A fresh
    // discovery pass means we're past any prior shutdown phase.
    this.stopTimedOut = false;
    this.discoveryState = MCPDiscoveryState.IN_PROGRESS;
    // also write the
    // module-global `mcpDiscoveryState`. Pre-fix the pool path only
    // updated `this.discoveryState` (manager-local) — `GET /workspace/mcp`
    // and the MCP preflight cell read the GLOBAL via
    // `getMCPDiscoveryState()` and reported `not_started` for a
    // workspace whose pool discovery was running or already
    // complete. Snapshot now reflects reality regardless of which
    // discovery path (legacy per-session or pool) is active.
    setMCPDiscoveryState(MCPDiscoveryState.IN_PROGRESS);
    // bracket the pass with the pool's budget
    // bulk-pass scope so per-server BudgetExhaustedError refusals
    // accumulate into ONE coalesced `refused_batch` event at end of
    // pass — matches per-pass contract for the snapshot
    // route AND the typed push event consumers depend on.
    const poolBudget = this.pool.getBudget();
    poolBudget?.beginBulkPass();
    try {
      const sessionId = this.cliConfig.getSessionId();
      const promptRegistry = this.cliConfig.getPromptRegistry();
      const resourceRegistry = this.cliConfig.getResourceRegistry();
      const servers = populateMcpServerCommand(
        this.cliConfig.getMcpServers() || {},
        this.cliConfig.getMcpServerCommand(),
      );
      // diff against the
      // current `pooledConnections` instead of releasing all then
      // re-acquiring everything. Pre-fix every incremental discovery
      // pass (the default progressive-mode boot path also routes
      // through here) was: `release-all` → `view.teardown` →
      // `removeMcpToolsByServer` for every server, then
      // `pool.acquire` → `view.applyTools` re-registers everything.
      // That left a brief window with zero MCP tools registered AND
      // bounced every pool entry's drain timer for no reason. Now:
      //   1. Build the desired (name, fingerprint) set from current
      //      config + filters (skip disabled, skip SDK MCP).
      //   2. Release stale pooled connections (server removed,
      //      disabled, or fingerprint changed) — survivors stay
      //      attached, no tool registry churn.
      //   3. Acquire only the desired connections we don't already
      //      hold by id.
      // SDK MCP servers always re-run via legacy
      // `discoverMcpToolsForServer` (idempotent on re-call; the
      // legacy path's `discoverMcpToolsForServer` purges existing
      // entries before rediscovery).
      const desiredIds = new Map<string, ConnectionId>();
      for (const [name, config] of Object.entries(servers)) {
        if (cliConfig.isMcpServerDisabled(name)) continue;
        // Trust boundary (#4615): a gated `.mcp.json`/workspace server pending
        // user approval must not be "desired" — otherwise the release loop
        // below would keep (or a hot-reload would acquire) a pool connection
        // before the user approves. The legacy path already skips pending; the
        // pool path must match. Optional-chain is defensive for the daemon
        // surface where `isMcpServerPendingApproval` may be absent.
        if (cliConfig.isMcpServerPendingApproval?.(name)) continue;
        if (isSdkMcpServerConfig(config)) continue;
        desiredIds.set(name, connectionIdOf(name, config));
      }
      // Release connections that are stale (no longer wanted, or
      // wanted but with a different fingerprint).
      for (const [name, conn] of [...this.pooledConnections]) {
        const desired = desiredIds.get(name);
        if (desired === undefined || desired !== conn.id) {
          try {
            conn.release();
          } catch (err) {
            debugLogger.debug(
              `Pool release error (ignored): ${getErrorMessage(err)}`,
            );
          }
          this.pooledConnections.delete(name);
        }
      }
      const acquirePromises = Object.entries(servers).map(
        async ([name, config]) => {
          if (cliConfig.isMcpServerDisabled(name)) {
            debugLogger.debug(
              `Skipping disabled MCP server (pool mode): ${name}`,
            );
            return;
          }
          // Trust boundary (#4615): never acquire a connection / spawn a
          // process for a gated server still pending approval. Mirrors the
          // legacy single-session path and the `desiredIds` filter above.
          if (cliConfig.isMcpServerPendingApproval?.(name)) {
            debugLogger.debug(
              `Skipping pending-approval MCP server (pool mode): ${name}`,
            );
            return;
          }
          // SDK MCP servers MUST
          // stay on the legacy McpClientManager path because their
          // `sendSdkMcpMessage` callback is bound per-session in this
          // manager's ctor, but the workspace-shared pool was
          // constructed in `QwenAgent` ctor without it. Routing SDK
          // MCP through `pool.acquire` would yield an McpClient with
          // `sendSdkMcpMessage: undefined`, breaking SDK MCP server
          // tool calls. The legacy path below preserves the
          // per-session callback wiring and SDK servers continue to
          // work bit-for-bit identically to the legacy daemon mode.
          if (isSdkMcpServerConfig(config)) {
            await this.discoverMcpToolsForServer(name, cliConfig);
            return;
          }
          // R2 follow-on: skip if we already hold the exact desired
          // connection (survived the diff above). Avoids the redundant
          // `pool.acquire` call which would otherwise just bump the
          // entry's refcount + trigger a snapshot replay.
          if (this.pooledConnections.has(name)) return;
          try {
            const conn = await this.pool!.acquire(
              name,
              config,
              sessionId,
              this.toolRegistry,
              promptRegistry,
              resourceRegistry,
            );
            //
            // subscribe to entry-level events so a `'failed'` event
            // (entry's restart hit reconnect-budget exhaustion →
            // terminal failure → entry removed from `pool.entries`)
            // evicts our stale handle.
            //
            // Keep a NAMED listener and unregister it on
            // 'failed' BEFORE deleting from `pooledConnections`. Pre-
            // fix the anonymous arrow stayed attached to the entry's
            // EventEmitter even after we deleted from
            // `pooledConnections` — the listener's closure pinned
            // `this` (manager) and `conn` (PooledConnection wrapper),
            // making cleanup depend on whole-object GC. With named +
            // self-unregister, the listener detaches as soon as the
            // 'failed' event fires.
            //
            // Idempotent — a second 'failed' event on the same id
            // is a no-op via `get(name) === conn` guard;
            // `releaseAllPooledConnections` / `stop` also call
            // `conn.release()` independently.
            const onFailed = (e: import('./mcp-pool-events.js').PoolEvent) => {
              if (e.kind !== 'failed') return;
              if (this.pooledConnections.get(name) === conn) {
                this.pooledConnections.delete(name);
              }
              conn.off('event', onFailed);
            };
            conn.on('event', onFailed);
            // skip
            // the set if shutdown already passed its 5s grace cap and
            // released pool connections. A late-resolving pool.acquire
            // (whose own 30s stdio timeout exceeds the shutdown cap)
            // would otherwise repopulate `pooledConnections` AFTER
            // `releaseAllPooledConnections` cleared it — orphan entry
            // (refcount never reaches 0, drain timer never fires).
            // Release the just-acquired connection so the pool's
            // refcount drops back to where it would have been if the
            // acquire had been refused.
            if (this.stopTimedOut) {
              try {
                conn.release();
              } catch {
                /* best effort — shutdown in progress */
              }
              return;
            }
            this.pooledConnections.set(name, conn);
          } catch (err) {
            // Pool acquire failure for one server is non-fatal for
            // siblings (matches the legacy `discoverMcpToolsForServer`
            // catch behavior). Operator visibility through standard
            // error logger; status snapshot reflects reality via the
            // global `serverStatuses` Map (pool's
            // `aggregateStatusByName` keeps it consistent).
            //
            // `BudgetExhaustedError` from the
            // pool's pre-spawn budget gate is not a "failure" — the
            // refusal was deliberate, already recorded by the pool's
            // `recordRefusal`, and will surface as a `refused_batch`
            // event at end of pass. Log at debug to avoid flooding
            // operators with one error per refused server.
            if (err instanceof BudgetExhaustedError) {
              debugLogger.debug(
                `Pool refused acquire for ${name} (budget exhausted, ` +
                  `budget=${err.budget}, reservedCount=${err.reservedCount})`,
              );
            } else {
              debugLogger.error(
                `Pool acquire failed for ${name}: ${getErrorMessage(err)}`,
              );
            }
          }
        },
      );
      await Promise.all(acquirePromises);
    } finally {
      poolBudget?.endBulkPass();
      this.discoveryState = MCPDiscoveryState.COMPLETED;
      // Same global update as the IN_PROGRESS write
      // above; preflight cell + snapshot route both read the global.
      setMCPDiscoveryState(MCPDiscoveryState.COMPLETED);
      this.eventEmitter?.emit('mcp-client-update', this.clients);
    }
  }

  private releaseAllPooledConnections(): void {
    for (const conn of this.pooledConnections.values()) {
      try {
        conn.release();
      } catch (err) {
        debugLogger.debug(
          `Pool release error (ignored): ${getErrorMessage(err)}`,
        );
      }
    }
    this.pooledConnections.clear();
  }

  /**
   * Stops all running local MCP servers and closes all client connections.
   * This is the cleanup method to be called on application exit.
   */
  async stop(): Promise<void> {
    // Stop all health checks first
    this.stopAllHealthChecks();

    const disconnectionPromises = Array.from(this.clients.entries()).map(
      async ([name, client]) => {
        try {
          await client.disconnect();
        } catch (error) {
          debugLogger.error(
            `Error stopping client '${name}': ${getErrorMessage(error)}`,
          );
        }
      },
    );

    await Promise.all(disconnectionPromises);
    this.clients.clear();
    this.connectedConfigKeys.clear();
    this.consecutiveFailures.clear();
    this.isReconnecting.clear();
    this.serverDiscoveryPromises.clear();
  }

  /**
   * Disconnects a specific MCP server.
   * @param serverName The name of the server to disconnect.
   */
  async disconnectServer(serverName: string): Promise<void> {
    // Stop health check for this server
    this.stopHealthCheck(serverName);

    const client = this.clients.get(serverName);
    if (client) {
      try {
        await client.disconnect();
      } catch (error) {
        debugLogger.error(
          `Error disconnecting client '${serverName}': ${getErrorMessage(error)}`,
        );
      } finally {
        this.clients.delete(serverName);
        this.connectedConfigKeys.delete(serverName);
        this.consecutiveFailures.delete(serverName);
        this.isReconnecting.delete(serverName);
        this.serverDiscoveryPromises.delete(serverName);
        this.eventEmitter?.emit('mcp-client-update', this.clients);
      }
    }
  }

  getDiscoveryState(): MCPDiscoveryState {
    return this.discoveryState;
  }

  /**
   * Gets the health monitoring configuration
   */
  getHealthConfig(): MCPHealthMonitorConfig {
    return { ...this.healthConfig };
  }

  /**
   * Updates the health monitoring configuration
   */
  updateHealthConfig(config: Partial<MCPHealthMonitorConfig>): void {
    this.healthConfig = { ...this.healthConfig, ...config };
    // Restart health checks with new configuration
    this.stopAllHealthChecks();
    if (this.healthConfig.autoReconnect) {
      this.startAllHealthChecks();
    }
  }

  /**
   * Starts health monitoring for a specific server
   */
  private startHealthCheck(serverName: string): void {
    if (!this.healthConfig.autoReconnect) {
      return;
    }

    // Clear existing timer if any
    this.stopHealthCheck(serverName);

    const timer = setInterval(async () => {
      await this.performHealthCheck(serverName);
    }, this.healthConfig.checkIntervalMs);

    this.healthCheckTimers.set(serverName, timer);
  }

  /**
   * Stops health monitoring for a specific server
   */
  private stopHealthCheck(serverName: string): void {
    const timer = this.healthCheckTimers.get(serverName);
    if (timer) {
      clearInterval(timer);
      this.healthCheckTimers.delete(serverName);
    }
  }

  /**
   * Stops all health checks
   */
  private stopAllHealthChecks(): void {
    for (const [, timer] of this.healthCheckTimers.entries()) {
      clearInterval(timer);
    }
    this.healthCheckTimers.clear();
  }

  /**
   * Starts health checks for all connected servers
   */
  private startAllHealthChecks(): void {
    for (const serverName of this.clients.keys()) {
      this.startHealthCheck(serverName);
    }
  }

  /**
   * Performs a health check on a specific server
   */
  private async performHealthCheck(serverName: string): Promise<void> {
    const client = this.clients.get(serverName);
    if (!client) {
      return;
    }

    // Skip if already reconnecting
    if (this.isReconnecting.get(serverName)) {
      return;
    }

    try {
      // Check if client is connected by getting its status
      const status = client.getStatus();

      if (status !== MCPServerStatus.CONNECTED) {
        // Connection is not healthy
        const failures = (this.consecutiveFailures.get(serverName) || 0) + 1;
        this.consecutiveFailures.set(serverName, failures);

        debugLogger.warn(
          `Health check failed for server '${serverName}' (${failures}/${this.healthConfig.maxConsecutiveFailures})`,
        );

        if (failures >= this.healthConfig.maxConsecutiveFailures) {
          // Trigger reconnection
          await this.reconnectServer(serverName);
        }
      } else {
        // Connection is healthy, reset failure count
        this.consecutiveFailures.set(serverName, 0);
      }
    } catch (error) {
      debugLogger.error(
        `Error during health check for server '${serverName}': ${getErrorMessage(error)}`,
      );
    }
  }

  /**
   * Reconnects a specific server
   */
  private async reconnectServer(serverName: string): Promise<void> {
    if (this.isReconnecting.get(serverName)) {
      return;
    }

    this.isReconnecting.set(serverName, true);
    debugLogger.info(`Attempting to reconnect to server '${serverName}'...`);

    try {
      // Wait before reconnecting
      await new Promise((resolve) =>
        setTimeout(resolve, this.healthConfig.reconnectDelayMs),
      );

      await this.discoverMcpToolsForServer(serverName, this.cliConfig);

      // Reset failure count on successful reconnection
      this.consecutiveFailures.set(serverName, 0);
      debugLogger.info(`Successfully reconnected to server '${serverName}'`);
    } catch (error) {
      debugLogger.error(
        `Failed to reconnect to server '${serverName}': ${getErrorMessage(error)}`,
      );
    } finally {
      this.isReconnecting.set(serverName, false);
    }
  }

  /**
   * Discovers tools incrementally for all configured servers.
   * Only updates servers that have changed or are new.
   */
  async discoverAllMcpToolsIncremental(cliConfig: Config): Promise<void> {
    if (!cliConfig.isTrustedFolder()) {
      return;
    }

    const servers = populateMcpServerCommand(
      this.cliConfig.getMcpServers() || {},
      this.cliConfig.getMcpServerCommand(),
    );

    this.discoveryState = MCPDiscoveryState.IN_PROGRESS;
    recordStartupEvent('mcp_discovery_start', {
      serverCount: Object.keys(servers).length,
      incremental: true,
    });
    // Mirrors `discoverAllMcpTools`: announce IN_PROGRESS so UI subscribers
    // (MCP status pill, AppContainer batch-flush effect) know discovery
    // started, even when no servers need updates this pass.
    this.eventEmitter?.emit('mcp-client-update', this.clients);

    // Tracks the first successful server discover so we can emit the
    // `mcp_first_tool_registered` event exactly once. "First successful
    // discover" rather than a tool-count delta — simpler and aligns with the
    // user-perceived metric ("first MCP server is ready").
    let firstToolEventFired = false;

    // Find servers that are new or have changed configuration
    const serversToUpdate: string[] = [];
    const currentServerNames = new Set(this.clients.keys());
    const newServerNames = new Set(Object.keys(servers));

    // Check for new servers or configuration changes
    for (const [name] of Object.entries(servers)) {
      // Mirror `discoverAllMcpTools` (line ~102): users who explicitly
      // disabled a server via `mcpServers.<name>.disabled: true` must not
      // see it reconnected by the incremental path. Without this, the
      // PR-A background path silently re-registers tools the user has
      // told us to ignore.
      if (cliConfig.isMcpServerDisabled(name)) {
        debugLogger.debug(`Skipping disabled MCP server: ${name}`);
        continue;
      }

      // Check for new servers or configuration changes
      for (const [name] of Object.entries(servers)) {
        // Mirror `discoverAllMcpTools` (line ~102): users who explicitly
        // disabled a server via `mcpServers.<name>.disabled: true` must not
        // see it reconnected by the incremental path. Without this, the
        // PR-A background path silently re-registers tools the user has
        // told us to ignore.
        // A project server (`.mcp.json`) that was pending approval at startup
        // is treated exactly like a disabled server here: never reconnected,
        // and torn down if a prior pass had connected it.
        if (
          cliConfig.isMcpServerDisabled(name) ||
          cliConfig.isMcpServerPendingApproval?.(name)
        ) {
          debugLogger.debug(
            cliConfig.isMcpServerDisabled(name)
              ? `Skipping disabled MCP server: ${name}`
              : `Skipping MCP server pending approval: ${name}`,
          );
          // If the server was previously enabled and got connected, we now
          // need to tear it down — otherwise its client, registered tools
          // and health checks linger after an enabled→disabled mid-session
          // transition (e.g. via `/mcp disable <name>`). `removeServer`
          // disconnects, drops the client entry, removes tools from the
          // registry, stops the health check, and removes the global
          // status so the Footer pill stops counting it.
          if (this.clients.has(name)) {
            await this.removeServer(name);
          }
          continue;
        }
        const existingClient = this.clients.get(name);
        if (!existingClient) {
          // pre-reservation
          // here was a TOCTOU race. The inner
          // `discoverMcpToolsForServerInternal` ALSO does `tryReserveSlot`
          // (added in R1 fix #1). With BOTH sites reserving, the
          // reservation lifecycle didn't align with the timeout
          // cleanup site — `runWithDiscoveryTimeout`'s timeout handler
          // could release the slot mid-flight while the inner
          // `connect()` later resolves successfully, leaving a
          // CONNECTED client with NO reservation. Next pass admits
          // another new server because `reservedSlots.size < budget`,
          // and `enforce` mode silently exceeds the cap.
          //
          // Fix: delete the pre-reservation. `discoverMcpToolsForServerInternal`
          // owns the reservation lifecycle end-to-end (reserve →
          // try-catch around connect → release on weReservedSlot
          // failure path → cleared by timeout handler if it fires).
          // Refusal still happens — just inside the inner call. The
          // operator-visible behavior is identical; only the race is
          // closed.
          serversToUpdate.push(name);
        } else if (
          existingClient.getStatus() === MCPServerStatus.DISCONNECTED
        ) {
          // Disconnected server, try to reconnect
          serversToUpdate.push(name);
        } else {
          // Still-connected server: detect an in-place config change
          // (command / url / env / headers / oauth, plus the discovery filters
          // trust / includeTools / excludeTools) by comparing the connected-
          // config key it was connected with against the desired one. This is
          // the single-session equivalent of the pool path's `desiredIds` diff
          // — without it, editing a live server's config at runtime would leave
          // it running on the stale config. `connectedConfigKeys` is set on
          // every successful connect, so a CONNECTED client without a recorded
          // key is not expected; guard against `undefined` anyway to avoid a
          // spurious reconnect of a healthy server.
          // `discoverMcpToolsForServerInternal` disconnects the stale client
          // before reconnecting with the freshly-read config, so pushing the
          // name is sufficient — no explicit teardown needed here.
          const currentKey = this.connectedConfigKeys.get(name);
          if (
            currentKey !== undefined &&
            currentKey !== this.singleSessionConnectedKeyOf(name, servers[name])
          ) {
            serversToUpdate.push(name);
          }
        }
      }
      // Note: Configuration change detection would require comparing
      // the old and new config, which is not implemented here
    }

    // Find removed servers
    for (const name of currentServerNames) {
      if (!newServerNames.has(name)) {
        // Server was removed from configuration
        await this.removeServer(name);
      }
    }

    // Update only the servers that need it. Each per-server discover is
    // wrapped in a discovery-only timeout (stdio default 30s, remote 5s,
    // per-server override via `discoveryTimeoutMs`). Tool-call timeout is
    // intentionally left alone — a long-running tool invocation is not a
    // startup pathology.
    const discoveryPromises = serversToUpdate.map(async (name) => {
      const serverConfig = servers[name];
      try {
        await this.runWithDiscoveryTimeout(name, serverConfig, () =>
          this.discoverMcpToolsForServer(name, cliConfig),
        );
        if (!firstToolEventFired) {
          firstToolEventFired = true;
          recordStartupEvent('mcp_first_tool_registered', {
            serverName: name,
          });
        }
        recordStartupEvent(`mcp_server_ready:${name}`, { outcome: 'ready' });
      } catch (error) {
        // Defensive cleanup: the dedup Map entry is normally removed by
        // `discoverMcpToolsForServer`'s `finally`, but `runWithDiscoveryTimeout`
        // can reject before that finally runs (the timeout also disconnects
        // the client to abort the underlying handshake). Without this
        // explicit delete, a brief window exists where a subsequent
        // `discoverMcpToolsForServer(name)` call would short-circuit on
        // a now-doomed promise.
        this.serverDiscoveryPromises.delete(name);
        recordStartupEvent(`mcp_server_ready:${name}`, {
          outcome: 'failed',
          reason: getErrorMessage(error),
        });
        debugLogger.error(
          `Error during incremental discovery for server '${name}': ${getErrorMessage(error)}`,
        );
      }
    });

    await Promise.all(discoveryPromises);

    // Start health checks for all connected servers
    if (this.healthConfig.autoReconnect) {
      this.startAllHealthChecks();
    }

    this.discoveryState = MCPDiscoveryState.COMPLETED;
    recordStartupEvent('mcp_all_servers_settled', {
      serverCount: Object.keys(servers).length,
      incremental: true,
    });
    // Trailing `mcp-client-update` AFTER flipping discoveryState to
    // COMPLETED. Without this the per-server updates above all fire while
    // the state is still IN_PROGRESS, so the AppContainer batch-flush
    // subscriber never observes the terminal state.
    this.eventEmitter?.emit('mcp-client-update', this.clients);
  }

  /**
   * Caps how long a single MCP server's discover handshake is allowed to
   * take during startup. Local stdio servers default to 30s; remote
   * HTTP/SSE servers default to 5s (mirrors Claude Code's
   * `CLAUDE_AI_MCP_TIMEOUT_MS`). Per-server override via
   * `mcpServers.<name>.discoveryTimeoutMs` in settings.
   */
  private runWithDiscoveryTimeout<T>(
    serverName: string,
    serverConfig: MCPServerConfig | undefined,
    fn: () => Promise<T>,
  ): Promise<T> {
    const timeoutMs = this.discoveryTimeoutFor(serverConfig);
    let timedOut = false;
    return new Promise<T>((resolve, reject) => {
      const timer = setTimeout(() => {
        timedOut = true;
        // CRITICAL: rejecting `runWithDiscoveryTimeout` does NOT cancel
        // the underlying `discoverMcpToolsForServer` — it keeps trying
        // to `connect()` / `discover()`, and if the slow server
        // eventually responds, `discover()` registers its tools into
        // the live `toolRegistry` and re-emits `mcp-client-update`.
        // From the user's perspective the server "failed" but its tools
        // are silently active, including any that shadow built-ins.
        // Disconnect the client to abort the handshake so the
        // background promise rejects (the `connect()` call throws when
        // its transport is closed mid-handshake), the underlying
        // promise's `finally` clears the dedup Map entry, and no tools
        // ever reach the registry.
        const client = this.clients.get(serverName);
        if (client) {
          void client.disconnect().catch((err) => {
            debugLogger.debug(
              `Forced disconnect of timed-out server '${serverName}' threw: ${getErrorMessage(err)}`,
            );
          });
        }
        // Drop any tools/prompts/resources that registered during the
        // disconnect window. No-op if the server hadn't reached `discover()`
        // yet, so it's safe to always call. A server that registered prompts /
        // resources but stalled `tools/list` past the timeout would otherwise
        // leak them bound to the closed transport.
        this.purgeServerRegistries(serverName);
        // Prevent the discovery `finally` block's `startHealthCheck` from
        // resurrecting this server: without removing the client entry,
        // `performHealthCheck` would observe `status !== CONNECTED` for
        // ~maxConsecutiveFailures intervals and then call
        // `reconnectServer()` → `discoverMcpToolsForServer()` directly,
        // bypassing `runWithDiscoveryTimeout` entirely. The intentionally
        // timed-out server would silently come back. Removing the client
        // entry + stopping any pending health-check timer closes that
        // loop; `startHealthCheck` early-returns when the client is
        // absent, so the trailing `finally`-block call becomes a no-op.
        this.stopHealthCheck(serverName);
        this.clients.delete(serverName);
        this.connectedConfigKeys.delete(serverName);
        // Release the budget slot ONLY if THIS in-flight
        // discoverMcpToolsForServerInternal call freshly reserved
        // it. `freshReservations.has(serverName)` distinguishes:
        //
        //   - Fresh reservation (never connected): release — a server
        //     that never connected shouldn't permanently consume a
        //     slot under enforce mode.
        //   - `'already_held'` reconnect (server was previously
        //     healthy, now flaky): KEEP the slot. Health-monitor
        //     retry doesn't have to compete for capacity with new
        //     servers admitted during the timeout window.
        //
        // Originally treated all timeouts as "release"
        // R8 #4 caught the asymmetry with the connect-failure
        // path's `weReservedSlot` guard. Now they match.
        if (this.freshReservations.has(serverName)) {
          this.releaseSlotName(serverName);
          this.freshReservations.delete(serverName);
        }
        // And drop any stale refusal entry — operator intent shifts
        // when a slot becomes free again, and snapshot consumers
        // shouldn't keep tagging a now-slotless server as
        // `disabledReason: 'budget'`.
        this.dropRefusalEntry(serverName);
        reject(
          new Error(
            `MCP server '${serverName}' discovery timed out after ${timeoutMs}ms`,
          ),
        );
      }, timeoutMs);
      fn().then(
        (value) => {
          clearTimeout(timer);
          // Suppress success after timeout — the timeout already
          // rejected the outer promise; resolving it again is a no-op
          // but the success path would also re-emit
          // `mcp_server_ready:ready` and `mcp_first_tool_registered`
          // even though the rest of the system has moved on.
          if (!timedOut) resolve(value);
        },
        (err) => {
          clearTimeout(timer);
          if (!timedOut) {
            reject(err instanceof Error ? err : new Error(String(err)));
          }
        },
      );
    });
  }

  /**
   * Minimum / maximum discovery timeouts. `0` or a negative value as a
   * per-server override would cause every discover to fire its timeout on
   * the next tick — combined with the lack of disconnect on timeout this
   * was a remote-exploitable silent-tool-registration vector (a
   * MITM/attacker-controlled MCP server could land its tools after the
   * timeout fired). `Infinity` / very large values would hang
   * `waitForMcpReady()` forever for non-interactive paths. The 100ms
   * floor is generous (real handshakes start in single-digit ms locally,
   * tens of ms remote); the 5-minute ceiling matches the longest tool
   * call timeouts we've documented.
   */
  private static readonly MIN_DISCOVERY_TIMEOUT_MS = 100;
  private static readonly MAX_DISCOVERY_TIMEOUT_MS = 300_000;

  private discoveryTimeoutFor(serverConfig?: MCPServerConfig): number {
    const override = serverConfig?.discoveryTimeoutMs;
    if (override !== undefined && Number.isFinite(override)) {
      return Math.max(
        McpClientManager.MIN_DISCOVERY_TIMEOUT_MS,
        Math.min(override, McpClientManager.MAX_DISCOVERY_TIMEOUT_MS),
      );
    }
    // Remote transports (HTTP/SSE/WebSocket) carry network risk and get
    // a shorter default; stdio servers we trust the user already runs
    // locally. `tcp` is the WebSocket transport field on
    // `MCPServerConfig` — without it, websocket servers fall through to
    // the stdio default and a hung WS handshake holds back the
    // non-interactive `waitForMcpReady()` for 30s instead of 5s.
    const isRemote = !!(
      serverConfig?.httpUrl ||
      serverConfig?.url ||
      serverConfig?.tcp
    );
    return isRemote ? 5_000 : 30_000;
  }

  /**
   * The single-session reconnect key for a server config. `connectionIdOf` is
   * intentionally transport-only (it excludes the per-session discovery filters
   * so the shared pool can reuse a transport across sessions with different
   * filters). But the single-session reconcile must ALSO reconnect when only a
   * discovery filter changes — `trust`, `includeTools`, `excludeTools` are
   * applied during `discover()` and baked into the registered tools, so a
   * config edit to them otherwise never takes effect mid-session. Append a
   * stable hash of those fields (arrays sorted so order alone doesn't churn).
   */
  private singleSessionConnectedKeyOf(
    serverName: string,
    config: MCPServerConfig,
  ): string {
    const discovery = JSON.stringify({
      trust: config.trust ?? null,
      includeTools: [...(config.includeTools ?? [])].sort(),
      excludeTools: [...(config.excludeTools ?? [])].sort(),
    });
    return `${connectionIdOf(serverName, config)}|${discovery}`;
  }

  /**
   * Purge a server's entries from all three registries (tools + prompts +
   * resources). Every teardown path must clean all three atomically — a missed
   * registry leaves stale entries bound to a closed client (selectable by the
   * model, or surfaced by `listMcpResources`). Centralized here so adding a
   * future registry is one edit, not a hunt across teardown sites. Callers keep
   * their own transport disconnect / map deletes / health-check / status /
   * budget handling — only the registry purge is shared.
   */
  private purgeServerRegistries(serverName: string): void {
    this.toolRegistry.removeMcpToolsByServer(serverName);
    this.cliConfig.getPromptRegistry().removePromptsByServer(serverName);
    this.cliConfig.getResourceRegistry().removeResourcesByServer(serverName);
  }

  /**
   * Removes a server and its tools
   */
  private async removeServer(serverName: string): Promise<void> {
    const client = this.clients.get(serverName);
    if (client) {
      try {
        await client.disconnect();
      } catch (error) {
        debugLogger.error(
          `Error disconnecting removed server '${serverName}': ${getErrorMessage(error)}`,
        );
      }
      this.clients.delete(serverName);
      this.stopHealthCheck(serverName);
      this.consecutiveFailures.delete(serverName);
    }
    this.connectedConfigKeys.delete(serverName);

    // server gone from config (or disabled mid-session) releases
    // the budget slot too — operator intent is "this server should not
    // be running", so it must not block a different server from taking
    // its place on the next discovery pass.
    this.releaseSlotName(serverName);
    // also drop the entry from the per-pass
    // refusal log so a snapshot taken between discoveries doesn't
    // stale-tag the (now-disabled or now-removed) server as
    // `disabledReason: 'budget'`. Operator action wins over the
    // last-pass startup refusal record.
    this.dropRefusalEntry(serverName);

    // Remove tools, prompts and resources for this server. Unlike
    // `ToolRegistry.disconnectServer`, this config-driven removal path never
    // cleaned up the prompt/resource registries, so a removed/changed server
    // leaked them across a hot-reload.
    this.purgeServerRegistries(serverName);

    // The server has been removed from configuration, so drop it from the
    // global status registry too — the health pill should no longer count it.
    removeMCPServerStatus(serverName);

    this.eventEmitter?.emit('mcp-client-update', this.clients);
  }

  async readResource(
    serverName: string,
    uri: string,
    options?: { signal?: AbortSignal },
  ): Promise<ReadResourceResult> {
    let client = this.clients.get(serverName);
    if (!client) {
      const servers = populateMcpServerCommand(
        this.cliConfig.getMcpServers() || {},
        this.cliConfig.getMcpServerCommand(),
      );
      const serverConfig = servers[serverName];
      if (!serverConfig) {
        throw new Error(`MCP server '${serverName}' is not configured.`);
      }

      const sdkCallback = isSdkMcpServerConfig(serverConfig)
        ? this.sendSdkMcpMessage
        : undefined;

      client = new McpClient(
        serverName,
        serverConfig,
        this.toolRegistry,
        this.cliConfig.getPromptRegistry(),
        this.cliConfig.getWorkspaceContext(),
        this.cliConfig.getDebugMode(),
        sdkCallback,
      );
      this.clients.set(serverName, client);
      this.eventEmitter?.emit('mcp-client-update', this.clients);
    }

    if (client.getStatus() !== MCPServerStatus.CONNECTED) {
      try {
        // wrap the
        // lazy-spawn `client.connect()` in the same discovery
        // timeout the bulk + incremental paths use. Pre-fix a hung
        // MCP server during a resource-read spawn would block
        // forever and permanently consume a budget slot under
        // `enforce` mode, cascading into total budget exhaustion
        // on subsequent discovery passes. Reuses
        // `discoveryTimeoutFor` so per-server `discoveryTimeoutMs`
        // overrides apply uniformly across spawn paths.
        //
        // R10 line 1572 cleanup contract: when the timeout side
        // wins the race, the catch below calls
        // `await client.disconnect()` to abort the orphan
        // `client.connect()` that's still pending in the
        // background. This relies on `McpClient.disconnect()`
        // cancelling an in-flight connect — closing the underlying
        // transport (stdio child SIGTERM, WebSocket close frame,
        // HTTP socket teardown) so the pending connect promise
        // settles. If `disconnect()` on a never-completed connect
        // were a no-op, the orphan transport would survive with
        // no `this.clients` entry and `stop()` couldn't reach it.
        // This same contract is relied on by
        // `runWithDiscoveryTimeout`'s timeout handler (bulk +
        // incremental paths), so all three spawn paths share the
        // assumption — verified by the bulk path having shipped
        // production-stable for several releases. Worth a unit
        // test in a follow-up that exercises the
        // disconnect-cancels-pending-connect invariant against
        // a fixture that asserts the transport is actually torn
        // down.

        const timeoutMs = this.discoveryTimeoutFor(serverConfig);
        let timeoutId: NodeJS.Timeout | undefined;
        await Promise.race([
          client.connect(),
          new Promise<never>((_, reject) => {
            timeoutId = setTimeout(() => {
              reject(
                new Error(
                  `MCP server '${serverName}' lazy connect timed out after ${timeoutMs}ms`,
                ),
              );
            }, timeoutMs);
          }),
        ]).finally(() => {
          if (timeoutId) clearTimeout(timeoutId);
        });
        // Record the fingerprint of the config this client connected with so a
        // later `discoverAllMcpToolsIncremental` can detect an in-place config
        // change. The reconcile guard skips a still-connected server whose
        // key is `undefined`; without this, a server first brought up by a lazy
        // resource read would silently ignore a subsequent edit.
        this.connectedConfigKeys.set(
          serverName,
          this.singleSessionConnectedKeyOf(serverName, serverConfig),
        );
        // start
        // the health monitor on a successful lazy spawn. Pre-fix
        // a lazy-spawned server that later disconnected (crash,
        // network) had no automatic reconnect path — the client
        // sat DISCONNECTED in `this.clients` until the next
        // readResource or incremental pass. Mirror the
        // `discoverMcpToolsForServerInternal` finally-block
        // pattern.
        this.startHealthCheck(serverName);
      } catch (err) {
        //
        // zombie slot leak + transport leak.
        //
        // A failed lazy spawn would otherwise permanently consume
        // a budget slot AND leave a never-CONNECTED client entry
        // in `this.clients` (which `getMcpClientAccounting`
        // correctly excludes from `total`, but the slot still
        // blocks other servers). Only release if THIS call did
        // the reservation — a reuse path with an already-tracked
        // client must not collateral-damage another caller's
        // slot.
        //
        // R9 #2: `connect()` may have established the transport
        // (spawned the stdio child / opened the socket) before
        // throwing on a later handshake step. Best-effort
        // `await client.disconnect()` closes that transport
        // before dropping the reference — mirrors the R7 #3 +
        // R8 #1 fixes in the discovery-side catch blocks.
        if (weReservedSlot) {
          try {
            await client.disconnect();
          } catch {
            // best-effort transport cleanup
          }
          this.releaseSlotName(serverName);
          this.clients.delete(serverName);
          this.eventEmitter?.emit('mcp-client-update', this.clients);
        }
        throw err;
      }
    }

    return client.readResource(uri, options);
  }

  // ────────────────────────────────────────────────────────────────────
  // T2.8: Runtime MCP server lifecycle (add / remove)
  // ────────────────────────────────────────────────────────────────────

  /**
   * Add (or replace) a runtime MCP server, wiring:
   *   1. Config runtime overlay (shadow-over-settings detection)
   *   2. Budget guard (enforce throws, warn returns skipped)
   *   3. Pool acquire (or standalone McpClient connect + discover)
   *
   * Returns a result object describing what happened. Throws
   * `McpBudgetWouldExceedError` on hard-cap violations,
   * `McpServerSpawnFailedError` on transport failures,
   * `InvalidMcpConfigError` on bad config.
   */
  async addRuntimeMcpServer(
    name: string,
    config: MCPServerConfig,
    originatorClientId: string,
  ): Promise<AddRuntimeMcpServerResult> {
    // Reject explicitly excluded servers
    if (this.cliConfig.isMcpServerDisabled(name)) {
      throw new InvalidMcpConfigError(
        name,
        `server '${name}' is in excludedMcpServers and cannot be added at runtime`,
      );
    }

    debugLogger.info(
      `addRuntimeMcpServer: ${name} (transport=${mcpTransportOf(config)}, client=${originatorClientId})`,
    );

    // Validate config minimally: must have at least one transport field
    const transport = mcpTransportOf(config);
    if (transport === 'unknown') {
      throw new InvalidMcpConfigError(
        name,
        'config must specify at least one of: command, url, httpUrl, tcp',
      );
    }

    // Detect shadow-over-settings
    const settingsServers = this.cliConfig.getSettingsMcpServers() ?? {};
    const shadowedSettings = name in settingsServers;

    // Check for idempotent replace: same name + same fingerprint means
    // no pool churn needed. Compare against the existing pooled
    // connection (if any).
    const newConnId = connectionIdOf(name, config);
    const ifAbsent =
      (config as MCPServerConfig & Record<string, unknown>)[
        RUNTIME_MCP_IF_ABSENT_CONFIG_FLAG
      ] === true;
    if (ifAbsent) {
      const existingRuntimeConfig = this.cliConfig.getRuntimeMcpServers()[name];
      const existingIsIfAbsent =
        (
          existingRuntimeConfig as
            | (MCPServerConfig & Record<string, unknown>)
            | undefined
        )?.[RUNTIME_MCP_IF_ABSENT_CONFIG_FLAG] === true;
      if (
        existingRuntimeConfig &&
        (!existingIsIfAbsent ||
          connectionIdOf(name, existingRuntimeConfig) !== newConnId)
      ) {
        return {
          name,
          skipped: true,
          reason: 'runtime_name_conflict',
        };
      }
    }
    const existingConn = this.pooledConnections.get(name);
    if (existingConn && existingConn.id === newConnId) {
      // Same fingerprint — no transport churn, just update Config overlay
      this.cliConfig.addRuntimeMcpServer(name, config);
      const toolCount = existingConn.toolsSnapshot.length;
      return {
        name,
        transport,
        replaced: false,
        shadowedSettings,
        toolCount,
        originatorClientId,
      };
    }

    // Budget guard — check using the appropriate budget layer
    const budget = this.pool?.getBudget();
    if (budget) {
      // Pool mode: use workspace budget
      const mode = budget.getMode();
      if (mode === 'enforce' || mode === 'warn') {
        // Only apply budget check if this is a genuinely NEW name
        // (not a re-add of the same name already holding a slot)
        const reservation = budget.tryReserve(name);
        if (reservation === 'refused') {
          // Hard cap — enforce mode
          throw new McpBudgetWouldExceedError(name);
        }
        // In warn mode, if the budget is at or above capacity and this
        // is a new reservation, return a soft refusal
        if (
          mode === 'warn' &&
          reservation === 'reserved' &&
          budget.getBudget() !== undefined &&
          budget.getReservedCount() > budget.getBudget()!
        ) {
          // Roll back the reservation — we're not actually spawning
          budget.release(name);
          return {
            name,
            skipped: true,
            reason: 'budget_warning_only',
          };
        }
      }
    } else if (this.budgetMode !== 'off') {
      // Standalone mode: use manager-level budget
      const reservation = this.tryReserveSlot(name);
      if (reservation === 'refused') {
        throw new McpBudgetWouldExceedError(name);
      }
      if (
        this.budgetMode === 'warn' &&
        reservation === 'reserved' &&
        this.clientBudget !== undefined &&
        this.reservedSlots.size > this.clientBudget
      ) {
        this.releaseSlotName(name);
        return {
          name,
          skipped: true,
          reason: 'budget_warning_only',
        };
      }
    }

    // Release existing connection for this name (if replacing with
    // different fingerprint)
    const replaced = this.pooledConnections.has(name) || this.clients.has(name);
    if (existingConn) {
      try {
        existingConn.release();
      } catch {
        /* best effort */
      }
      this.pooledConnections.delete(name);
      this.purgeServerRegistries(name);
      this.stopHealthCheck(name);
    }
    const existingClient = this.clients.get(name);
    if (existingClient) {
      this.stopHealthCheck(name);
      try {
        await existingClient.disconnect();
      } catch {
        /* best effort */
      }
      this.clients.delete(name);
      this.connectedConfigKeys.delete(name);
      this.purgeServerRegistries(name);
      // Do NOT releaseSlotName here — the budget slot carries over to
      // the new entry being spawned. Releasing + not re-reserving would
      // leave the running server unaccounted in the budget.
    }

    // Write the Config runtime overlay BEFORE spawning so
    // `getMcpServers()` reflects the new entry immediately (the pool
    // acquire + discover may read config for trust/filters).
    this.cliConfig.addRuntimeMcpServer(name, config);

    // Acquire the transport
    let toolCount = 0;
    try {
      if (this.pool && !isSdkMcpServerConfig(config)) {
        // Pool mode: acquire through the shared pool
        const sessionId = this.cliConfig.getSessionId();
        const promptRegistry = this.cliConfig.getPromptRegistry();
        const resourceRegistry = this.cliConfig.getResourceRegistry();
        const conn = await this.pool.acquire(
          name,
          config,
          sessionId,
          this.toolRegistry,
          promptRegistry,
          resourceRegistry,
        );
        this.pooledConnections.set(name, conn);
        toolCount = conn.toolsSnapshot.length;
      } else {
        // Standalone mode: create a per-session McpClient
        const sdkCallback = isSdkMcpServerConfig(config)
          ? this.sendSdkMcpMessage
          : undefined;
        const client = new McpClient(
          name,
          config,
          this.toolRegistry,
          this.cliConfig.getPromptRegistry(),
          this.cliConfig.getWorkspaceContext(),
          this.cliConfig.getDebugMode(),
          sdkCallback,
        );
        this.clients.set(name, client);
        this.eventEmitter?.emit('mcp-client-update', this.clients);
        await client.connect();
        await client.discover(this.cliConfig);
        this.connectedConfigKeys.set(
          name,
          this.singleSessionConnectedKeyOf(name, config),
        );
        this.eventEmitter?.emit('mcp-client-update', this.clients);
        toolCount = this.toolRegistry.getToolsByServer(name).length;
      }
    } catch (err) {
      // Spawn failed — roll back Config overlay + budget reservation
      this.cliConfig.removeRuntimeMcpServer(name);
      if (budget) {
        budget.release(name);
      } else if (this.budgetMode !== 'off') {
        this.releaseSlotName(name);
      }
      // Clean up any partial state (including tools/prompts/resources from a
      // partial discover) so a failed runtime add leaves nothing behind.
      this.purgeServerRegistries(name);
      this.pooledConnections.delete(name);
      removeMCPServerStatus(name);
      const failedClient = this.clients.get(name);
      if (failedClient) {
        try {
          await failedClient.disconnect();
        } catch {
          /* best effort */
        }
      }
      this.clients.delete(name);
      this.connectedConfigKeys.delete(name);
      this.stopHealthCheck(name);
      this.eventEmitter?.emit('mcp-client-update', this.clients);

      const message = err instanceof Error ? err.message : String(err);
      const isTimeout = message.includes('timed out');
      const exitCode =
        err instanceof Error && 'exitCode' in err
          ? (err as { exitCode?: number }).exitCode
          : undefined;
      throw new McpServerSpawnFailedError(name, {
        exitCode,
        stderr: message,
        timeout: isTimeout,
      });
    }

    return {
      name,
      transport,
      replaced,
      shadowedSettings,
      toolCount,
      originatorClientId,
    };
  }

  /**
   * Remove a runtime MCP server previously added via
   * `addRuntimeMcpServer`. Drops the Config overlay, releases the
   * pool connection (or disconnects the standalone client), and
   * releases the budget slot.
   *
   * Idempotent: returns `{skipped: true, reason: 'not_present'}` when
   * no runtime entry exists for `name`.
   */
  async removeRuntimeMcpServer(
    name: string,
    originatorClientId: string,
  ): Promise<RemoveRuntimeMcpServerResult> {
    // Check whether this name is a runtime entry
    // Config.removeRuntimeMcpServer returns true only if the entry was
    // in the runtime map.
    const wasRuntime = this.cliConfig.removeRuntimeMcpServer(name);
    if (!wasRuntime) {
      return { name, skipped: true, reason: 'not_present' };
    }

    // Detect whether this was shadowing a settings-layer entry
    const settingsServers = this.cliConfig.getSettingsMcpServers() ?? {};
    const wasShadowingSettings = name in settingsServers;

    // Release pool connection (identity-check prevents race with concurrent add)
    const poolConn = this.pooledConnections.get(name);
    if (poolConn) {
      try {
        poolConn.release();
      } catch {
        /* best effort */
      }
      if (this.pooledConnections.get(name) === poolConn) {
        this.pooledConnections.delete(name);
      }
    }

    // Disconnect standalone client
    const client = this.clients.get(name);
    if (client) {
      try {
        await client.disconnect();
      } catch {
        /* best effort */
      }
      this.clients.delete(name);
      this.eventEmitter?.emit('mcp-client-update', this.clients);
    }

    // Cleanup: tool registry, prompts, resources, status, health check,
    // diagnostics (mirrors removeServer)
    this.purgeServerRegistries(name);
    removeMCPServerStatus(name);
    this.stopHealthCheck(name);
    this.consecutiveFailures.delete(name);
    this.isReconnecting.delete(name);
    this.connectedConfigKeys.delete(name);
    this.dropRefusalEntry(name);

    // Release budget slot
    const budget = this.pool?.getBudget();
    if (budget) {
      budget.release(name);
    } else if (this.budgetMode !== 'off') {
      this.releaseSlotName(name);
    }

    return {
      name,
      removed: true,
      wasShadowingSettings,
      originatorClientId,
    };
  }
}

// ────────────────────────────────────────────────────────────────────
// T2.8: Result types for runtime MCP server add/remove
// ────────────────────────────────────────────────────────────────────

export type AddRuntimeMcpServerResult =
  | {
      name: string;
      transport: McpTransportKind;
      replaced: boolean;
      shadowedSettings: boolean;
      toolCount: number;
      originatorClientId: string;
    }
  | {
      name: string;
      skipped: true;
      reason: 'budget_warning_only' | 'runtime_name_conflict';
    };

export type RemoveRuntimeMcpServerResult =
  | {
      name: string;
      removed: true;
      wasShadowingSettings: boolean;
      originatorClientId: string;
    }
  | {
      name: string;
      skipped: true;
      reason: 'not_present';
    };

// Re-export error classes for convenience
export {
  McpBudgetWouldExceedError,
  McpServerSpawnFailedError,
  InvalidMcpConfigError,
} from './mcp-errors.js';
