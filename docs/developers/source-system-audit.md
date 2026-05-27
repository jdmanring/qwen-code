#  Source System Audit: The Standalone Plumbing

This document provides a detailed technical audit of how the Standalone stack operates from input to output. This serves as the primary reference for the migration to the monorepo structure.

##  The Execution Lifecycle

The system operates as a deterministic state machine following the **Act $\to$ Observe $\to$ Verify $\to$ Correct** loop.

### 1. Input & Orchestration
- **Entry Point**: The system is driven via the CLI (`skill_bridge.py`).
- **Request Flow**: `User Prompt` $\to$ `ControlPlane` $\to$ `IntentClassifier` $\to$ `Job Contract`.
- **Job Contract**: A structured object that defines the goal, the assigned agent, the required model (Primary vs Fast), and the success criteria.

### 2. The Tool Loop (The Heartbeat)
When the LLM decides to use a tool, the following sequence is triggered:

**LLM Request** $\to$ **Tool Dispatcher** $\to$ **Policy Engine** $\to$ **Execution** $\to$ **User Confirmation** $\to$ **Result**

- **Tool Dispatcher**: Intercepts the tool call regex `\{"tool": "...", "args": {...}\}`.
- **Policy Engine**: Checks the `job_contract` and `agent_name` against the permission matrix. If forbidden, the call is blocked and a denial is returned to the LLM.
- **Execution**: The tool is executed (e.g., `read_file`, `grep_search`). Results are cached in the `RuntimeContext`.
- **User Confirmation**: If `approvalMode` is not `YOLO`, the system pauses and requests user approval via `stdout`.

#### Multi-Agent Orchestration Plumbing
The system extends the basic tool loop to support advanced agentic patterns:
- **Subagent Dispatch**: The `agent` tool call triggers a new session context. The `ControlPlane` manages the parent-child relationship, ensuring the subagent's output is routed back to the parent's turn.
- **Arena Isolation**: The `arena` command triggers the creation of multiple `git worktrees`. The system manages multiple concurrent `RuntimeContexts`, one for each worktree, and provides a unified comparison UI.
- **Loop Management**: The `/loop` skill integrates with a background cron scheduler. The `StatusManager` tracks these background jobs and injects their results into the main session when they fire.

### 3. Verification & S-CORRECT
The system does not assume a tool call was successful just because it didn't crash.

- **Verification**: The `VerificationEngine` checks the output against the `job_contract`. (Example: If the task was "Fix a bug", the engine runs `pytest` to verify the fix).
- **S-CORRECT Loop**:
    - **Success**: The job is marked `completed`.
    - **Failure**: The system enters the `S-CORRECT` state, executing the following algorithm:
        1. **Observe**: Capture the failure logs and the current state of the file system.
        2. **Analyze**: Identify the root cause (e.g., logic error, missing dependency, path mismatch).
        3. **Isolate**: Determine the minimum set of files that need modification to fix the error.
        4. **Correct**: Implement the fix following the `Project Standard Code Standard`.
        5. **Re-Verify**: Run the verification suite again. If it fails, return to Step 1.

---

##  User Interface & Communication

### Input/Output Channels
- **Primary Channel**: `stdout` (Terminal).
- **Status Updates**: The `StatusManager` provides real-time, non-blocking updates on agent activity and job progress.
- **Interactive Prompts**: Used for tool confirmation and configuration changes.

### Output Formatting
The system distinguishes between two types of output:
1. **Final Response**: Natural language text delivered to the user.
2. **Internal Tool Call**: Structured JSON-like strings used to trigger system actions.

---

##  System Component Map

| Component | Responsibility | Key File/Module | State |
| :--- | :--- | :--- | :--- |
| **ControlPlane** | Job orchestration and lifecycle management | `packages/core/src/control_plane.py` | Target |
| **Skill Bridge** | LLM communication and persona injection | `packages/core/src/skill_bridge.py` | Target |
| **Policy Engine** | Permission and safety enforcement | `packages/core/src/policy_engine.py` | Target |
| **Intent Classifier**| Prompt analysis and model routing | `packages/core/src/route.py` | Target |
| **Status Manager** | UI updates and terminal output | `packages/cli/src/status_manager.ts` | Legacy |
