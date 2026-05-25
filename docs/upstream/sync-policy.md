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
| `ci.yml` | Upstream CI is written for their repo structure. We have our own CI. Overwriting it would break our quality gates. |
| `config/settings.json` | This file contains real credentials. It is not tracked at all. |

These exclusions are handled at the pipeline level. If upstream ever ships a file whose name
matches something we deliberately protect, the gate will flag it for manual review.

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
QwenLM/qwen-code (upstream remote)
        |
        | git fetch upstream main
        v
upstream-mirror branch (reset --hard each run)
        |
        | git merge upstream-mirror into a staging branch off integration
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

The pipeline script: `tooling/sync-upstreams/upstream_ingest_pipeline.py`

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

The mirror remote (`jdmanring/qwen-code`) is used only for outbound contributions. Upstream
code never flows through it — it flows inbound via the `upstream` remote directly.

Set up the mirror remote once:
```bash
git remote add mirror https://github.com/jdmanring/qwen-code.git
```

For single-commit cherry-picks, the helper script handles branch creation and push:
```bash
tooling/sync-upstreams/contribute-upstream.sh <commit-hash> <branch-name>
```

For multi-file dependency upgrades or PRs that require manual diff inspection, follow the
manual procedure in `upstream-pr-guide.md` — the script is insufficient for those cases.

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
# Is integration up to date with upstream?
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run

# How many commits behind are we?
git rev-list --count upstream/main ^integration
```
