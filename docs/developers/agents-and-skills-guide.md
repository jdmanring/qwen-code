# Agent & Skill Developer Guide: Qwen Code Agentic System

This document serves as the technical blueprint for extending the capabilities of the Qwen Code agentic system. It defines the specifications for creating atomic Skills, specialized SubAgents, and the routing logic provided by Execution Profiles.

---

## 1. Introduction: The Agentic Hierarchy

The Qwen Code system operates on a three-tier hierarchy designed to separate **capability**, **persona**, and **routing**.

1.  **Skills (`.qwen/skills/`)**: The smallest unit of capability. A skill defines *how* to perform a specific technical task and *when* it is applicable.
2.  **SubAgents (`.qwen/agents/`)**: Specialized personas. SubAgents provide isolated execution contexts with specific system prompts, tool restrictions, and approval modes.
3.  **Execution Profiles (`.qwen/agents/`)**: The routing layer. Profiles map incoming tasks (based on file patterns or keywords) to a set of required skills and a target model.

**Logic Flow:**  
`User Task` $\to$ `Execution Profile (Routing)` $\to$ `Skill Selection (Capability)` $\to$ `SubAgent (Execution Context)`

---

## 2. Skill Development

### Purpose
Skills encapsulate a specific operational procedure. Instead of relying on a general-purpose prompt, a Skill provides the LLM with a deterministic set of instructions, constraints, and tool-access rules for a narrow domain.

### Directory Structure
Each skill must reside in its own directory within the skills folder:
`.qwen/skills/<skill-name>/SKILL.md`

### Schema Specification

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | Yes | Unique identifier for the skill. |
| `description` | String | Yes | High-level summary of what the skill achieves. |
| `when_to_use` | String | Yes | Precise conditions/triggers for activating this skill. |
| `paths` | List | No | Globs/Paths where this skill is active (Conditional Activation). |
| `disable-model-invocation` | Boolean | No | If `true`, the skill is executed as a deterministic script/pipeline. |
| `model` | String | No | Override the default model for this specific skill. |
| `priority` | Integer | No | Execution order (lower number = higher priority). |
| `argument-hint` | String | No | Guidance for the LLM on how to format arguments for this skill. |
| `hooks` | List | No | Pre-execution or post-execution triggers. |
| `allowedTools` | List | No | Strict whitelist of tools available to this skill. |

### Concrete Example: `ts-refactor`
`.qwen/skills/ts-refactor/SKILL.md`

```markdown
---
name: typescript-refactor
description: Refactors TypeScript code for better type safety and readability.
when_to_use: "When the user requests refactoring, type-strengthening, or cleaning up .ts/.tsx files."
paths: ["src/**/*.ts", "src/**/*.tsx"]
disable-model-invocation: false
model: qwen-2.5-coder-32b
priority: 10
argument-hint: "Provide the file path and the specific architectural pattern to implement (e.g., 'Repository Pattern')."
allowedTools: ["read_file", "write_file", "run_shell"]
---

# TypeScript Refactor Protocol
1. Analyze existing types and identify `any` or `unknown` types.
2. Implement strict interfaces for all data structures.
3. Ensure all exported functions have explicit return types.
4. Run `npm run lint` to verify no regressions.
```

### Conditional Activation via `paths`
The `paths` attribute prevents "skill pollution." If a skill is defined for `src/**/*.ts`, it will not be loaded into the context when the user is working on `.md` or `.yml` files, reducing token noise and preventing the LLM from attempting irrelevant refactors.

---

## 3. SubAgent Development

### Purpose
SubAgents are used for **isolated sessions**. While a Skill is a "how-to," a SubAgent is a "who." They are used when a task requires a distinct persona (e.g., a Security Auditor) or a different safety profile (e.g., an agent that can run shell commands without approval).

### Directory Structure
SubAgents are defined as Markdown files in the agents directory:
`.qwen/agents/<agent-name>.md`

### Schema Specification

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | Yes | Unique identifier for the SubAgent. |
| `description` | String | Yes | The role the agent plays. |
| `tools` | List | Yes | Tools granted to this agent. |
| `disallowedTools` | List | No | Tools explicitly banned from this agent's context. |
| `approvalMode` | String | Yes | `Auto` (no prompt), `User` (manual approval), `YOLO` (all auto). |
| `model` | String | Yes | The LLM powering this SubAgent. |
| `runConfig` | Object | No | Runtime parameters (temperature, max_tokens, etc.). |
| `color` | String | No | UI Hex color for the agent's identity. |
| `background` | String | No | UI background style for the agent's chat bubble. |

