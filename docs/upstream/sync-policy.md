# Upstream Sync Policy

This document explains what we take from QwenLM/qwen-code, what we skip, how conflicts
are resolved, and how to contribute fixes back.

---

## Why we track upstream at all

Qwen Code is the CLI layer we build on. Upstream ships bug fixes, new tool types, SDK updates,
and provider changes. We want those. Without a sync pipeline, our fork would fall behind and
the cost of eventually reconciling would grow every week.

The pipeline makes staying current a routine operation rather than a major project.

---

## Inbound source: the fork, not QwenLM directly

The pipeline fetches from **`jdmanring/qwen-code`** (our public fork), not from
`QwenLM/qwen-code` directly. This means every QwenLM commit must pass through the fork before
it can enter our pipeline. The fork is the filter.

**How it works:**
1. Periodically sync the fork from QwenLM (human review step)
2. Run the ingest pipeline — it fetches from the fork's `main`
3. Changes flow through our three gates into `integration`

**Why fork-as-filter:**
- Human review gate: you decide when to absorb QwenLM changes, not on their schedule
- A bad QwenLM commit (breaking change, bad merge) cannot reach our pipeline unless it first
  enters the fork, giving you an opportunity to inspect it
- Single remote: the fork handles both inbound sync (pipeline) and outbound PRs

**To sync the fork from QwenLM:** run the fork sync pipeline from the monorepo root:

```bash
python3 tooling/sync-upstreams/fork_sync_pipeline.py --sync
```

The pipeline fetches QwenLM into a temporary ref (no persistent remote added), runs advisory
gates to flag CI file changes, protected file changes, manifest updates, and new files, then
asks for explicit confirmation before pushing to the fork. Use `--dry-run` to review gate
output without pushing.

---

## What we take from upstream

Everything in the upstream repository flows into `integration` as-is, subject to the quality
gates. This includes:

- CLI source code (`packages/cli/`, `packages/core/`, etc.)
- SDK changes (`packages/sdk-python/`)
- MCP server implementations (`packages/serve-bridge/`, etc.)
- Upstream configuration files
- Documentation from upstream (preserved in `docs/upstream/qwen-code-readme.md`)

---

## What we do not take

We skip upstream content that would conflict with or overwrite Megalonyx additions:

| What | Why |
|---|---|
| `.github/workflows/ci.yml` | Our CI is adapted for pnpm and our script names. Upstream's version would break our test runs. |
| `.github/workflows/e2e.yml` | Patched to use pnpm instead of npm. Upstream's version reverts this. |
| `packages/sdk-python/pyproject.toml` | We added `[project.optional-dependencies] dev` section. Upstream's version removes it. |
| `config/settings.json` | Real credentials. Never tracked at all. |

These exclusions are enforced in `tooling/sync-upstreams/upstream_ingest_pipeline.py` via the
`PROTECTED_FILES` list. After each merge, those files are restored to their integration-branch
version, so a non-conflicting upstream edit cannot silently overwrite our patches.

To add a new protected file, add its path to `PROTECTED_FILES` in the pipeline script.

## Workflow files that need pnpm patches after sync

These upstream workflow files have been modified to use pnpm instead of npm. If a future
upstream sync overwrites them, re-apply the following changes before merging to `develop`:

| File | What was changed |
|---|---|
| `.github/workflows/e2e.yml` | Added `pnpm/action-setup@v4` step; changed `cache: npm` → `cache: pnpm`; replaced `npm ci` with `pnpm install --frozen-lockfile`; removed npm rate-limit config step |
| `packages/sdk-python/pyproject.toml` | Added `[project.optional-dependencies] dev = [ruff, mypy, pytest]` so `pip install -e '.[dev]'` installs required tools |

After each upstream sync, run `git diff upstream/main HEAD -- .github/workflows/e2e.yml packages/sdk-python/pyproject.toml` to confirm our patches are still in place.

---

## The quality gates

Before any upstream change reaches `integration`, it must pass three gates in order:

