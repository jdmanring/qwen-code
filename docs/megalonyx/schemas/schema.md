# Skill Schema Definition

## Component Identity
The **Skill Schema** defines the structural requirements for any "Skill" (sub-agent) added to the Megalonyx. It ensures that all agentic capabilities are defined consistently, allowing the orchestrator to load and trigger them predictably.

## 🛠️ Implementation Status

**Status: Declarative**

The schema is currently used as a technical reference. Programmatic enforcement (i.e., automatic validation of `config/skills/*.yaml` files against this schema) is not yet implemented in the core engine.

## Technical Specification


### Required Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | Unique, lowercase identifier (e.g., `scout`). Used for internal routing. |
| `description` | `string` | Human-readable summary of the skill's purpose. |
| `type` | `string` | The architectural type. Currently, only `sub-agent` is supported. |
| `model` | `string` | The specific model ID or `inherit` to use the session's default model. |
| `tools` | `array[string]` | An explicit allow-list of tool names the skill can invoke. |
| `triggers` | `object` | The set of conditions that cause this skill to be activated. |

### Optional Trigger Fields
The `triggers` object can contain:
- `file_extensions`: List of extensions (e.g., `.py`, `.js`) that trigger the skill.
- `project_types`: Identifiers for specific project categories.
- `keywords`: User-prompt keywords that signal the need for this skill.

## Interdependencies
- **Orchestrator**: The orchestrator uses this schema to validate and load skill files from `config/skills/`.
- **Skill Implementations**: Every `.yaml` file in the skills directory must conform to this definition.

## Mirror Link
[Original Config: `config/schemas/schema.md`](../../config/schemas/schema.md)
