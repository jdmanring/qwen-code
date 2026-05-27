 
# VerificationEngine Architectural Documentation

## 1. Identity & Role
The `VerificationEngine` is the **Quality Gatekeeper** of the Execution Triangle. Its role is to ensure that no job is marked as `completed` unless its output strictly adheres to the defined contract and meets the required confidence threshold. 

It decouples the "execution" of a task from the "verification" of its result, preventing the "hallucination propagation" common in multi-agent systems.

## 2. Core Logic & Algorithm

### Contract-Based Evaluation
The engine operates on a registry of `BaseContract` objects. Each `job_type` (e.g., `mutation`, `discovery`) can be associated with a specific contract implementation.

The verification flow is as follows:
1. **Contract Lookup**: The engine retrieves the contract associated with the `job_type`.
2. **Evaluation**: The `contract.evaluate(output_data, context)` method is called, which performs the actual validation (e.g., running a test suite, checking for file existence, or LLM-based auditing).
3. **Confidence Thresholding**: The result is compared against the `min_confidence` (default 0.8). 

### Integration with State Management
The `VerificationEngine` does not just return a result; it actively drives the state of the system. If the evaluation is successful and confidence is sufficient, it commands the `JobStateManager` to transition the job to `completed`. Otherwise, it marks the job as `failed`.

### Default Behavior
If no contract is registered for a specific job type, the engine defaults to a "Permissive Mode":
- `is_success = True`
- `confidence = 0.5`
- `logs = "No contract defined..."`
This allows the system to continue operating while highlighting gaps in the verification suite.

## 3. Interface Specification

### Inputs
| Source | Parameter | Type | Description |
| :--- | :--- | :--- | :--- |
| Orchestrator | `job_id` | `str` | The ID of the job to verify. |
| Orchestrator | `job_type` | `str` | The category of work, used to select the contract. |
| Agent | `output_data` | `Any` | The actual result produced by the agent. |
| Orchestrator | `context` | `dict` | Additional environment or state data. |

### Outputs
| Destination | Parameter | Type | Description |
| :--- | :--- | :--- | :--- |
| Orchestrator | `VerificationResult`| `dataclass` | Contains `is_success`, `confidence`, `logs`, and `suggested_action` (`RETRY`, `PIVOT`, `ABORT`). |
| JobStateManager| `update_job_status` | `void` | Side-effect: Transitions job to `completed` or `failed`. |

## 4. State Transitions
The `VerificationEngine` is the primary driver for the final transitions in the job lifecycle:

- **Evaluation Pass** $\to$ `JobStateManager.update_job_status(job_id, "completed")`
- **Evaluation Fail** $\to$ `JobStateManager.update_job_status(job_id, "failed")`

## 5. Critical Dependencies
- **`JobStateManager`**: Required to persist the outcome of the verification.
- **`BaseContract`**: The abstract base class that defines the interface for all verification logic.
- **`settings.json`**: Used for global verification configurations.
