#  Magic Strings & Constants Manifest

This document serves as the Single Source of Truth (SSOT) for all hardcoded identifiers, state flags, and hidden constants within the Qwen Code Core logic.

## 1. State & Lifecycle Flags
These strings are used across the Control Plane to track the progress of jobs and the global system phase.

| Key | Meaning | Locations |
| :--- | :--- | :--- |
| `"pending"` | Job is queued and awaiting execution | `verification_engine.py`, `task_decomposer.py`, `job_state_manager.py`, `control_plane.py` |
| `"completed"` | Job finished successfully | `verification_engine.py`, `job_state_manager.py`, `control_plane.py` |
| `"failed"` | Job encountered an error or failed verification | `verification_engine.py`, `control_plane.py` |
| `"running"` | Job is currently being executed | `control_plane.py` |
| `"success"` | Operation result is successful | `skill_bridge.py`, `logger.py` |
| `"error"` | Operation result is an error | `lsp_manager.py`, `logger.py` |
| `"PLANNING"` | Global system phase for initial strategy | `state_manager.py` |
| `"IMPLEMENTATION"` | Global system phase for coding/execution | `state_manager.py` |
| `"in_progress"` | Intermediate job state | `job_state_manager.py` |
| `"retrying"` | Job is being attempted again after failure | `job_state_manager.py` |
| `"pivoting"` | Job strategy is being changed | `job_state_manager.py` |

## 2. Configuration & Schema Keys
These keys are used by `StateManager` and `JobStateManager` to persist and retrieve session data.

| Key | Meaning | Location |
| :--- | :--- | :--- |
| `"active_phase"` | Tracks current high-level workflow state | `state_manager.py` |
| `"todo_list"` | List of pending tasks in the session | `state_manager.py` |
| `"rag_context"` | Key-value store for retrieved knowledge | `state_manager.py` |
| `"archive"` | History of moved RAG items | `state_manager.py` |
| `"last_agent"` | The agent that last modified the state | `state_manager.py` |
| `"iteration_count"` | Number of loops in the current phase | `state_manager.py` |
| `"global_constraints"` | System-wide rules for the current session | `state_manager.py` |
| `"metadata"` | Session telemetry (start time, turn count) | `state_manager.py` |
| `"active_job_set"` | Key for current batch of jobs in StateManager | `job_state_manager.py` |
| `"jobs"` | Dictionary of job IDs to job data | `job_state_manager.py` |
| `"dependencies"` | List of job IDs that must complete first | `job_state_manager.py` |

## 3. Hidden Dependencies & Defaults
These are implicit requirements for the system to function, often involving filesystem paths.

| Dependency | Role | Default Path/Value | Location |
| :--- | :--- | :--- | :--- |
| `state.json` | Persistence of global state | `.qwen/state.json` | `state_manager.py` |
| `settings.json` | Job manager configuration | `~/.qwen/settings.json` | `job_state_manager.py` |
| `megalonyx_memory.sock` | IPC for memory server | `~/.local/share/megalonyx/sockets/megalonyx_memory.sock` | `stdio_socket_relay.py` |

## 4. Scoring & Thresholds
Critical constants that determine the behavior of the AI's verification and retry loops.

| Constant | Value | Impact | Location |
| :--- | :--- | :--- | :--- |
| `min_confidence` | `0.8` | Threshold for job success in `verification_engine.py` | `verification_engine.py` |
| `min_confidence` | `0.7` | Threshold for `SynthesisContract` (documents/plans) | `contracts.py` |
| `GLOBAL_RETRY_LIMIT` | `10` | Max attempts before a workflow is marked as failed | `control_plane.py` |
| `timeout` | `60s` | Max seconds for verification command execution | `contracts.py` |
| `timeout` | `2.5s` | Semantic search deadline | `rag_tool.py` |
| `temperature` | `0.2` | Determinism for agent/task generation | `packages/core/src/agent_generator.py`, `task_decomposer.py` |
| `INITIAL_BACKOFF` | `1.0s` | Base delay for retry logic | `skill_bridge.py` |
