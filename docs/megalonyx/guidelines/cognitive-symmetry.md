#  Cognitive-Symmetry Framework (CSF)

The Cognitive-Symmetry Framework (CSF) is the architectural foundation for the transition from "AI-Friendly" software engineering to "AI-Native" orchestration. It establishes a deterministic, bi-directional relationship between the system's configuration, its documentation, and its execution logic.

## 1. Executive Summary

### The Shift: AI-Friendly $\rightarrow$ AI-Native
Traditional "AI-Friendly" systems provide documentation that an AI *can* read. An "AI-Native" system is designed so that the AI *cannot fail* to understand it because the structure of the system is the documentation.

### Structural Determinism
The core goal of CSF is **Structural Determinism**: the principle that any piece of logic, configuration, or intent must have a mathematically predictable location and representation within the codebase. If an agent knows *what* it is looking for, the framework ensures it knows *exactly where* it is and *how* it is structured, eliminating probabilistic search and reducing context window waste.

---

## 2. The 4 Pillars of Symmetry

###  Pillar I: Contextual Anchors `[S-ANCHOR]`
Contextual Anchors prevent "context drift" and hallucination by providing immutable points of reference.

*   **The `.qwen-context` Standard**: Every modular component must contain a `.qwen-context` file (or section) defining its local axioms--the "ground truths" that never change for that specific module.
*   **Axiom Hierarchy**:
    1.  **Global Axioms** (`QWEN.md`): The supreme operational law.
    2.  **Domain Axioms** (`docs/guidelines/`): The rules for specific categories of work.
    3.  **Local Axioms** (`.qwen-context`): The constraints for a specific file or package.
*   **Agent Usage**: Agents MUST resolve conflicts by ascending the hierarchy. If a local axiom contradicts a global axiom, the global axiom prevails.

###  Pillar II: Symmetric Mirroring `[S-MIRROR]`
Symmetric Mirroring ensures that the "Map" (Documentation) and the "Territory" (Code/Config) are identical in structure.

*   **1:1 Mapping**: Every directory and file in `config/` must have a corresponding mirror in `docs/`.
    *   `config/agents/developer.json` $\leftrightarrow$ `docs/agents/developer.md`
    *   `config/skills/refactor-safe.json` $\leftrightarrow$ `docs/skills/refactor-safe.md`
*   **Analogy Navigation**: When an agent encounters a bug in a config file, it is mandated to check the mirrored documentation to understand the *intent* before attempting a fix. This prevents "blind patching" where the agent fixes the symptom but breaks the architectural intent.

###  Pillar III: Machine-Readable Contracts `[S-CONTRACT]`
To move beyond probabilistic markdown, CSF implements strict output contracts.

*   **JSON Schema Migration**: While humans read Markdown, agents verify via JSON Schema. All complex output contracts are defined as schemas.
*   **The Execution Flow**:
    `Executor (Produces Output)` $\rightarrow$ `Verifier (Validates against Schema)` $\rightarrow$ `Schema (The Ground Truth)`
*   **Determinism**: If the output does not validate against the schema, it is treated as a system failure, not a "slight hallucination," triggering an immediate `[S-CORRECT]` loop.

###  Pillar IV: Meta-Audit Loops `[S-AUDIT]`
The Meta-Audit loop is the "immune system" of the framework, ensuring the agent doesn't deviate from the operational law.

*   **The Judge Agent Pattern**: A specialized, read-only agent that does not perform tasks but audits the execution traces of other agents.
*   **Audit Criteria**: The Judge compares the `Tool Call` $\rightarrow$ `Result` sequence against the mandates in `QWEN.md`.
*   **Feedback Loop**: If a violation is found (e.g., an agent used `write_file` instead of `edit`), the Judge injects a "Correction Directive" into the prompt, forcing the agent to undo the action and follow the protocol.

---

## 3. The Information Pipeline

The flow of truth in the Mega Code stack is unidirectional and hierarchical, ensuring that tactical execution is always aligned with strategic intent.

| Level | Document | Purpose | Frequency of Change |
| :--- | :--- | :--- | :--- |
| **Strategic** | `master-plan.md` | High-level architectural goals & milestones. | Monthly/Quarterly |
| **Tactical** | `todo.md` | The authoritative roadmap of pending tasks. | Daily |
| **Operational** | `Session Tracker` | Real-time progress of the current session. | Per-Turn |
| **Execution** | `Agent Prompt` | The immediate instruction set for a tool call. | Immediate |

**The Truth Chain**: `MASTER_PLAN` $\rightarrow$ `TODO` $\rightarrow$ `Session Tracker` $\rightarrow$ `Agent Prompt`.

---

## 4. Implementation Roadmap

The rollout of CSF occurs in three phased waves:

1.  **Wave 1: Structural Alignment (Symmetry)**
    - Audit `config/` and `docs/` to ensure 1:1 mirroring.
    - Implement `.qwen-context` anchors in core packages.
2.  **Wave 2: Contractual Hardening (Schemas)**
    - Convert Markdown output contracts to JSON Schemas.
    - Integrate `Verifier` agents into the standard workflow.
3.  **Wave 3: Autonomous Governance (Audit)**
    - Deploy the `Judge Agent` for trace auditing.
    - Implement automated "Symmetry Checks" in the CI/CD pipeline.

---

## 5. Verification Matrix

How to prove the Cognitive-Symmetry Framework is operational.

| Check | Method | Success Criteria |
| :--- | :--- | :--- |
| **Symmetry Check** | `scripts/verify_symmetry.sh` | 0 discrepancies between `config/` and `docs/` paths. |
| **Axiom Validation** | Prompt Injection Test | Agent refuses to perform an action that violates a Global Axiom. |
| **Contract Integrity** | Schema Validation | 100% of `Executor` outputs pass the `Verifier` schema check. |
| **Audit Accuracy** | Trace Review | Judge Agent correctly identifies a protocol violation in a synthetic trace. |
