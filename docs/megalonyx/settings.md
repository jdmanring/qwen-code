# System Settings

The `settings.json` file contains the core configuration for the Megalonyx, including memory management, tool approval modes, localization, logging, and model provider definitions.

## Key Configuration Sections

###  Memory
- `enableManagedAutoMemory`: Toggles the automated memory management system.

###  Tools
- `approvalMode`: Defines how tool execution is approved (e.g., `default`, `yolo`).

###  General
- `language`: The primary system language.
- `outputLanguage`: The language used for agent responses.

###  Logging
- `log_level`: Severity level for system logs (e.g., `DEBUG`, `INFO`, `ERROR`).
- `log_path`: Absolute path to the system log file.
- `enable_trace`: Enables detailed execution tracing for debugging.

###  Environment Variables (`env`)
Contains mappings to environment variables for various API keys (OpenAI, Gemini, Tavily, etc.) used by the model providers.

###  Model Providers
Defines a catalog of available LLMs grouped by provider (e.g., `openai`, `gemini`). Each model entry includes:
- `id`: Unique identifier for the model.
- `name`: Human-readable name.
- `description`: Use-case guidance for the model.
- `capabilities`: Boolean flags for `reasoning`, `coding`, `toolCalling`, `vision`, and `audio`.
- `generationConfig`: Parameters for `timeout`, `contextWindowSize`, and `samplingParams` (temperature, top_p, max_tokens).

###  MCP Servers
Configuration for Model Context Protocol (MCP) servers, specifying the command and arguments required to launch them (e.g., `filesystem`, `memory`, `github`).

###  Model Defaults
- `model.name`: The default model used by the system.
- `fastModel`: A lightweight model used for high-throughput, low-latency tasks.
