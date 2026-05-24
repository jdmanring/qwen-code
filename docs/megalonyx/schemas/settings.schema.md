# Settings Schema Definition

## Component Identity
`settings.schema.json` is the formal JSON Schema that validates the global `settings.json` file. It ensures that all configuration keys are present, have the correct types, and fall within allowed ranges.

## 🛠️ Implementation Status

**Status: Declarative**

The schema is currently used as a technical reference. Programmatic enforcement (i.e., automatic validation of `~/.qwen/settings.json` against this schema) is not yet implemented in the core engine.

## Technical Specification
The schema enforces the following constraints:

### 1. Memory & Tools
- `memory.enableManagedAutoMemory`: Must be a boolean.
- `tools.approvalMode`: Must be one of `["default", "yolo", "strict"]`.

### 2. Logging
- `logging.log_level`: Must be one of `["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]`.
- `logging.enable_trace`: Must be a boolean.

### 3. Model Providers
The `modelProviders` object allows dynamic keys (provider names), where each value is an array of model objects. Required fields for models include:
- `id` and `name`: Strings.
- `generationConfig`: Includes `contextWindowSize` (integer) and `samplingParams` (temperature: 0-2, top_p: 0-1).

### 4. Environment
- `env`: A flexible object allowing any string-to-string mapping for environment variables.

## Interdependencies
- **Settings Validator**: The system uses this schema to validate `settings.json` on startup. If validation fails, the system may halt or revert to defaults.
- **UI/Config Editor**: Can be used by IDEs or configuration tools to provide autocomplete and validation for `settings.json`.

## Symmetry Link
[Original Config: `config/settings.schema.json`](../../config/settings.schema.json)
