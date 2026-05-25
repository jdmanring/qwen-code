# Project TODO

## Stage 1: Codebase Audit (Complete)

- [x] Audit git state: branches (`upstream-mirror`, `integration`, `develop`, `main`) and remotes (`upstream`, `mirror`, `origin`).
- [x] Audit tooling: verify `raw-inline.sh`, `integrate.sh`, `verification-gate.sh`, `symmetry-check.py`.
- [x] Audit config: verify `.qwen/config/` and `docs/` mapping.
- [x] Audit environment: verify `uv` and `pnpm` workspace configurations.

## Stage 2: Implementation Plan (Complete)

- [x] Define pre-flight checks for every tool.
- [x] Design upstream sync pipeline: Upstream → Mirror → Integration → Develop.
- [x] Define intake normalization steps: Lint → Format → Type-check → Naming review → Symmetry update.
- [x] Define completion criteria (all gates green, zero lint errors).

## Stage 3: Implementation

### 3.1: Branch and Environment Setup (Complete)
- [x] Restore `main` and `develop` branches from `origin`.
- [x] Configure `.ruff.toml`.
- [x] Verify `uv` and `pnpm` environments.

### 3.2: Upstream Sync Pipeline (Complete)
- [x] Implement `UpstreamIngestPipeline` (`tooling/sync-upstreams/upstream_ingest_pipeline.py`).
- [x] Build PreFlight → Sync → Gate(Boot/Lint/Symmetry) → Promote flow.
- [x] LKG (Last Known Good) tags on every successful promotion.
- [x] `--dry-run` mode: run gates against current state without syncing.
- [x] Ruff resolution: `uv run ruff` > `RUFF_BIN` > PATH.
- [x] Boot gate uses `uv lock --check` (runs before lint to prevent lockfile recreation).
- [x] Pre-flight: uncommitted change guard + up-to-date short-circuit.
- [x] Branch safety: `finally` block returns to `integration` on any failure.
- [x] `contribute-upstream.sh`: cherry-pick a fix to a clean upstream branch and push to public fork for PR.
- [x] First live run: confirmed "Already up to date".
- [x] Documentation: `docs/meta/git-strategy.md` and `docs/meta/pipeline-runbook.md`.

### 3.3: Pipeline Gate Failure Tests (Complete)
- [x] Test: merge conflict → verified promotion is blocked.
- [x] Test: symmetry gate failure → verified promotion is blocked.
- [x] Test: boot gate failure → verified promotion is blocked.
- [x] All three gate failure tests pass (`tooling/sync-upstreams/gate_failure_tests.py`).

## Phase 2: qwen_code_stack Migration (Complete — 2026-05-23/24)

### Step 1: Intake Normalization (`qwen_code_stack`) — Complete
- [x] Ruff lint pass — 183 violations cleared
- [x] Ruff format pass — 115 files reformatted
- [x] Mypy type-check pass — 26 errors fixed across 14 files
- [x] Naming review — 9 files renamed, classes/functions updated
- [x] Final verification — zero errors

### Step 4: Config, docs, and scripts migration — Complete
- [x] .qwen/agents/: 19 execution profile .md files migrated
- [x] .qwen/skills/: 21 missing skill definitions migrated
- [x] docs/megalonyx/: 213-file documentation tree migrated
- [x] scripts/megalonyx/: 18 utility scripts migrated, ruff-clean
- [x] config/settings.example.json created (env var references, no secrets)
- [x] qwen_code_stack can now be archived

### Step 2: Migration into monorepo — Complete
- [x] Three uv workspace members created: `apps/control-plane-daemon`, `packages/agent-memory`, `packages/agent-infra`
- [x] All source files copied from `qwen_code_stack`, imports rewritten as package-relative
- [x] Architectural inversion fixed: `SystemLogger` consolidated into `agent-infra` (single source)
- [x] ruff check + mypy clean across 37 source files (commit `4585f6b6c`)

