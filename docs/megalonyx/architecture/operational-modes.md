# 🕹️ Operational Modes: Policy & Constraints

This document describes the different operating modes of the Runtime Stack and how they are enforced via the `PolicyEngine`.

## 🛡️ The Policy Engine

The `PolicyEngine` (`packages/core/src/policy_engine.py`) is the central authority for safety and constraint enforcement. It does not rely on the LLM's instructions but instead intercepts every tool call to verify permissions.

### Permission Matrix
The engine maps the combination of **Intent** and **Agent** to a set of permissions:
- `can_read`: Boolean.
- `can_write`: Boolean.
- `allowed_paths`: A list of regex patterns for permitted file access.
- `approval_required`: Boolean.

---

## 🚦 Operating Modes

The system supports several modes that alter the behavior of the `PolicyEngine`.

### 1. Plan Mode (Read-Only)
**Purpose**: Exploratory analysis and architectural blueprinting.
- **Trigger**: Activated when the `IntentClassifier` identifies a planning-heavy intent.
- **Constraint**: `can_write = False`.
- **Behavior**: Any attempt to call `edit` or `write_file` is blocked. The AI is forced to use `todo_write` and read-only tools to build a plan.

### 2. Auto-Edit Mode (Surgical Automation)
**Purpose**: Rapid implementation of verified plans.
- **Trigger**: Enabled via `settings.json` or a specific session command.
- **Constraint**: `approval_required = False` for a specific set of "Safe" mutation tools.
- **Behavior**: The system executes `edit` and `write_file` operations without prompting the user for confirmation.

### 3. YOLO Mode (Global Override)
**Purpose**: Full autonomy for trusted environments.
- **Trigger**: Global override flag.
- **Constraint**: All `PolicyEngine` checks are bypassed.
- **Behavior**: The system operates with total freedom, executing any tool without confirmation or boundary checks.

---

## 📝 Planning & Task Tracking

Planning is a first-class operational state in the Runtime Stack.

### The Todo System
The `todo_write` tool is the primary mechanism for state tracking.
- **Ephemeral State**: The current todo list is held in memory during the session.
- **Persistence**: The `StateManager` (`packages/core/src/state_manager.py`) persists the session state to `~/.qwen/state.json`.
- **Schema**:
    - `active_phase`: Current stage of the loop (e.g., `PLANNING` $\to$ `IMPLEMENTATION`).
    - `todo_list`: Array of tasks with `id`, `content`, and `status` (`pending`, `in_progress`, `completed`).

### The Planning Loop
The system enforces a strict sequence:
`Plan` $\to$ `Validate` $\to$ `Implement` $\to$ `Verify`.
If the system is in `Plan Mode`, it cannot transition to `Implementation` until the `todo_list` is populated and the plan is validated.
