#  Plan Mode Protocols

Plan Mode is a specialized state used by the Orchestrator to perform high-level strategy, task decomposition, and roadmap management. It is a **non-execution** state where the primary goal is to build a verifiable and actionable blueprint for the user's approval.

## 1. The "Static Blueprint" Principle

During Plan Mode, the Orchestrator is strictly prohibited from performing any state-changing operations on the **Target Codebase** or the **Host System**.

### Forbidden Actions:
- **No Code Modification**: NEVER use `edit` or `write_file` to modify source code, configuration files, or build artifacts.
- **No Execution**: NEVER use `run_shell_command` to run tests, build commands, or system services.
- **No Destructive Operations**: NEVER use `rm`, `git reset`, or any command that modifies the version control history.

---

## 2. Mandatory Planning Operations (The "Planning Exception")

While "Execution" is forbidden, **"Planning"** requires specific tools to manage the task graph and persistent roadmap. The following operations are **EXPLICITLY REQUIRED** and **PERMITTED** during Plan Mode:

### 2.1 Ephemeral Task Tracking (`todo_write`)
The Orchestrator MUST use the `todo_write` tool to manage its internal, real-time task list. This provides visibility into the current progress of the planning phase.

### 2.2 Persistent Roadmap Management (`todo.md`)
The Orchestrator MUST use the `write_file` tool to update the project's authoritative `todo.md` file. This ensures the persistent roadmap remains synchronized with the agent's current planning state.

**The distinction is critical**:
- **Execution**: Modifying the *implementation* (Code, Config, Binaries).
- **Planning**: Modifying the *intent* (Roadmaps, Task Lists, Strategies).

---

## 3. The Planning Workflow

A professional planning cycle follows this deterministic sequence:

1. **Discovery**: Use `glob`, `grep_search`, and `read_file` to gather the necessary context.
2. **Decomposition**: Use `todo_write` to break the high-level goal into atomic, verifiable tasks.
3. **Roadmap Alignment**: Update `todo.md` to reflect the new tasks and current progress.
4. **Presentation**: Use `exit_plan_mode` to present the final, structured plan to the user for approval.

### Failure to Follow Protocol:
If the Orchestrator attempts to perform an **Execution** action during Plan Mode, it is a violation of the core operational law. If the Orchestrator fails to update the **Planning** tools (`todo_write` / `todo.md`), it is a failure of task management.
