# Agent Interaction Protocol (AIP)

## 1. Core Philosophy: The CPU-Worker Model
The AI-OS is designed around a strict separation between **Cognitive Synthesis (The CPU)** and **Atomic Execution (The Worker)**.

- **The Orchestrator (CPU)**: Maintains global state, performs complex analysis, synthesizes reports, and manages the task graph.
- **The Sub-Agent (Worker)**: Performs high-speed, narrow-scope data extraction and execution.

**CRITICAL RULE**: Synthesis NEVER happens in the sub-agent. Extraction happens in the sub-agent. Synthesis ALWAYS happens in the orchestrator.

---

## 2. Delegation Standards

###  The Forbidden Pattern: Outcome-Based Delegation
Do NOT prompt sub-agents for outcomes that require synthesis, analysis of multiple documents, or high-level planning. 

**Examples of Forbidden Prompts:**
- *"Research the codebase and write a developer guide."*
- *"Analyze the routing logic and tell me if it's efficient."*
- *"Find the memory leak and propose a fix."*
- *"Summarize the main features of this project."*

**Why it fails**: These prompts trigger long, complex ReAct loops that are prone to timeouts, context exhaustion, and "Subagent execution failed" errors.

###  The Mandatory Pattern: Atomic Execution
Prompt sub-agents for a single, verifiable, and narrow data point.

**Examples of Atomic Prompts:**
- *"List all file paths in /src that contain the string 'AES'."*
- *"Read lines 10-50 of /src/main.ts and return the exact text."*
- *"Find the function definition for `handleChat` in `/src/sse/handlers/chat.ts`."*
- *"Check if the file `.env.example` exists in the root directory."*

**Why it succeeds**: These prompts trigger short, deterministic loops with minimal memory overhead and near-zero failure rates.

---

## 3. The Interaction Loop (The "Atomic Cycle")

To achieve a complex goal, the Orchestrator must use a series of atomic cycles:

1.  **Targeting**: Orchestrator asks Worker to find a specific file/symbol.
2.  **Extraction**: Orchestrator asks Worker to read specific lines/blocks.
3.  **Synthesis**: Orchestrator analyzes the returned data in its own context.
4.  **Iteration**: Orchestrator uses the synthesis to formulate the *next* atomic request.

**Example Workflow: Analyzing a Routing Bug**
- **Wrong**: `Explore agent` $\rightarrow$ *"Analyze the routing bug in the proxy."* $\rightarrow$ (Crash)
- **Right**: 
    - `Explore agent` $\rightarrow$ *"Find files containing 'route' in /src/lib."*
    - `Orchestrator` $\rightarrow$ (Reads list, picks `intelligentRouting.ts`)
    - `Explore agent` $\rightarrow$ *"Read lines 1-100 of intelligentRouting.ts."*
    - `Orchestrator` $\rightarrow$ (Analyzes logic, finds potential flaw)
    - `Explore agent` $\rightarrow$ *"Search for where `intelligentRouting.ts` is imported."*

---

## 4. Decision Matrix for Delegation

| Task Type | Delegate to Agent? | Requirement |
| :--- | :--- | :--- |
| **Search / Find** |  YES | Use specific keywords, return paths only. |
| **Read / Extract** |  YES | Use specific paths, line ranges, or blocks. |
| **Validate / Check** |  YES | Boolean result or specific error message. |
| **Analyze / Reason** |  NO | Perform this in the Orchestrator context. |
| **Synthesize / Write** |  NO | Perform this in the Orchestrator context. |
| **Plan / Decompose** |  NO | Perform this in the Orchestrator context. |

---

# Agent Interaction Protocol (AIP)

## 1. Core Philosophy: The CPU-Worker Model
The AI-OS is designed around a strict separation between **Cognitive Synthesis (The CPU)** and **Atomic Execution (The Worker)**.

- **The Orchestrator (CPU)**: Maintains global state, performs complex analysis, synthesizes reports, and manages the task graph.
- **The Sub-Agent (Worker)**: Performs high-speed, narrow-scope data extraction and execution.

**CRITICAL RULE**: Synthesis NEVER happens in the sub-agent. Extraction happens in the sub-agent. Synthesis ALWAYS happens in the orchestrator.

---

## 2. Delegation Standards

###  The Forbidden Pattern: Outcome-Based Delegation
Do NOT prompt sub-agents for outcomes that require synthesis, analysis of multiple documents, or high-level planning.

