# 🛠️ The Skill System: Persona-Based Orchestration

This document describes the Skill System, a declarative orchestration layer that allows the Sovereign stack to dynamically switch between specialized agent behaviors based on the current task context.

## 🧩 Skill Definition & Registration

Skills are not hardcoded logic but are declarative configurations.

### 1. Definition Format
Skills are defined as **Markdown files with YAML frontmatter** (or standalone `.yaml` files) located in `config/skills/`.

**Skill Schema**:
- `name`: Unique identifier for the skill.
- `triggers`: A list of keywords, patterns, or file extensions that signal the skill's relevance.
- `capabilities`: Preferred tools, model overrides (e.g., forcing a specific "Fast" model), and reporting requirements.
- `persona`: The specific system prompt or persona reference that defines the agent's behavior while this skill is active.

### 2. Registration Process
The `SkillOrchestrator` (`packages/core/src/skill_selector.py`) handles the lifecycle of skills:
- **Loading**: Upon system boot, the orchestrator recursively scans the `config/skills/` directory.
- **Parsing**: YAML frontmatter is parsed and flattened into a global `skills` registry.
- **Activation**: The system evaluates the current context to select the most appropriate skill.

---

## 🚦 The Selection Logic (STRMAC Scoring)

The system uses a weighted scoring function to determine which skill should be active. This prevents "Persona Drift" and ensures the right expert is used for the right task.

### Scoring Weights
1. **Keyword Match (High Weight)**: If the user prompt contains keywords defined in the skill's `triggers`.
2. **File Extension (Moderate Weight)**: If the current active file matches the skill's domain (e.g., `.ts` $\to$ `typescript-expert`).
3. **Phase Alignment (Moderate Weight)**: Based on the current `active_phase` in the state manager:
    - `PLANNING` $\to$ Boosts `architect` skills.
    - `IMPLEMENTATION` $\to$ Boosts `developer` skills.
    - `VERIFICATION` $\to$ Boosts `reviewer` skills.
4. **Role Boosting (Contextual Weight)**: If the previous agent in the turn loop was not a reviewer and the system is in the `VERIFICATION` phase, the `reviewer` skill is automatically boosted.

---

## ⚖️ Skills vs. Tools: The Distinction

It is critical to distinguish between these two layers of the system:

| Feature | Skills (Personas) | Tools (Primitives) |
| :--- | :--- | :--- |
| **Nature** | Declarative / Behavioral | Imperative / Functional |
| **Purpose** | Defines *Who* is acting and *How* they think. | Defines *What* action is being performed. |
| **Configuration** | Defined in `config/skills/*.md`. | Defined in `packages/core/src/skill_bridge.py`. |
| **Scope** | High-level (e.g., "Security Auditor"). | Atomic (e.g., `read_file`). |
| **Relationship** | A Skill specifies which Tools are preferred. | A Tool is invoked by the agent acting under a Skill. |

---

## 🛠️ Skill Creation Workflow

To add a new capability to the Sovereign stack:
1. **Define the Trigger**: Identify the keywords or file types that should activate the skill.
2. **Create the File**: Add a new `.md` file to `config/skills/` with the required YAML frontmatter.
3. **Define the Persona**: Link the skill to an existing persona in `config/agents/` or provide a specialized system prompt.
4. **Test the Activation**: Use a prompt containing the triggers to verify the `SkillOrchestrator` selects the new skill.
