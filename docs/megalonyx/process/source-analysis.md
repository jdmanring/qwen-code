# 🔬 Source Analysis & Absorption Protocol

This document provides the detailed technical implementation for the **Config-Doc Sync Framework (CSF) Ingestion Protocol**. It defines how to analyze external source material (the "Source") for the purpose of importing its intelligence, patterns, or functionality into the Qwen Code project (the "Target").

To prevent "Divergence Debt" and technical contamination, this protocol must be followed absolutely.

---

## 1. The "Sterile Room" Principle

The most critical failure in source analysis is **Projection**: attributing the Target's goals or architecture to the Source's implementation.

### 1.1 Mental Firewall
- **Source $\neq$ Target**: The Source is a static artifact to be observed, not a prototype of the Target.
- **Observation Only**: When documenting the Source, describe *exactly what is there*, not what *should be there* or how it *could be improved* to fit the Target.
- **No-Assumption Rule**: Never assume a feature exists in the Source because it is desired in the Target. If it is not explicitly found in the code, it does not exist.

### 1.2 Terminology Isolation
To avoid concept bleed, use distinct naming conventions:
- **Target terms** (e.g., "Dual-Tier RAG", "Mirror-Destination") must **NEVER** appear in Source specifications.
- **Source terms** should be prefixed or qualified (e.g., "The Lab's Local Memory Implementation" instead of "The Memory System").

---

## 2. CSF-Ingestion Pipeline implementation

This section details the technical execution of the [CSF-Ingestion Protocol](docs/process/csf-ingestion-protocol.md).

### Phase 1: Physical Ingestion $\to$ Structural Discovery
- **Goal**: Map the "topography" of the source.
- **Actions**:
  - List all directories and key configuration files.
  - Identify the primary entry points (e.g., `main.ts`, `index.js`).
  - Map the dependency graph (e.g., `package.json`, `requirements.txt`).

### Phase 2: Structural Mapping $\to$ Pure Specification
- **Goal**: Create high-fidelity technical specifications of the source's logic.
- **Requirement**: These specs must be "Pure"—derived exclusively from the source code.
- **Format**: Use `spec-*.md` files. Each spec must:
  - Map class responsibilities and state transitions.
  - Trace the lifecycle of a request (The "Turn").
  - Document the exact logic of critical algorithms.
  - Include a "Component Responsibility Map" table.
- **Component Cataloging**: Create inventories of reusable assets (Agents, Tools, Prompts).

### Phase 3: Functional Distillation $\to$ Absorption Roadmap
- **Goal**: Identify the "Intelligence Gap" and define the path to integration.
- **Sterile Gap Analysis**: Create a comparison matrix:
  `[Source Feature]` $\rightarrow$ `[Target Status (Missing/Partial/Exists)]` $\rightarrow$ `[Priority]`.
- **Rule Synthesis**: Extract recurring patterns and convert them into `(Trigger $\to$ Action)` rules for the Target's memory system.
- **Absorption Roadmap**: Define the technical path (Patches or Skills) to integrate the intelligence.

### Phase 4: Verification $\to$ Certification
- **Goal**: Prove the repository is "AI-Navigable."
- **Zero-Shot Simulation**: Assign a fresh agent to a task in the ingested repo. Success is defined as completion without "how-to" guidance.

---

## 3. Verification & Audit Requirements

Documentation is not considered "Complete" until it passes the following audits:

### 3.1 Code-to-Doc Traceability
Every claim in a Pure Specification must be verifiable.
- **Audit**: Randomly select 3 claims from a spec and locate the corresponding lines of code in the source. If they cannot be found within 60 seconds, the spec is "Hallucinated" and must be rewritten.

### 3.2 Contamination Audit
A mandatory terminology check to ensure no Target-specific concepts leaked into the Source documentation.
- **Action**: Run `grep` (or equivalent) across all `spec-*.md` files for a list of Target-specific keywords.
- **Failure**: Any match results in an immediate "Contamination Alert" and a mandatory rewrite of the affected section.

### 3.3 AI-Navigability Check
Ensure the documentation is structured for AI consumption:
- Use Markdown headers for clear hierarchy.
- Use tables for responsibility maps.
- Use Mermaid diagrams or structured lists for state transitions.
