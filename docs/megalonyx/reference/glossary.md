# 📖 Project Glossary: Mega Code Stack

This glossary defines the core technical terminology used across the Mega Code codebase, documentation, and operational axioms. To maintain **Cognitive Symmetry**, these terms must be used consistently by both human contributors and AI agents.

---

## 🏗️ Architectural Pillars

### Blueprint
The **Blueprint** refers to the authoritative source code repository (the project root). It contains the static definitions, templates, and logic required to build the system. All changes must be committed to the Blueprint before being deployed to the Machine.

### Machine
The **Machine** refers to the deployed, runtime instance of the stack (typically located in `~/.local/share/megalonyx/`). It contains the active binaries, stateful databases (Qdrant), and environment-specific configurations.

### Cognitive-Symmetry Framework (CSF)
The **CSF** is the overarching design philosophy that ensures a 1:1 mapping between system configuration (`config/`) and technical documentation (`docs/`). It uses **Contextual Anchors** (`.qwen-context`) to provide directory-level operational laws, reducing context window saturation.

---

## 🧠 Intelligence & Orchestration

### Dreaming Pipeline
**Dreaming** is the system's internal background process for memory and reasoning refinement. It operates on two levels:
1.  **Systemic Dreaming (GC)**: A periodic Garbage Collection cycle that prunes stale memories (e.g., the 90-Day Rule), removes redundant vectors, and optimizes the semantic index for retrieval speed.
2.  **Agentic Dreaming (Synthesis)**: A process where the system autonomously generates code sketches, design alternatives, or synthesizes complex memories without direct user input to evolve the internal mental model.

### MQA-Snapshot-Suite
**MQA (Model Quality Assurance)** is the project's gold-standard verification framework. The **Snapshot-Suite** consists of high-entropy stress tests that capture the "state" of a request and verify that the system's output remains deterministic and high-quality across model updates or architectural changes.

### Job Contract
A **Job Contract** is the strictly typed JSON object emitted by the Routing Plane. It serves as the authoritative instruction set for the Execution Plane, specifying the `intent`, `risk_profile`, `recommended_skill`, and `suggested_tool_chain`.

---

## ⚙️ Operational Axioms

### S-READ (Lossless Reading)
The mandate that an agent must read the **entire** content of a file (using pagination/offsets if necessary) before attempting to edit it. "Peeking" or assuming content based on partial reads is forbidden.

### S-VERIFY (Deterministic Verification)
The requirement that every code change must be verified by an independent tool (e.g., `pytest`, `mypy`, `ruff`) rather than the agent's own self-assessment. A task is only "Completed" when the verification tool returns a success code.

### S-CORRECT (Deterministic Loop)
The operational loop used when verification fails: $\text{Observe} \to \text{Analyze} \to \text{Isolate} \to \text{Correct} \to \text{Re-Verify}$.

---

## 🛠️ Component Mapping

| Term | Component | Responsibility |
| :--- | :--- | :--- |
| **Control Plane** | `ControlPlane` | Intent $\to$ Decomposition $\to$ Job Set |
| **Routing Plane** | `OmniRoute` | Context $\to$ Skill Selection $\to$ Job Contract |
| **Execution Plane** | `SkillBridge` | Job Contract $\to$ Tool Execution $\to$ Result |
| **Interaction Plane**| `CLI / IDE` | User Input $\to$ Control Plane $\to$ UI Render |
