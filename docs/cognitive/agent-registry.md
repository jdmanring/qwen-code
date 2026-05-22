# 🎭 Agent Registry: Persona-as-Code

This document catalogs the specialized agent personas used by the Sovereign stack. Agent behaviors are decoupled from the execution engine and defined as "Persona-as-Code" via Markdown files.

## 📂 Persona Storage
All agent personas are stored as standalone Markdown files in the configuration directory:
`config/agents/*.md`

## 👥 Active Agent Catalog

| Agent | Persona File | Primary Responsibility | Key Constraints |
| :--- | :--- | :--- | :--- |
| **Architect** | `architect.md` | System design, decomposition, and blueprinting. | Must align with `QWEN.md` and `layer-manifest.md`. |
| **Developer** | `developer.md` | Implementation and atomic code generation. | Focus on verifiable, idiomatic changes. |
| **Reviewer** | `reviewer.md` | Quality auditing and correctness checking. | Must provide actionable, critical feedback. |
| **Security Auditor**| `security-auditor.md`| Vulnerability scanning and threat modeling. | Prioritize "Elite" security standards. |
| **Troubleshooter** | `troubleshooter.md`| Root-cause analysis and bug fixing. | Must reproduce the bug before implementing a fix. |
| **General Purpose** | `general.md` | Default fallback for non-specialized tasks. | Balanced reasoning and speed. |

---

## 💉 Persona Injection Process

The system injects these personas dynamically during the model call sequence in `packages/core/src/skill_bridge.py`:

1. **Assignment**: The `ControlPlane` assigns a specific agent/skill to the current job based on the `IntentClassifier`.
2. **Loading**: The system reads the corresponding `.md` file from the `config/agents/` directory.
3. **Payload Construction**: The content of the Markdown file is injected as the `system` message in the LLM request payload.
4. **Contextualization**: The persona is combined with the current `State Context` (Todo list, phase) to ensure the agent is aware of its current progress.

## 🛠️ Creating New Agents
To add a new agent to the registry:
1. Create a new `.md` file in `config/agents/`.
2. Define the **Identity**, **Goals**, and **Constraints** of the persona.
3. Update the `IntentClassifier` or `skill_bridge.py` to recognize the new agent.
