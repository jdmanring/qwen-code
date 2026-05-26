# 🗺️ Integration Roadmap: Transition to Monorepo

This document is the **Technical Specification** and **Migration Plan** for moving the `qwen_code_stack` (Blueprint) into the `megacode-monorepo` (Monorepo). 

The goal is to transition from a fragmented prototype to a unified, professional engineering stack where the architecture is self-documenting.

---

## 🎯 Target Architecture: The Monorepo

The destination is the `megacode-monorepo` monorepo. All components will be refactored into the following intuitive structure:

### 1. Monorepo Structure
- **`apps/`**: User-facing interfaces and orchestration.
    - `apps/qwen-orchestrator`: The primary system entry point.
- **`packages/`**: Modular logic and shared assets.
    - `packages/core`: The central engine (LLM clients, tool scheduling, memory bridge).
    - `packages/cli`: The terminal interface.
    - `packages/webui`: The browser interface.
    - `packages/sdk-typescript`: The programmatic API.

### 2. Core Interface & Tooling
- **MCP-First**: All external capabilities are integrated via the **Model Context Protocol (MCP)**.
- **Unified Tool Registry**: A single source of truth for all available tools, ensuring consistent discovery.
- **Deterministic Execution**: Root-relative paths and `Result` patterns for all external calls to eliminate ambiguity.

### 3. Engineering Standards
Any code moving into the monorepo must meet these clarity and quality requirements:
- **Type Safety**: Mandatory PEP 484 (Python) and `noImplicitAny` (TypeScript).
- **No Magic Strings**: All logic-critical strings must live in designated constants or settings files.
- **Symmetry**: Any change to a configuration file in `config/` must be mirrored in the corresponding `docs/` file.

---

## 🧠 Logic Port Specification

The core value of the `qwen_code_stack` is its verified execution loop. This will be ported to `packages/core` in TypeScript.

### 1. The Verified Execution Loop
The `GeminiClient` in `packages/core` will implement the **Act $\to$ Observe $\to$ Verify $\to$ Correct** cycle.

- **Intent Classifier**: Maps user prompts to specific system intents.
- **Task Decomposer**: Breaks intents into a sequence of verifiable **Jobs**.
- **Job State Manager**: Tracks the lifecycle of each job:
    - `PENDING` $\to$ `RUNNING` $\to$ `VERIFYING` $\to$ `COMPLETED` | `FAILED`.
- **Verification Engine**: Evaluates job output against a **Mutation Contract** (e.g., verifying a file edit actually occurred as intended).
- **Correction Service**: Triggers a `RETRY`, `PIVOT`, or `ABORT` based on verification results.

### 2. Agent & Skill Injection
- **Persona Loader**: Reads `.md` blueprints from `config/agents/` and injects them as system prompts.
- **Skill Orchestrator**: Maps `config/skills/*.md` definitions to specific tool-chains in the `ToolRegistry`.

---

## 💾 Memory Bridge Specification

The memory system will be unified into a single `MemoryBridge` in `packages/core/src/memory/`.

### 1. The Memory Hierarchy
The bridge manages a tiered memory system:
1. **Instructional**: Static laws and blueprints (`QWEN.md`).
2. **Semantic (Global)**: Cross-project knowledge in a vector store.
3. **Semantic (Local)**: Project-specific anchors and facts.
4. **Ephemeral**: Short-term session history.

### 2. The Sync Protocol
- **Ingestion**: Background process that extracts facts from code and injects them into the semantic store.
- **Recall**: A `RAGTool` that performs semantic search to inject relevant anchors into the prompt.
- **Eviction**: Protocol to move session data from ephemeral to semantic storage.

---

## 🛠️ Component Mapping & Migration Path

| Legacy Component (`qwen_code_stack`) | Target Destination (`megacode-runtime-stack`) | Migration Action |
| :--- | :--- | :--- |
| `skill_bridge.py` & Orchestration | `packages/core/src/core/` | Implement the Verified Execution Loop in TypeScript. |
| CLI implementation | `packages/cli/` | Port to monorepo CLI structure; unify command handlers. |
| Agent Personas (`docs/agents/`) | `config/agents/*.md` | Convert to persona blueprints. |
| Skill Definitions (`docs/skills/`) | `config/skills/*.md` | Convert to SKILL.md templates. |
| Tool Logic (Various) | `packages/core/src/tools/` | Implement as atomic tools or MCP servers. |
| Memory/RAG Logic | `packages/core/src/memory/` | Implement the Memory Bridge. |
| Testing Suites | `integration-tests/` & `tests/` | Port to Vitest and the `terminal-capture` TUI suite. |

---

## 🚀 Execution Plan: The Migration

### Phase 1: Monorepo Scaffolding
1. Initialize `apps/qwen-orchestrator` and `packages/core`.
2. Deploy engineering standards as the primary linting gate.
3. Setup the `McpClient` and `ToolRegistry` in `packages/core`.

### Phase 2: Logic Porting
1. **Logic Extraction**: Extract domain logic from `qwen_code_stack` and strip all metaphors.
2. **Type Hardening**: Apply strict typing to all ported functions.
3. **Path Normalization**: Convert all paths to root-relative workspace paths.
4. **Implementation**: Deploy the logic into `packages/core`.

### Phase 3: Tool & Interface Integration
1. **MCP Bridge**: Wrap legacy tools as MCP servers or native `core` tools.
2. **CLI Migration**: Port the `qc` command suite to `packages/cli`.
3. **TUI Integration**: Implement the status line and interaction patterns in the new CLI.

### Phase 4: Full-Stack Verification
1. **Unit Testing**: Ensure 100% coverage of ported core logic.
2. **Integration Testing**: Run the `terminal-capture` suite to verify the user experience.
3. **Fidelity Audit**: Run routing and recall tests against live providers.

---

## 🏁 User Experience Completion

The migration is complete when the user can:
1. Launch the system via `packages/cli`.
2. Execute complex tasks using the agent orchestration.
3. See real-time status updates via the TUI.
4. Extend the system by adding a new MCP server or `config/skills/` definition without modifying the core engine.
5. Verify that all actions are deterministic and compliant with the project's engineering standards.
