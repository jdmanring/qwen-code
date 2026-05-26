# Persona Blueprint Documentation

The `persona-blueprint.md` file provides the standardized structure for creating new agents within the Megalonyx. It ensures that every agent is defined by deterministic axioms and mandates rather than vague prompts.

## Blueprint Structure

### 1. Persona Identity
Defines the agent's **Role**, **Cognitive Bias**, and **Authority Level** (Standalone, Delegate, or Worker).

### 2. Operational Axioms `[M-AXIOM]`
Deterministic laws governing the agent's internal logic. These use ASCII logic symbols (`=>`, `<=>`) to define trigger-action pairs and verification contracts.

### 3. Core Mandates `[M-MANDATE]`
Absolute constraints on the agent's behavior, focusing on **Precision**, **Efficiency**, and **Symmetry**.

### 4. Tool-Chain Recipes
Standardized sequences for tool usage, typically following a `Recall` $\to$ `Analyze` $\to$ `Act` $\to$ `Ingest` workflow.

### 5. Guardrails
Explicit negative constraints ("NEVER" rules) to prevent critical failures (e.g., committing secrets).

---

## 🔗 Symmetry Link
Mirrored from: `config/templates/persona-blueprint.md`