### Step 3: Naming pass — Complete
- [x] File renames via `git mv`: `execution_profile_selector`, `vector_search_tool`, `execution_context`, `stdio_socket_relay`, `tool_executor`, `model_router`, `memory_mcp_server`
- [x] Class renames: `ExecutionProfileSelector`, `VectorSearchTool`, `ExecutionContext`
- [x] Paths migrated to `~/.local/share/megalonyx/`
- [x] Qdrant collections: `agent_memory_local` / `agent_memory_cloud`
- [x] Product identity: "Megalonyx Control Plane"
- [x] CI green on `integration` (commit `a21674cd5`)

## Phase 3: Integration, Documentation, and Boot

### Step 0: CI Fix — Complete
- [x] Create `docs/settings.example.md` (mirrors `config/settings.example.json`)
- [x] Create `docs/megalonyx/.env.md` (mirrors `config/megalonyx/.env.example`)
- [x] Add `tooling/git-hooks/pre-commit` + `tooling/install-hooks.sh` (mirrors CI locally)
- [x] Update CLAUDE.md: branch strategy, standards lint command, hook install instructions
- [x] Push to `integration` + `develop` — CI should be green

### Step 1: Branch promotion — Complete
- [x] Promote `integration` → `develop` (fast-forward merge)
- [x] Update CLAUDE.md branch usage rules (develop = active work; integration = upstream syncs)

### Step 1.5: Documentation system
- [ ] Preserve original Qwen Code README → `docs/upstream/qwen-code-readme.md`
- [ ] Write new `README.md`: plain engineering language, what this is, what's in it, how to use it
- [ ] Create `docs/upstream/cli-architecture.md` — Qwen Code CLI entry points and tool dispatch
- [ ] Create `docs/upstream/agent-framework.md` — SubAgent/Skills system
- [ ] Create `docs/upstream/mcp-servers.md` — bundled MCP servers and what they do
- [ ] Create `docs/upstream/provider-system.md` — how model providers are configured
- [ ] Create `docs/upstream/sync-policy.md` — what we take from upstream and why
- [ ] Audit `docs/megalonyx/`: fix jargon, fill gaps, remove duplicates, mark planned features
- [ ] Refactor `docs/megalonyx/` to target structure (architecture, control-plane-daemon, agent-memory, agent-infra, execution-profiles, memory-consolidation, configuration, operations)
- [ ] Create `docs/gap-analysis.md` — inherited vs added systems, integration points, migration plan
- [ ] Create `docs/index.md` — flat index of all significant doc files

### Step 2: First boot test
- [ ] Verify `uv sync` resolves all three workspace members cleanly
- [ ] Boot `control-plane-daemon` and confirm it starts without error
- [ ] Boot `agent-memory` daemon and confirm Qdrant connection succeeds
- [ ] Smoke-test: ingest one memory record, retrieve it via search

### Step 3: Wire execution profiles
- [ ] Verify `.qwen/agents/` execution profiles load correctly via `ExecutionProfileSelector`
- [ ] End-to-end: submit a task, confirm correct profile is selected and tool dispatch fires

### Step 4: CI coverage
- [ ] Add boot/smoke test to `python-quality.yml` or a separate `integration-test.yml`
- [ ] Confirm gate failure blocks promotion (mirrors Stage 3.3 for the new packages)

### Step 5: Naming enforcement cleanup
- [ ] Replace `print()` debug calls with `SystemLogger` in `command_manager.py`, `state_manager.py`, `memory_embeddings.py`
- [ ] Add `docs/meta/engineering-standards.md` reference to `QWEN.md`
- [ ] Add `.qwen-context` to `config/`, `docs/`, `packages/`, `scripts/`
- [ ] Rename AI-jargon files in `docs/megalonyx/explanation/` to engineering terms
- [ ] Expand CI linter scope after local audit (add `apps/`, `packages/`, `scripts/`, full `docs/`)

## Phase 4: Installer Unification

- [ ] Copy `qwen_code_stack/install.sh` → `scripts/megalonyx/install-megalonyx-stack-legacy.sh` with header comment
- [ ] Audit and update legacy installer paths (`megacode/` → `megalonyx/`, venv → uv, etc.)
- [ ] Write `scripts/megalonyx/install-megalonyx-stack.sh` — uv workspace + Qdrant + bin/ setup
- [ ] Write `scripts/megalonyx/install-megalonyx-full.sh` — composes Qwen Code installer + Megalonyx stack
- [ ] Create `docs/megalonyx/installation.md` — install topology, which installer to use when

