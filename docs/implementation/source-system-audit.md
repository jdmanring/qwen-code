# 🛠️ Source System Audit: The Sovereign Plumbing

This document provides a detailed technical audit of how the Sovereign stack operates from input to output. This serves as the primary reference for the migration to the monorepo structure.

## 🔄 The Execution Lifecycle

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

### 3. Verification & S-CORRECT
The system does not assume a tool call was successful just because it didn't crash.

- **Verification**: The `VerificationEngine` checks the output against the `job_contract`. (Example: If the task was "Fix a bug", the engine runs `pytest` to verify the fix).
- **S-CORRECT Loop**:
    - **Success**: The job is marked `completed`.
    - **Failure**: The system enters the `S-CORRECT` state. It analyzes the failure logs and either **Retries** (with a refined prompt) or **Pivots** (creates a new correction job).

---

## 🖥️ User Interface & Communication

### Input/Output Channels
- **Primary Channel**: `stdout` (Terminal).
- **Status Updates**: The `StatusManager` provides real-time, non-blocking updates on agent activity and job progress.
- **Interactive Prompts**: Used for tool confirmation and configuration changes.

### Output Formatting
The system distinguishes between two types of output:
1. **Final Response**: Natural language text delivered to the user.
2. **Internal Tool Call**: Structured JSON-like strings used to trigger system actions.

---

## 🔗 System Component Map

| Component | Responsibility | Key File/Module |
| :--- | :--- | :--- |
| **ControlPlane** | Job orchestration and lifecycle management | `packages/core/src/control_plane.py` |
| **Skill Bridge** | LLM communication and persona injection | `packages/core/src/skill_bridge.py` |
| **Policy Engine** | Permission and safety enforcement | `packages/core/src/policy_engine.py` |
| **Intent Classifier**| Prompt analysis and model routing | `packages/core/src/route.py` |
| **Status Manager** | UI updates and terminal output | `packages/cli/src/status_manager.ts` |
