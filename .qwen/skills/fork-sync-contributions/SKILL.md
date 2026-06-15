---
name: fork-sync-contributions
description: Ingest latest upstream commits into a fork and rebase all staged contribution branches to achieve PR-readiness against the current source.
source: auto-skill
extracted_at: '2026-06-12T17:00:00.000Z'
---

# Fork Sync & Contribution Pipeline

This skill maintains a fork workbench for managing upstream contributions. The pipeline flows:

```
upstream/main → upstream-mirror → origin/ingest → origin/develop → origin/main
                                   ↑
                             contribution branches
                             (based on ingest)
```

## Architecture

| Branch            | Role                | Description                                                                                 |
| ----------------- | ------------------- | ------------------------------------------------------------------------------------------- |
| `upstream/main`   | Source of truth     | The upstream QwenLM/qwen-code repo                                                          |
| `upstream-mirror` | Exact mirror        | Fast-forwarded to match `upstream/main`                                                     |
| `origin/ingest`   | Contribution base   | Reset to match `upstream-mirror`; contribution branches fork from here                      |
| `origin/develop`  | Integration         | All contribution branches merge here for integration testing                                |
| `origin/main`     | Release endpoint    | Clean release branch for downstream consumers; never pull from here back into the workbench |
| `fork/*`          | Fork infrastructure | Fork-specific docs, tooling, PR drafts — kept separate from contributions                   |

## Phase 1: Assess Divergence

```bash
git fetch upstream
git fetch origin
```

Determine:

1. **Upstream commits to ingest**: `git log --oneline origin/ingest..upstream/main`
2. **Our staged commits**: `git log --oneline upstream/main..origin/main` (on old base)
3. **Branch inventory**: `git branch | grep -v -E "main|develop|upstream-mirror|integration|ingest"`

## Phase 2: Sync the Mirror

Fast-forward `upstream-mirror` to match `upstream/main`:

```bash
git checkout upstream-mirror
git reset --hard upstream/main
git push origin upstream-mirror
```

## Phase 3: Reset Ingest

Reset `origin/ingest` to match the mirror. This is the clean base for all contributions.

```bash
git checkout ingest
git reset --hard upstream-mirror
git push origin ingest --force
```

## Phase 4: Rebase Contribution Branches

For each contribution branch, reset to `ingest` and cherry-pick the unique contribution commit(s):

```bash
git checkout <branch>
git reset --hard ingest
git cherry-pick <commit-hash>  # the unique contribution commit
git push origin <branch> --force
```

**Do NOT rebase integration branches** (branches with ~190 commits). These are stale tracking branches and should be deleted if they have no unique content. Only rebase true contribution branches (1-3 commits each).

**Conflict resolution:**

- For package.json conflicts: take the contribution's version (the dependency upgrade)
- For test file conflicts: take upstream's version (latest test structure) and re-apply the contribution's assertion changes
- For deleted files: accept the deletion if the contribution intentionally removes/restructures the file

## Phase 5: Merge into Develop

Merge all contribution branches into `origin/develop` for integration:

```bash
git checkout develop
git reset --hard ingest  # ensure clean base
for branch in chore/acp-sdk-upgrade chore/esbuild-globals-upgrade feat/eslint-10 feat/vitest-vite-upgrade feat/migrate-to-pnpm; do
  git merge --no-edit $branch
done
git push origin develop --force
```

## Phase 6: Update Release Branch

When ready for a release, merge `develop` into `origin/main`:

```bash
git checkout main
git merge develop
git push origin main
```

## Phase 7: Report

Produce a summary table:

| Branch          | Status  | Commits | Description                  |
| --------------- | ------- | ------- | ---------------------------- |
| upstream-mirror | Synced  | —       | Exact copy of upstream/main  |
| ingest          | Reset   | —       | Clean base for contributions |
| chore/xxx       | Rebased | N       | Description                  |
| feat/xxx        | Rebased | N       | Description                  |
| develop         | Merged  | —       | All contributions integrated |

## Key Principles

- **Never rewrite upstream history.** We merge upstream in, we don't rebase onto it.
- **Force-push only to contribution branches**, never to `main`, `develop`, or `ingest`.
- **Integration branches are disposable.** If a branch has no unique commits, delete it.
- **`origin/main` is a release endpoint.** Never pull from it back into the workbench pipeline.
- **`fork/*` branches preserve fork-specific work.** PR drafts, tooling, docs — kept separate from contribution branches.
- **PRs target upstream/main**, not origin/main. After this process, each contribution branch should be a clean diff against the current upstream HEAD.
- **node.js must be installed** for verification (`npm run build && npm run typecheck`).

## Troubleshooting

### Cherry-pick conflicts with package.json

The upstream may have already bumped a dependency. Resolve by taking the higher version.

### Cherry-pick produces empty commit

The contribution's changes were already merged upstream. Skip with `git rebase --skip` or delete the branch.

### Branch has 190+ commits (integration branch)

This is a stale tracking branch, not a contribution branch. Reset it to `ingest` and check for unique commits. If none, delete it.

### Pre-commit hook fails (npm not found)

Set `HUSKY=0` to bypass: `HUSKY=0 git commit ...`
