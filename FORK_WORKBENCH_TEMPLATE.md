# Fork Workbench Template

> **The standard for contribution workbenches.** This document is the authoritative reference for the branch architecture, workflow rules, and operational procedures of this fork. Read it completely before touching any branch.

This fork is a contribution workbench. Every fix, feature, and document defaults to upstream-candidate unless it specifically manages the fork/upstream relationship.

---

## Branch Architecture

```
upstream/main → upstream-mirror → sync/staging-* → [gates] → integration → develop → main
                                      ↑
                                contribution branches
```

| Branch | Role | Push? | Description |
|--------|------|-------|-------------|
| `upstream/main` | Source of truth | Read-only | The upstream repo |
| `upstream-mirror` | Exact mirror | Fast-forward only | Always matches `upstream/main` HEAD |
| `integration` | Vetted upstream changes | Force-push | Only the pipeline writes here; never commit directly |
| `develop` | Primary working branch | Force-push | All fork work lands here eventually |
| `main` | Stable fork releases | Merge only | For downstream consumers; never pull back into workbench |
| `feat/*`, `fix/*`, `chore/*` | Contribution branches | Force-push | Individual PR candidates, based on `upstream-mirror` |
| `fork/*` | Fork infrastructure | Push | Fork-specific docs, tooling, PR drafts |
| `sync/staging-*` | Temporary pipeline branches | None | Created and deleted automatically by the pipeline |

---

## Two Kinds of Work Branches — Different Origins

This is the most important rule. There are two categories of work and they require different branch origins.

**The default is upstream-candidate.** Fork-only is the narrow exception.

### Category 1: Upstream-Candidate (the default — almost all work)

These branches are staging for upstream pull requests. They must:
- Contain **only the changes for that one fix or feature**
- Start from `upstream-mirror` so they have no fork history
- Have a **single clean commit** (or a small number of tightly related commits)

```bash
git fetch origin upstream-mirror
git checkout -b fix/short-description origin/upstream-mirror
# ... do work, commit ...
git checkout develop
git cherry-pick <commit-hash>
git checkout fix/short-description   # branch stays — it's the upstream PR staging
```

The branch stays permanently as the upstream PR staging. Do not delete it after cherry-picking to develop.

### Category 2: Fork-Only (narrow exception)

These branches will never go upstream. They branch from `develop` and merge back. Fork-only is **only**:
- The sync pipeline (`tooling/sync-upstreams/` or equivalent)
- Fork CI (`.github/workflows/sync-upstream.yml` or equivalent)
- Fork management docs (`docs/fork/`, workflow documentation)

If you are unsure whether something belongs here, it belongs in Category 1.

```bash
git checkout develop
git checkout -b feat/short-description
# ... do work, commit ...
git checkout develop
git merge feat/short-description
```

---

## Remotes

```
origin    → git@github.com:<you>/<project>.git          (your fork — normal dev target)
upstream  → git@github.com:<upstream-org>/<project>.git  (source — NEVER push here)
```

---

## Issue-First Workflow

Every piece of work starts with a GitHub issue. No exceptions.

```
1. Create issue on your fork's GitHub
   - Bug: include OS, numbered Steps to Reproduce, Expected/Actual Behaviour
   - Enhancement: include Area, Problem/Motivation, Proposed Solution

2. Determine work category:
   - Upstream-candidate → branch from upstream-mirror
   - Fork-only          → branch from develop

3. Do the work; commit cleanly

4. Cherry-pick (upstream-candidate) or merge (fork-only) to develop

5. If upstream-candidate:
   - Branch stays at single clean commit, ready to file a PR
   - Update docs/fork/upstream/pr-status.md

6. Close the fork issue when the fix is confirmed working
```

---

## Upstream Ingest Pipeline

Upstream changes flow into this fork through a verified pipeline. **Never bypass it.**

```
upstream/main
    ↓  git fetch + reset
upstream-mirror
    ↓  merge into temp staging branch off integration
sync/staging-TIMESTAMP
    ↓  Gate 1: Build verification (pnpm install)
    ↓  Gate 2: Lint (eslint)
    ↓  Gate 3: Tests (vitest) — skippable in CI with --skip-tests
integration  [ff-only merge + LKG-TIMESTAMP tag]
    ↓  manual merge
develop
```

### Running the pipeline

