# Pipeline Operations Runbook

This document is the operational reference for the Upstream Ingest Pipeline. It covers how to run the pipeline, interpret its output, and recover from every failure mode. It is written to be actionable by an AI agent without additional context.

---

## Quick Reference

| Task | Command |
| :--- | :--- |
| Sync upstream into integration | `python3 tooling/sync-upstreams/upstream_ingest_pipeline.py` |
| Check gates without syncing | `python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run` |
| Run gate failure tests | `python3 tooling/sync-upstreams/gate_failure_tests.py` |
| Submit a fix to upstream | `./tooling/sync-upstreams/contribute-upstream.sh <commit> <branch-name>` |
| Roll back integration | `git reset --hard <LKG-tag>` |

---

## Prerequisites

Before the pipeline will run, all of these must be true:

- Current branch is `integration`
- Remotes `upstream` and `origin` both exist (`git remote`)
- `uv` is installed and on PATH
- `tooling/symmetry_check.py` exists
- No uncommitted changes to tracked files on `integration`

The pipeline checks these automatically at startup (pre-flight). If pre-flight fails, fix the stated condition and re-run.

---

## Normal Run — Expected Output

```
[INFO] Running pre-flight checks...
[OK]   Pre-flight passed.
[INFO] Fetching upstream/main...
[OK]   Already up to date — nothing to sync.      ← if no new upstream commits
```

or, when upstream has new commits:

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
[INFO] Gate 1/3: Boot test (uv lock --check)...
[OK]   Boot gate passed.
[INFO] Gate 2/3: Ruff lint...
[OK]   Lint gate passed.
[INFO] Gate 3/3: Symmetry check (config ↔ docs)...
[OK]   Symmetry gate passed.
[INFO] Promoting sync/staging-... → integration...
[OK]   Tagged as LKG-20260523-0426.
[OK]   Pipeline complete. LKG tag: LKG-20260523-0426
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
git remote add origin <your-private-monorepo-url>
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
  path/to/file.py

Resolve, commit, then re-run the ingest pipeline.
```

**Recovery:**
1. The staging branch has already been deleted. `integration` is clean.
2. Manually reconcile the conflict — either update `integration` to be compatible with upstream, or document why the divergence is intentional.
3. Re-run the pipeline.

---

### VERIFICATION failure — Gate 1: Boot

```
[FAIL] Boot gate failed — lockfile out of sync:
       error: Unable to find lockfile at `uv.lock`...
Fix with: uv lock
```

The `uv.lock` file is missing or inconsistent with `pyproject.toml`. This happens when upstream adds a dependency without regenerating the lockfile.

**Recovery:**
```bash
uv lock
git add uv.lock
git commit -m "fix: regenerate uv.lock after upstream dependency change"
# then re-run the pipeline
```

---

### VERIFICATION failure — Gate 2: Lint

```
[FAIL] Lint gate failed. Auto-fix attempt: uv run ruff check --fix .
```

Upstream introduced Python code that does not pass ruff.

**Recovery:**
```bash
uv run ruff check --fix .    # auto-fix what's safe
uv run ruff check .          # inspect remaining errors
# manually fix anything ruff can't auto-fix
git add -p                   # stage fixes
git commit -m "fix(lint): resolve upstream ruff violations"
# then re-run the pipeline
```

---

### VERIFICATION failure — Gate 3: Symmetry

```
[FAIL] Symmetry gate failed. config/ and docs/ are out of sync.

Symmetry Violation: The following config files are missing documentation mirrors:
  - .qwen/config/new-feature.toml  -->  docs/new-feature.toml.md
```

A config file exists in `.qwen/config/` without a matching `.md` in `docs/`.

**Recovery:**
```bash
# Create the missing documentation file
touch docs/new-feature.toml.md
# Add meaningful documentation describing what the config does
git add docs/new-feature.toml.md
git commit -m "docs: add mirror for new-feature config"
# then re-run the pipeline
```

---

## Dry Run

Use `--dry-run` to check whether the current state of `integration` passes all gates without fetching or staging anything:

```bash
python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run
```

This is useful to verify your environment is clean before a real sync, or to check that manual fixes resolved a gate failure.

---

## Gate Failure Tests

Verifies that all three pipeline failure modes are correctly blocked. Run after any changes to the pipeline itself:

```bash
python3 tooling/sync-upstreams/gate_failure_tests.py
```

Expected output ends with:
```
==========================================
PIPELINE GATE FAILURE TEST REPORT
==========================================
  Merge Conflict           : PASS
  Symmetry Violation       : PASS
  Boot Failure             : PASS
==========================================
[PASS] All gate failure tests passed.
```

---

## Rollback

Every successful promotion is tagged `LKG-YYYYMMDD-HHMM` (Last Known Good).

```bash
# List available LKG tags
git tag -l "LKG-*" | sort -r | head -10

# Inspect a tag without changing branch
git show LKG-20260523-0426

# Roll back integration to a prior LKG (destructive — confirm first)
git checkout integration
git reset --hard LKG-20260523-0426
```

After a rollback, the pipeline can be re-run to attempt a fresh sync from the current upstream state.

---

## Invariants

The pipeline guarantees these properties on every run:

1. **Integration is never modified until all gates pass.** Work happens on a throwaway staging branch.
2. **On any failure, the pipeline returns to `integration`.** The finally block enforces this even if a failure occurs mid-sync.
3. **Staging branches are always cleaned up.** They do not accumulate.
4. **If already up to date, the pipeline exits cleanly without creating branches or tags.**
5. **Uncommitted changes to tracked files on integration are rejected at pre-flight.** They cannot accidentally be included in a promotion.