---

## Phase 4.5: CI Hardening, Infrastructure, and Upstream PR Preparation (Complete — 2026-05-24/25)

### Architecture: Fork-as-Filter — Complete
- [x] Removed `upstream` remote pointing to QwenLM/qwen-code directly from megalonyx-monorepo
- [x] Renamed `mirror` remote → `upstream` (now points to jdmanring/qwen-code fork)
- [x] Pipeline fetches from the fork — human review gate before any upstream code enters
- [x] Added `PROTECTED_FILES` enforcement to pipeline: ci.yml, e2e.yml, sdk-python/pyproject.toml restored after each merge
- [x] Added `sync-fork-from-qwenlm.sh` — script to promote QwenLM commits into the fork after review
- [x] Updated contribute-upstream.sh: all `mirror` refs → `upstream`
- [x] Updated docs: sync-policy.md, git-strategy.md, CLAUDE.md, upstream-pr-guide.md

### CI: Eliminate npm — Complete
- [x] Rewrote ci.yml for pnpm: added pnpm/action-setup@v4, switched cache to pnpm, replaced npm ci → pnpm install --frozen-lockfile
- [x] Removed scripts that don't exist in our package.json (check:lockfile, check-i18n, test:ci, generate:settings-schema)
- [x] Confirmed release workflows (release.yml, release-sdk.yml, etc.) are guarded by `github.repository == 'QwenLM/qwen-code'` — won't run on our fork, no changes needed

### Infrastructure Gaps — Complete
- [x] Added .github/CODEOWNERS — @jdmanring on all paths
- [x] Added .github/SECURITY.md — responsible disclosure policy, credential file list
- [x] Fixed .github/dependabot.yml — corrected reviewer, re-enabled PRs, added ignore list for pinned packages, weekly Monday schedule targeting develop

### Quality Gates — Complete (with one blocker)
- [x] Created packages/webui/vitest.config.ts — 25 orphaned tests now reachable via pnpm test-all
- [x] Added coverage thresholds to packages/core/vitest.config.ts — 75% statements/lines, 77% functions, 78% branches
- [x] Added staged-file ESLint check to pre-commit hook (fast: only staged files)
- [x] CLI coverage thresholds — added at statements/lines 73%, branches 76%, functions 76% (Phase 4.7, commit 1d98f2acb)

### Upstream PR Backlog — Not Yet Submitted
All branches are prepared but NOT submitted. User must approve each before submission.
See `docs/upstream/upstream-pr-guide.md` and `docs/upstream/upstream-pr-checklist.md`.

| PR | Status |
|---|---|
| PR-1: fix(lint): extend node_modules ignore + yargs import | Pending approval |
| PR-2: fix(openai): narrow toolCall union type | Pending approval |
| PR-3–14: See upstream-pr-guide.md | Pending approval |

---

## Phase 4.6: Fix TypeScript Build Errors in packages/core and packages/cli (Complete — 2026-05-25, commit d99a41a89)

Full inventory and fix plan: `docs/meta/typescript-build-errors.md`

All errors were in QwenLM upstream source. `tsc --build` now exits 0 for both core and CLI.

- [x] Group 1: `pnpm add -D @types/shell-quote --filter @qwen-code/qwen-code-core`
- [x] Group 2: Add `forceFlush(): Promise<void>` to `FileLogExporter` (`src/telemetry/file-exporters.ts:55`)
- [x] Group 3: Add `src/types/abort-signal.d.ts` shim for `AbortSignal.any`
- [x] Group 7: Investigate `@agentclientprotocol/sdk` import in `src/services/fileSystemService.ts:22`
- [x] Group 8: Replace `URL.parse()` with `new URL()` in `src/extension/github.ts:118`
- [x] Group 4: Narrow content union type in `src/ide/ide-client.ts` (5 locations)
- [x] Group 5: Fix `Span | undefined` in `src/core/coreToolScheduler.ts:2524`
- [x] Group 6: Filter nulls in `src/services/gitWorktreeService.ts:830`
- [x] Group 9: Fix `string | string[]` in `src/extension/claude-converter.ts:127`
- [x] Group 10: Filter undefined in `src/extension/extensionManager.ts:1337`
- [x] Group 11: Annotate `child` variable in `src/tools/monitor.ts` and `src/utils/filesearch/crawler.ts`
- [x] Verify: `cd packages/core && pnpm exec tsc --build` exits 0
- [x] Verify: `cd packages/cli && pnpm exec tsc --build` exits 0
- [x] Run `pnpm test-all` — confirm no regressions

