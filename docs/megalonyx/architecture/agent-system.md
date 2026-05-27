 
# Architectural Mandate: Agentic Cognitive Systems

This document defines the formal requirements for the design, deployment, and operation of cognitive modules within the Megalonyx. Transitioning from "prompt-based" agents to "Axiomatic Personas" is mandatory to ensure deterministic behavior and architectural symmetry.

## 1. The Control Plane (Architectural Target)

The Control Plane is the **Target Architectural State** for agent orchestration. Its purpose is to move the system from a linear chat model to a deterministic engineering pipeline.

### [Current Implementation]
Currently, orchestration is handled by the **Primary Orchestrator**, which manages tool selection and planning in a linear flow. The "Control Plane" exists as a set of operational guidelines in `QWEN.md` rather than a programmatic enforcement layer.

### [Architectural Target]: The Deterministic Pipeline
The end-state is a programmatic Control Plane that brokers all cognitive cycles through the following pipeline:

`User Intent` => **Intent Classifier** => **Policy Engine** => **Task Decomposer** => **Job State Machine** => **Verification Engine** => `Final Result`

| Component | Functional Mandate | Constraint |
| :--- | :--- | :--- |
| **Intent Classifier** | Map request to high-level cognitive intent. | Must resolve to a registered `Persona`. |
| **Policy Engine** | Enforce tool-access boundaries. | Zero-Trust: Default all access to `OFF`. |
| **Task Decomposer** | Break intent into atomic, verifiable jobs. | Each job must have a defined `Verification Contract`. |
| **Job State Machine** | Manage lifecycle: `Pending` => `Executing` => `Verifying` => `Done`. | No state bypass permitted. |
| **Verification Engine** | Validate outcomes against the contract. | Binary result: `PASS` or `FAIL`. |

### 1.2 Recovery Axioms (Target State)
Once the Control Plane is implemented, the following recovery axioms will be programmatically enforced:
- **Retry**: `(Verification == FAIL => Inject Logs => Re-execute)` => Max 3 attempts.
- **Pivot**: `(Retry == FAIL => Generate Correction Job => Fix Root Cause)` => Must update `todo.md`.
- **Abort**: `(Critical Failure => Halt Pipeline => Escalate to User)` => Preserve state snapshot.

For the current implementation status and milestones, refer to [ROADMAP.md](../../ROADMAP.md).


---

## 2. The Axiomatic Agent Blueprint

An agent is a structured cognitive module, not a prompt. Every agent must be defined by five mandatory dimensions.

### 2.1 Dimension Matrix
| Dimension | Requirement | CSF Anchor |
| :--- | :--- | :--- |
| **Persona & Authority** | Role definition with explicit cognitive bias. | `Axiomatic Persona` |
| **Memory Profile** | Defined access to the Three-Layer Hierarchy. | `Symmetry Anchor` |
| **Tool-Chaining** | Standardized, deterministic recipes for tool use. | `Operational Law` |
| **Guardrails** | Negative constraints ("NEVER" rules). | `Hard Constraint` |
| **Output Standard** | Strict markdown template for final reports. | `Protocol Symmetry` |

### 2.2 Memory Hierarchy Access
1. **Instructional Memory**: Core mandates (The Agent's `.md` file).
2. **Semantic Memory (Cloud)**: Global architectural anchors and project laws.
3. **Semantic Memory (Local)**: Session-specific implementation details.
4. **Ephemeral Memory**: Immediate conversation context.

---

## 3. Cognitive Interaction Loop (Axioms)

To maintain cognitive consistency, all agents must adhere to the **Recall => Analyze => Act => Ingest** loop.

- **Recall**: `(Task Start => Query Semantic Memory => Retrieve Anchors)` => Prioritize Cloud over Local.
- **Analyze**: `(Retrieved Data => Synthesize with Intent => Identify Gaps)` => Must trigger `WebFetch`/`ReadFile` if gap $> 20\%$.
- **Act**: `(Validated Plan => Execute Tool-Chain Recipe => Update todo)` => Every `Edit` must be followed by a `Shell` verification.
- **Ingest**: `(New Discovery/Decision => Distill to Axiom => Commit to Cloud Memory)` => Mandatory for architectural shifts.

---

## 4. Agent Lifecycle Mandates

**Definition** => **Validation** => **Deployment** => **Optimization**

1. **Definition**: Establish persona in `../../config/agents/{name}/persona.md`.
2. **Validation**: Pass "Golden Test Cases" for guardrail adherence.
3. **Deployment**: Execute `../../install.sh` to mirror to machine state.
4. **Optimization**: Periodic review via `SYSTEM OPTIMIZER` to refine axioms based on failure logs.

---

##  Symmetry Link
This mandate governs the configuration of all agents in:
`../../config/agents/` <=> `agent-system.md`