### Concrete Example: `SecurityAuditor`
`.qwen/agents/security-auditor.md`

```markdown
---
name: security-auditor
description: Expert in OWASP and static analysis for vulnerability detection.
tools: ["read_file", "run_shell"]
disallowedTools: ["write_file"]
approvalMode: User
model: qwen-2.5-coder-32b
color: "#FF0000"
background: "#2D0000"
---

You are the Security Auditor. Your sole purpose is to find vulnerabilities. 
Do NOT suggest feature improvements. Focus exclusively on:
1. SQL Injection / XSS / CSRF.
2. Insecure dependency versions.
3. Hardcoded secrets.
Report findings in a structured table: [Severity | Location | Risk | Mitigation].
```

### Tool Registry & Approval Modes
SubAgents allow for **Privilege Escalation/Restriction**. A `SecurityAuditor` may be forbidden from using `write_file` to ensure it doesn't accidentally modify code while auditing, whereas a `DevOpsAgent` might have `approvalMode: Auto` for `run_shell` within a specific sandbox.

---

## 4. Execution Profiles

### Purpose
Execution Profiles act as the **Dispatcher**. They monitor the environment and the user's intent to decide which model and which set of skills should be activated for the current session.

### Directory Structure
Profiles are also located in the agents directory:
`.qwen/agents/<profile-name>.md`

### Schema Specification

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | Yes | Name of the profile. |
| `model` | String | Yes | Default model to use for tasks matching this profile. |
| `skills` | List | Yes | List of skill names to load into the context. |
| `triggers` | Object | Yes | Mapping of `file_patterns` and `task_keywords`. |

### Concrete Example: `Frontend-Profile`
`.qwen/agents/frontend-profile.md`

```markdown
---
name: frontend-dev-profile
model: qwen-2.5-coder-32b
skills: ["typescript-refactor", "css-optimizer", "react-component-generator"]
triggers:
  file_patterns: ["**/*.tsx", "**/*.jsx", "**/*.css", "**/*.scss"]
  task_keywords: ["ui", "frontend", "component", "style", "tailwind"]
---
```

### The Scoring Mechanism
When a task is initiated, the system calculates a match score for all profiles:
- **File Pattern Match**: If the current active file matches a `file_pattern`, the profile score increases.
- **Keyword Match**: If the user's prompt contains any `task_keywords`, the profile score increases.
- **Winner**: The profile with the highest score is selected, and its associated `skills` and `model` are injected into the orchestrator.

---

## 5. The Integrated Workflow

The lifecycle of a request follows this path:

1.  **Trigger**: User asks: *"Can you refactor the UserProfile component to use a custom hook?"*
2.  **Routing (Execution Profile)**: 
    - System detects `UserProfile.tsx` is open (matches `frontend-dev-profile` $\to$ `file_patterns`).
    - System detects keyword "refactor" (matches `frontend-dev-profile` $\to$ `task_keywords`).
    - **Result**: `frontend-dev-profile` is activated.
3.  **Capability Loading (Skills)**:
    - The system loads `typescript-refactor` because it is listed in the profile.
    - The `typescript-refactor` skill is further validated against the current path (`src/components/UserProfile.tsx` matches `src/**/*.ts`).
4.  **Contextual Execution (SubAgent)**:
    - If the task is high-risk, the orchestrator spawns a `SubAgent` with a restricted `approvalMode` and a specific `systemPrompt` to execute the refactor.

---

## 6. Verification Checklist

Developers must verify the following before committing new agents or skills:

- [ ] **YAML Validity**: Does the frontmatter parse correctly without syntax errors?
- [ ] **Path Precision**: Are `paths` globs specific enough to avoid loading the skill in irrelevant contexts?
- [ ] **Tool Alignment**: Does the `allowedTools` list in the Skill align with the `tools` list in the SubAgent?
- [ ] **Conflict Check**: Do multiple Execution Profiles have overlapping `task_keywords`? (If so, ensure `priority` is handled).
- [ ] **Symmetry**: Is the new capability documented in the project's `docs/` directory to mirror the `.qwen/` configuration?
