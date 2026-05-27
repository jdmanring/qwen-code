#  Algorithmic Standard for Mega Code Skills

## 1. Core Philosophy: Protocol over Persona
In Mega Code, a **Skill** is not a character description or a set of behavioral suggestions. It is a **deterministic protocol**. The goal is to move from "LLM intuition" to "Algorithmic Execution."

**The Mandate**: If a skill can be described as a sequence of steps, it MUST be implemented as a sequence of steps.

---

## 2. The Unix Layering Model
To ensure modularity and reliability, every skill must be decomposed into three distinct layers. No layer should perform the work of another.

### A. The Planner (The "What" and "When")
The Planner is the orchestrator. It does not execute tools; it defines the sequence of execution.
- **Responsibility**: Decomposing the high-level goal into atomic, verifiable jobs.
- **Implementation**: Defined in the `SKILL.md` as the "Deterministic Algorithm."
- **Unix Parallel**: A `Makefile` or a `bash script`.

### B. The Executor (The "How")
The Executor is the atomic worker. It performs one specific action and returns a raw result.
- **Responsibility**: Interfacing with the environment via MCP tools or specialized sub-agents.
- **Implementation**: MCP tools (e.g., `read_file`, `grep_search`) or "Atomic" sub-agents.
- **Unix Parallel**: `grep`, `sed`, `ls`, `curl`.

### C. The Verifier (The "Is it correct?")
The Verifier is the quality gate. It ensures the Executor's output satisfies the requirements.
- **Responsibility**: Validating the output against a predefined "Output Contract."
- **Implementation**: Control Plane Verification Engine / Verification Contracts.
- **Unix Parallel**: `diff`, `test`, `checksum`.

---

## 3. Mandatory `SKILL.md` Schema
Every skill in `config/skills/` must adhere to this exact structure. Any skill missing these sections is considered non-compliant.

### 1. Objective
A single, concise sentence defining the "Definition of Done."
*Example: "Perform a professional security audit of the provided diff and identify all critical vulnerabilities."*

### 2. Deterministic Algorithm
A numbered list of absolute steps. Each step must follow the format:
`Step [N]: [Action] using [Tool] $\rightarrow$ [Expected Output]`
*Example: "Step 1: Identify changed files using `git diff --name-only` $\rightarrow$ List of target files."*

### 3. Hard Constraints
Explicit "Never/Always" rules that override LLM intuition.
*Example: "NEVER report a bug without providing the exact line number and a theoretical trigger input."*

### 4. Output Contract
A strict markdown template for the final report.
*Example: "The final report MUST contain a 'CRITICAL FINDINGS' section and a 'CONFIDENCE SCORE' (0.0-1.0)."*

---

## 4. Compliance Checklist
Before a skill is deployed, it must pass this check:
- [ ] Does it have a clear, single Objective?
- [ ] Is the algorithm a numbered list of deterministic steps?
- [ ] Are the tools used in each step explicitly named?
- [ ] Does it have at least three Hard Constraints?
- [ ] Is there a strict Output Contract template?
- [ ] Is the persona secondary to the process?
