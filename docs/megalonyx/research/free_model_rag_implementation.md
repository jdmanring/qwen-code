| QWEN CODE -- VERIFIED FREE MODEL + RAG IMPLEMENTATION PLAN                   |
| STATUS: NORMALIZED AGAINST VERIFIED API BEHAVIOR                             |
| TARGET: Qwen Code settings.json                                              |
| DATE: 2026-05-12                                                             |


OBJECTIVE
---------
Create a stable multi-provider free-inference environment for Qwen Code with:

- working model IDs
- correct compatibility sections
- correct endpoint handling
- valid provider separation
- remote agent orchestration support
- free-tier utilization
- stable RAG architecture
- minimal breakage risk
- scalable autonomous agent support

The following reflects the CURRENT VERIFIED MODEL SET and WORKING
PROVIDER BEHAVIOR.


| PROVIDER COMPATIBILITY LAYOUT                                                |


OPENAI-COMPATIBLE SECTION
-------------------------
These belong under:

"modelProviders": {
  "openai": []

Providers:
- Groq
- OpenRouter
- NVIDIA NIM
- LongCat
- Mistral AI
- Cerebras
- Local vLLM/OpenAI-compatible servers
- Pollinations
- GitHub Models (OpenAI compatibility)
- Quoder/OpenAI-compatible gateways

These expose OpenAI-style chat/completions APIs.


+------------------------------------------------------------------------------+

GEMINI SECTION
--------------
These belong under:

"modelProviders": {
  "gemini": []

Providers:
- Gemini API
- Gemma models served through Google AI Studio

Do NOT place Gemini/Gemma models under OpenAI.


| VERIFIED WORKING MODEL INVENTORY                                             |


 GROQ
-------
Base URL:
https://api.groq.com/openai/v1

Compatible Section:
openai

Verified Models:
- meta-llama/llama-4-scout-17b-16e-instruct
- qwen/qwen3-32b
- openai/gpt-oss-120b
- openai/gpt-oss-20b

Notes:
- Groq model names are strict.
- Wrong aliases immediately produce 404 errors.
- Excellent low-latency orchestration provider.
- Best used for fast worker agents.


+------------------------------------------------------------------------------+

 OPENROUTER
-------------
Base URL:
https://openrouter.ai/api/v1

Compatible Section:
openai

Verified Models:
- openai/gpt-oss-120b:free
- openai/gpt-oss-20b:free
- qwen/qwen3-coder-480b-a35b-instruct:free
- openrouter/auto

Notes:
- :free suffix matters.
- openrouter/auto is an excellent fallback router.
- Good overflow provider when others rate-limit.
- Best emergency fallback provider.


+------------------------------------------------------------------------------+

 NVIDIA NIM
-------------
Base URL:
https://integrate.api.nvidia.com/v1

Compatible Section:
openai

Verified Models:
- qwen/qwen3-coder-480b-a35b-instruct
- deepseek-ai/deepseek-v4-pro
- deepseek-ai/deepseek-v4-flash
- moonshotai/kimi-k2-instruct
- nvidia/llama-3.1-nemotron-ultra-253b-v1
- nvidia/nemotron-3-super-120b-a12b

Notes:
- NVIDIA IDs are namespace-sensitive.
- Missing vendor prefixes often fail.
- Best heavy-reasoning provider in free tier.


+------------------------------------------------------------------------------+

 LONGCAT
----------
Base URL:
https://api.longcat.chat/openai/v1

Compatible Section:
openai

Verified Models:
- LongCat-Flash-Lite
- LongCat-Flash-Chat
- LongCat-Flash-Thinking-2601
- LongCat-Flash-Omni-2603
- LongCat-2.0-Preview

CRITICAL:
---------
Do NOT use anthropic compatibility mode in Qwen Code for LongCat.

Reason:
Qwen Code appends:
  /v1/messages

LongCat anthropic endpoint already includes:
  /anthropic/v1

Result:
  /anthropic/v1/v1/messages

This causes:
  404 Not Found

Therefore:
USE ONLY OPENAI MODE FOR LONGCAT.

Correct:
https://api.longcat.chat/openai/v1

Incorrect:
https://api.longcat.chat/anthropic/v1

Notes:
- LongCat is ideal for huge-token background agents.
- Excellent for summarization and autonomous loops.
- Best large-volume free token provider.


+------------------------------------------------------------------------------+

 MISTRAL AI
-------------
Base URL:
https://api.mistral.ai/v1

Compatible Section:
openai

Verified Models:
- codestral-latest
- devstral-latest
- devstral-small-latest
- magistral-medium-latest
- ministral-3b-latest
- ministral-8b-latest
- ministral-14b-latest
- mistral-small-latest
- mistral-large-latest
- mistral-medium-latest
- mistral-tiny-latest
- mistral-vibe-cli-latest

Notes:
- Mistral aliases rotate internally.
- "-latest" naming is correct behavior.
- Codestral remains one of the best coding specialists.
- Strong developer-agent provider.


+------------------------------------------------------------------------------+

 CEREBRAS
-----------
Base URL:
https://api.cerebras.ai/v1

Compatible Section:
openai

Verified Models:
- llama3.1-8b
- gpt-oss-120b
- qwen-3-235b-a22b-instruct-2507
- zai-glm-4.7

Notes:
- Cerebras offers extremely fast inference.
- Excellent orchestration-worker provider.
- Very strong throughput characteristics.


+------------------------------------------------------------------------------+

 GEMINI / GOOGLE
------------------
Compatible Section:
gemini

Verified Models:
- gemini-2.5-flash
- gemini-2.5-flash-lite
- gemini-3-flash-preview
- gemini-3.1-flash-lite-preview
- gemma-4-26b-a4b-it
- gemma-4-31b-it

CRITICAL GEMINI NOTES
---------------------
Do NOT specify:
- baseUrl
- thinking level overrides

Qwen Code internally handles Gemini endpoint routing.

If baseUrl is manually overridden:
- routing failures occur
- model lookup failures occur

If thinking level is forced:
- Gemini Flash models may reject requests

Correct:
{
  "id": "gemini-2.5-flash",
  "name": "Gemini 2.5 Flash",
  "envKey": "GEMINI_API_KEY"
}

Notes:
- gemma-4-31b-it is strong for orchestration.
- Gemini Flash models are best for large-context ingestion.
- Gemini models are highly efficient for RAG synthesis.


+------------------------------------------------------------------------------+

 POLLINATIONS
---------------
Base URL:
https://text.pollinations.ai/openai

Compatible Section:
openai

Notes:
- OpenAI-compatible free inference gateway.
- Best for overflow agents and experimental workers.
- Reliability varies.
- Good backup provider.


+------------------------------------------------------------------------------+

 GITHUB MODELS
----------------
Base URL:
https://models.inference.ai.azure.com

Compatible Section:
openai

Authentication:
GITHUB_TOKEN

Notes:
- Uses GitHub Models marketplace.
- OpenAI-compatible behavior.
- Good experimental provider.
- Rate limits depend on GitHub tier.


| RECOMMENDED AGENT ASSIGNMENT                                                 |


PRIMARY ORCHESTRATOR
--------------------
Model:
gemma-4-31b-it

Reason:
- strongest conversational orchestration
- strong instruction discipline
- excellent coordination quality
- stable planning behavior


+------------------------------------------------------------------------------+

ARCHITECT
---------
Model:
qwen/qwen3-coder-480b-a35b-instruct

Provider:
NVIDIA NIM

Purpose:
- systems planning
- architecture
- complex code synthesis


+------------------------------------------------------------------------------+

SECURITY AUDITOR
----------------
Model:
qwen/qwen3-coder-480b-a35b-instruct

Provider:
NVIDIA NIM

Purpose:
- adversarial analysis
- exploit detection
- security validation


+------------------------------------------------------------------------------+

REVIEWER
--------
Model:
openai/gpt-oss-120b

Provider:
Groq

Purpose:
- critique
- verification
- consistency checking


+------------------------------------------------------------------------------+

DEVELOPER
---------
Model:
codestral-latest

Provider:
Mistral

Purpose:
- implementation
- debugging
- iterative coding


+------------------------------------------------------------------------------+

RESEARCHER
----------
Model:
gemini-2.5-flash

Provider:
Google

Purpose:
- huge-context ingestion
- research synthesis
- document analysis


+------------------------------------------------------------------------------+

FAST SCOUT
----------
Model:
meta-llama/llama-4-scout-17b-16e-instruct

Provider:
Groq

Purpose:
- repository search
- fast triage
- lightweight exploration


+------------------------------------------------------------------------------+

GENERAL LOW-COST WORKER
-----------------------
Model:
qwen/qwen3-32b

Provider:
Groq

Purpose:
- utility work
- lightweight reasoning
- cheap background tasks


| FREE RAG STACK                                                               |


PRIMARY INTERNET SEARCH
-----------------------
Tavily MCP

Purpose:
- live internet search
- grounding
- retrieval augmentation
- search-first agent workflows

IMPORTANT:
----------
Do NOT use Tavily as your primary vector memory system.

Reason:
- Tavily is retrieval/search oriented
- not optimized for persistent semantic storage
- expensive if abused as pseudo-memory


+------------------------------------------------------------------------------+

PRIMARY VECTOR DATABASE
-----------------------
Qdrant Local

Purpose:
- persistent semantic memory
- embeddings storage
- local retrieval memory
- project indexing
- long-term agent memory

Advantages:
- fully local
- free
- extremely strong performance
- ideal for autonomous agents
- excellent MCP ecosystem support


+------------------------------------------------------------------------------+

CODE INDEXING
-------------
code-index-mcp

Purpose:
- semantic repository indexing
- symbol navigation
- retrieval over source trees
- agent code search

Recommended Usage:
- pair with Qdrant
- persistent repository indexing
- autonomous coding agents


+------------------------------------------------------------------------------+

EMBEDDING PROVIDERS
-------------------
Recommended Free Embedding Sources:

1. Gemini Embedding
2. Gemini Embedding 2
3. Local sentence-transformers
4. nomic-embed-text (local)

Recommended Strategy:
- use Gemini embeddings for remote quality
- use local embeddings for large indexing jobs


| RECOMMENDED RAG ARCHITECTURE                                                 |


RECOMMENDED FLOW
----------------

User Request
    |
    v

Primary Orchestrator
(gemma-4-31b-it)
    |
    +--> Tavily MCP
    |      |
    |      +--> live web search
    |
    +--> code-index-mcp
    |      |
    |      +--> repository retrieval
    |
    +--> Qdrant
           |
           +--> persistent semantic memory

Result:
- live internet grounding
- local long-term memory
- repository-aware retrieval
- scalable autonomous agents


| RECOMMENDED PRIORITY ORDER                                                   |


TIER 1 -- BEST DAILY DRIVERS
----------------------------
- gemma-4-31b-it
- gemini-2.5-flash
- qwen/qwen3-32b
- llama-4-scout-17b-16e-instruct
- codestral-latest


+------------------------------------------------------------------------------+

TIER 2 -- HEAVY REASONING
-------------------------
- qwen/qwen3-coder-480b-a35b-instruct
- gpt-oss-120b
- deepseek-v4-pro
- magistral-medium-latest


+------------------------------------------------------------------------------+

TIER 3 -- MASSIVE TOKEN BUDGET
------------------------------
- LongCat-Flash-Lite
- LongCat-Flash-Chat

Best Use:
- autonomous loops
- indexing
- summarization
- background agents
- RAG preprocessing


| FINAL IMPLEMENTATION RULES                                                   |


1. ALL NON-GEMINI REMOTE PROVIDERS
----------------------------------
Place under:
"modelProviders": {
  "openai": []
}

2. GEMINI + GEMMA
-----------------
Place under:
"modelProviders": {
  "gemini": []
}

3. DO NOT USE LONGCAT ANTHROPIC MODE
------------------------------------
Use:
https://api.longcat.chat/openai/v1

4. DO NOT MANUALLY SET GEMINI baseUrl
-------------------------------------
Qwen Code handles this internally.

5. USE EXACT MODEL IDS
----------------------
Most provider failures were caused by:
- alias mismatches
- removed prefixes
- obsolete names

6. KEEP openrouter/auto
-----------------------
Excellent fallback routing model.

7. DO NOT FORCE THINKING SETTINGS ON GEMINI
-------------------------------------------
Flash models may reject them.

8. SEPARATE SEARCH FROM VECTOR MEMORY
-------------------------------------
Use:
- Tavily -> internet retrieval
- Qdrant -> persistent memory

9. USE QDRANT FOR AUTONOMOUS AGENTS
-----------------------------------
Best free local vector database in this stack.

10. KEEP HEAVY MODELS OFF BACKGROUND TASKS
------------------------------------------
Reserve:
- Qwen3 Coder 480B
- GPT-OSS 120B
- DeepSeek V4 Pro

For:
- architecture
- security
- critical reasoning


| RESULT                                                                       |


You now have:

- verified provider routing
- working endpoint behavior
- verified model identifiers
- correct compatibility separation
- stable RAG architecture
- scalable agent foundation
- persistent semantic memory
- internet retrieval support
- free inference orchestration capability
- multi-provider fallback resilience
- autonomous-agent-ready infrastructure
