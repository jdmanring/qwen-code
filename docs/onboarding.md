# Onboarding: The Life of a Request

To understand how Megalonyx works, it is best to follow a single request as it travels through the architectural layers.

## The Scenario
**User Prompt:** `/bugfix "Fix the memory leak in the uds_bridge.py"`

### The Execution Trace

#### 1. The Entry Point (Interaction Plane)
The user types the command into the **Qwen Code CLI**. The CLI recognizes the `/bugfix` slash-command and forwards the request, along with the current session context (CWD, open files), to the **Control Plane Daemon** via a Unix Domain Socket.

#### 2. Strategic Analysis (Control Plane)
The Daemon receives the request and puts it through the classification pipeline:
- **Intent Classification**: The `IntentClassifier` analyzes the prompt and maps it to the `Targeted Bugfix` intent. It assigns a "Medium" risk profile.
- **Task Decomposition**: The `TaskDecomposer` determines that a bugfix cannot be done in one step. It generates a sequence of atomic jobs:
    1. **Explore**: Locate the leak in `uds_bridge.py` and analyze the cause.
    2. **Developer**: Implement the fix using the `edit` tool.
    3. **Test Engineer**: Run the existing test suite to verify the fix and ensure no regressions.

#### 3. The Execution Loop (Action $\to$ Observation)
The Daemon now executes the jobs sequentially:

- **Executing Job 1 (Explore)**: The Daemon calls the CLI's `explore` skill. The CLI runs `grep` and `read_file`. The results are sent back to the Daemon.
- **Updating Memory**: The Daemon identifies the root cause and calls the `agent-memory` MCP server's `ingest` tool. The leak's location and cause are stored in **Qdrant** for future reference.
- **Executing Job 2 (Developer)**: The Daemon calls the `developer` skill. The CLI performs a precise `edit` on `uds_bridge.py`.
- **Executing Job 3 (Test Engineer)**: The Daemon calls the `test-engineer` skill. The CLI runs `pytest`.

#### 4. Verification and Closure
The **Verification Engine** checks the output of the `test-engineer` job. Since the tests passed, the Daemon marks the overall task as `completed` and notifies the user via the CLI.

---

## Component Map

| Step | Component | Key File | Responsibility |
| :--- | :--- | :--- | :--- |
| **Forwarding** | Qwen CLI | `packages/cli/` | Transport user prompt to Daemon |
| **Classification** | Intent Classifier | `intent_classifier.py` | Map prompt $\to$ Intent Taxonomy |
| **Decomposition** | Task Decomposer | `task_decomposer.py` | Map Intent $\to$ Atomic Job Sequence |
| **Execution** | Job Executor | `tool_executor.py` | Bridge jobs to CLI skills |
| **Memory** | Agent Memory | `memory_mcp_server.py` | Semantic storage in Qdrant |
| **Verification** | Verification Engine | `verification_engine.py` | Validate job output against criteria |
