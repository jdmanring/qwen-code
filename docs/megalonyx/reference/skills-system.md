# Unified Agentic Services Technical Reference

## Overview
In Mega Code, a **Service** is a unified agentic capability. Unlike legacy skills, a Service consolidates the **Persona**, **Configuration**, and **Documentation** into a single atomic unit. This ensures that the agent's identity, the tools it is permitted to use, and the workflow it must follow are always synchronized.

## Anatomy of a Service
### File Structure
Each service resides in its own directory within `config/services/`.
```text
config/services/<service-name>/
├── service.yaml   (Persona, Triggers, and Tool-set)
└── README.md      (Detailed Workflow and Documentation)
```

### `service.yaml` Schema
The `service.yaml` file defines the operational parameters of the agent.

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | The unique identifier for the service. |
| `description` | `string` | A high-level summary used by the Intent Classifier for discovery. |
| `persona` | `object` | Contains the `role` and `system_prompt`. This defines the agent's cognitive identity. |
| `capabilities` | `object` | Defines the `triggers` (keywords) and `tools` (whitelist of permitted MCP tools). |
| `policies` | `object` | Defines the `risk_profile` and `verification_level` for the Control Plane. |

### `README.md` (The Workflow)
The `README.md` serves as the human-readable and AI-accessible specification of the service's internal logic. It typically includes:
- **Objective**: The primary goal of the service.
- **Step-by-Step Workflow**: The exact sequence of actions the agent must take.
- **Constraints**: Hard boundaries and "Never" rules.
- **Reporting Schema**: The required format for the final output.

## Control Plane Integration
Services are not invoked in isolation; they are orchestrated by the **Control Plane**.

### The Execution Pipeline
When a user prompt is received, the system follows this flow:
1. **Intent Classification**: The prompt is mapped to a specific Service (e.g., `refactor-safe`).
2. **Policy Enforcement**: The `Policy Engine` checks the service's `policies` to restrict tool access (e.g., a read-only service cannot call `edit`).
3. **Dynamic Decomposition**: The `TaskDecomposer` breaks the intent into a sequence of atomic jobs, assigning each to a specific Service.
4. **Verification Gate**: Every job must pass a **Verification Contract** (e.g., `MutationContract`) before the pipeline progresses.
5. **Autonomous Recovery**: If verification fails, the system triggers a `RETRY` or `PIVOT` (creating a correction job) to self-heal.

## Prompt Optimization
To maximize token efficiency, the actual system prompts are stored as individual YAML files in `config/prompts/`.
- **Agents**: `config/prompts/agents/{name}.yaml`
- **Skills**: `config/prompts/skills/{name}.yaml`

This allows the orchestrator to load only the necessary prompt for the current job, rather than the entire library.

## Current Service Library
The following services are bundled with the stack:

| Service | Purpose | Key Goal |
| :--- | :--- | :--- |
| **codebase-mapper** | Semantic mapping of foreign codebases | Architecture maps and data flow. |
| **commit** | Professional git commit management | Atomic, Conventional Commits. |
| **doc-sync** | Documentation synchronization | Eliminates "doc rot". |
| **refactor-safe** | Systemic structural changes | Large-scale migrations with 0% regression. |
| **review** | Professional code audit | Identification of security holes and flaws. |
| **root-cause-hunter** | Bug isolation | Rapid movement from logs to line of failure. |
| **test-coverage-max** | Edge-case test generation | Elimination of "dark logic". |
