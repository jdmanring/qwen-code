# Pipeline Operations Runbook

This document is the operational reference for the Upstream Ingest Pipeline. It covers how to run the pipeline, interpret its output, and recover from every failure mode.

---

## Quick Reference

| Task | Command |
| :--- | :--- |
| Sync upstream into integration | `python3 tooling/sync-upstreams/upstream_ingest_pipeline.py` |
| Check gates without syncing | `python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run` |
| Skip tests (CI mode) | `python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --skip-tests` |
| Push after sync | `python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --push` |
| Run gate failure tests | `python3 tooling/sync-upstreams/gate_failure_tests.py` |
| Roll back integration | `python3 tooling/sync-upstreams/rollback_to_lkg.py` |
| List LKG tags | `python3 tooling/sync-upstreams/rollback_to_lkg.py --list` |

---

## Prerequisites

Before the pipeline will run, all of these must be true:

- Current branch is `integration`
- Remotes `upstream` and `origin` both exist (`git remote`)
- No uncommitted changes to tracked files on `integration`
- Node.js 22 and pnpm installed

The pipeline checks these automatically at startup (pre-flight). If pre-flight fails, fix the stated condition and re-run.

---

## Normal Run — Expected Output

```
[INFO] Running pre-flight checks...
[OK]   Pre-flight passed.
[INFO] Fetching upstream/main...
[INFO] 12 new upstream commit(s) to integrate.
[INFO] Resetting upstream-mirror to upstream/main...
[OK]   Mirror synchronized.
[INFO] Creating staging branch: sync/staging-20260523042600
[INFO] Merging upstream-mirror into sync/staging-20260523042600...
[OK]   Merge clean.
[INFO] Restored 2 protected file(s).
[INFO] Gate 1/3: Build verification (pnpm install)...
[OK]   Build gate passed.
[INFO] Gate 2/3: Lint (eslint)...
[OK]   Lint gate passed.
[INFO] Gate 3/3: Tests (vitest)...
[OK]   Test gate passed.
[INFO] Promoting sync/staging-... → integration...
[OK]   Promoted and tagged as LKG-20260523-0426.
```

---

## Failure Modes and Recovery

### PREFLIGHT failure

**"Must be on 'integration' branch"**
```bash
git checkout integration
```

**"Missing required remotes"**
```bash
git remote add upstream https://github.com/QwenLM/qwen-code.git
git remote add origin git@github.com:<you>/qwen-code.git
```

**"Integration branch has uncommitted changes"**
```bash
git stash        # if you want to keep the changes
# or
git diff HEAD    # inspect, then commit or discard
```

---

### PIPELINE_ERROR — Merge Conflict

The pipeline aborts and leaves `integration` untouched. The error lists the conflicting files.

```
Merge conflict — manual resolution required:
  path/to/file.ts

Resolve, commit, then re-run the ingest pipeline.
```

**Recovery:**
1. `integration` is clean — the pipeline aborted before modifying it.
2. Manually reconcile the conflict — either update `integration` to be compatible with upstream, or document why the divergence is intentional.
3. Re-run the pipeline.

---

### VERIFICATION failure — Gate 1: Build

```
[FAIL] Build gate failed — pnpm install --frozen-lockfile failed.
```

**Recovery:**
```bash
pnpm install
git add pnpm-lock.yaml
git commit -m "fix: regenerate lockfile after upstream dependency change"
# then re-run the pipeline
```

---

### VERIFICATION failure — Gate 2: Lint

```
[FAIL] Lint gate failed.
```

**Recovery:**
```bash
npx eslint . --fix    # auto-fix what's safe
npx eslint .          # inspect remaining errors
# manually fix anything eslint can't auto-fix
git add -p
git commit -m "fix(lint): resolve upstream lint violations"
# then re-run the pipeline
```

---

### VERIFICATION failure — Gate 3: Tests

```
[FAIL] Test gate failed.
```

**Recovery:**
```bash
npx vitest run         # run tests to see what failed
# Fix the failing test or the upstream regression
git add -p
git commit -m "fix: resolve upstream test regression"
# then re-run the pipeline
```

---

## Upstream Already Has the Change

**Cherry-pick says "nothing to commit":**
```bash
git cherry-pick <hash>
# "nothing to commit, working tree clean"
# → The change is already upstream. Skip it.
git cherry-pick --skip
```

**Contribution branch has no unique commits:**
```bash
git diff upstream-mirror..fix/branch-name
# (empty output)
# → Delete the branch. The work is already upstream.
git checkout develop
git branch -d fix/branch-name
```

**Partial overlap — upstream has some but not all of your changes:**
```bash
git rebase upstream-mirror
# Drop commits that are already upstream, keep only what's still needed
git rebase -i upstream-mirror  # interactive: drop duplicates
```

---

## Dry Run

Use `--dry-run` to check whether the current state of `integration` passes all gates without fetching or staging:

```bash
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run
```

---

## Rollback

Every successful promotion is tagged `LKG-YYYYMMDD-HHMM` (Last Known Good).

**Using the rollback utility (Recommended):**
```bash
python3 tooling/sync-upstreams/rollback_to_lkg.py              # most recent LKG
python3 tooling/sync-upstreams/rollback_to_lkg.py --tag LKG-20260523-1200
```

**Manual rollback (Destructive — confirm first):**
```bash
git tag -l "LKG-*" | sort -r | head -10          # list tags
git show LKG-20260523-1200                       # inspect
git checkout integration
git reset --hard LKG-20260523-1200                # roll back
```

---

## Invariants

1. **Integration is never modified until all gates pass.** Work happens on a throwaway staging branch.
2. **On any failure, the pipeline returns to `integration`.** The finally block enforces this.
3. **Staging branches are always cleaned up.** They do not accumulate.
4. **If already up to date, the pipeline exits cleanly** without creating branches or tags.
5. **Uncommitted changes to tracked files on integration are rejected at pre-flight.**
