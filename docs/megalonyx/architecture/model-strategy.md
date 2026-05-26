# 🧠 Model Strategy: The Tiered Reasoning Engine

This document describes the model hierarchy and routing strategy used by the Runtime Stack to balance deep architectural reasoning with high-throughput execution.

## ⚖️ Tiered Model Architecture

The system employs a dual-track model strategy to optimize for both quality and latency.

### 1. The Primary Model (The Architect)
**Role**: High-stakes reasoning, complex task decomposition, and final synthesis.
- **Configuration**: Defined in `settings.json` under the `model` object.
- **Use Case**: 
    - Initial project planning.
    - Complex refactoring of core logic.
    - Final verification of security-critical changes.
- **Behavior**: Prioritizes depth, accuracy, and strict adherence to `QWEN.md`.

### 2. The Fast Model (The Worker)
**Role**: Atomic task execution, bulk generation, and rapid iterations.
- **Configuration**: Defined in `settings.json` as the `fastModel` key.
- **Use Case**: 
    - Running linter fixes.
    - Generating boilerplate code.
    - Performing simple file reads/searches.
- **Behavior**: Prioritizes speed and token efficiency.

---

## 🚦 Routing & Selection Logic

The system does not use a single model for all tasks. Instead, it uses a dynamic routing mechanism.

### The Intent Classifier
Routing is coordinated by the `ControlPlane` via the `IntentClassifier` (`packages/core/src/route.py`).

1. **Analysis**: When a prompt is received, the `IntentClassifier` analyzes the request to determine the "cognitive load."
2. **Job Contract**: The classifier returns a `job_contract` which specifies the model requirement:
    - `inherit`: Use the primary model defined in `settings.json`.
    - `fast`: Route the task to the `fastModel`.
    - `specialized`: Route to a specific model optimized for a task (e.g., a coding-specific model).

### Fallback Mechanism
To ensure system resilience, `skill_bridge.py` implements a `FALLBACK_MODELS` map. If the primary provider fails or returns a critical error, the system automatically pivots to a pre-defined fallback model to maintain continuity.

---

## ⚙️ Configuration Mapping

| Setting | Location | Description |
| :--- | :--- | :--- |
| `model.name` | `settings.json` | The ID of the Primary Model. |
| `fastModel` | `settings.json` | The ID of the Fast Model. |
| `provider` | `settings.json` | The API provider (e.g., Google, LongCat). |
| `api_base` | `settings.json` | The endpoint URL for the provider. |
