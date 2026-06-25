---
name: fork-workbench-pipeline
description: Workbench pipeline for managing a fork of an upstream project, staging contributions, and submitting PRs back to the source.
source: auto-skill
extracted_at: '2026-06-12T17:00:00.000Z'
---

# Fork Workbench Pipeline

This skill manages a fork as a workbench for developing upstream contributions. It defines the branch architecture, workflow, and rules for keeping the fork in sync with upstream while staging contributions as clean, individual PRs.

## Branch Architecture

```
upstream/main (source of truth)
    ↓ fetch + reset
upstream-mirror (exact copy of upstream/main)
    ↓ merge into staging branch off integration
sync/staging-TIMESTAMP (temporary)
    ↓ Gate 1: npm run build
    ↓ Gate 2: npm run typecheck
    ↓ Gate 3: symmetry check
integration  [ff-only merge + LKG tag]
    ↓ rebase PR branches onto integration
    ↓ rebuild develop from integration + unique commits
develop
    ↓ merge when ready
main (release endpoint)
```

### Branch Roles

| Branch                       | Role                | Push?             | Description                                              |
| ---------------------------- | ------------------- | ----------------- | -------------------------------------------------------- |
| `upstream/main`              | Source of truth     | Read-only         | The upstream repo (QwenLM/qwen-code)                     |
| `upstream-mirror`            | Exact mirror        | Fast-forward only | Always matches `upstream/main` HEAD                      |
| `integration`                | Vetted upstream     | Force-push        | Only the pipeline writes here. Never commit directly.    |
| `develop`                    | Primary working     | Force-push        | All fork work lands here eventually.                     |
| `main`                       | Release endpoint    | Merge only        | For downstream consumers; never pull back into workbench |
| `fork/*`                     | Fork infrastructure | Push              | Fork-specific docs, tooling, pipeline scripts            |
| `feat/*`, `fix/*`, `chore/*` | PR candidates       | Force-push        | Individual upstream-candidate branches                   |
| `sync/staging-*`             | Temporary           | Auto-deleted      | Created and deleted by the pipeline.                     |

## Pipeline

The full workflow is implemented in `tooling/sync-upstreams/upstream_ingest_pipeline.py`.

### Usage

```bash
# Full sync: upstream → mirror → staging → gates → integration → rebase → develop
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py

# Dry run: run gates only against current state
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run

# Skip build + typecheck gates (CI mode)
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --skip-build

# Push integration and tags to origin after sync
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --push

# Rebase-only: skip upstream sync, just rebase branches onto current integration
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --rebase-only
```

### CI

`.github/workflows/sync-upstream.yml` runs the pipeline daily at 3am UTC with `--skip-build --push`.

### What the pipeline protects

After every upstream merge, the pipeline restores these files to their `integration` branch state:

| Protected                                            | Why                            |
| ---------------------------------------------------- | ------------------------------ |
| `tooling/sync-upstreams/upstream_ingest_pipeline.py` | The pipeline itself            |
| `tooling/sync-upstreams/gate_failure_tests.py`       | Pipeline tests                 |
| `tooling/symmetry-check.py`                          | Symmetry gate                  |
| `pyproject.toml`                                     | Fork-specific Python config    |
| `pnpm-workspace.yaml`                                | Fork-specific workspace config |
| `scripts/*`                                          | Fork-specific dev scripts      |
| `.husky/pre-commit`                                  | Fork-specific git hook         |
| `.qwen/skills/fork-/*`                               | Fork-specific workbench skills |

To add a new protected file, add it to `PROTECTED_FILES` in the pipeline source.

### How develop is rebuilt

After promoting to integration, the pipeline:

1. Finds the merge-base between `develop` and `upstream-mirror` (the fork-only base)
2. Identifies `develop`'s unique commits (not on upstream-mirror)
3. Resets `development` to the new integration HEAD
4. Cherry-picks each unique commit on top

If a cherry-pick conflicts, the pipeline aborts and reports the conflicting commit. Resolve manually, then re-run with `--rebase-only`.

### How PR branches are rebased

After promoting to integration, the pipeline:

1. Finds all local branches matching `feat/*`, `fix/*`, `chore/*`, `refactor/*`, `perf/*`
2. For each, finds unique commits (not on upstream-mirror)
3. Rebases onto integration: `git rebase --onto <integration> <upstream-mirror> <branch>`
4. If rebase conflicts, aborts and reports

If a rebase fails, resolve manually:

```bash
git checkout <branch>
git rebase upstream-mirror
# resolve conflicts
git rebase --continue
```

## Manual Workflow (if pipeline is unavailable)

### 1. Sync Mirror

```bash
git fetch upstream
git checkout -f upstream-mirror
git reset --hard upstream/main
```

### 2. Merge into Integration

```bash
git checkout integration
git merge upstream-mirror
# Resolve conflicts if any
```

### 3. Rebase PR Branches

```bash
git checkout <branch>
git rebase --onto integration $(git merge-base upstream-mirror <branch>) <branch>
```

### 4. Update Develop

```bash
git checkout develop
git reset --hard integration
# Cherry-pick develop's unique commits
for commit in $(git log --oneline --format=%H upstream-mirror..develop); do
  git cherry-pick $commit
done
```

### 5. Release (when ready)

```bash
git checkout main
git merge develop
git push origin main
```

## Rules

1. **Never rewrite upstream history.** We merge upstream in, we don't rebase onto it.
2. **Force-push only to PR branches**, never to `main`, `develop`, or `integration`.
3. **`main` is a release endpoint.** Never pull from it back into the workbench.
4. **`upstream-mirror` is reset-only.** Never commit here.
5. **PR branches target upstream/main.** Each is a clean diff against current upstream HEAD.
6. **`fork/*` branches preserve fork-specific work.** Keep PR drafts, tooling, and docs separate from contributions.
7. **Integration is disposable.** It's a gatekeeper, not a working branch.

## Verification

For each PR branch:

```bash
npm install && npm run build && npm run typecheck
```

For develop (integration):

```bash
npm install && npm run build && npm run typecheck
cd packages/core && npx vitest run
cd packages/cli && npx vitest run
```
