# Git Strategy: The Independent Flow

## Branch Architecture

| Branch | Tracks | Purpose | Who writes to it |
| :--- | :--- | :--- | :--- |
| `upstream-mirror` | `upstream/main` (jdmanring/qwen-code fork) | Clean snapshot of the fork. Reset on every sync — never commit local work here. | Pipeline only |
| `integration` | `upstream-mirror` (via pipeline) | Normalization layer. All upstream changes must pass three gates before landing here. | Pipeline + Integration Lead |
| `develop` | `integration` | Active feature development on the verified base. | Developers |
| `main` | `develop` | Stable, production-ready release branch. | Architect |


---

## Why Two Remotes?

GitHub does not allow making a fork private. The solution is a two-track setup:

- **`upstream` remote** → `jdmanring/qwen-code` (our fork of QwenLM — NOT QwenLM directly)
- **`origin` remote** → `jdmanring/megalonyx-monorepo` (private monorepo — all independent development)

The `upstream` remote is the fork, not QwenLM. Before running the ingest pipeline, the fork must be synced from QwenLM using `fork_sync_pipeline.py --sync`. The ingest pipeline then fetches from `upstream` (the fork).

Upstream code flows in two steps:
1. QwenLM/qwen-code → `jdmanring/qwen-code` fork (via `fork_sync_pipeline.py --sync`)
2. `upstream/main` (fork) → `upstream-mirror` → `integration` (via `upstream_ingest_pipeline.py`)

The fork is also used in the outbound direction: monorepo commits can be cherry-picked onto the fork as prepared contribution branches via `fork_sync_pipeline.py --contribute`. **No PRs to QwenLM are ever opened — this is a permanent policy.**

---

## The Upstream Ingest Pipeline

All upstream ingestion runs through `tooling/sync-upstreams/upstream_ingest_pipeline.py`. It enforces three gates in a specific order before any change reaches `integration`.

```
upstream/main  (jdmanring/qwen-code fork — synced from QwenLM via fork_sync_pipeline.py --sync)
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
    v  Gate 3: python3 tooling/symmetry_check.py  (config/ ↔ docs/ 1:1 mirror)
    |
    |  all gates pass →
    v  git merge --ff-only  (into integration)
    v  git tag LKG-YYYYMMDD-HHMM
integration
```

### package-lock.json auto-resolution

QwenLM uses npm and commits `package-lock.json`. This repo uses pnpm and has no `package-lock.json`. The pipeline auto-resolves this conflict on every merge by keeping the monorepo's version (i.e., deleting `package-lock.json` from the merge). No manual intervention needed.

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

## Contributing to the Fork

When monorepo commits should also land on `jdmanring/qwen-code` (as prepared contributions):

```bash
python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <commit-hash> <branch-name>
```

What it does:
1. Creates a clean branch from `upstream/main` — no monorepo history, no local-only changes
2. Cherry-picks the commit onto it
3. Pushes to `upstream` remote (jdmanring/qwen-code fork)

**No PRs to QwenLM are ever opened — permanent policy.** Branches are prepared as a record only.

### Cherry-pick conflict patterns

Contribution branches are based on `upstream/main` (no pnpm, different package.json). Expect:

| File | Type | Resolution |
| :--- | :--- | :--- |
| `pnpm-lock.yaml` | DU (deleted-by-us) | `git rm pnpm-lock.yaml` |
| `package.json` (root) | UU | `git checkout --ours`, then manually re-apply version bumps |
| Test files (`.test.ts`) | UU | `git checkout --theirs` — diffs are formatting auto-fixes only |

`pnpm-lock.yaml` is Megalonyx-specific and must never appear on contribution branches.

---

## Tooling Reference

| File | Purpose |
| :--- | :--- |
| `tooling/sync-upstreams/upstream_ingest_pipeline.py` | **Primary entry point.** Full pipeline: fetch → stage → gate → promote. |
| `tooling/sync-upstreams/gate_failure_tests.py` | Gate failure test suite. Run to verify all three pipeline failure modes are correctly blocked. |
| `tooling/sync-upstreams/fork_sync_pipeline.py` | Sync fork from QwenLM (`--sync`) or contribute commits to fork (`--contribute <hash> <name>`). |
| `tooling/sync-upstreams/verification-gate.sh` | Standalone gate runner. Mirrors pipeline gate logic for manual use. |
| `tooling/sync-upstreams/raw-inline.sh` | Low-level: resets `upstream-mirror` to `upstream/main` only. |
| `tooling/sync-upstreams/merge-upstream.sh` | **Deprecated.** Exits with error pointing to `upstream_ingest_pipeline.py`. |
| `tooling/symmetry_check.py` | Checks that every file in `.qwen/config/` has a matching `.md` in `docs/`. |

---

## Ruff Configuration

Ruff is configured exclusively in `.ruff.toml` at the project root. There is no `[tool.ruff]` section in `pyproject.toml` — having config in both places causes silent conflicts where `.ruff.toml` wins without warning.

The pipeline resolves ruff via `uv run ruff` (project-pinned). Override with `RUFF_BIN=/path/to/ruff` for CI environments without uv.
