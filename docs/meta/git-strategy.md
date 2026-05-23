# Git Strategy: The Sovereign Flow

## Branching Architecture

| Branch | Source | Purpose | Authority |
| :--- | :--- | :--- | :--- |
| `upstream-mirror` | `upstream/main` | Clean snapshot of official qwen-code. Windows artifacts removed and committed. | Read-only |
| `integration` | `upstream-mirror` | Sovereignization layer — ruff, symmetry, and boot gates enforced. | Integration Lead |
| `develop` | `integration` | Active feature development on the verified base. | Developer |
| `main` | `develop` | Stable, production-ready Sovereign Blueprint. | Architect |

### Why a separate `upstream-mirror` branch?

GitHub does not allow making a fork private. The solution is a dual-track setup:

- A **public fork** of qwen-code on GitHub (the `mirror` remote) — used only for PR submission back to upstream.
- This **private monorepo** (`origin`) — where all sovereign development happens.

`upstream-mirror` is reset directly from `upstream/main` (not from the public fork), so upstream code reaches the monorepo without going through a public intermediary.

---

## The Integration Pipeline

All upstream ingestion runs through the Integration Orchestrator, which enforces three gates before any change reaches `integration`.

```
upstream/main
    |
    v  [git fetch + reset --hard]
upstream-mirror  [Windows .bat files purged and committed]
    |
    v  [git merge into short-lived staging branch off integration]
sync/staging-TIMESTAMP
    |
    v  Gate 1: ruff lint    (uv run ruff check .)
    v  Gate 2: symmetry     (config/ <-> docs/ 1:1 mirror)
    v  Gate 3: boot         (uv lock --check)
    |
    v  [--ff-only merge + LKG tag]
integration
```

### Running the pipeline

```bash
# Full sync: fetch upstream, merge, run gates, promote if green
python3 tooling/sync-upstreams/orchestrator.py

# Dry run: run gates against current state, no commits or tags
python3 tooling/sync-upstreams/orchestrator.py --dry-run
```

### Last Known Good (LKG) tags

Every successful promotion creates an annotated tag (`LKG-YYYYMMDD-HHMM`). To roll back:

```bash
git checkout LKG-20260523-1200   # inspect
git checkout integration
git reset --hard LKG-20260523-1200  # roll back (destructive — confirm first)
```

---

## Contributing a Fix Back to Upstream

When a bug is found in the sovereign layer that also affects the official project:

```bash
./tooling/sync-upstreams/contribute-upstream.sh <commit-hash> <branch-name>
```

**What it does:**

1. Creates a clean branch from `upstream/main` — no monorepo history, no sovereign changes.
2. Cherry-picks only your fix commit onto it.
3. Pushes the branch to your public fork (the `mirror` remote).
4. Prints the direct URL to open a PR against `QwenLM/qwen-code`.

**Requirement:** a `mirror` remote pointing to your public fork of qwen-code.

```bash
git remote add mirror https://github.com/YOUR_FORK/qwen-code.git
```

---

## Tooling Reference

| Script | Purpose |
| :--- | :--- |
| `orchestrator.py` | Full pipeline entry point. Use this for all syncs. |
| `verification-gate.sh` | Standalone gate runner (lint + symmetry + boot). |
| `raw-inline.sh` | Low-level: resets `upstream-mirror` to `upstream/main`. |
| `integrate.sh` | Low-level: merges `upstream-mirror` into current branch. |
| `contribute-upstream.sh` | Prepares a fix for upstream PR submission. |
| `merge-upstream.sh` | **Deprecated.** Exits with error and redirects to orchestrator. |

---

## Ruff Configuration

Ruff is configured exclusively in `.ruff.toml` at the project root. The `[tool.ruff]` section in `pyproject.toml` is intentionally absent — having config in both places causes silent conflicts where `.ruff.toml` wins without warning.

All pipeline scripts resolve ruff via `uv run ruff` (project-pinned version) so every environment uses the same binary. Override with `RUFF_BIN=/path/to/ruff` if needed.
