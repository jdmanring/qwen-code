# 🌿 Git & Branching Strategy: Sovereign Monorepo (v2.0)

This document defines the version control protocol for the integration of multiple upstream projects into the Sovereign Monorepo.

## 1. Remote Configuration
We use **Dedicated Upstream Remotes** to track original projects without the rigidity of submodules.

### Initial Setup
```bash
# General Pattern: git remote add upstream-<project-name> <repository-url>
git remote add upstream-qwen https://github.com/Qwen/qwen-code.git
git remote add upstream-aider https://github.com/paul-gauthier/aider.git
git remote add upstream-cline https://github.com/cline/cline.git
git remote add upstream-openhands https://github.com/All-Hands-AI/OpenHands.git
git remote add upstream-omniroute https://github.com/omniroute/omniroute.git
git remote add upstream-opencode https://github.com/opencode/opencode.git
git remote add upstream-claw https://github.com/claw/claw-code.git
```

---

## 2. The Branching Model
We use a tiered branching strategy to isolate integration work from stable production code.

### A. The Permanent Branches
| Branch | Role | Access/Policy |
| :--- | :--- | :--- |
| `main` | **Production** | Only accepts merges from `develop`. Must be 100% stable. |
| `develop` | **Integration Hub** | The "staging" area. All feature branches merge here first. |

### B. The Ephemeral Branches
| Branch Type | Naming Convention | Purpose |
| :--- | :--- | :--- |
| **Tracking** | `upstream/<project>/main` | A read-only mirror of the original project's latest code. |
| **Integration** | `feat/integrate-<project>` | The "Work-Bench" for merging and refactoring. |
| **Fix** | `fix/<issue-id>` | Targeted fixes for bugs discovered in `develop`. |

---

## 3. The Integration Workflow

### Standard Ingestion Pipeline
1. **Synchronize**: `git fetch upstream-<project>`
2. **Isolate**: `git checkout develop && git pull origin develop && git checkout -b feat/integrate-<project>`
3. **Ingest**: `git merge upstream-<project>/main` (or cherry-pick for specific fixes).
4. **Adapt**: Move files to `/packages/<project>`, update the Bridge Adapter, and align with Symmetry standards.
5. **Verify**: Run package-level unit tests and Bridge integration tests.
6. **Promote**: Merge `feat/integrate-<project>` $\to$ `develop` $\to$ `main`.

---

## 4. Clean-Room Upstream Bug Reporting
To ensure original authors accept our bug reports, we must prove the bug exists in their original environment.

### The Protocol
1. **Isolate**: Clone the upstream repo into a fresh temporary directory: `/tmp/clean-room/[bug-id]`.
2. **Mirror**: Checkout the exact commit hash currently used in our monorepo.
3. **Environment**: Install dependencies using the upstream's original `requirements.txt` or `package.json` (NOT our `uv.lock`).
4. **Reproduction**: Write a minimal reproduction script (`repro.py`) that triggers the bug.
5. **Report**: Submit the `repro.py` and environment specs to the original author's GitHub issue tracker.

### Tracking
Store these in `/upstreams/bug-reports/[project-name]/[bug-id]/` with a `meta.json` containing the upstream commit and issue link.

---

## 5. Automation Suite (The Tooling)
To make this process foolproof, we use the `/tooling` suite.

| Script | Purpose | Input | Output |
| :--- | :--- | :--- | :--- |
| `sync-upstreams.sh` | Fetches all remotes and reports updates. | `package_name` (optional) | JSON summary of updates. |
| `integrate-package.sh`| Automates the branching and merging pipeline. | `repo_url`, `name` | New package directory. |
| `verify-bridges.sh` | Validates that adapters still fit contracts. | `package_name` (optional) | JUnit XML test report. |
| `check-compliance.sh` | Scans `LICENSE` files against whitelist. | None | Compliance CSV report. |

**Execution Standard**: All scripts use strict exit codes (`0` for success, `1` for infra error, `2` for test failure) to integrate with CI/CD.
