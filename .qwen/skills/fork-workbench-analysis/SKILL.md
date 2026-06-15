---
name: fork-workbench-analysis
description: Analyze a fork workbench repo for branch topology health, pipeline integrity, and contribution readiness.
source: auto-skill
extracted_at: '2026-06-13T04:13:28.074Z'
---

# Fork Workbench Analysis

This skill performs a comprehensive health check of a fork workbench repository. It examines branch topology, pipeline integrity, contribution readiness, and identifies issues that need remediation.

## When to Use

Use this skill when:

- Auditing a fork workbench before a release cycle
- Diagnosing why PRs are not clean against upstream
- Onboarding a new fork to the workbench pattern
- Recovering from a pipeline failure or branch divergence

## Analysis Procedure

### 1. Remote & Branch Inventory

```bash
git remote -v
git branch -a
git branch -r | grep origin/ | grep -v HEAD
```

Identify:

- **Remotes**: `origin` (fork), `upstream` (source), any others (e.g., `megalonyx`)
- **Local branches**: contribution branches, `develop`, `main`, `integration`, `upstream-mirror`
- **Remote-only branches**: branches on `origin` that don't exist locally (orphaned staging)
- **Stale tracking branches**: branches that haven't been updated since initial setup

### 2. Branch Topology Analysis

For each key branch, determine its position relative to `upstream/main`:

```bash
# Branch positions
git rev-parse origin/main
git rev-parse origin/develop
git rev-parse origin/integration
git rev-parse upstream/main

# Divergence counts
git rev-list --count upstream/main..origin/main
git rev-list --count upstream/main..origin/develop
git rev-list --count upstream/main..origin/integration

# Ancestry checks
git merge-base --is-ancestor upstream/main origin/main
git merge-base --is-ancestor upstream/main origin/develop
git merge-base --is-ancestor origin/main origin/develop
git merge-base --is-ancestor origin/develop origin/main

# Merge base of main and develop
git merge-base origin/main origin/develop
```

**Key questions to answer:**

- Is `origin/main` ahead of, behind, or in sync with `upstream/main`?
- Is `origin/main` an ancestor of `origin/develop` (or vice versa)?
- What is the merge-base of `main` and `develop`? Is it current or stale?
- Does `integration` match `upstream/main` (it should)?

### 3. Pipeline Infrastructure Audit

Verify the pipeline files exist and are correctly configured:

```bash
# Pipeline files
ls tooling/sync-upstreams/upstream_ingest_pipeline.py
ls tooling/sync-upstreams/rollback_to_lkg.py
ls tooling/sync-upstreams/gate_failure_tests.py

# CI workflow
ls .github/workflows/sync-upstream.yml

# Documentation
ls FORK_WORKBENCH_TEMPLATE.md
ls CHEAT_SHEET.md
ls docs/runbook.md
ls docs/fork/README.md
ls docs/fork/changes-from-upstream.md
ls docs/fork/upstream/pr-status.md
```

Run the gate failure tests:

```bash
python3 tooling/sync-upstreams/gate_failure_tests.py
```

Check LKG tags:

```bash
git tag -l "LKG-*"
```

### 4. Contribution Branch Analysis

For each contribution branch (local and remote):

```bash
# Check branch base (should be upstream-mirror, not develop)
git merge-base <branch> upstream-mirror
git merge-base <branch> develop

# Check if branch has unique content
git log --oneline upstream/mirror..<branch>

# Check for fork-specific file leaks
git diff upstream/mirror..<branch> --name-only
```

**Red flags:**

- Branch based on `develop` instead of `upstream-mirror`
- Branch contains fork-specific files (docs/fork/, tooling/sync-upstreams/, etc.)
- Branch has more than 3-5 commits (scope creep)
- Branch has no unique commits (already upstream)

### 5. Stale Branch Detection

Identify branches that are no longer useful:

```bash
# Remote-only branches (not local)
comm -23 <(git branch -r | grep origin/ | grep -v HEAD | sed 's/origin\///' | sort) <(git branch | sort)

# Branches fully merged into main
git branch --merged origin/main

# Branches whose content is in main
git log --oneline origin/main..<branch>  # empty = fully merged
```

### 6. Documentation Consistency

Check for stale references:

```bash
# Should find zero branch-name "ingest" references (renamed to "integration")
grep -rn "\bingest\b" --include="*.md" docs/fork/ docs/ai/ .qwen/skills/fork-sync-contributions/ .qwen/skills/fork-workbench-pipeline/ AI.md
```

Verify issue tracker and PR status are current:

- Every contribution branch has a corresponding issue
- PR drafts exist for each contribution
- Status fields are accurate

## Report Format

Produce a structured report with these sections:

### Summary

One-line health assessment: **HEALTHY** / **NEEDS ATTENTION** / **CRITICAL**

### Branch Topology

```
upstream/main (source)
  ├── origin/upstream-mirror (should match)
  ├── origin/integration (should match upstream/main)
  │   └── origin/develop (ahead by N commits)
  └── origin/main (ahead/behind by N commits)
```

### Issues Found

Each issue with:

- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Description**: What's wrong
- **Risk**: What could go wrong
- **Fix**: Recommended remediation

### Pipeline Health

- Gate failure tests: PASS/FAIL (N/8)
- LKG tags: count and recency
- CI workflow: present/absent
- Rollback utility: present/absent

### Contribution Branches

Table of all contribution branches with status:
| Branch | Base | Commits | Unique | Status |

### Recommendations

Prioritized list of actions (immediate, short-term, long-term)

## Common Findings

| Finding                                        | Severity | Fix                                                 |
| ---------------------------------------------- | -------- | --------------------------------------------------- |
| `origin/main` not ancestor of `origin/develop` | HIGH     | Reset main to upstream/main, re-apply contributions |
| `origin/upstream-main` stale                   | MEDIUM   | Delete or update                                    |
| Orphaned remote branches                       | LOW      | Delete after confirming content is merged           |
| Contribution branch based on `develop`         | HIGH     | Rebase onto upstream-mirror                         |
| Gate failure tests failing                     | HIGH     | Fix pipeline code                                   |
| No LKG tags                                    | MEDIUM   | Run pipeline to generate initial tag                |
| Stale `fork/workbench-items` branch            | LOW      | Delete or rebase                                    |
