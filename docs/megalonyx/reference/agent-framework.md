# Agent Framework

This document defines the internal agent management system, the orchestration patterns, and the technical specifications for sub-agents within the Qwen Code stack.

## 1. Interaction Model: Manager-Worker

Qwen Code operates on a **Manager-Worker** architectural pattern, separating high-level orchestration from low-level execution to maximize reasoning quality and token efficiency.

### The Primary Agent (The Manager)
The Primary Agent is the direct interface for the user. It serves as the "brain" of the operation.
- **Role**: Orchestration, planning, and communication.
- **Responsibilities**: Maintaining conversation state, managing the todo list, and decomposing complex requests into actionable tasks.
- **Authority**: Hires specialized sub-agents via the `agent` tool for focused or autonomous execution.

#### Lean Toolset Policy
To prevent "tool confusion" and maximize efficiency, the Primary Agent is restricted to a minimal set of orchestration tools:
- **Permitted**: `agent`, `skill`, `todo_write`, `read_file`, `tool_search`.
- **Delegated**: Search (`grep`, `glob`), Modification (`edit`, `write_file`), Execution (`shell`), and Research (`tavily`, `web_fetch`).

### Sub-Agents (The Workers)
Sub-agents are transient, task-specific entities spawned by the Primary Agent.
- **Role**: Execution and specialized research.
- **Lifecycle**: Created for a specific goal $\rightarrow$ Autonomous execution $\rightarrow$ Termination upon delivery of the final report.

### Communication Loop
**User** $\rightarrow$ **Primary Agent** $\rightarrow$ **Sub-Agent** $\rightarrow$ **Primary Agent** $\rightarrow$ **User**

---

## 2. Core Components

### SubagentManager
The central orchestrator for the agent lifecycle, managing agents across three scopes:
- **User Scope**: Global agents in `~/.qwen/agents/`.
- **Project Scope**: Project-specific agents in `.qwen/agents/`.
- **Session Scope**: Transient agents for a single session.

### SubagentValidator
Ensures agent configurations adhere to the required schema and constraints to prevent runtime instantiation errors.

### BuiltinAgentRegistry
Maintains the collection of pre-defined, general-purpose agents provided by the CLI.

### Agent Communication Protocol (ACP) & SubAgentTracker
Provides observability into the agentic workflow, tracking:
- **Execution Flow**: Sequence of actions.
- **Tool Calls**: Arguments and invocations.
- **Messages**: Prompts and responses.

---

## 3. Operational Stability & Failure Handling

### The Resilience Layer (Self-Healing)
Implements stability measures within `skill_bridge.py` to mitigate external API instability:
1. **Exponential Backoff**: Jittered backoff to prevent "thundering herd" problems.
2. **Model Downshifting**: Automatic fallback chain (e.g., `Qwen3-480B` $\rightarrow$ `GPT-OSS-120B` $\rightarrow$ `Qwen2.5-7B`).
3. **Dynamic Timeouts**: Adjusted by model size (e.g., 300s for 480B vs 60s for 7B).

### The System Watchdog (Stagnation Detection)
Monitors for "Agentic Deadlocks" (Repetition, Confidence Plateaus, or Agent Ping-Pong). Upon detection, it injects a **Reflection Prompt**, forcing the agent to meta-analyze the failure and pivot strategy.

### The Report Validator (Schema Enforcement)
Checks sub-agent responses against a mandatory schema. Missing sections trigger a **Correction Turn** for regeneration.

### The Read-Before-Edit Guard
A hard constraint in `skill_bridge.py` that rejects `edit` calls if the target file has not been accessed via `read_file` in the current session.

### The Anti-Loop Protocol

The system implements a two-layered defense against repetition:

1.  **Strategic Anti-Looping (Livelock Detection)**:
    Detected "model repetition collapse" (where the agent repeats the same high-level action or response across turns) triggers an immediate halt, root-cause analysis, and institutionalization of a new rule in `QWEN.md` to prevent recurrence. This is managed by the `SystemWatchdog`.

2.  **Stream Anti-Looping (Token Degeneration)**:
    Token-level repetition within a single response (common in Gemma 4 models) is mitigated via `repetition_penalty` sampling and real-time stream interception.

For detailed technical specifications and model-specific mitigation parameters, refer to the **[Model Stability Guide](model-stability.md)**.

---

## 4. Agent Configuration & Management

### SubagentConfig
Agents are defined by configurations stored as Markdown files with YAML frontmatter.

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | Unique identifier for the agent. |
| `description` | `string` | When and how to use this agent. |
| `systemPrompt` | `string` | Core instructions and persona. |
| `tools` | `string[]` | Allowlist of permitted tools. |
| `disallowedTools` | `string[]` | Blocklist of forbidden tools (overrides allowlist). |
| `approvalMode` | `string` | `default`, `plan`, `auto-edit`, or `yolo`. |
| `model` | `string` | Model ID or `inherit`. |
| `runConfig` | `object` | Runtime limits (`max_time_minutes`, `max_turns`). |
| `color` | `string` | UI display color. |
| `background` | `boolean` | Whether it always runs as a background task. |

