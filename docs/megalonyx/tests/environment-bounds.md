#  Environment Boundaries

This document defines the operational boundaries of the Mega Code agentic stack. It specifies the limits of the agent's authority over the host system to ensure security, predictability, and testability.

## 1. Scope of Authority

The agent's authority is strictly bound to the **Project Root** (the directory where the CLI is invoked). Any operation outside this root is considered a boundary violation unless explicitly permitted by the sandboxing profile.

### The Working Directory (WD)
- **Definition**: The absolute path of the current project being edited.
- **Implicit Permission**: The agent has full read/write access to the WD for the purpose of implementing features and fixing bugs.
- **Verification**: All file paths used by tools must be resolved against the Project Root.

## 2. Access Control Matrix

| Zone | Path Pattern | Permission | Purpose |
| :--- | :--- | :---: | :--- |
| **Project Root** | `/home/user/projects/[project]/` | `RW` | Primary codebase manipulation |
| **Config Root** | `~/.qwen/` | `R` | Reading settings and model registry |
| **Machine Root** | `~/.local/share/megalonyx/` | `R` | Reading logs and telemetry |
| **System Config** | `/etc/`, `/var/lib/` | `Forbidden` | Prevent system-wide destabilization |
| **User Secrets** | `~/.ssh/`, `~/.gnupg/`, `~/.aws/` | `Forbidden` | Prevent credential exfiltration |
| **OS Binaries** | `/bin/`, `/usr/bin/` | `R` | Executing standard utilities |

## 3. Sandboxing & Enforcement

Boundaries are enforced through a multi-layered approach:

### Layer 1: Logical Filtering (Core)
The `ControlPlane` and `ToolExecutor` validate that requested paths are within the Project Root before passing them to the underlying OS calls.

### Layer 2: OS-Level Sandboxing (Machine)
When `QWEN_SANDBOX=true`, the system employs a provider-specific sandbox:
- **Docker/Podman**: The agent runs in a container where the Project Root is mounted as a volume. The rest of the host filesystem is inaccessible.
- **macOS Seatbelt**: Uses kernel-level profiles to restrict file system access to specific directories.

### Layer 3: Command Whitelisting
High-risk shell commands (e.g., `rm -rf /`, `chmod -R 777 /`) are flagged by the `IntentClassifier` and require explicit user confirmation or are blocked entirely by the sandbox profile.

## 4. Boundary Verification (Testing)

The stability of these boundaries is verified using the **Adversarial Test Suite**:

- **Path Traversal Tests**: Attempting to read `/etc/passwd` via `read_file` must result in a `PermissionError` or a logical block.
- **Write-Violation Tests**: Attempting to write to `~/.qwen/settings.json` directly via a tool must fail.
- **Sandbox Leak Tests**: Running `ls /` inside a sandboxed session must not reveal the host's root directory structure.

## 5. Boundary Exceptions

Exceptions to these rules (e.g., needing to modify a global config for a specific integration test) must be:
1.  Documented in the test case.
2.  Implemented using a temporary, isolated environment (e.g., a temporary directory created via `tempfile`).
3.  Cleaned up immediately after execution.