---

## Phase 4.7: Test Infrastructure and Coverage Gates (Complete — 2026-05-25)

### Test Failures Resolved
- [x] vitest.config.ts alias ordering: moved all `@qwen-code/acp-bridge` subpath aliases before the
      base package alias — resolved 33 CLI test file failures caused by `@rollup/plugin-alias`
      prefix-matching the base alias first (commit cee2e0f18)
- [x] httpAcpBridge.test.ts: added `unstable_forkSession` to `FakeAgent` mock for ACP SDK v0.22.1
      rename from `unstable_resumeSession`; updated 2 test cases to use `forkSessionImpl`/`forkSessionCalls`
      (same commit)

### Coverage Gates
- [x] Both core and CLI vitest configs: added `reportOnFailure: true` — vitest 3.2.4 defaults to
      `false`, silently skipping coverage writes when any test fails (commit 1d98f2acb)
- [x] CLI coverage thresholds added: statements/lines 73%, branches 76%, functions 76%
      (measured baseline: lines 76.9%, functions 79.9%, branches 80.1%; set ~4% below)
- [x] Core `reportOnFailure` fixed (thresholds 75/78/77/75 were already in place)

### Current test status
- 376/377 CLI test files passing (1 file, 2 tests — pre-existing upstream issue in `useAtCompletion`
  re: directory trailing slash in suggestions; verified pre-existing via git stash check)

---

## Phase 5: Dependency Upgrades

Full plan: `docs/megalonyx/dependency-upgrade-plan.md`

### Phase A — Trivial housekeeping (no code changes)
- [ ] nx 22.7.2 → 22.7.3 (`package.json`)
- [ ] mime 4.0.7 → 4.1.0 (`packages/core/package.json`)
- [ ] @lydell/node-pty* 1.2.0-beta.10 → beta.12 (`packages/core/package.json`)
- [ ] @teddyzhu/clipboard* 0.0.5 → 0.0.10 (`packages/cli/package.json`)
- [ ] @types/archiver ^6 → ^7 (`packages/cli/package.json`)
- [ ] @types/supertest ^6 → ^7 (`packages/cli/package.json`)
- [ ] @types/react + react-dom ^18 → ^19 (`packages/web-templates/package.json`)
- [ ] Remove @types/diff from cli + core (deprecated — diff 7.x ships own types)
- [ ] Remove @types/dotenv from cli + core (deprecated — dotenv 16.x ships own types)
- [ ] Remove @types/minimatch from core (deprecated — minimatch 9.x ships own types)
- [ ] Remove @types/tar from core (deprecated — tar 7.x ships own types)
- [ ] `pnpm update semver yaml` — pick up 7.8.1 and 2.9.0 from lockfile
- [ ] Verify: `node dist/cli.js --version` returns 0.16.1
- [ ] Commit Phase A

