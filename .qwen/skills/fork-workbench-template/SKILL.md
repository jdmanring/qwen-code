---
name: fork-workbench-template
description: Template for setting up a fork as a contribution workbench with gated inbound sync, staged contributions, and clean upstream PRs.
source: auto-skill
extracted_at: '2026-06-13T02:15:00.000Z'
---

# Fork Workbench Template

This skill provides a reusable template for configuring a fork as a contribution workbench. It synthesizes best practices from three existing workbenches (qwen-code, odysseus, megalonyx-monorepo) into a single optimal pipeline.

The complete template project lives at `/home/james/Projects/fork-workbench-template/` — copy files from there rather than writing them from scratch.

## When to Use

Use this template when:

- Setting up a new fork intended as a contribution workbench
- An existing fork lacks gates, automation, or rollback capability
- You need a standard, repeatable process across multiple projects

## Pipeline Architecture

```
upstream/main → upstream-mirror → sync/staging-* → [gates] → integration → develop → main
                                      ↑
                                contribution branches
                                (based on upstream-mirror)
```

### Stage Definitions

| Stage           | Branch                   | How written                                      | Purpose                                                    |
| --------------- | ------------------------ | ------------------------------------------------ | ---------------------------------------------------------- |
| Source of truth | `upstream/main`          | Read-only fetch                                  | The upstream project                                       |
| Mirror          | `upstream-mirror`        | `git reset --hard upstream/main`                 | Exact copy of upstream HEAD                                |
| Staging         | `sync/staging-TIMESTAMP` | Throwaway branch off `integration`               | Gates run here; never touches `integration` until all pass |
| Vetted          | `integration`            | Fast-forward merge from staging after gates pass | Clean, verified upstream surface                           |
| Development     | `develop`                | Manual merge from `integration`                  | All fork work lives here                                   |
| Release         | `main`                   | Merge from `develop`                             | Downstream consumers; never pull back into workbench       |

## Template File Inventory

The template project at `/home/james/Projects/fork-workbench-template/` contains:

| File                                                 | Purpose                                                    | Copy to fork as                                      |
| ---------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| `FORK_WORKBENCH_TEMPLATE.md`                         | Authoritative guide — branch architecture, rules, workflow | `FORK_WORKBENCH_TEMPLATE.md` (root)                  |
| `README.md`                                          | Quick start, design decisions, ecosystem reference         | `README.md` (root)                                   |
| `CONTRIBUTING.md`                                    | How upstream contributors interact with this fork          | `CONTRIBUTING.md` (root)                             |
| `docs/runbook.md`                                    | Pipeline failure recovery — every failure mode             | `docs/runbook.md`                                    |
| `docs/fork/README.md`                                | Navigation hub for fork management docs                    | `docs/fork/README.md`                                |
| `docs/fork/issue-tracker.md`                         | Issue-to-branch mapping with labels and status             | `docs/fork/issue-tracker.md`                         |
| `docs/fork/changes-from-upstream.md`                 | Master record of deliberate divergence                     | `docs/fork/changes-from-upstream.md`                 |
| `docs/fork/upstream/pr-status.md`                    | Status of staged upstream contributions                    | `docs/fork/upstream/pr-status.md`                    |
| `tooling/sync-upstreams/upstream_ingest_pipeline.py` | Python pipeline script                                     | `tooling/sync-upstreams/upstream_ingest_pipeline.py` |
| `tooling/sync-upstreams/upstream_ingest_pipeline.sh` | Node.js pipeline script                                    | `tooling/sync-upstreams/upstream_ingest_pipeline.sh` |
| `tooling/sync-upstreams/rollback_to_lkg.py`          | Rollback utility                                           | `tooling/sync-upstreams/rollback_to_lkg.py`          |
| `tooling/sync-upstreams/gate_failure_tests.py`       | Pipeline self-tests                                        | `tooling/sync-upstreams/gate_failure_tests.py`       |
| `.github/workflows/sync-upstream.yml`                | Daily CI auto-ingest (standalone)                          | `.github/workflows/sync-upstream.yml`                |
| `.github/workflows/sync-upstream-reusable.yml`       | Reusable workflow (workflow_call)                          | `.github/workflows/sync-upstream-reusable.yml`       |

