#  System Alignment Findings: qwen_code_stack vs labs/qwen-code

This document tracks the gaps and misalignments discovered during the audit of the base repository (`labs/qwen-code`) and the current implementation (`qwen_code_stack`).

## 1. Memory System Alignment
**Status**:  **Partial Misalignment (Intelligence Gap)**

| Feature | Base Repo (`labs/qwen-code`) | Our Project (`qwen_code_stack`) | Gap / Risk |
| :--- | :--- | :--- | :--- |
| **Storage** | File-based / Index files | Dual-Tier Qdrant (Local/Cloud) |  Upgrade (Better) |
| **Retrieval** | Keyword/Model-driven scan | Vector Similarity Search |  Upgrade (Better) |
| **Extraction** | **Agentic**: LLM analyzes chat to extract facts | **Atomic**: Simple ingest of provided text |  **Loss of Intelligence**. We lack the cognitive layer that decides *what* is worth remembering. |
| **Dreaming** | **Agentic**: LLM synthesizes & consolidates | **Systemic**: Basic hash-based deduplication |  **Loss of Intelligence**. We lack the synthesis capability for complex memory consolidation. |

### Interface Compatibility Analysis
The base orchestrator (`client.ts`) expects a `MemoryManager` with `recall`, `scheduleExtract`, and `scheduleDream` methods.
- **`recall`**:  Compatible. Our MCP server provides the necessary data for the orchestrator to build its prompts.
- **`scheduleExtract`**:  Functional Gap. The base repo expects autonomous extraction; we only provide atomic ingestion.
- **`scheduleDream`**:  Functional Gap. The base repo expects cognitive synthesis; we only provide hash-based deduplication.

**Recommendation**: Retain the base repo's Agentic Memory Planners but route their output through our `mega-memory-manager` MCP server to use Qdrant.


---

## 2. Skills & Services Alignment
**Status**:  **Critical Misalignment (Algorithm Loss)**

**Finding**: We have replaced the base repo's **Algorithmic Skills** with **Persona-based Services**.

- **Base Repo Approach**: Skills (like `review`) are defined as precise, multi-step algorithms (e.g., "Step 1: Scope $\rightarrow$ Step 2: Rules $\rightarrow$ Step 3: Deterministic Audit $\rightarrow$ Step 4: Parallel Agents").
- **Our Approach**: Skills are defined as high-level personas (e.g., "You are an Adversarial Auditor").

**Risk**: By removing the explicit algorithm, we are re-introducing "ego agent" behavior where the LLM improvises the process. This leads to inconsistent results and the omission of critical steps (like running deterministic linters before the LLM review).

**Recommendation**: The `SKILL.md` files in our `config/skills/` directory must be updated to include the precise operational algorithms from the base repo's `bundled/` skills.

---

## 3. Orchestration Alignment
**Status**:  **Aligned (Architectural Upgrade)**

Our "Control Plane" (Intent $\rightarrow$ Policy $\rightarrow$ Decomposition) is a superior architectural wrapper around the base repo's execution model. As long as the "Decomposition" layer produces tasks that follow the base repo's algorithms, this is a significant upgrade.

---

## Summary of Action Items
1. [ ] **Restore Agentic Memory Logic**: Integrate `extractionAgentPlanner` and `dreamAgentPlanner` from base repo into the `mega-memory-manager` workflow.
2. [ ] **Algorithm Restoration**: Copy the detailed operational steps from `labs/qwen-code/packages/core/src/skills/bundled/*/SKILL.md` into our `config/skills/*/SKILL.md`.
3. [ ] **Interface Verification**: Ensure the `mega-memory-manager` MCP toolset fully supports the requirements of the base repo's memory agents.
