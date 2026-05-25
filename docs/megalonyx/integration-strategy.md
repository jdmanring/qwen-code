# Integration Strategy: Integrated Monorepo

## Objective

Transition from an installer wrapper around external tools into a fully integrated platform.
This means merging the Megalonyx agent stack, proprietary memory system, and the upstream
QwenLM/qwen-code CLI into a single versioned repository with a controlled upstream sync pipeline.

---

## Architecture: monorepo with upstream sync

All components live in one repository. The upstream QwenLM/qwen-code project is tracked as a
remote and pulled through a quality-gated pipeline — not forked and abandoned.

**Why monorepo:**
- A single commit updates both the agent stack and the memory system in sync
- Shared libraries (agent-infra) are managed once, consumed by multiple packages
- Refactoring a function and updating its call site happens atomically
- Engineering standards (naming, type hints, config-doc mirroring rules) apply uniformly

**Upstream sync is not a fork.** Changes from QwenLM/qwen-code flow through
`tooling/sync-upstreams/upstream_ingest_pipeline.py` which gates on ruff, mypy, mirroring, and
boot verification before promoting to `integration`. This means we receive upstream bug fixes and
security updates without overwriting our own work.

---

## Repository structure

```
megalonyx-monorepo/
  apps/
    control-plane-daemon/    orchestration: intent classify -> decompose -> execute
  packages/
    agent-memory/            memory: Qdrant ingest, search, MCP server
    agent-infra/             shared: logging, git worktree, cron
    sdk-python/              upstream: QwenLM Python SDK (do not modify)
  tooling/                   internal: sync pipeline, linters, smoke tests
  scripts/
    megalonyx/               stack: install, start, stop, health
    installation/            upstream: Qwen Code installers (do not modify)
  config/                    templates and static config (no secrets)
  docs/                      mirrors config/ structure + megalonyx/ + upstream/
  bin/                       mega-* entry points
  .qwen/                     agents/, skills/, commands/ loaded by Qwen Code
```

---

## Branch architecture

| Branch | Purpose | Rules |
|---|---|---|
| `upstream-mirror` | Reset to `upstream/main` on every sync | Never commit here |
| `integration` | Upstream sync target | Changes come in via pipeline only |
| `develop` | Active Megalonyx development | All stack work happens here |
| `main` | Stable release | Merge from develop when stable |

Flow: `upstream/main` -> `upstream-mirror` -> pipeline gates -> `integration` -> `develop` -> `main`

---

## Implementation phases

### Phase 1 — Foundation (complete)
- Base repository established from QwenLM/qwen-code fork
- Upstream remote configured and sync pipeline operational
- `packages/`, `apps/`, `tooling/` directory structure in place
- Branch architecture (`upstream-mirror`, `integration`, `develop`, `main`) enforced

### Phase 2 — Standardization (complete)
- All qwen_code_stack packages migrated into monorepo with renamed modules:
  - `packages/core/src/` -> `apps/control-plane-daemon/src/control_plane_daemon/`
  - `packages/memory/` -> `packages/agent-memory/src/agent_memory/`
  - `packages/infra/` -> `packages/agent-infra/src/agent_infra/`
- Naming standards enforced: no AI jargon, no project metaphors, plain engineering terms
- Config/docs mirroring enforced by `project_standards_linter.py` and `symmetry_check.py`
- Pre-commit hook and CI pipeline both run the full quality gate
- All three packages importable via `uv sync --all-packages`

### Phase 3 — Integration (in progress)
- Execution pipeline wired end-to-end: intent classify -> profile select -> tool execute
- Smoke tests cover boot verification, profile routing, and memory round-trip
- Integration CI workflow with Qdrant service container
- Installer unification: `install-megalonyx-stack.sh` (in progress)
- Remaining test migration from qwen_code_stack: fidelity/, debug/, validators/

### Phase 4 — Verification (planned)
- Full end-to-end test suite passing against live services
- Mirroring audit: all new config mirrored in docs
- Deployment validation: install-megalonyx-stack.sh verified on clean machine
- T3 GUI integration
- Public release repo preparation

---

## What we do not modify

- `scripts/installation/` — upstream Qwen Code installers, overwritten on sync
- `packages/sdk-python/` — upstream Python SDK, tracked but not modified
- `ci.yml` — upstream CI, overwritten on sync
- Any file on the `upstream-mirror` branch

---

## Key decisions on record

**uv workspace over standalone venv**: The qwen_code_stack used an isolated venv with manually
pinned PyTorch. The monorepo uses uv workspace so all three packages share a single lockfile,
imports are editable, and `uv sync --all-packages` replaces the entire venv setup step.

**Composer pattern for installers**: `install-megalonyx-full.sh` calls the upstream Qwen Code
installer and then `install-megalonyx-stack.sh` in sequence. We do not extend the upstream
installer directly, which would create a merge conflict on every sync.

**README.md per directory over custom context files**: Earlier design used `.qwen-context` files
(our own invention). Replaced with `README.md` per directory — the same standard used by
Kubernetes, VS Code, etc. GitHub renders it when browsing; AI agents disambiguate by full path.