Copy the entire `tooling/sync-upstreams/`, `docs/fork/`, and `.github/workflows/` directories into your fork. Then adapt the files as described below.

## Required Files (adapted from template)

### 1. `docs/dev/git-branch-workflow.md` (Authoritative Reference)

This is the single most important file. It must contain:

```markdown
# Git Branch Workflow

## Branch Map

| Branch | Purpose | Rules |
| (every branch with its role and constraints)

## Two Kinds of Work Branches — Different Origins

### Category 1: Upstream-Candidate (default)

- Branch from upstream-mirror
- Single clean commit
- Cherry-pick to develop
- Branch stays permanently as PR staging

### Category 2: Fork-Only (narrow exception)

- Branch from develop
- Merge back to develop
- Only for: sync pipeline, fork CI, fork management docs

## Issue-First Workflow

1. Create issue
2. Determine category
3. Branch from correct origin
4. Do work, commit cleanly
5. Cherry-pick/merge to develop
6. Update tracking docs

## Pipeline Commands

(exact commands for sync, rebase, promote)

## Failure Recovery

(what to do when gates fail, merge conflicts, etc.)

## Pre-Flight Checklist

- [ ] Branch starts from correct origin
- [ ] Single clean commit
- [ ] Diff contains only intended files
- [ ] No hardcoded paths/tokens
- [ ] Commit message clear
- [ ] Tests pass
```

### 2. `tooling/sync-upstreams/upstream_ingest_pipeline.py`

Core pipeline script. Must implement:

