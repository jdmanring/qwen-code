# settings.example.json

`config/settings.example.json` is the template for the Qwen Code runtime configuration file. Copy it
to `config/settings.json` (never commit the live copy — it contains real API keys) and fill in your
credentials.

## Setup

```bash
cp config/settings.example.json ~/.config/qwen/settings.json
# Edit ~/.config/qwen/settings.json — review model providers, set auth type.
# The $VARNAME values in the env block are references, not placeholders — they read from your shell environment.
```

## Sections

### `env`

Holds API keys for every external service. Each value is a reference to an environment variable
(`"$VARIABLE_NAME"`). The example file never contains real keys. The services that consume them:

| Key | Service |
|---|---|
| `VLLM_API_KEY` | Local vLLM inference server |
| `QDRANT_LOCAL_URL` | Local Qdrant vector database (default: `http://localhost:6333`) |
| `QDRANT_CLOUD_URL` | Qdrant Cloud instance (optional) |
| `QDRANT_API_KEY` | Qdrant Cloud authentication |
| `TAVILY_API_KEY` | Tavily internet search MCP server |
| `OPENAI_API_KEY` | OpenAI-compatible providers |
| `GITHUB_TOKEN` | GitHub MCP server and Copilot |
| `GEMINI_API_KEY` | Google Gemini models and embedding |
| `GROQ_API_KEY` | Groq inference |
| `OPENROUTER_API_KEY` | OpenRouter multi-provider routing |
| `NVIDIA_API_KEY` | NVIDIA NIM inference |
| `LONGCAT_API_KEY` | LongCat inference (primary provider) |
| `MISTRAL_API_KEY` | Mistral inference |

### `modelProviders`

Defines available language models grouped by provider type (`openai`, `gemini`). Each entry
specifies the model ID, display name, which API key it uses, its base URL, capabilities
(tool calling, vision, audio), generation parameters (temperature, context window, max tokens),
and streaming preference.

Add new models here when you want them available for selection. The `ExecutionProfileSelector`
in `apps/control-plane-daemon` uses these entries to route tasks to the appropriate model.

### `mcpServers`

Defines which MCP servers the agent can call and how to start them:

| Key | What it starts |
|---|---|
| `filesystem` | Node.js filesystem MCP server (read/write local files) |
| `memory` | Megalonyx memory MCP server (`packages/agent-memory`) |
| `github` | GitHub MCP server (issues, PRs, code search) |
| `internet-search` | Tavily web search MCP server |
| `code-index` | Code indexing MCP server |

### `model`

Sets the default model name used when no execution profile specifies one, the maximum number
of session turns (`-1` = unlimited), and context compression behavior.

### `fastModel`

The model used for quick/cheap operations like summaries and routing decisions.

### `logging`

Controls where the agent writes its log file, the log level, and whether trace-level output
is enabled.

### `security.auth.selectedType`

Sets the active authentication method (`gemini`, `openai`, etc.). Must match a provider
defined in `modelProviders`.

## What not to commit

`~/.config/qwen/settings.json` (the live file) must never be committed — it lives outside the repo tree.
Only `config/settings.example.json` is tracked. The live file is deployed by the installer.
