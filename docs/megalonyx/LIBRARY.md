# 📚 The Authoritative Knowledge Map

This document serves as the central index for all knowledge contained within the `qwen_code_stack`. It is the primary entry point for agents seeking to understand the system's capabilities and constraints.

## 🗺️ Knowledge Domains

### 🏛️ Domain 1: Operational Guidelines
*Mandates and constraints governing system behavior.*

| Document | Purpose | Link |
| :--- | :--- | :--- |
| [Operational Guidelines: QWEN](meta/QWEN.md) | Core operational axioms and mandates. | `meta/QWEN.md` |
| [Agent System Architecture](architecture/agent-system.md) | Definition and execution of agents. | `architecture/agent-system.md` |
| [Symmetry Law](meta/symmetry.md) | Rules for mirrored documentation. | `meta/symmetry.md` |

### 🏗️ Domain 2: System Architecture
*Design documents and structural definitions.*

| Document | Purpose | Link |
| :--- | :--- | :--- |
| [System Layout](architecture/layout.md) | Blueprint vs Machine mapping. | `architecture/layout.md` |
| [Memory Hierarchy](explanation/system-overview.md) | RAG architecture overview. | `explanation/system-overview.md` |
| [Cognitive Efficiency](explanation/cognitive-efficiency.md) | Token optimization and semantic anchoring. | `explanation/cognitive-efficiency.md` |
| [Semantic Navigation](architecture/semantic-navigation.md) | AST and symbol mapping logic. | `architecture/semantic-navigation.md` |
| [Tool Isolation](architecture/tool-isolation.md) | WASM sandboxing specification. | `architecture/tool-isolation.md` |

### 🛠️ Domain 3: Process Guides
*Step-by-step protocols for implementation and maintenance.*

| Document | Purpose | Link |
| :--- | :--- | :--- |
| [CSF-Ingestion Protocol](process/csf-ingestion-protocol.md) | Transforming repos into Cognitive Assets. | `process/csf-ingestion-protocol.md` |
| [Surgical Workflow](how-to/workflow.md) | Lab => Patch => Blueprint => Deploy. | `how-to/workflow.md` |

### 📖 Domain 4: Technical Reference
*Low-level specifications and research logs.*

| Document | Purpose | Link |
| :--- | :--- | :--- |
| [PII Scrubbing](explanation/pii-scrubbing.md) | Masking middleware specification. | `explanation/pii-scrubbing.md` |
| [Advanced RAG](intelligence/advanced-rag.md) | Dreaming, CRAG, and GraphRAG. | `intelligence/advanced-rag.md` |
| [Project History](meta/project_history.md) | Evolutionary log of the stack. | `meta/project_history.md` |

---

## 🔍 Navigation Guide
To find information, follow the **Symmetry Path**:
`Knowledge Need` $\to$ `LIBRARY.md` $\to$ `Blueprint (docs/)` $\to$ `Machine (config/ or packages/)`.
