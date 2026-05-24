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

## Archive
*Superseded approaches, kept for reference.*

- [x] Initial file migration (moved to apps/qwen-orchestrator)
- [x] Initial branching strategy (documented)
- [x] Initial config relocation (moved to .qwen/config)
