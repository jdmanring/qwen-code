# 🛠️ Execution Plane Protocols

This document defines the mandatory, deterministic workflows for all code discovery, modification, and verification tasks within the Mega Code stack. These protocols are designed to eliminate probabilistic "guessing" and ensure a verifiable chain of custody for every change.

## 1. [S-DISCOVER] Surgical Discovery Protocol

To prevent context dilution and "hallucinated" file structures, all codebase exploration must follow this exact sequence:

### The Sequence:
1. **Scope (Glob)**: Use `glob` to find all files matching a general pattern.
   - *Goal*: Establish the boundaries of the search.
2. **Target (Grep)**: Use `grep_search` to find specific symbols, function names, or keywords within the scoped files.
   - *Goal*: Narrow down to the exact lines of interest.
3. **Extract (Read)**: Use `read_file` to capture the full context of the targeted files.
   - *Goal*: Obtain the final ground truth for implementation.

### Forbidden Actions:
- NEVER `read_file` a path based on a guess or a partial grep result without first verifying the scope via `glob`.
- NEVER assume a file's content based on its name.

---

## 2. [S-VERIFY] Verification Contract

No action is considered "complete" until it has been verified by an independent tool.

### The Contract:
`Action` $\rightarrow$ `Verification Tool` $\rightarrow$ `Pass/Fail`

### Verification Mapping:
| Action | Primary Verification Tool | Success Criteria |
| :--- | :--- | :--- |
| `edit` / `write_file` | `read_file` | Content matches the intended change exactly. |
| Logic Change | `run_shell_command` (Tests) | All relevant tests pass (exit code 0). |
| Config Change | `run_shell_command` (Service Start) | Service starts and health check passes. |
| Dependency Add | `run_shell_command` (Build/Lint) | Build succeeds without type/dependency errors. |

### Constraint:
A task in `todo.md` MUST NOT be marked `completed` until the Verification Contract is satisfied.

---

## 3. [S-CORRECT] The Correction Loop

When a verification fails, the agent must enter a deterministic correction state rather than simply retrying the action.

### The Loop:
1. **Observe**: Capture the exact error message or diff from the verification tool.
2. **Analyze**: Compare the **Actual Result** vs. the **Expected Result**.
3. **Isolate**: Identify the root cause (e.g., typo, missing import, incorrect path, environment mismatch).
4. **Correct**: Apply a surgical fix targeting the root cause.
5. **Re-Verify**: Repeat the `S-VERIFY` process.

### Forbidden Actions:
- NEVER "try again" with the same or a slightly modified prompt without first performing a Diff Analysis.
- NEVER ignore a verification failure by claiming it's "minor" or "irrelevant."

---

## 4. [S-SURGERY] Surgical Editing Protocol

To maintain codebase integrity and prevent the accidental deletion of context, comments, or unrelated logic, all modifications must follow the Surgical Editing Protocol.

### The Mandate:
Modification of existing files MUST be performed using the `edit` tool. The `write_file` tool is strictly reserved for the creation of new files or the complete replacement of configuration files.

### The Protocol:
1. **Fresh Read**: Perform a `read_file` of the target file immediately before the `edit` call.
2. **Exact Match**: The `old_string` MUST be a literal, exact match of the text in the file, including all whitespace and indentation.
3. **Contextual Anchoring**: Include at least 3 lines of context before and after the target change to ensure the edit is anchored to a unique location.
4. **Failure Handling**: If an `edit` fails (0 occurrences found), the agent MUST NOT use `write_file` as a workaround. Instead:
   - Re-read the file.
   - Analyze the diff between the expected `old_string` and the actual content.
   - Correct the `old_string` to match the current state of the disk.
   - Retry the `edit`.

---

## 5. [S-AUTH] System Authority & Environment Integrity

To prevent divergence between the agent's internal model and the actual host environment, all interactions with system-level services must follow this protocol.

### The Mandate:
The agent is a software engineering agent, not a system administrator. It has no implicit authority over the host's running services, daemons, or environment-level configurations.

### The Protocol:
1. **Principle of Least Authority (PoLA)**: Assume all services (Qdrant, daemons, etc.) are `[OFF]` unless explicitly verified via the user's preferred management tools (e.g., `mega-memory-manager status`).
2. **The Discrepancy Halt**: If a command reports success (e.g., `mega-memory-manager start` returns exit code 0) but subsequent verification (e.g., a connection attempt) fails, the agent MUST NOT attempt to "fix" the code. This is an **Environment Discrepancy**, not a code bug. The agent must halt and report the discrepancy to the user.
3. **External Truth Only**: The agent must prioritize the user's direct observations and the output of the user's management tools over its own inferred state.

---

## 6. [S-REALITY] The Reality Check Protocol

To prevent "hallucinated environment" failures, the agent must implement a mandatory Reality Check loop for all system-dependent tasks. A professional engineer does not trust a tool's report of success; they verify the actual effect on the system.

### The Loop:
1. **Pre-Flight Check**: Before executing any test or tool that depends on a service, verify the service is active and reachable.
   - *Example*: Run `mega-memory-manager status` AND check the socket with `ss -lx`.
2. **Action**: Perform the intended operation (e.g., `mega-memory-manager start`).
3. **Independent Verification**: Verify the result using a **different** tool or method than the one used to perform the action.
   - *Example*: If `mega-memory-manager start` was used, verify via `ps aux` or `ss -lx`.
4. **Discrepancy Halt**: If the action reports success but the independent verification fails, the agent must halt immediately. This is a critical environment failure. Do not proceed with the plan.

### Forbidden Actions:
- NEVER assume a service is running based solely on the exit code of a startup command.
- NEVER proceed to a test if the Pre-Flight Check reveals the service is unreachable.
- NEVER ignore a discrepancy between a tool's report and the actual system state.

---

## 7. [S-PLAN] Plan Mode Protocols

Planning is a distinct operational state. While code modification is forbidden, task management is mandatory.

### The Mandate:
During Plan Mode, the Orchestrator MUST use `todo_write` for ephemeral session tracking and `write_file` for updating the persistent `todo.md` roadmap. These are considered **Planning Operations**, not **Execution Operations**.

### The Protocol:
1. **Discovery**: Use `glob`, `grep_search`, and `read_file` to gather context.
2. **Decomposition**: Use `todo_write` to break goals into atomic tasks.
3. **Roadmap Alignment**: Update `todo.md` to reflect the current state.
4. **Presentation**: Use `exit_plan_mode` to present the plan for approval.

For detailed rules on Plan Mode, see `docs/guidelines/plan-mode.md`.
