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

## Phase 2: qwen_code_stack Migration

### Step 1: Intake Normalization (`qwen_code_stack`) — In Progress
- [x] Ruff lint pass — 183 violations cleared
- [ ] Ruff format pass
- [ ] Mypy type-check pass
- [ ] Naming review (file names, class names, function names match engineering-standards.md)
- [ ] Final verification (zero errors)

### Step 2: Migration
- [ ] Move normalized `qwen_code_stack` into `integration` branch.
- [ ] Extract shared logic to `packages/`.
- [ ] Merge to `develop` after gate pass.
- [ ] First successful monorepo boot test.

---

## Archive
*Superseded approaches, kept for reference.*

- [x] Initial file migration (moved to apps/qwen-orchestrator)
- [x] Initial branching strategy (documented)
- [x] Initial config relocation (moved to .qwen/config)