```bash
git checkout integration
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py           # full run
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run  # gates only
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --skip-tests  # skip test gate
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --push     # push after success
```

### CI automation

A scheduled CI workflow runs daily (`.github/workflows/sync-upstream.yml`). It syncs upstream, runs build/lint gates (skips tests in CI for speed), and pushes to `integration`.

### Promoting integration to develop

The pipeline lands changes on `integration`. To get them into `develop`:

```bash
git checkout develop
git merge integration
```

This is a manual step — the pipeline does not auto-merge to `develop`.

---

## Gates — Qwen Code Ecosystem

| Gate | Command | Purpose |
|------|---------|---------|
| Build | `pnpm install --frozen-lockfile` | Lockfile consistency |
| Lint | `npx eslint .` | Code style |
| Tests | `npx vitest run` | Full test suite |

---

## Last Known Good (LKG) Tags

Every successful pipeline promotion creates an annotated tag `LKG-YYYYMMDD-HHMM`. To roll back:

```bash
git tag -l "LKG-*" | sort -r | head -10          # list tags
git checkout LKG-20260523-1200                     # inspect
git checkout integration
git reset --hard LKG-20260523-1200                 # roll back (destructive)
```

A `rollback_to_lkg.py` script is provided in `tooling/sync-upstreams/` for safe rollback.

---

## Protected Files

The pipeline restores these files to their `integration` state after every upstream merge:

| Protected | Why |
|-----------|-----|
| `tooling/sync-upstreams/upstream_ingest_pipeline.py` | The pipeline itself |
| `.github/workflows/sync-upstream.yml` | Fork-only workflow — does not exist upstream |
| `AI.md` | Fork-specific AI guidance |
| `docs/ai/` | Fork-specific AI context and rules |
| `docs/fork/` | Fork management documentation |

---

## Pipeline Failure Recovery

See `docs/runbook.md` for detailed failure recovery procedures. Summary:

### Gate failure (build/lint/test)

Upstream introduced a regression. Do NOT bypass the gate. Investigate what broke. Options:
1. File an upstream issue; wait for them to fix it
2. Apply a minimal fix on the staging branch, then re-run gates
3. If urgent: run `--dry-run` to understand scope, then decide

### Merge conflict

The pipeline aborts and `integration` is untouched. The staging branch contains the conflict.

```bash
git checkout sync/staging-TIMESTAMP
# Resolve conflicts in the listed files
git add <resolved files>
git commit -m "chore(sync): resolve merge conflict with upstream"
git checkout integration
git merge --ff-only sync/staging-TIMESTAMP
git tag -a LKG-MANUAL -m "Last Known Good — manual conflict resolution"
git branch -D sync/staging-TIMESTAMP
```

### Pre-flight failure

| Cause | Fix |
|-------|-----|
| Not on `integration` branch | `git checkout integration` |
| Uncommitted changes | `git stash` or commit them |
| Missing `upstream` remote | `git remote add upstream <url>` |
| Missing tooling dependency | Install pnpm, Node.js 22 |

---

## Rebasing a Contribution Branch

When `upstream-mirror` advances (after a sync), contribution branches need rebasing:

```bash
# Check if rebase is needed
git log --oneline fix/branch-name..upstream-mirror | wc -l   # if > 0, rebase needed
git checkout fix/branch-name
git rebase upstream-mirror
```

**Conflict resolution:** Keep your fix AND incorporate upstream's changes. Remove all conflict markers.

**If stuck:** `git rebase --abort` to return to pre-rebase state.

**After rebase:** Develop's cherry-picks may be stale. Verify with `git diff upstream-mirror develop -- <files>`.

---

## Releasing to Main

When ready to publish a stable release for downstream consumers:

### Pre-release checklist

- [ ] `develop` branch is clean (`git status` shows nothing to commit)
- [ ] All intended contribution branches are merged to `develop`
- [ ] CI passes on `develop` (build, lint, tests)
- [ ] No uncommitted changes or unexpected files (`git diff --stat upstream-mirror..develop`)

### Release procedure

```bash
TAG="v$(date +%Y%m%d)"
git checkout main
git merge develop --no-ff -m "release: sync with upstream + contributions ${TAG}"
git tag -a "$TAG" -m "Release ${TAG} — upstream sync + fork contributions"
git push origin main --follow-tags
```

**Why `--no-ff`:** The merge commit records when the release happened and what was included.

