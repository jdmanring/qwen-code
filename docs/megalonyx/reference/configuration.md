# Technical Specification: System Configuration

This specification defines the configuration architecture of the Qwen Code project. The system utilizes a dual-tier strategy to decouple sensitive infrastructure secrets from operational orchestration rules.

## 1. Configuration Hierarchy

The system resolves configuration using the following strict precedence (Highest $\to$ Lowest):

1. **Runtime Overrides**: CLI flags or environment-specific injections.
2. **`settings.json`**: Central orchestration for model routing and system behavior.
3. **`.env` File**: Infrastructure endpoints and sensitive API credentials.
4. **System Defaults**: Hardcoded fallbacks within the `core` package.

---

## 2. Environment Variable Matrix (`.env`)

Environment variables are restricted to sensitive credentials and infrastructure connectivity.

### 2.1 API Credentials
| Variable | Requirement | Default | Purpose |
| :--- | :---: | :---: | :--- |
| `GEMINI_API_KEY` | Recommended | - | Google Gemini Inference |
| `OPENAI_API_KEY` | Optional | - | OpenAI Compatible Endpoints |
| `ANTHROPIC_API_KEY`| Optional | - | Anthropic Claude Inference |
| `OPENROUTER_API_KEY`| Optional | - | Model Aggregator Access |
| `GROQ_API_KEY` | Optional | - | High-Speed Inference |
| `MISTRAL_API_KEY` | Optional | - | Mistral AI Inference |
| `NVIDIA_API_KEY` | Optional | - | NVIDIA NIM Endpoints |
| `TAVILY_API_KEY` | Recommended | - | Search Engine Integration |
| `GITHUB_TOKEN` | **Required** | - | GitHub API Operations |
| `HF_TOKEN` | Optional | - | HuggingFace Model Access |

### 2.2 Infrastructure
| Variable | Requirement | Default | Purpose |
| :--- | :---: | :---: | :--- |
| `QDRANT_LOCAL_URL` | Local Only | `http://localhost:6333` | Local Vector Store |
| `QDRANT_CLOUD_URL` | Cloud Only | - | Managed Vector Store |
| `QDRANT_API_KEY` | Conditional | - | Vector Store Authentication |

---

## 3. Settings Orchestration (`settings.json`)

The `settings.json` file governs the runtime behavior of the Orchestrator.

### 3.1 Memory Domain
- `enableManagedAutoMemory` (bool): Automates context commitment to long-term memory.
- `policy` (object):
    - `cloud_signals` (array): Keywords triggering **Cloud Tier** storage (e.g., `"architecture"`, `"policy"`).
    - `noise_words` (array): Filter list for trivial entry rejection.
    - `dedup_window_size` (int): Bounded hash window for redundancy prevention.

### 3.2 Tooling Domain
- `approvalMode` (enum):
    - `default`: Prompt for destructive actions.
    - `yolo`: Zero-confirmation execution.
    - `strict`: Mandatory confirmation for all calls.

### 3.3 General & UI Domain
- `language` (string): Primary system prompt language (e.g., `"en"`).
- `accessibility.enableLoadingPhrases` (bool): Toggles streaming status indicators.

---

## 4. Model Provider Schema

Each provider definition must adhere to the following property matrix:

| Property | Type | Requirement | Description |
| :--- | :--- | :---: | :--- |
| `id` | string | **Required** | Unique routing identifier. |
| `name` | string | **Required** | UI Display Label. |
| `envKey` | string | **Required** | Linked `.env` variable key. |
| `provider` | string | **Required** | Provider category (e.g., `OpenRouter`). |
| `baseUrl` | string | **Required** | API Endpoint. |
| `capabilities` | object | **Required** | `toolCalling`, `vision`, `reasoning`, `ocr` (booleans). |
| `generationConfig` | object | **Required** | `timeout`, `contextWindowSize`, `samplingParams`. |

### 4.1 Sampling Parameters
- `temperature` (float): Randomness control ($0.0 = \text{Deterministic}$, $1.0+ = \text{Creative}$).
- `top_p` (float): Nucleus sampling threshold.
- `max_tokens` (int): Hard output limit.

---

## 🔗 Mirror Link
This specification mirrors the runtime configuration in:
`../../config/settings.json` $\leftrightarrow$ `configuration.md`
