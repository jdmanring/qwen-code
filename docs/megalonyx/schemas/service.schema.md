# Agentic Service JSON Schema

## Component Identity
The `service.schema.json` is the formal JSON Schema definition for Agentic Services. While `schema.md` provides a human-readable guide for skills, this JSON schema provides the machine-readable validation layer for service configurations.

## 🛠️ Implementation Status

**Status: Declarative**

The schema is currently used as a technical reference. Programmatic enforcement (i.e., automatic validation of `config/services/*.yaml` files against this schema) is not yet implemented in the core engine.

## Technical Specification
The schema defines a structured object with the following primary sections:

### 1. Basic Metadata
- `name`: Required string. Unique identifier for the service.
- `description`: Required string. High-level purpose.

### 2. Persona (`persona`)
- `role`: Required string. The agent's professional identity.
- `system_prompt`: Required string. The core instructions governing behavior.
- `reporting_schema`: Optional string. The required format for the agent's output.

### 3. Capabilities (`capabilities`)
- `tools`: Required array of strings. The list of permitted tools.
- `triggers`: Object containing `keywords` (array) and `file_patterns` (array) used for activation.
- `model`: String with a default of `inherit`.

### 4. Policies (`policies`)
- `risk_profile`: Enum (`Low`, `Med`, `High`, `Critical`). Defines the danger level of the agent's actions.
- `verification_level`: Enum (`Low`, `Medium`, `High`, `Critical`). Defines how strictly the output must be verified.

## Interdependencies
- **Config Validator**: Used by the system to ensure `service.yaml` files are syntactically and structurally correct before deployment.
- **Agent Loader**: Ensures that the agent has all required fields (like `system_prompt`) before being instantiated.

## Mirror Link
[Original Config: `config/schemas/service.schema.json`](../../config/schemas/service.schema.json)
