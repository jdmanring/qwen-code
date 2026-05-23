# Git Strategy: The Sovereign Flow

## Branch Architecture

| Branch | Tracks | Purpose | Who writes to it |
| :--- | :--- | :--- | :--- |
| `upstream-mirror` | `upstream/main` (QwenLM/qwen-code) | Clean snapshot of official upstream. Reset on every sync — never commit local work here. | Pipeline only |
| `integration` | `upstream-mirror` (via pipeline) | Normalization layer. All upstream changes must pass three gates before landing here. | Pipeline + Integration Lead |
| `develop` | `integration` | Active feature development on the verified base. | Developers |
| `main` | `develop` | Stable, production-ready release branch. | Architect |

> `develop` and `main` are not yet restored from `origin`. Active work is on `integration`.

---

## Why Two Remotes?

GitHub does not allow making a fork private. The solution is a two-track setup:

- **`upstream` remote** → `QwenLM/qwen-code` (official source, read-only)
- **`origin` remote** → this private monorepo (all sovereign development)
- **`mirror` remote** → a public fork of qwen-code on GitHub (used only to submit PRs back upstream)

Upstream code flows: `upstream/main` → `upstream-mirror` → `integration`. It never passes through the public fork. The public fork is used only in the outbound direction when contributing fixes back.

---

## The Upstream Ingest Pipeline

All upstream ingestion runs through `tooling/sync-upstreams/upstream_ingest_pipeline.py`. It enforces three gates in a specific order before any change reaches `integration`.

```
upstream/main  (QwenLM/qwen-code)
    |
    v  git fetch upstream main
    |  git rev-list --count upstream/main ^integration
    |  → exit early if already up to date
    |
    v  git reset --hard upstream/main  (on upstream-mirror branch)
upstream-mirror
    |
    v  git merge upstream-mirror  (into short-lived staging branch off integration)
sync/staging-TIMESTAMP
    |
    v  Gate 1: uv lock --check         (boot — runs FIRST, before uv run can recreate lockfile)
    v  Gate 2: uv run ruff check .     (lint — project-pinned ruff version)
    v  Gate 3: python3 tooling/symmetry-check.py  (config/ ↔ docs/ 1:1 mirror)
    |
    |  all gates pass →
    v  git merge --ff-only  (into integration)
    v  git tag LKG-YYYYMMDD-HHMM
integration
```

### Gate order matters

Boot runs before lint deliberately. `uv run ruff check .` recreates a missing `uv.lock` as a side effect of uv's environment management. Running boot first ensures a stale or missing lockfile is caught before lint can silently repair it.

### Staging branch isolation

The pipeline never modifies `integration` directly until all gates pass. Work happens on a throwaway `sync/staging-TIMESTAMP` branch. On any failure, that branch is deleted and `integration` is untouched.

---

## Running the Pipeline

```bash
# Full sync — fetch upstream, merge, run gates, promote if green
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py

# Dry run — run gates against current state, no commits or tags
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run
```

See `docs/meta/pipeline-runbook.md` for what to do when gates fail.

---

## Last Known Good (LKG) Tags

Every successful promotion creates an annotated tag `LKG-YYYYMMDD-HHMM`. To roll back:

```bash
git log --tags --simplify-by-decoration --pretty="format:%d %ci" | head -10  # list tags
git checkout LKG-20260523-1200    # inspect at that point
git checkout integration
git reset --hard LKG-20260523-1200  # roll back (destructive — confirm first)
```

---

## Contributing a Fix Back to Upstream

When a bug found in this repo also affects the official qwen-code project:

```bash
./tooling/sync-upstreams/contribute-upstream.sh <commit-hash> <branch-name>
```

What it does:
1. Creates a clean branch from `upstream/main` — no monorepo history, no sovereign changes
2. Cherry-picks only your fix commit onto it
3. Pushes to your public fork (`mirror` remote)
4. Prints the URL to open a PR against `QwenLM/qwen-code`

Requires a `mirror` remote pointing to your public fork:
```bash
git remote add mirror https://github.com/YOUR_FORK/qwen-code.git
```

---

## Tooling Reference

| File | Purpose |
| :--- | :--- |
| `tooling/sync-upstreams/upstream_ingest_pipeline.py` | **Primary entry point.** Full pipeline: fetch → stage → gate → promote. |
| `tooling/sync-upstreams/gate_failure_tests.py` | Gate failure test suite. Run to verify all three pipeline failure modes are correctly blocked. |
| `tooling/sync-upstreams/contribute-upstream.sh` | Submits a fix to upstream as a PR via the public fork. |
| `tooling/sync-upstreams/verification-gate.sh` | Standalone gate runner. Mirrors pipeline gate logic for manual use. |
| `tooling/sync-upstreams/raw-inline.sh` | Low-level: resets `upstream-mirror` to `upstream/main` only. |
| `tooling/sync-upstreams/merge-upstream.sh` | **Deprecated.** Exits with error pointing to `upstream_ingest_pipeline.py`. |
| `tooling/symmetry-check.py` | Checks that every file in `.qwen/config/` has a matching `.md` in `docs/`. |

---

## Ruff Configuration

Ruff is configured exclusively in `.ruff.toml` at the project root. There is no `[tool.ruff]` section in `pyproject.toml` — having config in both places causes silent conflicts where `.ruff.toml` wins without warning.

The pipeline resolves ruff via `uv run ruff` (project-pinned). Override with `RUFF_BIN=/path/to/ruff` for CI environments without uv.