**Examples of Forbidden Prompts:**
- *"Research the codebase and write a developer guide."*
- *"Analyze the routing logic and tell me if it's efficient."*
- *"Find the memory leak and propose a fix."*
- *"Summarize the main features of this project."*

**Why it fails**: These prompts trigger long, complex ReAct loops that are prone to timeouts, context exhaustion, and "Subagent execution failed" errors.

###  The Mandatory Pattern: Atomic Execution
Prompt sub-agents for a single, verifiable, and narrow data point.

**Examples of Atomic Prompts:**
- *"List all file paths in /src that contain the string 'AES'."*
- *"Read lines 10-50 of /src/main.ts and return the exact text."*
- *"Find the function definition for `handleChat` in `/src/sse/handlers/chat.ts`."*
- *"Check if the file `.env.example` exists in the root directory."*

**Why it succeeds**: These prompts trigger short, deterministic loops with minimal memory overhead and near-zero failure rates.

---

## 3. The Interaction Loop (The "Atomic Cycle")

To achieve a complex goal, the Orchestrator must use a series of atomic cycles:

1.  **Targeting**: Orchestrator asks Worker to find a specific file/symbol.
2.  **Extraction**: Orchestrator asks Worker to read specific lines/blocks.
3.  **Synthesis**: Orchestrator analyzes the returned data in its own context.
4.  **Iteration**: Orchestrator uses the synthesis to formulate the *next* atomic request.

**Example Workflow: Analyzing a Routing Bug**
- **Wrong**: `Explore agent` $\rightarrow$ *"Analyze the routing bug in the proxy."* $\rightarrow$ (Crash)
- **Right**:
    - `Explore agent` $\rightarrow$ *"Find files containing 'route' in /src/lib."*
    - `Orchestrator` $\rightarrow$ (Reads list, picks `intelligentRouting.ts`)
    - `Explore agent` $\rightarrow$ *"Read lines 1-100 of intelligentRouting.ts."*
    - `Orchestrator` $\rightarrow$ (Analyzes logic, finds potential flaw)
    - `Explore agent` $\rightarrow$ *"Search for where `intelligentRouting.ts` is imported."*

---

## 4. Decision Matrix for Delegation

| Task Type | Delegate to Agent? | Requirement |
| :--- | :--- | :--- |
| **Search / Find** |  YES | Use specific keywords, return paths only. |
| **Read / Extract** |  YES | Use specific paths, line ranges, or blocks. |
| **Validate / Check** |  YES | Boolean result or specific error message. |
| **Analyze / Reason** |  NO | Perform this in the Orchestrator context. |
| **Synthesize / Write** |  NO | Perform this in the Orchestrator context. |
| **Plan / Decompose** |  NO | Perform this in the Orchestrator context. |

---

## 5. Enforcement
Any prompt that requires the sub-agent to "think," "analyze," or "summarize" is a violation of this protocol. If a sub-agent fails, the immediate remedy is to **break the prompt into smaller, atomic requests.**

---

## 6. Management of Long-Running & Large-Scale Operations

To prevent timeouts and resource exhaustion, long-running or massive tasks must be managed using the following protocols.

###  The Forbidden Pattern: Blind Retries
Do NOT attempt to re-run the exact same large-scale command after a timeout or failure. This causes "Looping Behavior" and wastes computational resources.

###  The Mandatory Patterns:

#### A. Background Execution (The "Daemon" Mode)
For operations that are expected to run for several minutes or indefinitely (e.g., installing heavy dependencies, starting servers, or mass-cloning repositories), use the `is_background: true` flag. 
- **Benefit**: Prevents the agent from hanging on a single, time-limited tool call.

#### B. Task Chunking (The "Incremental" Mode)
For large-scale file operations, directory scans, or mass-modifications, do NOT attempt the entire task in one command.
- **Action**: Break the task into small, verifiable segments (e.g., instead of `rm -rf /large_dir`, use a script that deletes files in batches of 100).
- **Verification**: Verify each chunk is complete before starting the next.

#### C. The Timeout Recovery Protocol
If a command hits a timeout, the Orchestrator must execute the following recovery sequence:
1. **Identify Progress**: Use `ls`, `find`, or `logs` to determine if the task was partially completed.
2. **Checkpointing**: If partially complete, identify the last successful state.
3. **Resumption**: Re-run the task starting from the last checkpoint (e.g., using a script that checks for existing files before cloning, like `populate-labs-v2.sh`).
4. **Escalation**: If the task repeatedly fails or hits timeouts without making progress, stop and report the obstruction to the user.
