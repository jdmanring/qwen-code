 
# TaskDecomposer Architectural Documentation

## 1. Identity & Role
The `TaskDecomposer` serves as the **Strategic Planner** within the Execution Triangle. Its primary purpose is to translate a high-level user intent (encoded in a Job Contract) into a deterministic, sequential, and atomic set of executable jobs. 

It transforms an ambiguous goal into a "Surgical Pipeline," ensuring that no mutation (code change) occurs without prior discovery and subsequent verification.

## 2. Core Logic & Algorithm

### Dynamic LLM Decomposition
The `TaskDecomposer` primarily utilizes a Large Language Model (LLM) to perform semantic decomposition. The process follows these steps:
1. **Skill Discovery**: The component scans `config/prompts/agents/*.yaml` to build a real-time registry of available agent personas and their capabilities.
2. **Contextual Prompting**: It constructs a system prompt that enforces the **UNIX Philosophy** (do one thing well) and mandates a specific pipeline for feature development:
   `Investigate` $\to$ `Design` $\to$ `Test Plan` $\to$ `Dry-Run` $\to$ `Implement` $\to$ `Verify` $\to$ `Review`.
3. **JSON Synthesis**: The LLM outputs a structured list of jobs, each containing a description, assigned skill, job type, and binary verification criteria.

### Static Fallback Mechanism
To ensure system robustness, the `TaskDecomposer` implements a template-based fallback. If the LLM call fails or returns invalid JSON, the system maps the `intent` to predefined archetypes:
- **Exploratory Analysis**: Discovery $\to$ Analysis $\to$ Synthesis.
- **Surgical Correction**: Isolation $\to$ Mutation $\to$ Verification.
- **Feature Synthesis**: Discovery $\to$ Analysis $\to$ Planning $\to$ Verification (Dry-Run) $\to$ Mutation $\to$ Verification $\to$ Review.

### Job Enrichment
Regardless of the source (LLM or Template), the decomposer enriches each job with:
- **Unique Job ID**: Derived from the intent and sequence index.
- **Dependency Graph**: Automatically assigns all preceding jobs in the sequence as dependencies.
- **Initial State**: Sets status to `pending`.

## 3. Interface Specification

### Inputs
| Source | Parameter | Type | Description |
| :--- | :--- | :--- | :--- |
| Orchestrator | `job_contract` | `dict` | Contains `intent` (e.g., "Feature Synthesis") and `original_prompt`. |
| System | `settings.json` | `file` | Provides LLM model configuration and environment variables. |

### Outputs
| Destination | Parameter | Type | Description |
| :--- | :--- | :--- | :--- |
| JobStateManager | `enriched_jobs` | `list[dict]` | A sequence of atomic jobs with IDs, skills, dependencies, and verification criteria. |

## 4. State Transitions
The `TaskDecomposer` is largely stateless. However, it defines the initial state for the rest of the pipeline:
- **Input**: `User Intent` $\to$ **Process**: `Decompose()` $\to$ **Output**: `JobSet {status: pending}`.

## 5. Critical Dependencies
- **`litellm`**: Used for provider-agnostic LLM communication.
- **`PyYAML`**: Used to parse agent persona files in the config directory.
- **`settings.json`**: Critical for model selection and API authentication.
