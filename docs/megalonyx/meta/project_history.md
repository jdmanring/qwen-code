 
# qwen-code-stack -- Project Evolution & History

This document tracks the evolution of the qwen-code-stack from a simple CLI wrapper to a state-aware, resilient agentic system.

##  Evolution Timeline

### Phase 1: Foundation (Complete)
- **Infrastructure**: Setup of Node.js, vLLM, and Qwen Code CLI.
- **Local Model**: Deployment of Qwen2.5-Coder-7B-AWQ for low-latency local execution.
- **Verification**: Implementation of `scripts/test.sh` for basic health checks.

### Phase 2: Tooling & MCP (Complete)
- **MCP Integration**: Added GitHub API and `code-index` (AST-aware search).
- **Tooling Policy**: Established the "Lean Toolset" for the Primary Agent to maximize token efficiency.

### Phase 3: External Intelligence (Complete)
- **Multi-Model Routing**: Integration of Gemini, Groq, OpenRouter, and NVIDIA NIM.
- **Tiered Intelligence**: Implementation of the "Ultimate Free Stack" for high-reasoning tasks.

### Phase 4: Behavioral Guardrails (Complete)
- **QWEN.md**: Created a strict set of behavioral rules to prevent "lazy" AI patterns (e.g., "Read before Edit").
- **Settings Optimization**: Enabled auto-memory, checkpointing, and chat compression.

### Phase 5: AST-Aware RAG (Complete)
- **Vector Store**: Integrated Qdrant for semantic codebase search.
- **Indexing Pipeline**: Developed a Python script to chunk code by AST (functions/classes) and embed via Ollama.
- **Semantic Search**: Added `semantic_search` tool to the Scout and Researcher agents.

### Phase 6: The Brain Upgrade (Complete)
- **State-Aware Orchestration**: Transformed the orchestrator from a stateless router to a state-aware manager using STRMAC scoring.
- **SDLC Phase Management**: Implemented global state persistence (`.qwen/state.json`) to track phases (`PLANNING` $\rightarrow$ `IMPLEMENTATION` $\rightarrow$ `VERIFICATION`).
- **Loop Guards**: Added iteration limits per phase to prevent repetition loops.

### Phase 7: System Hardening (Complete)
- **Resilience Layer**: Implemented exponential backoff, model downshifting (fallback), and dynamic timeouts in `skill_bridge.py`.
- **Report Validator**: Added schema enforcement to ensure sub-agents return structured reports.
- **System Watchdog**: Implemented stagnation detection and "Reflection Turns" to break agentic deadlocks.
- **Chaos Testing**: Created a mock-failure suite to verify the resilience layer under stress.
- **Audit Logging**: Integrated `SystemLogger` for structured JSON post-mortem analysis.

### Phase 8: Model & Workflow Optimization (Complete)
- **Token Lean-out**: Offloaded execution rules from global `QWEN.md` to specialized sub-agent YAMLs, reducing Primary Agent overhead.
- **Read-then-Edit Mandate**: Implemented a mandatory `read_file` $\rightarrow$ `analyze` $\rightarrow$ `edit` sequence for the Developer to eliminate "fail-first" loops.
- **Model Re-Alignment**: 
  - Moved **Scout** to `qwen/qwen3-32b` (Groq) for ultra-fast, cloud-based navigation.
  - Moved **Developer** to `codestral-latest` (Mistral) for superior idiomatic code generation.
- **Dependency Decoupling**: Removed reliance on local vLLM for core navigation, ensuring system availability even when local servers are offline.

---

##  Current System State

The system is now a **Professional-Grade Agentic Stack** featuring:
- **Tiered Intelligence**: Routing tasks to the most capable model (up to 480B).
- **AST-Aware RAG**: Semantic navigation of large codebases.
- **Self-Healing**: Automatic recovery from API timeouts and 500 errors.
- **State Persistence**: Ability to resume complex tasks across sessions.
- **Operational Purity**: All environments managed in `~/venvs`, keeping the project folder clean.
