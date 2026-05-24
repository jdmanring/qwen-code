# Naming Conventions

Consistent naming conventions ensure that the codebase remains predictable, searchable, and idiomatic. By adhering to these standards, we reduce cognitive load for developers and ensure compatibility with standard tooling.

---
PYTHON FILES & TESTS
---

All Python source files and test files must follow the **snake_case** convention.

**Standard**: `lower_case_with_underscores.py`

**Why**:
This follows [PEP 8](https://peps.python.org/pep-0008/), the official style guide for Python code, ensuring that the project remains idiomatic and compatible with Python linting tools.

| Correct | Incorrect | Note |
| :--- | :--- | :--- |
| `transform_skills.py` | `transformSkills.py` | No camelCase in Python filenames. |
| `test_qdrant_mcp.py` | `test-qdrant-mcp.py` | Use underscores, not hyphens. |
| `memory_manager.py` | `MemoryManager.py` | Filenames should be lowercase. |

---
SHELL SCRIPTS & CLI TOOLS
---

All shell scripts and command-line interface (CLI) tools must follow the **kebab-case** convention.

**Standard**: `lower-case-with-hyphens.sh`

**Why**:
Hyphens are the standard spacer for Unix/Linux CLI utilities. This ensures the tools feel native to the shell environment and avoid issues with certain shell expansions or tab-completion behaviors.

| Correct | Incorrect | Note |
| :--- | :--- | :--- |
| `mega-memory-manager.sh` | `stack_manager.sh` | Use hyphens for scripts. |
| `sync-upstream.sh` | `syncUpstream.sh` | No camelCase in CLI tools. |
| `mega-status` | `qwen_status` | CLI binaries should use kebab-case. |

---
HIGH-LEVEL MANIFESTS
---

Major project-wide manifests and authoritative roadmaps must follow the **kebab-case** convention to ensure consistency and reduce cognitive friction for AI agents.

**Standard**: `lower-case-with-hyphens.md`

**Why**:
This aligns with the project's Cognitive Naming Standards, treating manifests as first-class documentation rather than static constants. This reduces visual noise and ensures a unified look across the root directory and the `docs/` folder.

| Correct | Incorrect | Note |
| :--- | :--- | :--- |
| `master-plan.md` | `MASTER_PLAN.md` | Manifests now use kebab-case. |
| `TODO.md` | `todo.md` | Key trackers remain prominent. |
| `architecture-log.md` | `ARCHITECTURE_LOG.md` | Use hyphens for manifests. |

For a deeper dive into the engineering logic behind these choices and the full realignment mapping, refer to the [Cognitive Naming Standards](../meta/COGNITIVE_NAMING_STANDARDS.md).

---
SUMMARY REFERENCE
---

| Asset Type | Convention | Example | Standard |
| :--- | :--- | :--- | :--- |
| Python Files | `snake_case` | `core_logic.py` | PEP 8 |
| Shell Scripts | `kebab-case` | `setup-env.sh` | Unix/Linux |
| Manifests | `kebab-case` | `master-plan.md` | Cognitive Standard |

---
END OF GUIDELINES
---
