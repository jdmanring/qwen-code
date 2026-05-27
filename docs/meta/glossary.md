#  Project Technical Glossary

This document defines the authoritative technical terminology for the Megalonyx project. To ensure 100% intuitive AI understanding and zero ambiguity, every core concept must be referred to by a single, descriptive technical term.

##  Architectural Pillars

| Term | Definition | Intuitive AI Understanding |
| :--- | :--- | :--- |
| **Blueprint** | The monorepo source code and configuration. | The authoritative source of truth; the "design" from which the system is deployed. |
| **Runtime Stack** | The deployed state on the host (`~/.local/share/megalonyx`). | The physical manifestation of the Blueprint; the "Machine" that actually executes. |
| **Runtime Venv** | The isolated Python environment in the Runtime Stack. | The specific Python interpreter and library set used for all system execution. |
| **Independent Monorepo** | The project's private repository structure. | A codebase that integrates upstream sources while maintaining proprietary, decoupled advancements. |

##  Connectivity & Transport

| Term | Definition | Intuitive AI Understanding |
| :--- | :--- | :--- |
| **UDS Bridge** | The Unix Domain Socket relay (`stdio_socket_relay.py`). | A lightweight proxy that translates MCP `stdio` to UDS for daemon communication. |
| **Memory Daemon** | The long-running memory process (`memory_daemon.py`). | The central authority for semantic memory, embeddings, and Qdrant interaction. |
| **UDS Socket** | The physical socket file (`megalonyx_memory.sock`). | The communication endpoint used by the Bridge to talk to the Daemon. |

##  Governance & Standards

| Term | Definition | Intuitive AI Understanding |
| :--- | :--- | :--- |
| **Project Standard** | The core operational laws (defined in `QWEN.md`). | The mandatory engineering constraints and axioms that govern all agent behavior. |
| **System Failure Analysis** | The record of technical regressions (SFMA). | Institutional memory of "how we broke things" and the architectural fixes applied. |
| **Symmetry Law** | The 1:1 mirror between `config/` and `docs/`. | The requirement that every configuration has a corresponding technical explanation. |

##  Operational Tools

| Term | Definition | Intuitive AI Understanding |
| :--- | :--- | :--- |
| **Runtime Stack Installer** | The `install-megalonyx-stack.sh` script. | The tool that transforms the Blueprint into a functional Runtime Stack. |
| **Runtime Wrapper** | The shell scripts in `~/.local/bin/` (e.g., `mega-run-py`). | The entry points that activate the Runtime Venv and execute system tools. |

##  Search & Retrieval

| Term | Definition | Intuitive AI Understanding |
| :--- | :--- | :--- |
| **External Search Retrieval System** | The multi-layered search pipeline. | The system that aggregates results from SearXNG, OrioSearch, and Domain APIs. |
| **External Search Retrieval Pipeline** | The data flow: Expand $\to$ Retrieve $\to$ Extract $\to$ Rerank. | The specific sequence of operations to transform a query into a high-signal context. |
| **Search Infrastructure** | The self-hosted components (SearXNG, OrioSearch, Qdrant). | The physical servers and databases required to power the retrieval system. |

---

**Naming Rule**: If a term is not in this glossary, it must be named based on its **function** (Noun) rather than its **status** (Adjective). Avoid branding ("Megalonyx") unless referring to the project as a whole.
