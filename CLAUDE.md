# CLAUDE.md — AI Agent Guide for megalonyx-monorepo

This file is loaded automatically by Claude Code. It tells you what this repo is, how it works, and how to operate in it without asking the user for context.

---

## What this repo is

A private monorepo that:
1. Tracks and selectively ingests changes from the upstream [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) project via a controlled pipeline.
2. Houses the Megalonyx sovereign AI stack (being migrated in from `qwen_code_stack`).
3. Serves as the integration point between upstream tooling and proprietary extensions.

---

## Branch architecture

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
| `todo.md` | Current work tracking — read this to understand project state |

---

## What to avoid

- **Do not commit directly to `upstream-mirror`** — the pipeline resets it.
- **Do not modify `ci.yml`** — it is upstream content and will be overwritten on sync.
- **Do not use `git commit --no-verify`** unless debugging the hook itself.
- **Do not name things with project metaphors** — use plain engineering terms.
