# 🛠️ Maintainer's Guide: Tooling & Harnesses

This document provides the recommended toolset for managing the Independent Monorepo. While the core logic is handled by scripts and Git, these "harnesses" are used to reduce cognitive load, prevent manual errors, and provide visual clarity for the maintainer.

## 1. Git Visualization (The Map)
Managing multiple upstream remotes and complex branching strategies in a terminal is error-prone. A visual Git client is mandatory for maintaining the "Inside" and "Outside" branch model.

### Recommended Tools: **Fork** or **GitKraken**
These tools provide a visual graph of the repository, allowing the maintainer to:
- **Visualize Remotes**: See all `upstream-` remotes in a side panel and compare their heads to the local `develop` branch.
- **Visual Merging**: Perform merges, rebases, and cherry-picks using a drag-and-drop interface rather than complex CLI commands.
- **Conflict Resolution**: Use high-fidelity side-by-side diff editors to resolve conflicts during upstream ingestion.

---

## 2. Monorepo Management (The Control Panel)
Because the project uses **Nx** to manage the dependency graph and task execution, a GUI is recommended to avoid memorizing complex CLI flags.

### Recommended Tool: **Nx Console (VS Code Extension)**
The Nx Console transforms the CLI into a menu-driven experience.
- **Task Execution**: Run `verify-bridges`, `build`, or `test` for specific packages via a dropdown menu.
- **Graph Visualization**: View the dependency graph to see exactly which packages are affected by a change before running a merge.
- **Simplified Input**: Provides a UI for entering parameters into Nx commands.

---

## 3. CI/CD Harness (The Automated Guard)
To ensure that "human error" does not reach the `main` branch, the project utilizes an automated harness.

### Tool: **GitHub Actions**
The following automation gates are implemented in the CI pipeline:
- **The Quality Gate**: Every Pull Request to `develop` automatically triggers `verify-bridges.sh`. If the bridge contract is violated, the merge is hard-blocked.
- **The Legal Gate**: Every new package addition triggers `check-compliance.sh`. If a forbidden license is detected, the merge is blocked.
- **The Regression Gate**: Merges from `develop` $\rightarrow$ `main` trigger the full integration suite to ensure zero regressions.

---

## 4. Upstream Monitoring (The Early Warning System)
To avoid the manual burden of checking for updates daily, the system uses scheduled automation.

### Tool: **Scheduled GitHub Actions (Cron)**
- **The Heartbeat**: A scheduled action runs `sync-upstreams.sh` every 24 hours.
- **Notifications**: If an upstream project (e.g., `upstream-aider`) is found to be significantly behind the remote, the system automatically opens a GitHub Issue or sends a notification to the maintainer.
- **Benefit**: Integration work is only performed when there is a verified update available.

---

## 5. Summary Tool-Stack

| Domain | Tool | Purpose |
| :--- | :--- | :--- |
| **Version Control** | **Fork / GitKraken** | Visual branch mapping & remote management. |
| **Monorepo Ops** | **Nx Console** | GUI for task execution & dependency graphing. |
| **Quality Assurance**| **GitHub Actions** | Automated gates & compliance enforcement. |
| **Upstream Sync** | **Scheduled Actions** | Automated update detection. |
| **Dependency Walls** | **uv / pnpm** | Strict environment isolation per package. |