### Phase B — ESLint 9 + @typescript-eslint 8
- [ ] eslint 8.57.1 → ^9.0.0 (`package.json` root + `packages/sdk-typescript`)
- [ ] @typescript-eslint/* 7.18.0 → ^8.0.0 (same locations)
- [ ] Verify all ESLint plugins support ESLint 9 (react, react-hooks, import, vitest, storybook)
- [ ] `pnpm install` + `pnpm check`
- [ ] Fix any new lint errors from stricter @typescript-eslint 8 rules
- [ ] Commit Phase B

### Phase C — OpenTelemetry suite
- [ ] Bump all @opentelemetry/* OTLP packages: ^0.203.0 → ^0.218.0 (`packages/core/package.json`)
- [ ] sdk-trace-node: ^2.0.0 → ^2.7.0
- [ ] `pnpm install` + run core tests
- [ ] Verify telemetry SDK initialization (sdk.ts)
- [ ] Commit Phase C

### Phase D — iconv-lite 0.6 → 0.7
- [ ] Bump `packages/core/package.json`: ^0.6.3 → ^0.7.0
- [ ] Verify iconvHelper.ts default import still works
- [ ] Commit Phase D

### Phase E — comment-json 4 → 5
- [ ] Bump `packages/cli/package.json`: ^4.2.5 → ^5.0.0
- [ ] Verify parse/stringify API unchanged
- [ ] Commit Phase E

### Phase F — chokidar 4 → 5
- [ ] Bump `packages/core/package.json`: ^4.0.3 → ^5.0.0
- [ ] Verify FSWatcher API unchanged in skill-manager.ts
- [ ] Commit Phase F

### Phase G — esbuild 0.25 → 0.28
- [ ] Bump `package.json` root: "^0.25.0" → "^0.28.0"
- [ ] `pnpm install` + `node esbuild.config.js`
- [ ] Verify `node dist/cli.js --version` + `--help`
- [ ] Commit Phase G

### Phase H — vitest 3 → 4 + vite 5 → 6
- [ ] Update overrides in `pnpm-workspace.yaml`: vitest + @vitest/coverage-v8 → ^4.0.0, vite → ^6.0.0
- [ ] Bump @vitejs/plugin-react: ^4 → ^6 in webui + web-templates
- [ ] `pnpm install` + `pnpm test-all`
- [ ] Fix any vitest 4 API changes in test configs
- [ ] Commit Phase H

### Phase I — web-tree-sitter 0.24 → 0.26
- [ ] Bump `packages/core/package.json`: ^0.24.7 → ^0.26.0
- [ ] Verify shellAstParser.ts Parser.init() + WASM loading
- [ ] Test both bundle and dev mode
- [ ] Commit Phase I

### Phase J — @xterm/headless 5 → 6
- [ ] Bump `packages/core/package.json`: 5.5.0 → ^6.0.0
- [ ] Update shellExecutionService.ts + terminalSerializer.ts for any API changes
- [ ] Test PTY chain + ANSI color serialization
- [ ] Commit Phase J

### Phase K — @anthropic-ai/sdk 0.36 → 0.98
- [ ] Bump `packages/core/package.json`: ^0.36.1 → ^0.98.0
- [ ] Read CHANGELOG 0.37→0.98 for RawMessageStreamEvent, MessageCreateParams, Tool types
- [ ] Update anthropicContentGenerator.ts streaming event switch (lines 771-968)
- [ ] Update thinking config (lines 681-757) and beta headers (lines 356-394)
- [ ] Test: streaming, tool calling, thinking, caching, DeepSeek proxy
- [ ] Commit Phase K

### Phase L — @google/genai 1 → 2
- [ ] Bump `packages/core/package.json`: 1.30.0 → ^2.0.0
- [ ] Read v2 migration guide
- [ ] Update geminiContentGenerator.ts + geminiChat.ts
- [ ] Run `tsc --noEmit` to find all 60+ type import breakages
- [ ] Fix type imports across all affected files
- [ ] Test: streaming, tool calling, thinking, token counting, embedding
- [ ] Commit Phase L

### Phase M — TypeScript 5.3.3 → 6.x
- [ ] Investigate why packages/cli/tsconfig.json excludes 97 test files
- [ ] Add strict: true to packages/vscode-ide-companion/tsconfig.json
- [ ] Bump override in `pnpm-workspace.yaml`: "5.3.3" → "^6.0.0"
- [ ] `pnpm install` + `tsc --noEmit` per package
- [ ] Fix type errors package by package (core → cli → others)
- [ ] Full test suite + rebuild + smoke test
- [ ] Commit Phase M

---

## Archive
*Superseded approaches, kept for reference.*

- [x] Initial file migration (moved to apps/qwen-orchestrator)
- [x] Initial branching strategy (documented)
- [x] Initial config relocation (moved to .qwen/config)
