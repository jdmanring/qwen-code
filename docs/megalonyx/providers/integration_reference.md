| AI PROVIDER INTEGRATION REFERENCE           |
| QWEN CODE PROJECT -- FREE API ACCESS MATRIX |
| Updated: 2026-05-11                         |


| PURPOSE                                                                  |


Reference for integrating AI providers into Qwen Code ecosystem:
- inference providers
- routing layers
- search/RAG systems
- tooling/IDE platforms
- hybrid BYOK systems


| SCOPE CLARIFICATION                                                     |


1. TRUE INFERENCE PROVIDERS
   - host models + generate tokens

2. ROUTING / AGGREGATION LAYERS
   - forward requests across providers

3. TOOLING / IDE PLATFORMS
   - require external inference (BYOK)

4. RETRIEVAL / SEARCH SYSTEMS
   - not LLM inference


| PROVIDER SUMMARY MATRIX                                                 |


+----------------+----------------+----------------+----------------------+----------------------+
| Provider       | Category       | Free API       | Auth Method          | API Standards        |
+----------------+----------------+----------------+----------------------+----------------------+
| Hugging Face   | Inference Hub  | Yes            | Token + OAuth        | OpenAI (partial)     |
| Tavily         | Retrieval      | Limited        | API Key              | Custom REST          |
| OpenAI         | Inference      | No             | API Key + OAuth      | OpenAI Native        |
| OpenRouter     | Routing Layer  | Yes            | API Key              | OpenAI Compatible    |
| Groq           | Inference      | Yes            | API Key              | OpenAI Compatible    |
| NVIDIA NIM     | Inference      | Yes            | API Key + Login      | OpenAI Compatible    |
| LongCat        | Inference      | Yes            | API Key              | Dual (OpenAI + Anthropic) |
| Mistral AI     | Inference      | Yes            | API Key              | OpenAI Compatible    |
| Cerebras AI    | Inference      | Yes            | API Key              | OpenAI Compatible    |
| Gemini         | Inference      | Yes            | API Key + OAuth      | Google GenAI Native  |
| Pollinations   | Inference      | Yes            | None / Optional      | Custom REST          |
| GitHub Models  | Inference Hub  | Yes            | GitHub Token         | OpenAI Compatible    |
| Quoder AI      | IDE / BYOK     | Limited        | OAuth + External Key | External Providers   |
| Kiro AI        | IDE / BYOK     | BYOK           | OAuth + External Key | OpenAI / Bedrock     |
+----------------+----------------+----------------+----------------------+----------------------+


| QUICK ACCESS LINKS (SIGNUP / DASHBOARD)                                 |


+----------------+----------------------------------------------+
| Provider       | Access URL                                   |
+----------------+----------------------------------------------+
| Hugging Face   | https://huggingface.co/join                  |
| Tavily         | https://app.tavily.com                       |
| OpenAI         | https://platform.openai.com                  |
| OpenRouter     | https://openrouter.ai/signup                 |
| Groq           | https://console.groq.com                     |
| NVIDIA NIM     | https://build.nvidia.com                     |
| LongCat        | https://longcat.chat/platform                |
| Mistral AI     | https://console.mistral.ai                   |
| Cerebras AI    | https://inference.cerebras.ai                |
| Quoder AI      | https://app.quoder.ai                        |
| Pollinations   | https://pollinations.ai                      |
| Gemini         | https://aistudio.google.com                  |
| GitHub Models  | https://github.com/marketplace/models        |
| Kiro AI        | https://kiro.dev                             |
+----------------+----------------------------------------------+


| COMPATIBLE INFERENCE ENDPOINTS                                          |


+--------------------+------------------------------------------+
| Provider           | OpenAI-Compatible Base URL               |
+--------------------+------------------------------------------+
| Groq               | https://api.groq.com/openai/v1           |
| OpenRouter         | https://openrouter.ai/api/v1             |
| Cerebras AI        | https://api.cerebras.ai/v1               |
| NVIDIA NIM         | https://integrate.api.nvidia.com/v1      |
| Mistral AI         | https://api.mistral.ai/v1                |
| LongCat            | https://api.longcat.chat/openai          |
+--------------------+------------------------------------------+

+--------------------+------------------------------------------+
| Provider           | Anthropic-Compatible Base URL            |
+--------------------+------------------------------------------+
| Anthropic          | https://api.anthropic.com/v1/messages    |
| Vercel AI Gateway  | https://ai-gateway.vercel.sh             |
| LM Studio          | http://localhost:1234                    |
| Ollama             | http://localhost:11434                   |
| DeepSeek           | /anthropic-compatible (implementation varies) |
| LongCat            | https://api.longcat.chat/anthropic       |
+--------------------+------------------------------------------+

IMPORTANT CORRECTION NOTES:
- Anthropic compatibility is NOT universal across providers
- Only providers explicitly exposing /v1/messages or documented schema parity qualify

+--------------------+--------------------------------------------------+
| Provider           | Gemini-Compatible Base URL                       |
+--------------------+--------------------------------------------------+
| Google Gemini      | https://generativelanguage.googleapis.com/v1beta |
+--------------------+--------------------------------------------------+


| PROVIDER ROLE DEFINITIONS                                               |


INFERENCE PROVIDERS
-------------------
- Groq
- Gemini
- Mistral AI
- Cerebras AI
- NVIDIA NIM
- LongCat
- Hugging Face (inference endpoints)
- Pollinations

ROUTING / AGGREGATION LAYERS
----------------------------
- OpenRouter

INFERENCE HUBS (NOT ROUTERS)
----------------------------
- GitHub Models

SEARCH / RETRIEVAL
------------------
- Tavily

IDE / TOOLING / BYOK
--------------------
- Quoder AI
- Kiro AI


| KEY ARCHITECTURAL CORRECTION                                             |


LONGCAT CLASSIFICATION (IMPORTANT)
----------------------------------
LongCat is a TRUE dual-interface provider:

- OpenAI-compatible endpoint: YES (documented)
- Anthropic-compatible endpoint: YES (documented)
- Both endpoints are first-class, not proxy wrappers

Source confirmation:
- LongCat API docs explicitly define both /openai and /anthropic surfaces
- Same API key works across both endpoints


| RECOMMENDED QWEN CODE ARCHITECTURE                                      |


CORE PRINCIPLE
--------------
Qwen Code = ORCHESTRATION BRAIN

Providers = PLUG-IN EXECUTION LAYERS

PRIMARY INFERENCE
-----------------
- Groq (speed)
- Gemini (reasoning + context)
- LongCat (dual-protocol agent execution)

ROUTING
-------
- OpenRouter

OPEN MODEL ECOSYSTEM
--------------------
- Hugging Face
- NVIDIA NIM
- Mistral AI
- Cerebras AI

RETRIEVAL
---------
- Tavily

TOOLING LAYER (NON-INFERENCE)
----------------------------
- Kiro AI
- Quoder AI
- GitHub Models


| END                                                                       |
