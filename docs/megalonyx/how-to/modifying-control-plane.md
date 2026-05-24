# Modifying the Control Plane: Extending the System Brain

This guide provides detailed instructions for developers to extend and modify the "Brain" of the system. The Control Plane is the central nervous system of the Cognitive-Symmetry Framework (CSF), responsible for intent classification, task decomposition, and policy enforcement.

## Overview of the Control Plane

The Control Plane operates as a pipeline that transforms a high-level user request into a set of atomic, executable jobs. The flow is as follows:

**`IntentClassifier`** $\to$ **`TaskDecomposer`** $\to$ **`JobStateManager`**

1.  **`IntentClassifier`**: Analyzes the input to determine the user's goal based on a predefined taxonomy.
2.  **`TaskDecomposer`**: Breaks down the classified intent into a sequence of atomic jobs (the "Plan").
3.  **`JobStateManager`**: Tracks the execution state, handles retries, and manages the lifecycle of each job.

---

## 1. Extending the Intent Taxonomy

The `IntentClassifier` uses a structured taxonomy to map user input to specific operational profiles. To add a new capability to the system, you must first define it in the taxonomy.

### Location
`packages/core/src/intent_classifier.py` $\to$ `INTENT_TAXONOMY`

### Process
Add a new entry to the `INTENT_TAXONOMY` dictionary. Each entry must define the following keys:

- `description`: A human-readable summary of what the intent represents.
- `goal`: The primary objective the system should achieve.
- `tool_chain`: A list of tool categories required for this intent.
- `risk_profile`: The risk level associated with the intent (e.g., `low`, `medium`, `high`).
- `verification`: The required level of verification (e.g., `automatic`, `manual_review`).

### Example
```python
INTENT_TAXONOMY = {
    # ... existing intents ...
    "FEATURE_IMPLEMENTATION": {
        "description": "Implementing a new feature or extending existing functionality.",
        "goal": "Deliver a working implementation that passes all tests and adheres to architecture.",
        "tool_chain": ["file_system", "shell", "pytest"],
        "risk_profile": "medium",
        "verification": "automatic"
    },
}
```

> [!IMPORTANT]
> The `IntentClassifier` utilizes an LLM with a decision-tree prompt. If you add a complex intent that overlaps with existing ones, you may need to update the prompt template in `intent_classifier.py` to ensure the LLM can accurately distinguish between them.

---

## 2. Creating Slash-Commands & Workflows

Slash-commands provide a shortcut to trigger complex, multi-step workflows. These are managed by the `CommandManager` and referenced within the `ControlPlane`.

### Location
`packages/core/src/command_manager.py`

### Workflow Syntax
Workflows are defined using Markdown-based logic. They utilize two primary operational patterns to coordinate the system:

#### A. Agent Spawning
To delegate a specific step to a specialized persona, use the spawning pattern:
`Spawn the [agent-id] agent`

#### B. Todo Operations
To programmatically manage the session's task list, use `TODO_OP`:
`TODO_OP: [list|add|done] [args]`

### Example: `/bugfix` Workflow
A typical bugfix workflow might look like this in the command configuration:

```markdown
# /bugfix Workflow
1. TODO_OP: add "Analyze bug report and reproduce"
2. Spawn the `debugger` agent to locate the root cause.
3. TODO_OP: add "Implement fix and verify"
4. Spawn the `logic-implementer` agent to apply the patch.
5. Spawn the `tester` agent to run regression tests.
6. TODO_OP: done "Analyze bug report and reproduce"
7. TODO_OP: done "Implement fix and verify"
```

---

## 3. Modifying Security & Tool Policies

The `PolicyEngine` ensures that agents operate within safe boundaries, preventing unauthorized file access or dangerous command execution.

### Location
`packages/core/src/policy_engine.py`

### The Agent-Tool Map
The `agent_tool_map` dictionary defines which roles have access to which tools. To grant a new agent access to a tool, update this map.

```python
agent_tool_map = {
    "logic-implementer": ["edit", "read_file", "run-pytest"],
    "knowledge-sync": ["read_file", "write_file"],
    "debugger": ["read_file", "run-shell", "inspect-stack"],
}
```

### Intent Boundaries
The `get_permissions` method restricts access based on the current classified intent. This prevents "privilege escalation" where an agent might try to edit core system files during a simple documentation task.

- **`allowed_paths`**: A list of directories the agent can access.
- **`can_write`**: A boolean indicating if the agent is permitted to modify files.

**Example Logic:**
If the intent is `Knowledge Sync`, the `PolicyEngine` will restrict `allowed_paths` to the `docs/` directory and set `can_write` to `True` only for `.md` files.

---

## Summary Checklist for Extensions

| Task | File to Modify | Key Component |
| :--- | :--- | :--- |
| Add New Intent | `intent_classifier.py` | `INTENT_TAXONOMY` |
| Create Command | `command_manager.py` | Workflow Markdown |
| Grant Tool Access | `policy_engine.py` | `agent_tool_map` |
| Restrict Access | `policy_engine.py` | `get_permissions()` |
