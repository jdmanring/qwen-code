# CLAUDE.md — AI Agent Guide for megalonyx-monorepo

This file is loaded automatically by Claude Code. It tells you what this repo is, how it works, and how to operate in it without asking the user for context.

---

## What this repo is

A private monorepo that:
1. Tracks and selectively ingests changes from the upstream [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) project via a controlled pipeline.
2. Houses the Megalonyx sovereign AI stack (being migrated in from `qwen_code_stack`).
3. Serves as the integration point between upstream tooling and proprietary extensions.

---

## Remotes and branch architecture

**Remotes:**

| Remote | URL | Purpose |
| :--- | :--- | :--- |
| `origin` | `jdmanring/megalonyx-monorepo` | Private monorepo |
| `upstream` | `jdmanring/qwen-code` | Fork — inbound filter for pipeline AND outbound PR channel |

The pipeline fetches from the **fork** (`jdmanring/qwen-code`), not from QwenLM directly.
This means QwenLM commits must be reviewed and promoted into the fork before they can enter
our pipeline. Run `tooling/sync-upstreams/sync-fork-from-qwenlm.sh` inside a fork checkout.

**Branches:**

| Branch | Purpose |
| :--- | :--- |
| `upstream-mirror` | Reset to `upstream/main` on every sync. Never commit here. |
| `integration` | Upstream sync target only. Changes come in via the pipeline, not direct commits. |
| `develop` | Active development branch. All Megalonyx work happens here. |
| `main` | Stable release branch. |

**Active work happens on `develop`.** When in doubt, check out `develop`.

---

## Running the upstream sync pipeline

```bash
# Full sync — fetch upstream, run gates, promote if green
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py

# Check gates only, no git operations
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run

# Run gate failure tests (verifies all three failure modes are blocked)
python3 tooling/sync-upstreams/gate_failure_tests.py
```

The pipeline requires: `integration` branch, `upstream` and `origin` remotes, `uv` on PATH, no uncommitted tracked changes.

See `docs/meta/pipeline-runbook.md` for failure recovery.

---

## Python tooling

| Tool | Command | What it checks |
| :--- | :--- | :--- |
| Ruff lint | `uv run ruff check .` | Style, imports, bugs |
| Ruff format | `uv run ruff format .` | Formatting |
| Mypy | `uv run mypy tooling/ packages/sdk-python/src/` | Type safety |
| Symmetry | `uv run python3 tooling/symmetry_check.py` | `.qwen/config/` ↔ `docs/` mirror |
| Standards lint | `uv run python3 tooling/project_standards_linter.py --strict tooling/ docs/meta/` | Naming, config symmetry, debug prints |

All five run in CI (`python-quality.yml`). The pre-commit hook (`tooling/git-hooks/pre-commit`) runs ruff + standards lint locally. Install it once:

```bash
bash tooling/install-hooks.sh
```

---

## Naming standard

Names must be immediately descriptive. An AI reading a name should predict the contents without opening the file.

- **Good**: `gate_failure_tests.py`, `upstream_ingest_pipeline.py`, `intake_normalization`
- **Bad**: `chaos_tests.py`, `orchestrator.py`, `sovereign_scrub`

Full standard: `docs/meta/engineering-standards.md`

---

## Key files

| File | Purpose |
| :--- | :--- |
| `tooling/sync-upstreams/upstream_ingest_pipeline.py` | Upstream sync pipeline — fetch → gate → promote |
| `tooling/sync-upstreams/gate_failure_tests.py` | Tests that each pipeline gate correctly blocks failures |
| `tooling/symmetry_check.py` | Verifies `.qwen/config/` ↔ `docs/` 1:1 mirror |
| `tooling/project_standards_linter.py` | Enforces naming, config symmetry, and code standards |
| `tooling/git-hooks/pre-commit` | Pre-commit hook source — install via `tooling/install-hooks.sh` |
| `docs/meta/pipeline-runbook.md` | Operations guide — what to do when gates fail |
| `docs/meta/git-strategy.md` | Branch architecture and pipeline flow diagram |
| `docs/meta/engineering-standards.md` | Code quality and naming requirements |
| `ROADMAP.md` | Strategic architecture, completed phases, and feature targets |

---

## Task tracking

All executable work lives in the task board — use `TaskCreate`, `TaskList`, and `TaskUpdate`.

- **Find work**: `TaskList` — pending tasks with no owner and no open blockers are available to claim.
- **Claim work**: `TaskUpdate {taskId, owner: "<agent-id>", status: "in_progress"}` before starting.
- **Complete work**: `TaskUpdate {taskId, status: "completed"}` — this unblocks any dependent tasks.
- **Add work**: `TaskCreate` with a description rich enough to start cold (context, steps, verification).
- **Model dependencies**: use `addBlockedBy`/`addBlocks` — independent tasks can be claimed in parallel.

`ROADMAP.md` is the strategic reference (phases, architecture, feature targets). Do not add task-level items to it.

`todo.md` and `claude.todo.md` have been deleted. Do not recreate them.

---

## Security constraints

These are always in effect — no exceptions:

- **Never commit**: `config/settings.json`, `config/megalonyx/secrets.json`, `config/config.yaml`
- **Push to `origin` only** (`jdmanring/megalonyx-monorepo`) for all development work
- **Push contribution branches to `upstream`** (`jdmanring/qwen-code` fork) only
- **No PRs to QwenLM/qwen-code — ever** (permanent policy)

---

## What to avoid

- **Do not commit directly to `upstream-mirror`** — the pipeline resets it.
- **Do not modify protected files without updating `PROTECTED_FILES`** in `upstream_ingest_pipeline.py` — see `docs/upstream/sync-policy.md` for the full list.
- **Do not use `git commit --no-verify`** unless debugging the hook itself.
- **Do not name things with project metaphors** — use plain engineering terms.
