# Creating New Skills

Skills are high-level workflow macros that extend the capabilities of the Mega Code orchestrator. They transform basic tool use into repeatable, professional engineering patterns.

## 1. The Skill Entity Standard

To ensure AI-optimality and token efficiency, the system uses a **Folder-per-Entity** layout. Every skill must reside in its own directory within `config/skills/`.

### Skill Structure
```text
config/skills/<skill-name>/
├── <skill-name>.yaml   (Tool schema & trigger definitions)
└── SKILL.md            (Detailed workflow & implementation guide)
```

---

## 2. Step-by-Step Guide to Creating a Skill

### Step 1: Create the Skill Directory
Create a folder named after your skill in the `config/skills/` directory.
```bash
mkdir -p config/skills/code-auditor
```

### Step 2: Define the `{skill}.yaml` Manifest
The YAML file defines how the orchestrator recognizes and invokes the skill.

#### Example `code-auditor.yaml`
```yaml
name: code-auditor
description: Performs a professional security and quality audit of a specific module.
triggers:
  keywords:
    - audit
    - security check
    - "review for bugs"
capabilities:
  tools:
    - read_file
    - grep_search
    - web_fetch
  model: "gpt-4o" # Or "inherit" to use the current active model
workflow_reference: "SKILL.md"
```

### Step 3: Create the `SKILL.md` Documentation
The `SKILL.md` file is the "Cognitive Blueprint" for the agent. It defines the exact steps the agent must take to execute the skill successfully.

#### Example `SKILL.md`
```markdown
# Code Auditor Workflow

## Objective
To identify security vulnerabilities and logic errors in a target module.

## Execution Protocol
1. **Scope Discovery**: Use `grep_search` to find all entry points and data-flow boundaries.
2. **Pattern Analysis**: Cross-reference found patterns with known CVEs using `web_fetch`.
3. **Deep Dive**: Read critical files to verify if the vulnerability is exploitable.
4. **Reporting**: Document findings in a structured report with:
   - Location (File/Line)
   - Risk Level (Critical/High/Med/Low)
   - Remediation Suggestion.

## Guardrails
- NEVER suggest a fix without first proving the vulnerability exists.
- ALWAYS verify that the suggested fix does not introduce new regressions.
```

---

## 3. Deployment & Activation

Once the skill is defined in the Blueprint:

1. **Deploy**: Run the installer to mirror the skill to the Machine:
   ```bash
   ./install.sh
   ```
2. **Invoke**: The orchestrator will now automatically trigger this skill when the user's prompt matches the `triggers` defined in the YAML.

## 4. Best Practices for Skill Design

- **Atomicity**: A skill should do one thing exceptionally well. If a skill is becoming too complex, break it into two specialized skills.
- **Verification**: Always include a "Verification" step in the `SKILL.md` to ensure the outcome is deterministic.
- **Tool-Chaining**: Define a clear sequence of tools (e.g., `Glob` $\rightarrow$ `Grep` $\rightarrow$ `ReadFile`) to minimize token waste.