1. **Pre-flight checks**: correct branch, remotes exist, no uncommitted changes
2. **Fetch upstream**: `git fetch upstream`, reset `upstream-mirror` to `upstream/main`
3. **Staging isolation**: create `sync/staging-TIMESTAMP` off `integration`, merge mirror into it
4. **Gates** (run on staging branch, not integration):
   - Gate 1: Boot/lockfile check (language-appropriate)
   - Gate 2: Lint (project's linter)
   - Gate 3: Test suite (or project-appropriate verification)
5. **Promote**: fast-forward merge staging → integration, tag `LKG-YYYYMMDD-HHMM`
6. **Cleanup**: delete staging branch, even on failure (use `finally` block)

### 3. `tooling/sync-upstreams/rollback_to_lkg.py`

Rollback utility:

- List LKG tags
- Reset `integration` to a chosen tag
- Confirm before destructive operation

### 4. `.github/workflows/sync-upstream.yml`

CI automation:

- Schedule: daily (e.g., 3am UTC)
- Checkout `integration` with full history
- Add upstream remote, fetch
- Run pipeline script with `--push`
- Use `GH_PAT` for authentication if needed

### 5. `docs/ai/CONTEXT.md` and `docs/ai/RULES.md`

Split knowledge system:

- `CONTEXT.md`: mental model, architecture, pipeline diagram
- `RULES.md`: hard constraints, "Never" lists, branch origin rules

## Setup Procedure

### Step 1: Configure Remotes

```bash
git remote add upstream <upstream-url>
git remote set-url origin <fork-url>
```

### Step 2: Create Branch Structure

```bash
# Create upstream-mirror from upstream/main
git checkout -b upstream-mirror upstream/main
git push origin upstream-mirror

# Create integration from upstream-mirror
git checkout -b integration upstream-mirror
git push origin integration

# Ensure develop exists (may already)
git checkout -b develop integration  # or use existing
git push origin develop
```

### Step 3: Create Pipeline Scripts

Create `tooling/sync-upstreams/` directory with:

- `upstream_ingest_pipeline.py` (see requirements above)
- `rollback_to_lkg.py`

### Step 4: Create CI Workflow

Create `.github/workflows/sync-upstream.yml` with scheduled trigger.

### Step 5: Create Documentation

Create `docs/dev/git-branch-workflow.md` with full reference.

### Step 6: Define Protected Files

In the pipeline script, maintain a `PROTECTED_FILES` list of fork-specific files that are restored after every upstream merge. Common entries:

- Pipeline script itself
- Fork CI workflow
- Fork documentation
- Configuration files with fork-specific values

### Step 7: Test the Pipeline

```bash
# Dry run (no changes)
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run

# Full run
git checkout integration
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --push

# Verify
git log --oneline integration ^develop  # should be 0 (in sync)
git tag -l "LKG-*" | sort -r | head -3  # should show new tag
```

## Contribution Workflow

### Creating a New Contribution

```bash
# 1. Ensure upstream-mirror is current
git fetch upstream
git checkout upstream-mirror
git pull origin upstream-mirror

# 2. Create branch from upstream-mirror (NOT develop)
git checkout -b fix/short-description upstream-mirror

# 3. Do work — only files relevant to this fix
git add <specific files>
git commit -m "fix: clear description"

# 4. Cherry-pick to develop
git checkout develop
git cherry-pick <commit-hash>

# 5. Branch stays as upstream PR staging — do NOT delete
```

### Rebasing After Upstream Sync

```bash
# Check if rebase needed
git log --oneline fix/branch-name..upstream-mirror | wc -l

# Rebase
git checkout fix/branch-name
git rebase upstream-mirror
# Resolve conflicts: keep fix + incorporate upstream changes

# Re-cherry-pick to develop if needed
git checkout develop
git cherry-pick <commit-hash>
```

## Key Rules (Non-Negotiable)

1. **Never push to `upstream` remote** — it is read-only
2. **Never commit to `upstream-mirror`** — reset-only, commits destroyed on sync
3. **Never cherry-pick upstream → develop directly** — always use the pipeline
4. **Branch origin matters** — upstream-candidate from `upstream-mirror`, fork-only from `develop`
5. **Force-push only to contribution branches** — never to `main`, `develop`, or `integration`
6. **`main` is a release endpoint** — never pull from it back into the workbench
7. **Issue first, branch second** — no branch without a corresponding issue
8. **Integration is never modified until all gates pass** — staging branch isolation

## Adaptation Notes

### For Python Projects (like odysseus)

- Gate 1: `python -m py_compile` on changed files
- Gate 2: `ruff check .`
- Gate 3: `pytest` (smoke tests)

### For Node.js/TypeScript Projects (like qwen-code)

- Gate 1: `pnpm install` (lockfile check)
- Gate 2: `pnpm run lint`
- Gate 3: `pnpm test`

### For Monorepos with Separate Build Systems (like megalonyx)

- Consider a two-remote architecture only if the monorepo cannot be a GitHub fork
- Add isolation gates to outbound contributions (block fork-specific keywords)
- Use `package-lock.json` auto-resolution when upstream and fork use different package managers

### For Projects Without CI

- Skip `sync-upstream.yml`
- Run pipeline manually before each contribution cycle
- LKG tags still provide rollback safety

## Common Mistakes to Avoid

| Mistake                                          | Why bad                             | Correct action                 |
| ------------------------------------------------ | ----------------------------------- | ------------------------------ |
| Branching upstream-candidate off `develop`       | Pollutes branch with fork history   | Branch from `upstream-mirror`  |
| Merging upstream-candidate to `develop`          | Imports upstream history            | Cherry-pick specific commits   |
| Skipping gates on upstream merge                 | Regressions land in `integration`   | Always run the full pipeline   |
| Deleting contribution branches after cherry-pick | Loses the upstream PR staging       | Branch stays permanently       |
| Pulling from `main` back into workbench          | Contaminates with release artifacts | `main` is outbound only        |
| Committing to `upstream-mirror`                  | Destroyed on next sync              | Use as branch origin only      |
| Not tagging promotions                           | No rollback point                   | Always tag `LKG-YYYYMMDD-HHMM` |

## Operational Procedures

### Contribution Branch Health Check

Before filing an upstream PR, verify the branch is clean:

```bash
# Verify branch starts from upstream-mirror (not develop)
git merge-base fix/branch-name upstream-mirror
# Should return the same commit as: git rev-parse upstream-mirror

# Verify only your commits are on the branch
git log --oneline upstream-mirror..fix/branch-name

# Verify no fork-specific files in the diff
git diff upstream-mirror..fix/branch-name --name-only

# Verify the diff is clean (no conflict markers, no accidental whitespace)
git diff upstream-mirror..fix/branch-name --check
```

### Pre-Commit Hook Bypass

When hooks require tooling not available in the current environment (common during pipeline operations):

```bash
# Option A: HUSKY=0 (for husky-based projects)
HUSKY=0 git commit -m "your message"

# Option B: --no-verify (skips all hooks)
git commit --no-verify -m "your message"

# Option C: Skip specific hooks
SKIP=eslint,prettier git commit -m "your message"
```

**Only use during pipeline operations (cherry-picks, sync commits). Never bypass hooks on direct development.**

### Upstream Already Has the Change

When a cherry-pick or contribution branch produces no diff:

```bash
# Cherry-pick says "nothing to commit" → upstream already has the change
git cherry-pick --skip

# Branch has no unique commits → delete it
git diff upstream-mirror..fix/branch-name  # empty output
git checkout develop
git branch -d fix/branch-name

# Partial overlap → rebase and drop duplicates
git rebase -i upstream-mirror  # interactive: drop commits already upstream
```

### Draft PR on Complex Conflicts

When upstream merge creates complex conflicts that need collaborative resolution:

```bash
git checkout -b sync/conflict-$(date +%Y%m%d) integration
git merge upstream-mirror --no-commit --no-ff
# Leave conflict markers in place
git add -A
git commit -m "chore(sync): draft PR for upstream merge conflict $(date +%Y%m%d)"
git push origin sync/conflict-$(date +%Y%m%d)
gh pr create --title "⚠️ Upstream sync conflict $(date +%Y%m%d)" \
  --body "Merge conflict with upstream. Needs manual resolution." --draft
```

## Release Procedure

### Pre-release Checklist

- [ ] `develop` is clean, all intended contributions merged
- [ ] CI passes on `develop` (build, lint, tests)
- [ ] No unexpected divergence from upstream (`git diff --stat upstream-mirror..develop`)
- [ ] Changelog or release notes updated (if applicable)

### Release Merge

```bash
TAG="v$(date +%Y%m%d)"
git checkout main
git merge develop --no-ff -m "release: sync + contributions ${TAG}"
git tag -a "$TAG" -m "Release ${TAG}"
git push origin main --follow-tags
```

**Why `--no-ff`:** The merge commit records when the release happened. `git log --first-parent main` shows a clean release timeline.

### Hotfix When Develop Has Unreleasable Changes

```bash
# Branch from main (not develop)
git checkout -b hotfix/critical-fix main
# ... make fix, commit ...
git checkout main
git merge hotfix/critical-fix --no-ff -m "hotfix: description $(date +%Y%m%d)"
git push origin main

# Keep develop in sync
git checkout develop
git cherry-pick <hotfix-commit-hash>
```

## Quick-Start Adaptation Checklist

When setting up a new workbench from this template, do these steps in order:

1. **Copy files** from `/home/james/Projects/fork-workbench-template/` into your fork
2. **Choose your pipeline**: use `upstream_ingest_pipeline.py` (Python) or `upstream_ingest_pipeline.sh` (Node.js). Delete the other.
3. **Configure branch names**: edit `INTEGRATION_BRANCH`, `MIRROR_BRANCH`, `UPSTREAM_BRANCH` in the pipeline script to match your upstream's default branch
4. **Configure remotes**: edit `REQUIRED_REMOTES` if your remote names differ from `origin`/`upstream`
5. **Set protected files**: edit `PROTECTED_FILES` list to include your fork-specific files
6. **Set auto-resolve files**: edit `AUTO_RESOLVE_OURS` for lockfile format differences (e.g., `package-lock.json` if fork uses pnpm)
7. **Uncomment gate commands**: in the pipeline script, uncomment the build/lint/test commands for your ecosystem
8. **Configure CI**: edit `.github/workflows/sync-upstream.yml` — set the upstream URL, choose Python or Node.js steps, uncomment
9. **Create branches**: `upstream-mirror`, `integration`, `develop` (see Setup Procedure above)
10. **Test**: `python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run`
11. **Customize the guide**: edit `FORK_WORKBENCH_TEMPLATE.md` with your project-specific details (ecosystem, commands, file paths)
12. **Write `docs/dev/git-branch-workflow.md`**: your fork's authoritative reference, adapted from the template
