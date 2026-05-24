# ✍️ Authoring and Extending Templates

This guide provides instructions for developers on how to author, extend, and integrate new templates into the Megalonyx. Templates are the fundamental building blocks used to maintain consistency across agent personas, command workflows, and skill definitions.

---

## 🧩 Template Taxonomy

The stack utilizes several distinct types of templates, each serving a specific purpose within the Cognitive-Symmetry Framework.

| Template Type | Primary Location | Purpose |
| :--- | :--- | :--- |
| **Agent Personas** | `config/agents/` | Defines the identity, mandates, and capabilities of a specialized agent. |
| **Command Workflows** | `config/commands/` | Defines multi-step, Markdown-based slash-commands for the orchestrator. |
| **Skill Definitions** | `config/skills/` | Defines the tool schemas and execution logic for specialized skills. |
| **System Templates** | `config/templates/` | Provides standardized structures for prompt engineering and documentation. |

---

## 🛠️ Authoring Workflow

To ensure all new templates are properly integrated and maintain system symmetry, follow this standardized workflow.

### 1. Discovery & Analysis
Before creating a new template, analyze the existing patterns in the target directory.
* **Identify the Schema**: Examine existing files in the directory (e.g., `config/agents/`) to understand the required structure and metadata.
* **Check for Overlap**: Ensure your new template does not duplicate existing functionality or intents.

### 2. Implementation
Create your template file following the established patterns.

* **For Agent Personas**: Ensure you include the core identity, operational laws (mandates), and capability definitions.
* **For Command Workflows**: Use structured Markdown with clear, step-by-step instructions that the orchestrator can parse.
* **For Skill Definitions**: Strictly adhere to the JSON schema defined in the corresponding `config/skills/` directory.

### 3. Symmetry Verification (Mandatory)
Every new template added to the `config/` directory **MUST** have a corresponding documentation file in the `docs/` directory.

* **The Rule**: `config/{path}/{file}.{ext}` $\leftrightarrow$ `docs/{path}/{file}.md`
* **Example**: If you add `config/agents/security_auditor.md`, you must also create `docs/agents/security_auditor.md`.
* **Verification**: Run `scripts/symmetry-check.py` to confirm that no symmetry gaps were introduced.

### 4. Deployment
Templates are not active on the Machine until they are deployed.
1.  Commit your changes to the **Blueprint** (the repository).
2.  Run the installation script to materialize the new template on the Machine:
    ```bash
    ./install.sh
    ```

---

## 💡 Best Practices

* **Maintain High Density**: Use ASCII logic (e.g., `=>`, `<=>`, `AND`/`OR`) and specific emojis (🏛️, 🧠, ⚙️) to optimize token usage and provide visual anchors.
* **Avoid Absolute Paths**: Always use relative paths or placeholders (e.g., `${STACK_ROOT}`) within your templates to ensure they are location-agnostic.
* **Strict Markdown**: Use consistent Markdown formatting (headers, lists, tables) to ensure the templates are easily readable by both humans and LLMs.
* **Atomic Design**: Keep templates focused and modular. Instead of one massive template, create several small, specialized ones that can be composed.

---
**VERSION**: `v1.0.0` | **Status**: `Stable` | **Last Updated**: `May 21, 2026`
