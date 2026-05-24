# Mega Code Architectural Blueprint Specification

## 1. Executive Vision
**Mega Code** transforms LLM-based coding from a linear "chat" interaction into a structured, deterministic system. By separating intent, routing, execution, and interaction into distinct planes, the AI-OS ensures architectural scalability, provider-agnosticism, and strict privacy controls.

## 2. The 4-Layer Model

### 2.1 Control Plane (`qwen_code_stack`)
The Control Plane serves as the **"Central Nervous System"**. It governs the high-level logic and orchestration.
- **Intent Routing**: Translates ambiguous user requests into concrete, actionable goals.
- **Deterministic Policy Engine**: Applies hard constraints (e.g., *"Never modify `.env` files"*, *"Always run tests before committing"*).
- **Memory Management**: Handles long-term and short-term context, RAG orchestration, and state persistence.
- **Task Decomposition**: Breaks down complex goals into a sequence of atomic tasks (Jobs).
- **Strategic Asset**: This is the unique intelligence layer of the stack. It should be developed as a standalone orchestrator that wraps the execution kernel.

### 2.2 Routing Plane (`OmniRoute`)
The Routing Plane acts as the **"Intelligence Gateway"**, decoupling the system from specific LLM providers.
- **Provider Abstraction**: A unified API layer that normalizes requests/responses across OpenAI, Anthropic, DeepSeek, and local models.
- **Fallback Chains**: Automatic redirection to alternative models if a primary provider fails or hits rate limits.
- **Cost/Latency Balancing**: Dynamic routing based on task complexity (e.g., formatting $\rightarrow$ fast/cheap model; refactoring $\rightarrow$ high-reasoning model).
- **Encrypted Secret Management**: Secure handling of API keys, ensuring credentials never enter the model prompt.

### 2.3 Execution Plane (`Qwen Code`)
The Execution Plane is the **"Operational Arm"**, where conceptual plans are turned into physical changes.
- **Subagent Orchestration**: Deploying specialized agents (e.g., Reviewer, Tester) for targeted tasks.
- **Tool Orchestration**: Managing the lifecycle of tool calls (shell execution, file I/O, grep).
- **Filesystem Operations**: Atomic modification of the codebase with built-in backup/rollback capabilities.
- **Verification Loop**: Running linters and tests to validate the output of the Execution Plane.

### 2.4 Interaction Plane (IDE/MCP/CLI)
The Interaction Plane is the **"Interface Layer"**, defining how users and external systems communicate with the AI-OS.
- **Real-time Editing**: Direct integration with IDEs for seamless code injection and diff views.
- **Tool Access**: Exposing AI-OS capabilities via Model Context Protocol (MCP) for external ecosystem integration.
- **CLI Interface**: A powerful command-line entry point for automation and headless operation.
- **Feedback Loop**: Capturing user corrections to refine the Control Plane's policy engine.

---

## 3. Decision Authority Matrix

| Plane | Primary Question | Authority | Key Output |
| :--- | :--- | :--- | :--- |
| **Control** | *What* needs to be done? | Policy & Intent | Task Graph / Job List |
| **Routing** | *Which* model is best? | Performance & Cost | Model Endpoint |
| **Execution** | *How* is it physically done?| Tooling & Logic | File Changes / Logs |
| **Interaction**| *How* is it experienced? | UX & Integration | UI/UX State |

---

## 4. Integration of Fork Capabilities

- **Engineer Runner $\rightarrow$ Control Plane**: The deterministic logic and "runner" patterns are integrated here to ensure rigorous, step-by-step execution of complex engineering tasks.
- **Provider Forks $\rightarrow$ Routing Plane**: Specialized provider implementations are housed here to enable deep optimization for specific APIs without affecting core logic.
- **IDE/MCP Forks $\rightarrow$ Interaction Plane**: Integration-specific forks (e.g., VS Code extensions) are treated as Interaction modules, allowing the AI-OS to be embedded in various environments.

---

## 5. Privacy-Preserving Architecture

### 5.1 Privacy as a Policy Layer
Privacy is a fundamental constraint managed by the Control Plane. All data flows are subjected to a **"Privacy Filter"** before leaving the local environment.

### 5.2 Local-First Requirements
- **Telemetry Stripping**: Automated removal of PII and internal paths from prompts sent to cloud providers.
- **Local Encrypted Credentials**: API keys are stored in a local encrypted vault, accessed only by the Routing Plane at the moment of request.
- **Sandboxed Execution**: The Execution Plane operates within restricted environments (Containers/VMs) to prevent unauthorized system access.

---

## 6. The Task Contract (Job Lifecycle)

A **Job** is the unit of work moving through the AI-OS.

### 6.1 Job Schema (Conceptual)
```json
{
  "job_id": "uuid-v4",
  "intent": "Refactor UserAuth module to use JWT",
  "context": {
    "files": ["src/auth.ts", "src/user.ts"],
    "memory_snapshot": "ref-123"
  },
  "policy": {
    "max_tokens": 4096,
    "require_tests": true,
    "privacy_level": "strict"
  },
  "route": {
    "suggested_model": "claude-3-5-sonnet",
    "fallback": "gpt-4o"
  },
  "state": "pending | routing | executing | verifying | completed | failed"
}
```

### 6.2 Movement Flow
1. **Control Plane**: Creates `Job` $\rightarrow$ Defines `Intent` and `Policy`.
2. **Routing Plane**: Receives `Job` $\rightarrow$ Assigns `Route` $\rightarrow$ Forwards to LLM.
3. **Execution Plane**: Receives LLM response $\rightarrow$ Executes tools $\rightarrow$ Updates `State`.
4. **Control Plane**: Validates result $\rightarrow$ Marks `Job` as `completed` or triggers retry.

---

## 7. Extension Strategy: Extend, Do Not Replace

To avoid **Divergence Debt** and maintenance burden, the AI-OS follows a strict "Extension" philosophy regarding the Execution Plane (Qwen Code):

- **Baseline**: Use the upstream mainline Qwen Code as the execution kernel.
- **Mechanism**: Extend functionality via:
  - **Patches**: Targeted changes to core behavior.
  - **Adapters**: Translation layers between the Control Plane and the Kernel.
  - **Wrappers**: Process managers (like `mega-memory-manager`) that orchestrate the kernel.
  - **Plugins**: Modular additions to the toolset.

**CRITICAL**: Do NOT fork the Qwen Code core. Treat it as an immutable binary that we wrap with our strategic intelligence.
