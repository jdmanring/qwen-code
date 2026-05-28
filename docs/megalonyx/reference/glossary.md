#  Project Glossary: Mega Code Stack

This glossary defines the core technical terminology used across the Mega Code codebase, documentation, and operational rules. To maintain **Documentation Synchronization**, these terms must be used consistently by both human contributors and AI agents.

---

##  Architectural Pillars

### Source Repository
The **Source Repository** refers to the authoritative code repository (the project root). It contains the static definitions, templates, and logic required to build the system. All changes must be committed to the Source Repository before being deployed to the Runtime Environment.

### Runtime Environment
The **Runtime Environment** refers to the deployed, runtime instance of the stack (typically located in `~/.local/share/megalonyx/`). It contains the active binaries, stateful databases (Qdrant), and environment-specific configurations.

### Config-Doc Sync Framework (CSF)
The **CSF** is the design standard that ensures a 1:1 mapping between system configuration (`config/`) and technical documentation (`docs/`). It uses **Contextual Anchors** (`.mega-context`) to provide directory-level operational rules, reducing context window saturation.

---

##  Intelligence & Orchestration

### Memory Refinement Pipeline
**Memory Refinement** is the system's internal background process for memory and reasoning optimization. It operates on two levels:
1.  **Systemic Refinement (GC)**: A periodic Garbage Collection cycle that prunes stale memories (e.g., the 90-Day Rule), removes redundant vectors, and optimizes the semantic index for retrieval speed.
2.  **Agentic Refinement (Synthesis)**: A process where the system autonomously generates code sketches, design alternatives, or synthesizes complex memories without direct user input to evolve the internal knowledge model.

### MQA-Snapshot-Suite
**MQA (Model Quality Assurance)** is the project's gold-standard verification framework. The **Snapshot-Suite** consists of high-entropy stress tests that capture the "state" of a request and verify that the system's output remains deterministic and high-quality across model updates or architectural changes.

### Job Contract
A **Job Contract** is the strictly typed JSON object emitted by the Routing Plane. It serves as the authoritative instruction set for the Execution Plane, specifying the `intent`, `risk_profile`, `recommended_skill`, and `suggested_tool_chain`.

---

##  Operational Rules

### S-READ (Lossless Reading)
The rule that an agent must read the **entire** content of a file (using pagination/offsets if necessary) before attempting to edit it. "Peeking" or assuming content based on partial reads is forbidden.

### S-VERIFY (Deterministic Verification)
The requirement that every code change must be verified by an independent tool (e.g., `pytest`, `mypy`, `ruff`) rather than the agent's own self-assessment. A task is only "Completed" when the verification tool returns a success code.

### S-CORRECT (Deterministic Loop)
The operational loop used when verification fails: $\text{Observe} \to \text{Analyze} \to \text{Isolate} \to \text{Correct} \to \text{Re-Verify}$.

### OPS (Optimization Preservation Standard)
The **OPS** is the project's standard for lossless file optimization. It mandates **Structural Symmetry** (maintaining a 1:1 mapping of headers, tags, and sequence) and **Anchor Preservation** (protecting critical infrastructure like "Fast-Activate" sections) to prevent the "Lost in the Middle" effect during compression.

---

##  Component Mapping

| Term | Component | Responsibility |
| :--- | :--- | :--- |
| **Control Plane** | `ControlPlane` | Intent $\to$ Decomposition $\to$ Job Set |
| **Routing Plane** | `ModelRouter` | Context $\to$ Skill Selection $\to$ Job Contract |
| **Execution Plane** | `Job Executor` | Job Contract $\to$ Tool Execution $\to$ Result |
| **Interaction Plane**| `CLI / IDE` | User Input $\to$ Control Plane $\to$ UI Render |
