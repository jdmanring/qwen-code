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

### Step 1.5: Documentation system — Complete (2026-05-25, large docs reorg)
- [x] Preserve original Qwen Code README → `docs/upstream/qwen-code-readme.md`
- [x] Write new `README.md`: plain engineering language, what this is, what's in it, how to use it
- [x] Create `docs/upstream/cli-architecture.md` — Qwen Code CLI entry points and tool dispatch
- [x] Create `docs/upstream/agent-framework.md` — SubAgent/Skills system
- [x] Create `docs/upstream/mcp-servers.md` — bundled MCP servers and what they do
- [x] Create `docs/upstream/provider-system.md` — how model providers are configured
- [x] Create `docs/upstream/sync-policy.md` — what we take from upstream and why
- [x] Audit `docs/megalonyx/`: fix jargon, fill gaps, remove duplicates, mark planned features
- [x] Refactor `docs/megalonyx/` to target structure (architecture, control-plane-daemon, agent-memory, agent-infra, execution-profiles, memory-consolidation, configuration, operations)
- [x] Create `docs/gap-analysis.md` — inherited vs added systems, integration points, migration plan
- [x] Create `docs/index.md` — flat index of all significant doc files

### Step 2: First boot test — Complete (2026-05-25)
- [x] Verify `uv sync` resolves all three workspace members cleanly
- [x] Boot `control-plane-daemon` and confirm it starts without error
- [x] Boot `agent-memory` daemon and confirm Qdrant connection succeeds
- [x] Smoke-test: ingest one memory record, retrieve it via search

### Step 3: Wire execution profiles — Complete (2026-05-25)
- [x] Verify `.qwen/agents/` execution profiles load correctly via `ExecutionProfileSelector`
- [x] End-to-end: submit a task, confirm correct profile is selected and tool dispatch fires

### Step 4: CI coverage — Complete (2026-05-25)
- [x] Add boot/smoke test to `python-quality.yml` or a separate `integration-test.yml`
- [x] Confirm gate failure blocks promotion (mirrors Stage 3.3 for the new packages)

### Step 5: Naming enforcement cleanup — Complete (2026-05-25)
- [x] Replace `print()` debug calls with `SystemLogger` in `command_manager.py`, `state_manager.py`
- [x] Add `docs/meta/engineering-standards.md` reference to `QWEN.md`
- [x] Add `.qwen-context` to `config/`, `docs/`, `packages/`, `scripts/`
- [x] Rename AI-jargon files in `docs/megalonyx/explanation/` to engineering terms
- [x] Expand CI linter scope after local audit (add `apps/`, `packages/`, `scripts/`, full `docs/`)

## Phase 4: Installer Unification — Complete (2026-05-25)

- [x] Copy `qwen_code_stack/install.sh` → `scripts/megalonyx/install-megalonyx-stack-legacy.sh` with header comment (later superseded and deleted)
- [x] Audit and update legacy installer paths (`megacode/` → `megalonyx/`, venv → uv, etc.)
- [x] Write `scripts/megalonyx/install-megalonyx-stack.sh` — uv workspace + Qdrant + bin/ setup
- [x] Write `scripts/megalonyx/install-megalonyx-full.sh` — composes Qwen Code installer + Megalonyx stack + upstream remote config
- [x] Create `docs/megalonyx/installation.md` — install topology, which installer to use when

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

## Phase 4.8: pnpm Developer Experience Hardening (In Progress — 2026-05-25)

### Completed
- [x] `scripts/generate-git-commit-info.js`: removed `read-package-up` phantom dep — now reads
      `packages/cli/package.json` directly via `readFileSync`. Previously would fail under pnpm
      strict isolation and would read root version 0.1.0 instead of CLI version 0.16.1.
- [x] Root `package.json`: added `workspaces` field for `scripts/clean.js` compatibility
      (pnpm uses `pnpm-workspace.yaml`; `clean.js` reads `package.json#workspaces`)
- [x] Root `package.json`: added scripts — `build`, `build:packages`, `build:all`, `bundle`,
      `start`, `typecheck`, `format`, `clean`, `preflight`
