# Control Plane & Orchestration Implementation Guide: Qwen Code

This document defines the architecture and operational logic of the Qwen Code Control Plane. The Control Plane is the central orchestrator that transforms a high-level user request into a deterministic sequence of atomic, verifiable jobs.

---

## 1. Introduction: The Orchestration Layer

The Control Plane manages the high-level lifecycle of a request. It ensures that tasks are decomposed into a professional engineering pipeline with built-in verification and correction loops.

**The High-Level Flow:**  
`User Prompt` $\to$ `Intent Classification` $\to$ `Task Decomposition` $\to$ `Job Execution Loop` $\to$ `Final Aggregation`

---

## 2. The Request Lifecycle

### Step 1: Intent Classification
When a prompt is received, the `IntentClassifier` maps it to a predefined **Intent Taxonomy**. This determines the risk profile and the suggested tool chain.

**The Intent Taxonomy:**
- **Exploratory Analysis**: Read-only investigation (e.g., "How does the auth flow work?").
- **Surgical Correction**: Targeted bug fix (e.g., "Fix the null pointer in `auth.ts`").
- **Feature Synthesis**: New functionality implementation (e.g., "Add OAuth2 support").
- **Structural Evolution**: Systemic refactoring (e.g., "Migrate from Express to Fastify").
- **Adversarial Review**: Vulnerability and bottleneck search (e.g., "Find memory leaks in the cache").
- **Knowledge Sync**: Documentation alignment (e.g., "Update README to match the new API").

### Step 2: Task Decomposition
The `TaskDecomposer` breaks the classified intent into a sequence of **Atomic Jobs**. 

**The Correction Workflow:** For complex mutations (Feature/Structural), the system follows a strict engineering sequence:
`Investigate` $\to$ `Design` $\to$ `Test Plan` $\to$ `Dry-Run` $\to$ `Implement` $\to$ `Verify` $\to$ `Review`

**Decomposition Mechanism:**
- **Dynamic**: An LLM generates the job list based on the available skills and the task-specific context.
- **Static Fallback**: If dynamic decomposition fails, the system uses hardcoded templates based on the intent.

### Step 3: The Execution Loop (Act $\to$ Observe $\to$ Verify $\to$ Correct)
The `ControlPlane` executes jobs sequentially. Each job follows a strict lifecycle:

1.  **ACT**: The system resolves the `assigned_skill` and executes the job using `run_job_execution`.
2.  **OBSERVE**: The output is captured and fed into the `VerificationEngine`.
3.  **VERIFY**: The result is checked against the job's `verification_criteria` (e.g., "Tests pass").
4.  **CORRECT**: If verification fails, the system chooses a recovery path:
    - **RETRY**: Add the failure logs to the history and try again.
    - **PIVOT**: Create a new, immediate "Correction Job" to fix the specific failure before returning to the original job.
    - **ABORT**: Stop the entire job set if a critical failure is detected.

---

## 3. Specialized Execution Paths

### Slash Commands & Workflows
Requests starting with `/` bypass the `IntentClassifier` and `TaskDecomposer`. Instead, they trigger the `CommandManager`.

**Workflow Execution:**
Commands can define a Markdown-based workflow. The `execute_workflow` engine parses these steps:
- **Agent Spawning**: "Spawn the [agent] agent" triggers the creation of a specialized sub-session.
- **Todo Operations**: `TODO_OP: add/list/done` allows the workflow to manage a task list dynamically.
- **General Execution**: Standard steps are routed through the general orchestrator.

---

## 4. Developer's Guide to Extension

The Control Plane is designed to be extensible without modifying the core loop.

### Adding a New Intent
To support a new type of request:
1. Update the `INTENT_TAXONOMY` in `intent_classifier.py`.
2. Define the `description`, `goal`, `tool_chain`, and `risk_profile`.
3. (Optional) Add a static decomposition template in `task_decomposer.py` for fallback.

### Refining Decomposition Logic
To change how the system breaks down tasks:
- Modify the `system_prompt` in `TaskDecomposer.decompose`.
- Update the "Correction Workflow" instructions to include new required steps (e.g., adding a "Security Audit" step before "Review").

### Extending Verification
To add new ways to verify jobs:
- Implement a new `VerificationContract` (e.g., `PerformanceContract`).
- Register the contract in `ControlPlane.__init__` using `self.ve.register_contract()`.

---

## 5. Verification Checklist

- [ ] **Intent Alignment**: Does the new intent map to the correct risk profile?
- [ ] **Pipeline Integrity**: If a mutation is involved, does the decomposition follow the Investigate $\to$ Verify sequence?
- [ ] **Verification Criteria**: Does every job in the sequence have a binary, verifiable success condition?
- [ ] **Fallback Stability**: Does the static template provide a reasonable sequence if the LLM fails to decompose?
- [ ] **Workflow Validity**: Do slash commands correctly reference existing agents and `TODO_OP` syntax?
