# 🧠 Naming Standards: Engineering-First Clarity

This document defines the standards for naming files and directories in the Megalonyx. The goal is to minimize **Cognitive Friction**—the mental overhead an agent or developer experiences when inferring the purpose of a file.

---

## 🎯 The Engineering Logic of Naming

AI agents process information through pattern recognition. Inconsistent naming (e.g., mixing `Screaming_Caps` with `kebab-case`) or ambiguous terms (e.g., `_alt`, `_sim`) force the agent to read the file content to understand its role, increasing token usage and latency.

### 1. The "No Paradox" Rule
Names must not send conflicting signals.
- **Paradox**: `.env.md` (Signals both "Hidden Secret" and "Visible Documentation").
- **Standard**: Use descriptive, visible names for documentation (e.g., `environment-variables.md`).

### 2. The "Actionable" Validator Standard
Tests and validators should be named as **processes**, not **objects**, to signal their role in the verification loop.
- **Ambiguous**: `config_check.py` (The "Check" is a noun).
- **Actionable**: `validate_config.py` (The "Validate" is a verb).

### 3. The Case Standard (Symmetry)
To reduce visual noise and maintain consistency, the project adheres to a strict casing policy:
- **Source Code**: `snake_case.py` (Python PEP 8 standard).
- **Documentation & Config**: `kebab-case.md` / `kebab-case.json` (Standard for web/CLI docs).
- **Avoid**: `SCREAMING_SNAKE_CASE.md` for documentation.

---

## 🗺️ Cognitive Realignment Mapping

The following table maps high-friction names to cognitive-optimal counterparts.

### Root Documentation
| Current Name | Role | Proposed Name | Rationale |
| :--- | :--- | :--- | :--- |
| `MAINTAINER_GUIDE.md` | Maintainer instructions | `maintainer-guide.md` | Case normalization. |
| `SOVEREIGN_INTEGRATION_BLUEPRINT.md` | Integration architecture | `integration-blueprint.md` | Case normalization. |
| `MASTER_PLAN.md` | Strategic roadmap | `master-plan.md` | Case normalization. |
| `MAINTENANCE_AUTOMATION.md` | Tooling specifications | `maintenance-automation.md` | Case normalization. |
| `GIT_STRATEGY.md` | Version control protocol | `git-strategy.md` | Case normalization. |
| `INTEGRATION_STRATEGY.md` | Merger strategy | `integration-strategy.md` | Case normalization. |

### Testing & Validation
| Current Name | Role | Proposed Name | Rationale |
| :--- | :--- | :--- | :--- |
| `tests/recovered/test_server_alt.py` | Fallback server test | `tests/recovered/test_server_fallback.py` | "Fallback" is explicit intent. |
| `tests/integration/test_server_alt.py` | Fallback server test | `tests/integration/test_server_fallback.py` | "Fallback" is explicit intent. |
| `tests/fidelity/test_ui_sim.py` | UI Handshake simulation | `tests/fidelity/test_ui_mcp_handshake.py` | Be specific about the mechanism. |
| `tests/validators/stack_validate.py` | Full-stack health check | `tests/validators/validate_stack.py` | Verb-first naming. |
| `tests/validators/index_codebase.py` | Indexing verification | `tests/validators/validate_indexing.py` | Verb-first naming. |
| `tests/validators/config_check.py` | Config file verification | `tests/validators/validate_config.py` | Verb-first naming. |
| `tests/validators/audit_workflow.py` | Agent log audit | `tests/validators/validate_workflow.py` | Verb-first naming. |
| `tests/validators/analyze_logs.py` | Telemetry reporting | `tests/validators/validate_telemetry.py` | Verb-first naming. |

### Core Infrastructure
| Current Name | Role | Proposed Name | Rationale |
| :--- | :--- | :--- | :--- |
| `packages/core/agent_generator.py` | Legacy entry point | **(DELETE)** | Remove duplicate to eliminate ambiguity. |
| `packages/core/src/agent_generator.py`| Agent synthesis logic | `packages/core/src/agent_generator.py` | Maintain as Source of Truth. |

---

## 🛠️ Implementation Protocol
All renames must follow the **Surgical Realignment Protocol**:
1. **Reference Map**: Identify all imports and shell calls.
2. **Atomic Update**: Rename file and update references in a single batch.
3. **Verification**: Run `pytest` and `symmetry-check.py`.