### Storage Levels & Priority
If names conflict, the higher priority (top) wins.

| Level | Location | Priority | Persistence |
| :--- | :--- | :--- | :--- |
| **Session** | Memory | 1 (Highest) | Ephemeral |
| **Project** | `.qwen/agents/` | 2 | Persistent (Project) |
| **User** | `~/.qwen/agents/` | 3 | Persistent (Global) |
| **Extension** | Extension Folder | 4 | Persistent (Plugin) |
| **Built-in** | Hardcoded in CLI | 5 (Lowest) | Permanent |

---

## 5. The Professional Role Pipeline

The system implements a multi-role pipeline to ensure production-grade quality.

**Workflow**: Architect (Plan) $\rightarrow$ Researcher (Knowledge) $\rightarrow$ Developer (Implement) $\rightarrow$ Reviewer (Audit) $\rightarrow$ QA Lead (Certify).

| Role | Tier | Primary Goal | Key Tools | Key Contribution |
| :--- | :--- | :--- | :--- | :--- |
| **Scout** | 2 | Navigation | `glob`, `grep`, `github_search` | Project map and file discovery. |
| **Researcher** | 2 | Knowledge | `tavily_search`, `web_fetch` | External API specs and briefs. |
| **Developer** | 2 | Implementation | `edit`, `read_file`, `shell` | Code implementation based on plan. |
| **Architect** | 3 | Strategy | `read_file`, `shell`, `glob` | Technical design and constraints. |
| **Reviewer** | 3 | Adversarial QA | `read_file`, `grep`, `shell` | Bug and security hole identification. |
| **QA Lead** | 3 | Certification | `read_file`, `grep`, `shell` | Test coverage and final sign-off. |
| **Doc Expert** | 2 | Documentation | `read_file`, `edit`, `glob` | Accuracy and structure of docs. |
| **Security Auditor**| 3 | Hardening | `read_file`, `grep`, `shell` | Vulnerability identification. |
| **System Optimizer** | 3 | Meta-Analysis | `read_file`, `edit`, `shell` | Behavioral guidelines updates. |

### 5.1 Delegation Constraints
To ensure reproducibility and auditability, specific high-impact actions are restricted to specialized agents. The Primary Agent **never** performs these actions directly.

| Action                        | Allowed tool | Agent that must perform it |
|-----------------------------------|---|-----------------------------------|
| File edits (`edit`, `write_file`) | – | **Developer**                     |
| Symbol / code search              | – | **Scout**                         |
| High‑level design or architecture | – | **Architect**                     |
| Documentation generation          | – | **Doc‑Expert**                    |
| Security review                   | – | **Security‑Auditor**              |

---

## 6. Model Management & Tiered Intelligence

### LiteLLM Bridge
Uses `.qwen/skills/skill_bridge.py` to route tasks to any provider (OpenRouter, Groq, Gemini, vLLM) via a standardized OpenAI interface.

### Model Selection Matrix (Recommended)

| Role | Tier | Recommended Model | Reasoning |
| :--- | :--- | :--- | :--- |
| **User-Facing (Primary)** | Orchestrator | `gemma-4-31b-it` | Superior instruction following. |
| **High Reasoning** | Tier 3 | `qwen3-coder-480b` | Peak intelligence for auditing/planning. |
| **Implementation** | Tier 2 | `codestral-latest` | Specialized for idiomatic code. |
| **Fast/Light Tasks** | Tier 1 | `qwen3-32b` | Optimal speed/intelligence ratio. |

---

## 7. The Zero-Waste Workflow

All agents must adhere to these constraints to prevent looping and token waste:

1. **The 3-Strike Rule**: Stop and report failure if the same tool is called 3 times without a tangible change in state.
2. **Implementation-First Bias**: Prioritize the "smallest correct change" over "perfect understanding."
3. **Tool-to-Todo Mapping**: Every tool call must correspond to an active `todo` item.
4. **No Verification Loops**: Verify a fix once. If it fails, change the approach; do not repeat the same test.

---

## 8. RAG & Knowledge Retrieval Specification

### Core Invariants
RAG correctness is defined by the alignment of: **Embedding Model $\rightarrow$ Vector Dimension $\rightarrow$ Qdrant Collection $\rightarrow$ Routing Policy**.

| System | Embedding Model | Dim | Purpose |
| :--- | :--- | :--- | :--- |
| **Local RAG** | `all-MiniLM-L6-v2` | 384 | Codebase, structural, procedural memory. |
| **Remote RAG** | `gemini-embedding-2` | 3072 | External docs, API knowledge, long-term memory. |

### Hard Rules
1. Local and cloud embeddings are **NEVER** interchangeable.
2. Each Qdrant MCP owns exactly one embedding space.
3. Query embedding MUST match target MCP embedding model.

### Scout Authority Model
**Scout is the ONLY agent allowed to:**
- Decide whether a query goes to local or remote RAG.
- Translate semantic queries into retrieval requests.
- Resolve ambiguity in retrieval targets.

All other agents MUST NOT construct embedding queries directly or decide RAG routing.