- [x] `packages/web-templates/package.json`: added `prettier: ^3.5.3` devDep — `build.mjs`
      imports prettier at build time; pnpm strict isolation exposes this phantom dep
- [x] Root `package.json`: added `prettier: ^3.5.3` devDep (upstream has it; we were missing it)
- [x] `pnpm build` fixed: targets `nx run @qwen-code/qwen-code:build` (CLI + deps only);
      `pnpm build:all` available for all packages. `node dist/cli.js --version` → 0.16.1

- [x] Root `package.json`: added `"packageManager": "pnpm@11.2.2"` — enables Corepack to auto-install
      correct pnpm version on clone; blocks accidental `npm install`
- [x] `.npmrc`: added `strict-peer-dependencies=false` (upstream packages have unresolved peer deps)
      and `link-workspace-packages=true` (explicit workspace symlink behavior)
- [x] README: added Node.js/pnpm Getting Started section with command table and npm→pnpm comparison

### Remaining
- [ ] vscode-ide-companion TypeScript errors — see tracked issue below
- [ ] **FUTURE: Migrate `overrides` → `pnpm catalog:`** — pnpm 9+ feature. Replace
      `pnpm-workspace.yaml overrides` with `catalog:` entries; update each `package.json` to use
      `"vitest": "catalog:"` etc. Makes version pinning visible and opt-in rather than silent global
      override. Requires touching ~15 package.json files. Track as Phase 4.9.

### Known Issue: vscode-ide-companion build (`pnpm build:all` only — does not block `pnpm build`)
`qwen-code-vscode-ide-companion:build` has 20+ TypeScript errors exposed by pnpm strict isolation
and upstream API changes. These do NOT affect the CLI build (`pnpm build` succeeds). Tracked here
for future resolution:

| Category | Error | Files affected |
|---|---|---|
| Phantom dep | `@qwen-code/qwen-code-core` not in devDeps or tsconfig paths | diff-manager, extension, ide-server, open-files-manager, qwenSessionManager/Reader, sessionExportService, settingsWriter, acpModelInfo, imageSupport (11+ files) |
| ACP SDK rename | `unstable_listSessions` → unknown (v0.22.1) | acpConnection.ts:561–562 |
| SDK API missing | `DaemonClient`, `DaemonSessionClient` not in `@qwen-code/sdk` | daemonIdeConnection.ts:21–22 |
| webui API missing | `stripZeroWidthSpaces`, `AskUserQuestionDialog`, `InsightProgressCard`, `ImageMessageRenderer`, `ImagePreview`, `ZERO_WIDTH_SPACE` not in `@qwen-code/webui` | App.tsx:26–46, sessionExportService.ts:26 |
| Type narrowing | `ContentBlock[] | {type,text}[]` not assignable | acpConnection.ts:475 |
| Type narrowing | `UserMessageProps` type mismatch | App.tsx:194 |
| Implicit any | parameter `m` | settingsWriter.test.ts:123 |

Fix order when addressed: phantom dep first (tsconfig paths + devDeps), then API changes
(check @agentclientprotocol/sdk v0.22.1 changelog for listSessions rename, check @qwen-code/sdk
exports for Daemon types, check @qwen-code/webui exports for missing members).

---

## Phase 5: Dependency Upgrades

Full plan: `docs/megalonyx/dependency-upgrade-plan.md`

### Absorbed via upstream QwenLM merges — Complete

These were completed by syncing QwenLM's commits rather than manual upgrade:

- [x] Phase C — @opentelemetry/* 0.203 → 0.218; sdk-trace-node ^2.7.0; instrumentation-undici added
- [x] Phase D — iconv-lite 0.6 → 0.7
- [x] Phase E — comment-json 4 → 5
- [x] Phase F — chokidar 4 → 5
- [x] Phase J — @xterm/headless 5 → 6
- [x] Phase K — @anthropic-ai/sdk 0.36 → 0.98
- [x] Phase L — @google/genai 1 → 2.6
- [x] Phase A (partial) — mime 4.0.7→4.1.0, node-pty beta.10→beta.12, @types/react→^19 absorbed;
      @types/diff, @types/dotenv, @types/minimatch, @types/tar removed from core

### Monorepo upgrades — Complete

- [x] Phase H — vitest 3→4, vite 5→6, @vitejs/plugin-react ^5, vitest 4 config migration
      Contributed to upstream fork: `contribute/phase-h-vitest-vite`
- [x] Phase I — web-tree-sitter 0.24→0.26.9, shellAstParser.ts API migration, WASM binaries updated
      Contributed to upstream fork: `contribute/phase-i-web-tree-sitter`
- [x] Phase M — TypeScript 5.3.3→6.0.3, remove deprecated baseUrl, test mock isolation fixes
      Contributed to upstream fork: `contribute/phase-m-typescript-6`

### Still pending

- [ ] **Phase B/ESLint 10** — `eslint` 9.39.4→10.4.0, `@eslint/js`→10.0.1,
      `eslint-plugin-react-hooks` 5.2.0→7.1.1 (Dependabot PR open); flat config already in place
- [ ] **Phase G/esbuild** — check root `package.json` pin vs latest; bump if behind
- [ ] **Vite 8** — `vite` 6.x→8.x + `@vitejs/plugin-react` 4.7.0→6.0.2 (Dependabot PR open);
      two major versions — review breaking changes before upgrading
- [ ] **tailwindcss 4** — 3.4.19→4.3.0 (Dependabot PR open); v4 changes config format to CSS-based;
      HIGH risk — defer until user prioritizes

### Phase A remaining items (low priority)
- [ ] nx 22.7.2 → latest
- [ ] @teddyzhu/clipboard* 0.0.5 → 0.0.10
- [ ] @types/archiver ^6 → ^7
- [ ] @types/supertest ^6 → ^7
- [ ] `pnpm update semver yaml` — pick up latest from lockfile
- [ ] Verify: `node dist/cli.js --version` returns 0.16.1 after each batch

---

## Phase 4.9: Upstream Contribution and Sync (Complete — 2026-05-26)

### Build Verification — Complete
- [x] `pnpm run build` succeeds; `node dist/cli.js --version` → 0.16.1
- [x] Fixed `packages/acp-bridge/tsconfig.json`: removed deprecated `baseUrl` (TS 6 TS5101)
- [x] Created `packages/memory/pyproject.toml` to register uv workspace member

### Upstream Fork Contributions — Complete
Three clean cherry-pick branches on `jdmanring/qwen-code` (PR to QwenLM pending user approval):
- [x] `contribute/phase-h-vitest-vite` — vitest 3→4, vite 5→6 upgrade
- [x] `contribute/phase-i-web-tree-sitter` — web-tree-sitter 0.24→0.26.9
- [x] `contribute/phase-m-typescript-6` — TypeScript 5.3.3→6.0.3

### QwenLM Sync (10 commits) — Complete
- [x] Synced: abort signal refactor, headless guardrails, runBudget, parallel agent display,
      telemetry/traceparent propagation, skill creation fix, several bug fixes
- [x] LKG tag created: `LKG-20260526-0117`
- [x] Merged integration → develop; origin/develop updated

### Pipeline Hardening — Complete
- [x] `upstream_ingest_pipeline.py`: auto-resolve `package-lock.json` on merge (keep ours — pnpm)
- [x] `upstream_ingest_pipeline.py`: use `core.editor=true` for `merge --continue`
- [x] GitHub notifications cleared (44 notifications, all stale failures now resolved)

---

## Archive
*Superseded approaches, kept for reference.*

- [x] Initial file migration (moved to apps/qwen-orchestrator)
- [x] Initial branching strategy (documented)
- [x] Initial config relocation (moved to .qwen/config)

## Phase 6: Operational Rigor & Data Completeness (In Progress)

- [ ] Implement Data Completeness Standard: transform [S-READ] into mandatory pagination loop
- [ ] Update [A-VERIFY] to require hard evidence (exit codes/stdout)
- [ ] Overhaul context-window-optimization.md: replace Token Efficiency with Session-Level Resource Optimization
- [ ] Document 'Incomplete-Information Waste' in optimization docs
- [ ] Formalize Iterative Discovery Protocol (Breadth -> Semantic -> Depth)
- [ ] Add mandatory 'Data Exhaustion Check' to discovery process
- [ ] Audit and align all specialized agent prompts with new standards
