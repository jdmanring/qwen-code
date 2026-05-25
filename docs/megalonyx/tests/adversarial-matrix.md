# 🛡️ Adversarial Test Matrix

This document defines the "Expected Failure" scenarios for the Qwen Code project. The goal is to move from "Testing if it works" to "Proving it cannot be broken in predictable ways."

## 1. Failure Taxonomy

We categorize adversarial tests into three primary failure domains: **Transport**, **Process**, and **State**.

### A. Transport Failures (The "Pipe")
Focuses on the Unix Domain Socket (UDS) and MCP bridge.

| Scenario ID | Failure Trigger | Expected Behavior | Verification Metric |
| :--- | :--- | :--- | :--- |
| `TRANS-01` | UDS Socket deleted mid-session | Bridge detects `BrokenPipeError` or `ConnectionResetError`. | Error logged; bridge attempts reconnect or reports failure. |
| `TRANS-02` | Socket buffer overflow (large payload) | System handles large MCP payloads without truncation. | Payload integrity check (checksum). |
| `TRANS-03` | Permission denied on socket | Bridge reports `PermissionError` clearly. | Error message contains "Permission denied". |
| `TRANS-04` | Socket timeout/hang | Bridge implements a strict timeout (e.g., 30s). | `asyncio.TimeoutError` raised; process does not hang. |

### B. Process Failures (The "Daemon")
Focuses on the lifecycle of background services (e.g., `memory_daemon`).

| Scenario ID | Failure Trigger | Expected Behavior | Verification Metric |
| :--- | :--- | :--- | :--- |
| `PROC-01` | Daemon SIGKILL (Hard crash) | Orchestrator detects service death via socket failure. | `ConnectionRefusedError` handled gracefully. |
| `PROC-02` | Daemon SIGTERM (Graceful) | Daemon closes socket and cleans up PID files. | Socket file is removed from `/tmp/`. |
| `PROC-03` | Zombie Process (Hanging) | Health check fails; orchestrator triggers restart. | `mega-memory-manager` restarts the process. |
| `PROC-04` | Resource Exhaustion (OOM) | System logs OOM event; fails without corrupting DB. | Qdrant WAL integrity check passes. |

### C. State Failures (The "Data")
Focuses on the integrity of the vector store and configuration.

| Scenario ID | Failure Trigger | Expected Behavior | Verification Metric |
| :--- | :--- | :--- | :--- |
| `STAT-01` | Corrupted `settings.json` | System falls back to safe defaults or exits with clear error. | JSON decode error handled; no silent failures. |
| `STAT-02` | Vector Store Index Corruption | Daemon detects corruption on boot; triggers recovery. | Recovery from WAL (Write-Ahead Log) successful. |
| `STAT-03` | Concurrent Write Conflict | System implements locking or sequential queueing. | No data loss; final state is consistent. |
| `STAT-04` | Invalid Model ID in Config | System reports "Model Not Found" instead of crashing. | Clear error: `Model [ID] not found in provider list`. |

---

## 2. Implementation Strategy

Each scenario in this matrix must be mapped to a test case in the `tests/fidelity/` or `tests/adversarial/` directories.

**Verification Contract:**
Every adversarial test must follow the `Fail-Observe-Recover` loop:
1.  **Fail**: Trigger the failure (e.g., `os.remove(socket_path)`).
2.  **Observe**: Attempt an operation (e.g., `mgr.call_tool(...)`).
3.  **Recover**: Verify the system either recovers automatically or reports the error according to the "Expected Behavior" column.
