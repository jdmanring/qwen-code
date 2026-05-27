# Model Provider System

This document describes how model providers are configured in Qwen Code and how Megalonyx
extends the provider list.

---

## What a provider is

A provider is a service that accepts model inference requests. Qwen Code supports any service
that implements the OpenAI-compatible chat completions API, plus native Gemini API support.

The CLI does not hard-code specific models -- every model available in a session comes from the
provider configuration in `config/settings.json`.

---

## Configuration structure

Providers are configured under `modelProviders` in `settings.json`, grouped by protocol type:

```json
"modelProviders": {
  "openai": [ ... ],
  "gemini": [ ... ]
}
```

Each entry in the array describes one model:

| Field | What it controls |
|---|---|
| `id` | The model ID sent in API requests (e.g. `"gpt-4o"`) |
| `name` | Display name shown in the UI |
| `description` | One-sentence summary of when to use this model |
| `envKey` | The environment variable that holds the API key for this model |
| `provider` | Display name for the provider company |
| `baseUrl` | The API endpoint (omit for official OpenAI and Gemini endpoints) |
| `capabilities.toolCalling` | Whether this model can use tools reliably |
| `capabilities.vision` | Whether this model accepts image input |
| `capabilities.audio` | Whether this model accepts audio input |
| `generationConfig.timeout` | Request timeout in milliseconds |
| `generationConfig.contextWindowSize` | Maximum tokens in the context window |
| `generationConfig.samplingParams` | `temperature`, `top_p`, `max_tokens`, etc. |
| `stream` | Whether to use streaming responses |

---

## How the CLI loads providers

File: `packages/core/src/models/modelsConfig.ts`

The `ModelsConfig` class loads the merged settings (user + project + extension layers) and builds
a registry of available models. When a session starts, the registry maps model IDs to their
configurations.

Provider selection:
- The `--model` flag overrides the default model for the session
- The `--auth-type` flag selects which authentication method to use (corresponds to a provider type)
- The `model` section in `settings.json` sets the default model and fast model

File: `packages/cli/src/config/settings.ts` handles loading and merging the settings layers.

---

## Authentication types

The `security.auth.selectedType` field in `settings.json` sets the active auth method. Valid
values correspond to provider types configured under `modelProviders`. The CLI uses this to
determine which API key to send with requests.

Currently configured in `config/settings.example.json`: `"selectedType": "gemini"`.

---

## Megalonyx provider additions

The example file at `config/settings.example.json` includes two provider groups beyond the
qwen-code defaults:

**LongCat** -- OpenAI-compatible endpoint at `https://api.longcat.chat/openai/v1`.
Six models ranging from a lightweight flash model (`LongCat-Flash-Lite`) to a large
experimental model (`LongCat-2.0-Preview`). All use `LONGCAT_API_KEY`.

**Extended Gemini list** -- Adds Gemini 2.5/3.x models beyond what qwen-code ships,
including `gemini-2.5-pro`, `gemini-3.1-pro-preview`, and rolling aliases
(`gemini-flash-latest`, `gemini-pro-latest`). All use `GEMINI_API_KEY`.

To add a new provider, add entries to the appropriate group in `config/settings.json`.
No code changes are required.

---

## The fast model

`settings.json` has a `fastModel` field (separate from `model.name`) that selects a cheap,
fast model for operations that don't need the primary model's full capability -- routing
decisions, summaries, and similar lightweight steps. Currently set to `"LongCat-2.0-Preview"`
in the example config.

---

## What the control-plane-daemon adds

The `ModelRouter` in `apps/control-plane-daemon` uses provider and model information from
`settings.json` to make routing decisions at the application level -- assigning a specific
model to a specific job based on its intent classification and execution profile. It reads
`settings.json` at startup to know what models are available, then selects based on task
requirements rather than always using the default.

See `docs/megalonyx/control-plane-daemon.md` for details.
