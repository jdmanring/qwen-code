# Prompt Engineering Strategy

This document defines the standards and patterns for all prompts within the `qwen_code_stack` ecosystem. The goal is to maximize reliability, reduce "empty nest" (streaming) failures, and ensure consistent behavior across the agent framework.

## 1. Core Prompting Patterns

We adopt the following industry-standard patterns to ensure high-quality agentic behavior:

### A. The ReAct Loop (Reasoning + Acting)
All agents must follow the **Reasoning $\rightarrow$ Acting $\rightarrow$ Observation** cycle.
- **Constraint**: An agent must never call a tool without first explaining *why* it is doing so in a `Thought` block.
- **Structure**:
    - `Thought`: Analysis of current state and reasoning for the next step.
    - `Action`: The specific tool call.
    - `Observation`: The result returned by the tool (handled by the system).
    - `Thought`: Analysis of the observation and determination of next steps.

### B. The Reflexion Loop (Self-Correction)
Complex tasks must employ a **Draft $\rightarrow$ Critique $\rightarrow$ Revise** cycle.
- **Implementation**: The `Developer` agent produces an implementation, and the `Reviewer` agent provides a structured critique. The `Developer` must then address every point in the critique before the task is marked as completed.

### C. Structured Chain-of-Thought (CoT)
For architectural or planning tasks, agents must use a "Step-by-Step" decomposition.
- **Pattern**:
    1. **Deconstruction**: Break the goal into atomic requirements.
    2. **Alternative Analysis**: Consider 2-3 different approaches.
    3. **Trade-off Evaluation**: Compare approaches based on complexity, performance, and maintainability.
    4. **Final Decision**: Select the optimal path with justification.

---

## 2. Prompt Architecture (The Unified Model)

To maximize token efficiency and prevent context fragmentation, Mega Code uses a **Decoupled Prompt Library**.

### The Prompt Hierarchy
Instead of monolithic prompt files, prompts are split into specialized YAML files in `config/prompts/`:
- **Agent Personas (`config/prompts/agents/`)**: Define the core identity and guidelines for a specific role (e.g., `architect.yaml`).
- **Skill Workflows (`config/prompts/skills/`)**: Define the specific sequence of steps and constraints for a specialized task (e.g., `refactor-safe.yaml`).

### Dynamic Prompt Injection
The **Control Plane** dynamically constructs the system prompt for every job:
`Final System Prompt` = `Agent Persona` + `Skill Workflow` + `Current System State (Phase/Todos)`.

This ensures the LLM only receives the context strictly necessary for the current atomic task, drastically reducing token usage and improving instruction adherence.

---

## 3. Safety and Stability Guidelines

To reduce API-side failures (e.g., safety filter triggers):
- **Neutral Phrasing**: Avoid aggressive or "demanding" language in prompts.
- **Explicit Bounds**: Clearly define what the agent *should not* do to prevent it from accidentally wandering into "forbidden" content zones.
- **Gradual Complexity**: Use few-shot examples to guide the model toward the desired output format.

## 4. Implementation Roadmap

1. [x] Audit all current agent personas against these standards.
2. [x] Migrate `prompts.json` to a YAML-based directory structure.
3. [x] Implement the Control Plane for dynamic prompt injection.
4. [x] Standardize `service.yaml` templates to include a "Reporting Schema" section.
