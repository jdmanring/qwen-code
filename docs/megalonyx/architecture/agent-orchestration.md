#  Agent Orchestration: Multi-Agent Patterns

This document describes the advanced orchestration patterns used by the Runtime Stack to handle complex tasks through delegation, competition, and iterative loops.

##  Orchestration Patterns

The system employs three primary patterns to move beyond single-agent execution.

### 1. The Subagent Delegation Pattern
**Purpose**: Task decomposition and context window optimization.
- **Mechanism**: The **Orchestrator** identifies a focused sub-task and dispatches it to a **Subagent**.
- **Lifecycle**: 
    1. **Dispatch**: Orchestrator calls the `agent` tool with a specific persona and prompt.
    2. **Execution**: The Subagent operates in a focused context, completing the atomic task.
    3. **Integration**: The Subagent returns the result; the Orchestrator integrates this into the main session.
- **Benefit**: Prevents "Context Bloat" by keeping implementation details out of the main orchestrator's window.

### 2. The Agent Arena Pattern
**Purpose**: Model evaluation and solution optimization.
- **Mechanism**: The system launches multiple independent agents in **isolated Git worktrees**.
- **Lifecycle**:
    1. **Isolation**: Each agent gets a clean copy of the repo in a temporary worktree.
    2. **Competition**: Different models (e.g., Gemini vs GPT-4) tackle the same prompt.
    3. **Selection**: The user or a "Judge" agent compares results.
    4. **Merge**: The winning worktree is merged back into the main workspace.
- **Benefit**: Eliminates "Model Bias" and ensures the highest quality implementation.

### 3. The Loop Taxonomy
The Runtime Stack utilizes three distinct types of loops to ensure correctness and automation.

#### A. The S-CORRECT Loop (The Quality Gate)
The fundamental state machine for all tool execution:
`Act` $\to$ `Observe` $\to$ `Verify` $\to$ `Correct` $\to$ `Re-Verify`
- **Exit Condition**: Verification passes or maximum retry limit is reached.

#### B. The Iterative Reverse Audit (The Deep Scan)
Used primarily in `Code Review` workflows:
- **Mechanism**: Multiple rounds of gap-finding where each round receives the cumulative findings of the previous rounds.
- **Exit Condition**: A round returns "No issues found" or the 3-round cap is hit.

#### C. The Temporal Loop (`/loop`)
A user-facing scheduling system:
- **Mechanism**: A background cron job that triggers a prompt at a specified interval.
- **Exit Condition**: Manual cancellation or 3-day automatic expiration.

---

##  Orchestration Logic Flow

**User Query** $\to$ **Orchestrator** $\to$ **[Decision]**
- $\to$ *Low Complexity* $\to$ **Direct Execution**
- $\to$ *High Complexity* $\to$ **Subagent Delegation**
- $\to$ *High Uncertainty* $\to$ **Agent Arena Competition**

Every path eventually feeds back into the **S-CORRECT Loop** for final verification.
