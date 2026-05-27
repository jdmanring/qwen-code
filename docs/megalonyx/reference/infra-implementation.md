#  Infrastructure Implementation Reference

This document provides a deep-dive technical specification of the `packages/infra/` layer. It describes the internal logic and mechanisms used to manage the lifecycle, deployment, and environment isolation of the Megalonyx.

---

##  Core Architecture

The infrastructure layer acts as the bridge between the **Blueprint** (the version-controlled source) and the **Machine** (the deployed runtime). It is responsible for ensuring that the Machine is a high-fidelity, reproducible projection of the Blueprint.

### 1. Git Worktree Management

To support multi-branch development and testing without polluting the main repository, the system utilizes Git worktrees. This is managed by the `GitWorktreeManager` class.

* **Implementation**: `packages/infra/git_worktree_manager.py`
* **Core Mechanisms**:
    * **Asynchronous CLI Wrapper**: Uses `asyncio` to wrap standard `git worktree` commands, providing non-blocking management of worktrees.
    * **Programmatic Parsing**: Employs `git worktree list --porcelain` to ensure deterministic parsing of active worktrees, including their filesystem paths and associated branches.
    * **Lifecycle Operations**:
        * `list_worktrees()`: Retrieves a structured list of all active worktrees.
        * `add_worktree(branch, path)`: Automates the creation of a new worktree for a specific branch.
        * `remove_worktree(path)`: Safely cleans up and removes an existing worktree.
        * `prune_worktrees()`: Runs `git worktree prune` to clear stale metadata and maintain repository hygiene.

### 2. Manifest-Driven Deployment

The deployment process is governed by a declarative "Layout Manifest," ensuring that the deployment is predictable and verifiable.

* **Source of Truth**: `config/meta/layout.json`
* **Orchestration**: `install.sh`

#### **The Two-Stage Deployment Process**

1.  **Bulk Mirroring (High-Speed)**:
    The installer uses `rsync` to perform a high-speed, selective copy of the project structure from the Blueprint to the Machine (`~/.local/share/megalonyx/`).
    * **Selective Exclusion**: Development artifacts (e.g., `.git`, `tests/`, `__pycache__/`) are explicitly excluded to keep the Machine lean.
    * **Integrity**: The `rsync --update --inplace` flags ensure that existing runtime files are updated efficiently without unnecessary overhead.

2.  **Manifest-Specific Deployment (Fine-Grained)**:
    After the bulk mirror, a specialized Python routine within `install.sh` parses `config/meta/layout.json` to handle complex mappings:
    * **Directory Mirroring**: Ensures entire sub-trees (e.g., `config/agents/`) are correctly placed.
    * **File-Level Mapping**: Handles specific file copies that may require special handling.
    * **Symbolic Link Creation**: Creates critical symlinks for binaries (e.g., mapping `scripts/status.sh` to `~/.local/bin/mega-status`).

### 3. Runtime Path Resolution

A critical step in the deployment process is the resolution of relative paths to ensure the system remains location-agnostic on the Machine.

* **Mechanism**: Post-deployment, the installer parses `~/.qwen/settings.json`.
* **Transformation**: Any relative paths used in configuration (e.g., in `mcpServers` arguments) are converted into absolute paths relative to the `STACK_ROOT` (`~/.local/share/megalonyx/`).
* **Purpose**: This ensures that the MCP daemon and other background services can be reliably spawned regardless of the user's current working directory.

### 4. Environment Isolation

To prevent dependency conflicts and ensure hardware compatibility, the stack operates within a strictly managed Python virtual environment.

* **Implementation**: Managed by `install.sh`.
* **Isolation Strategy**:
    * **Dedicated Venv**: A dedicated virtual environment is created at `$STACK_ROOT/py/venv`.
    * **Strict Dependency Enforcement**: The installer enforces a "Final Override" policy for critical libraries. For example, it mandates a specific version of `torch` (e.g., `2.12.0+cu130`) using a specific `--index-url` to ensure CUDA compatibility.
    * **Command Wrappers**: To provide a seamless user experience, the installer installs several shell wrappers in `~/.local/bin/` (e.g., `mega-run-py`, `mega-memory-manager`, and `mega-status`). These wrappers automatically use the interpreter and libraries located within the isolated virtual environment.

---
**VERSION**: `v1.0.0` | **Status**: `Stable` | **Last Updated**: `May 21, 2026`