**When to release:**
- After a set of contribution branches has been merged to `develop` and tested
- After a major upstream version has been ingested and verified
- On a regular cadence (e.g., weekly, monthly) if this fork has downstream consumers

**What main should contain:**
- All upstream changes (via the ingest pipeline)
- All merged contribution branches (via develop)
- A clean, linear history that downstream consumers can rely on

**Never pull from main back into the workbench.**

---

## Pre-Flight Checklist (before marking "Ready to File")

- [ ] Branch starts from `upstream-mirror` (not `develop`)
- [ ] Single clean commit (or tightly related commits)
- [ ] Diff contains only intended files — no fork-specific content
- [ ] No hardcoded paths, usernames, or tokens
- [ ] Commit message is clear and written for upstream reviewers
- [ ] Build verification passes
- [ ] Lint passes
- [ ] Tests pass locally
- [ ] Cross-platform considered: no platform-only assumptions in shared code

---

## Contribution Branch Health Checks

```bash
# Verify branch starts from upstream-mirror (not develop)
git merge-base fix/branch-name upstream-mirror
# Should return the same commit as: git rev-parse upstream-mirror

# Verify only your commits are on the branch
git log --oneline upstream-mirror..fix/branch-name
# Should show only your 1-3 commits

# Verify no fork-specific files in the diff
git diff upstream-mirror..fix/branch-name --name-only
# Should contain only files relevant to the fix/feature

# Verify the diff is clean (no conflict markers, no accidental whitespace)
git diff upstream-mirror..fix/branch-name --check
```

---

## When Upstream Already Has the Change

Sometimes a contribution branch's changes have already been merged upstream:

- **Cherry-pick produces empty commit:** `git cherry-pick <hash>` results in "nothing to commit". Skip it.
- **Gate passes but diff is empty:** If `git diff upstream-mirror..fix/branch-name` shows nothing, delete the branch.
- **Partial overlap:** `git rebase upstream-mirror`, drop the duplicate commits, keep only what's still needed.

---

## Common Mistakes to Avoid

| Mistake | Why bad | Correct action |
|---------|---------|----------------|
| Classifying work as fork-only without a specific reason | Prevents valid upstream contributions | Default to upstream-candidate |
| Branching an upstream-candidate off `develop` | Pollutes branch with fork commits | Branch from `origin/upstream-mirror` |
| Committing to `upstream-mirror` | Commits destroyed on next sync | Use as branch origin only |
| Cherry-picking from `upstream/main` directly to `develop` | Bypasses gates | Run the ingest pipeline |
| Merging an upstream-candidate branch to `develop` | Would import upstream history | Cherry-pick specific commits |
| Closing an issue before verifying the fix works | Disrupts workflow tracking | Verify first, close after |
| Creating a branch without an issue | Untraceable work | Create issue first, always |
| Editing `develop` directly for upstream-candidate work | Creates untracked work | Branch from upstream-mirror |
| Forgetting to update docs | Future agents lack context | Update fork documentation |

---

## Pipeline Invariants

1. **Integration is never modified until all gates pass.** Work happens on a throwaway staging branch.
2. **On any failure, the pipeline returns to `integration`.** The finally block enforces this.
3. **Staging branches are always cleaned up.** They do not accumulate.
4. **If already up to date, the pipeline exits cleanly** without creating branches or tags.
5. **Uncommitted changes to tracked files on integration are rejected at pre-flight.**

---

## Directory Structure for Fork Management

```
CONTRIBUTING.md                     # How upstream contributors interact with this fork
FORK_WORKBENCH_TEMPLATE.md          # This file — authoritative reference
docs/
  fork/
    README.md                       # Fork management hub — navigation
    issue-tracker.md                # Issue-to-branch mapping
    changes-from-upstream.md        # Master record of all fork divergence
    upstream/
      pr-status.md                  # Status of all staged upstream PRs
      pr-drafts/                    # PR draft files for upstream-candidate contributions
  runbook.md                        # Pipeline failure recovery procedures
tooling/
  sync-upstreams/
    upstream_ingest_pipeline.py     # Primary pipeline: fetch → stage → gate → promote
    rollback_to_lkg.py              # Roll back integration to a previous LKG tag
    gate_failure_tests.py           # Verify pipeline gates correctly block failures
.github/
  workflows/
    sync-upstream.yml               # Scheduled CI: daily auto-ingest
```
