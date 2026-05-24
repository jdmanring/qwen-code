# Lean Snapshot Schema (MQA-Snapshot)

To maximize token efficiency and minimize "context drift," the Qwen Code stack uses a high-density Markdown-based snapshot for the agent's state. This replaces the previous, heavy XML-based `<state_snapshot>` block.

## Schema Definition

The snapshot is injected into the `system_prompt` at the end of the prompt (Recency-Bias) using the following structure:

```md
# STATE
- **Phase**: [ACTIVE_PHASE]
- **Todos**:
[TODO_LIST_ITEMS]
```

### Field Specifications

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **Phase** | `string` | The current operational phase (e.g., `PLANNING`, `IMPLEMENTATION`). | `- **Phase**: IMPLEMENTATION` |
| **Todos** | `list[string]` | A list of current, uncompleted tasks from the project todo list. | `- [in_progress] Implement the API` |

## Implementation Details

### Injection Point
The snapshot is appended to the `sys_prompt` within `packages/core/core/skill_bridge.py` during the dynamic prompt resolution phase.

### Token Efficiency
By using Markdown headers and bullet points instead of XML tags, we achieve a ~60% reduction in the token overhead of the state context.

### Evolution: Knowledge Eviction
As the session progresses, the `KNOW` (Knowledge) section will be managed via an **Eviction Policy**:
1. **Active Knowledge**: High-relevance facts currently required for the `current_plan`.
2. **Archived Knowledge**: Facts that have been verified and are no longer needed for immediate reasoning. These are moved to the Semantic Memory (Qdrant) and removed from the prompt snapshot to maintain a lean context window.
