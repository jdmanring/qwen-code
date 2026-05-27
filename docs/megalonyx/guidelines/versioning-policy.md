#  Versioning & Release Policy

This document codifies the versioning protocol for the **Mega Code** stack. We adhere to **Semantic Versioning (SemVer) 2.0.0** to ensure predictable, deterministic, and automated lifecycle management.

---

## 1. The Versioning Standard: SemVer

All releases follow the `MAJOR.MINOR.PATCH` format:

| Segment | Name | When to Increment | Example |
| :--- | :--- | :--- | :--- |
| **MAJOR** | Breaking | Fundamental architectural changes, breaking changes to the installer, or breaking changes to the core API/Protocol. | `1.0.0` $\rightarrow$ `2.0.0` |
| **MINOR** | Feature | New capabilities, new core services, or significant functional additions that are backward-compatible. | `0.2.1` $\rightarrow$ `0.3.0` |
| **PATCH** | Fix | Bug fixes, documentation updates, or minor refactors that do not change functionality. | `0.2.1` $\rightarrow$ `0.2.2` |

---

## 2. Single Source of Truth (SSOT)

To prevent "Version Drift," the version of the project is defined in exactly **one** machine-readable location:

**`config/meta/versions.lock`**

All other files (`README.md`, `master-plan.md`, etc.) must be synchronized with this value.

---

## 3. Agentic Versioning Protocol (The "Law")

To ensure AI agents (like Qwen Code) can autonomously manage the lifecycle, the following protocol is mandatory:

### **A. Detection**
Before any major change, the agent MUST read `config/meta/versions.lock` to identify the current baseline.

### **B. Decision Tree**
When a change is proposed, the agent must determine the increment:
1.  **Does this change break existing user workflows or the installer's contract?** $\rightarrow$ **MAJOR**
2.  **Does this add a new capability or service?** $\rightarrow$ **MINOR**
3.  **Is this a fix or a documentation update?** $\rightarrow$ **PATCH**

### **C. Execution Sequence**
A version bump must follow this atomic sequence:
1.  **Update `config/meta/versions.lock`** with the new `project_version`.
2.  **Update `README.md`** and **`master-plan.md`** to reflect the new version.
3.  **Commit** the changes with a conventional commit message (e.g., `chore: bump version to 0.2.2`).
4.  **Tag** the commit in Git (e.    g., `git tag -a v0.2.2 -m "Release v0.2.2"`).

---

## 4. Automation & Enforcement

*   **Manifest-Driven**: The installer and orchestrator use `versions.lock` to verify environment compatibility.
*   **Compliance Check**: Any attempt to modify core logic without a corresponding version bump in the manifests is a violation of the **Architectural Integrity** principle.