1. **Boot gate** (`uv lock --check`) — confirms the Python lockfile is consistent. Runs first to prevent `uv sync` from silently regenerating the lockfile and masking dependency issues.

2. **Lint gate** (`uv run ruff check .`) — runs Ruff on all Python in scope. Zero violations required. This catches upstream Python changes that introduce style or correctness issues.

3. **Symmetry gate** (`python3 tooling/symmetry_check.py`) — verifies that `.qwen/config/` and `docs/` remain in 1:1 correspondence. Upstream changes that add config files without documentation would break this.

If any gate fails, the pipeline stops and the `integration` branch is left unchanged.
See `docs/meta/pipeline-runbook.md` for how to recover from each failure mode.

---

## The pipeline flow

```
QwenLM/qwen-code
        |
        | fork_sync_pipeline.py --sync
        | [GATE-CIFILES]   CI workflow files changed?
        | [GATE-PROTECTED] PROTECTED_FILES changed?
        | [GATE-MANIFESTS] package.json / lockfiles changed?
        | [GATE-NEWFILES]  new files added?
        | [human confirmation]
        v
jdmanring/qwen-code  ← "upstream" remote in megalonyx-monorepo
        |
        | upstream_ingest_pipeline.py
        | git fetch upstream main → reset upstream-mirror
        | merge upstream-mirror into staging branch off integration
        | [PROTECTED_FILES restored to integration version post-merge]
        v
[Boot gate] → [Lint gate] → [Symmetry gate]
        |
        | all gates pass
        v
integration branch (fast-forward merge from staging)
        |
        | tagged as LKG (Last Known Good)
        v
developer manually merges integration → develop when ready
```

Ingest pipeline: `tooling/sync-upstreams/upstream_ingest_pipeline.py`  
Fork sync pipeline: `tooling/sync-upstreams/fork_sync_pipeline.py`

---

## Merge conflicts

When upstream changes a file that Megalonyx also modified, you get a merge conflict. The
pipeline stops at the merge step and leaves the repo in a conflicted state.

Resolution steps:
1. Read `docs/meta/pipeline-runbook.md` — it describes each failure mode
2. Resolve the conflict manually, favoring Megalonyx changes unless the upstream fix is critical
3. Run the pipeline with `--dry-run` to verify gates pass before re-running the full sync

---

## Contributing a fix back to upstream

When you fix a bug in the CLI code (in `packages/cli/` or `packages/core/`) that also affects
the upstream project, read the full procedure before doing anything:

- **`docs/upstream/upstream-pr-guide.md`** — complete preparation and submission procedure
- **`docs/upstream/upstream-pr-checklist.md`** — mandatory gate checklist to run before every submission

The `upstream` remote (`jdmanring/qwen-code`) serves dual purpose: it is both the inbound
filter for the pipeline AND the outbound channel for upstream PRs. Topic branches for PRs are
pushed to the fork, then opened as PRs against `QwenLM/qwen-code`.

The `upstream` remote is already set up (part of the standard monorepo setup):
```bash
# Confirm:
git remote -v  # should show upstream → git@github.com:jdmanring/qwen-code.git
```

For single-commit cherry-picks, the fork sync pipeline handles isolation gates, branch
creation, and push automatically:
```bash
python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <commit-hash> <branch-name>
```

For multi-file dependency upgrades or PRs that require manual diff inspection, follow the
manual procedure in `upstream-pr-guide.md`.

---

## Keeping the LKG tag

Every successful pipeline run tags `integration` with `lkg/<timestamp>`. If a bad upstream
change gets through the gates and breaks something at runtime, roll back to the last tag:

```bash
git checkout lkg/20260524-1200
```

List tags: `git tag --list 'lkg/*' | sort`

---

## Checking sync status

```bash
# Full picture: fork lag vs QwenLM, pipeline lag vs fork, active PR branches
python3 tooling/sync-upstreams/fork_sync_pipeline.py --status

# Is integration up to date with the fork?
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run
```
