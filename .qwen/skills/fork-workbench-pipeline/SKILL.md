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
    ↓ fast-forward
upstream-mirror (exact copy of upstream/main)
    ↓ reset
origin/ingest (clean base for contributions)
    ↓ individual branches
contribution branches (1-3 commits each)
    ↓ merge
origin/develop (integration — all contributions combined)
    ↓ merge when ready
origin/main (release endpoint for downstream consumers)
```

### Branch Roles

| Branch | Role | Push? | Description |
|--------|------|-------|-------------|
| `upstream/main` | Source of truth | Read-only | The upstream repo (e.g., QwenLM/qwen-code) |
| `upstream-mirror` | Exact mirror | Fast-forward only | Always matches `upstream/main` HEAD |
| `origin/ingest` | Contribution base | Force-push | Reset to match mirror; all contributions fork from here |
| `origin/develop` | Integration | Force-push | All contribution branches merge here |
| `origin/main` | Release endpoint | Merge only | For downstream consumers; never pull back into workbench |
| `fork/*` | Fork infrastructure | Push | Fork-specific docs, tooling, PR drafts |
| `feat/*`, `chore/*` | Contributions | Force-push | Individual PR candidates based on `ingest` |

## Workflow

### 1. Sync Mirror

```bash
git fetch upstream
git checkout upstream-mirror
git reset --hard upstream/main
git push origin upstream-mirror
```

### 2. Reset Ingest

```bash
git checkout ingest
git reset --hard upstream-mirror
git push origin ingest --force
```

### 3. Rebase Contributions

For each contribution branch, identify the unique commit(s) and cherry-pick onto `ingest`:

```bash
git checkout <branch>
git reset --hard ingest
git cherry-pick <commit-hash>
git push origin <branch> --force
```

### 4. Merge into Develop

```bash
git checkout develop
git reset --hard ingest
for branch in <contribution-branches>; do
  git merge --no-edit $branch
done
git push origin develop --force
```

### 5. Release (when ready)

```bash
git checkout main
git merge develop
git push origin main
```

## Rules

1. **Never rewrite upstream history.** We merge upstream in, we don't rebase onto it.
2. **Force-push only to contribution branches**, never to `main`, `develop`, or `ingest`.
3. **`origin/main` is a release endpoint.** Never pull from it back into the workbench.
4. **Integration branches are disposable.** If a branch has no unique commits, delete it.
5. **Contributions are individual branches.** Each dependency upgrade or feature is a separate branch with 1-3 commits.
6. **PRs target upstream/main.** After sync, each contribution branch is a clean diff against current upstream HEAD.
7. **`fork/*` branches preserve fork-specific work.** Keep PR drafts, tooling, and docs separate from contributions.

## Recovering from Other Forks

When another fork (e.g., megalonyx-monorepo) has work that should be staged as upstream contributions:

1. Add the fork as a remote: `git remote add <name> <path>`
2. Fetch: `git fetch <name>`
3. Identify unique dependency upgrade commits (not infrastructure/tooling)
4. Cherry-pick onto `ingest` to create new contribution branches
5. Focus on package.json changes, CI updates, and source code changes
6. Skip fork-specific files (custom CI, Python code, project scaffolding)

## Verification

For each contribution branch:
```bash
npm install
npm run build
npm run typecheck
```

For the develop branch (integration):
```bash
npm install
npm run build
npm run typecheck
npm test
```
