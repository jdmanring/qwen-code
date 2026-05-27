 
#  Blueprint vs. Machine Gap Analysis

This document serves as the living manifest of discrepancies between the **Blueprint** (source code in `../../`) and the **Machine** (deployed state in `~/.local/share/megalonyx/`).

The goal of this document is to ensure that the Blueprint remains the absolute source of truth and that the system is 100% reproducible from source.

---

##  Synchronization Goal
**$\text{Blueprint} \approx \text{Machine}$**

Any tool, script, or configuration that exists on the Machine and is required for operation **MUST** be mirrored in the Blueprint. Runtime-generated state (logs, PIDs, databases) is exempt.

---

##  Current State (Last Audit: May 20, 2026)

###  Resolved Gaps (The Truth Sync)
The following items were identified as missing from the Blueprint and have been recovered:

| Item | Blueprint Path | Status | Note |
| :--- | :--- | :--- | :--- |
| `mega-memory-manager.sh` | `scripts/mega-memory-manager.sh` | **Recovered** | Critical lifecycle and health-check logic. |
| `simulate_mcp.py` | `tests/recovered/simulate_mcp.py` | **Recovered** | Essential MCP testing utility. |
| `test_*.py` Suite | `tests/recovered/` | **Recovered** | Connection and server validation scripts. |
| `test_settings.json` | `tests/recovered/test_settings.json` | **Recovered** | Test configuration baseline. |
| `QWEN.md` (Machine) | `docs/meta/machine-qwen.md` | **Recovered** | Machine-side operational notes. |
| `TEST_TODO.md` | `docs/meta/machine-test-todo.md` | **Recovered** | Historical testing progress. |

###  Persistent/Intentional Gaps
These items exist on the Machine but should **NOT** be mirrored in the Blueprint:

| Item | Type | Reason |
| :--- | :--- | :--- |
| `data/`, `storage/` | State | Contains local vector databases and cached data. |
| `pids/`, `tmp/` | Runtime | Process IDs and temporary sockets. |
| `~/.qwen/.env` | Secret | Contains active API keys; mirrored via `.env.example`. |
| `~/.qwen/settings.json` | Config | Environment-specific overrides (now using agnostic paths). |

---

##  Synchronization Protocol

When drift is detected (e.g., a new utility script is created on the Machine), the following protocol must be followed:

### 1. Detection (The Audit)
Run a recursive listing of both directories and compare:
```bash
# List Machine scripts
ls -R ~/.local/share/megalonyx/scripts/
# List Blueprint scripts
ls -R ../../scripts/
```

### 2. Verification (The Safe Sync)
Before copying a file from Machine $\to$ Blueprint:
1.  **Check for Collision**: If the file exists in the Blueprint, **do not overwrite**. Use `diff` to analyze changes.
2.  **Path Generalization**: Ensure the file contains no absolute paths (e.g., `/home/james/...`). Replace with `${STACK_ROOT}` or `~`.
3.  **Categorization**: Place tests in `tests/recovered/` and utilities in `scripts/`.

### 3. Validation
Verify that the recovered tool works in the Blueprint environment before committing.

---

##  Sync Checklist
- [ ] All operational scripts in `~/.local/share/megalonyx/scripts/` are mirrored in `scripts/`.
- [ ] All `bin/` wrappers are synchronized.
- [ ] No absolute paths exist in the Blueprint's configuration templates.
- [ ] All debug/test scripts used on the Machine are archived in `tests/recovered/`.
