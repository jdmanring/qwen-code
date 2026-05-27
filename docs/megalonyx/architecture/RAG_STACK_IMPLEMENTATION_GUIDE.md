 
# RAG Stack Implementation Guide

This document defines the technical infrastructure powering the semantic memory and retrieval capabilities of the Qwen Code stack. We follow the "Best Overall Free Stack" architecture to maximize intelligence while maintaining zero cost. For a detailed component breakdown, see the [Memory Technical Map](reference/memory-technical-map.md).

## 1. The Retrieval Architecture

Our system uses a hybrid retrieval approach, combining local codebase indexing with remote web research.

### Architecture Flow
`Qwen Code Orchestrator` $\rightarrow$ `MCP Tool Layer` (Tavily, GitHub, Code-Index) $\rightarrow$ `Model Provider Layer` (Groq, Gemini, OpenRouter) $\rightarrow$ `Vector/RAG Layer` (Qdrant, HF Embeddings).

### Local Code RAG (The "Internal Eye")
Used by **Scout**, **Explore**, and **Developer** to navigate the project.
- **Vector Database**: `Qdrant` (Local binary).
- **Code Indexer**: `code-index-mcp` (AST-aware semantic indexing).
- **GitHub Integration**: `GitHub MCP` (For remote repo browsing and PR analysis).
- **Embeddings**: Hugging Face `BGE` models (e.g., `BAAI/bge-base-en-v1.5`).

### Remote Web RAG (The "External Eye")
Used by the **Researcher** and **Architect** to ingest external documentation.
- **Retrieval Engine**: `Tavily` (via `tavily-mcp`).
- **Inference/Synthesis**: `Gemini 2.5 Flash` (Chosen for its massive context window, allowing for "Long-Context RAG" where entire docs are ingested).

---

## 2. Provider Mapping & Roles

| Component | Provider | Role in Stack | Agent Primary User |
| :--- | :--- | :--- | :--- |
| **Tavily** | Tavily MCP | Live web retrieval & citations | `Researcher` |
| **Qdrant** | Local Binary | Persistent semantic memory | `Scout`, `Explore` |
| **Code-Index** | code-index-mcp | AST-aware codebase retrieval | `Scout`, `Developer` |
| **GitHub** | GitHub MCP | Remote repo & issue retrieval | `Scout`, `Reviewer` |
| **Gemini** | Google | Long-context synthesis | `Researcher`, `Architect` |
| **Groq** | Groq | Low-latency RAG answer generation | `Explore`, `general-purpose` |

---

## 3. Final Recommended Free Stack

**Inference:**
- Groq
- Gemini
- LongCat
- OpenRouter (Fallback)

**Retrieval:**
- Tavily MCP

**Code Intelligence:**
- code-index-mcp
- GitHub MCP

**Vector Database:**
- Local Qdrant

**Embeddings:**
- Hugging Face BGE models

---

## 4. Implementation Order

### Phase 1: Working Agent
- [ ] Configure Groq, Gemini, and OpenRouter.
- [ ] Verify Qwen Code inference.

### Phase 2: Retrieval
- [ ] Install Tavily MCP (`npm install -g tavily-mcp`).
- [ ] Verify web retrieval and citations.

### Phase 3: Vector Memory
- [ ] Install Qdrant.
- [ ] Install embedding model.
- [ ] Build document ingestion.

### Phase 4: Code RAG
- [ ] Install `code-index-mcp` (`uvx code-index-mcp`).
- [ ] Configure GitHub MCP.
- [ ] Index repositories.

### Phase 5: Autonomous Workflows
- [ ] LongCat integration.
- [ ] Multi-provider routing.
- [ ] Persistent memory agents.

---

## 5. Practical Advice & Constraints

### The "Symmetry" Rule
To prevent "RAG Hallucinations," the system follows the **Symmetry Rule**:
- **Search $\rightarrow$ Fetch $\rightarrow$ Synthesize**.
- An agent must never synthesize an answer based on a search snippet alone. It MUST `web_fetch` or `read_file` the actual content before reporting.

### Performance Tuning
- **Latency**: Use Groq-based models for the final "Answer Generation" phase of RAG to ensure the user isn't waiting for a slow 480B model to summarize a search result.

## Testing

The RAG stack is verified through a multi-layered testing approach:

1.  **Unit Tests**: Individual components like the `CodeIndexer` are tested in isolation using mocks for external dependencies (e.g., Qdrant).
2.  **Integration Tests**: The full RAG pipeline, including the `CodeIndexer`, Qdrant, and embedding models, is tested to ensure end-to-end semantic search accuracy.
3.  **MCP Server Tests**: The `qdrant_mcp` server is tested to ensure it correctly handles MCP protocol commands and integrates with the Qdrant vector database.
4.  **Automated Suite**: All tests are integrated into the unified `tests/run_all.sh` runner for continuous verification.

## 6. Service Stability & Lifecycle

To ensure high availability and prevent common failure modes (such as stale WAL locks in Qdrant), the system employs a hardened lifecycle management strategy via the `mega-memory-manager` wrapper:

- **Pre-flight Cleanup**: The `start` command automatically detects and terminates any existing Qdrant processes before attempting to boot, ensuring a clean state and preventing `Kind(WouldBlock)` errors.
- **Aggressive Termination**: The `stop` command implements a multi-stage shutdown, falling back to `pkill -9` if the PID file is missing or the process is unresponsive.
- **Robust Status Detection**: The `status` command utilizes `pgrep` as a fallback to correctly report the service state even when PID files are corrupted or absent.

## 7. Data Integrity & Optimization

### Reliability & Recovery (WAL)
To prevent data loss during crashes or unexpected shutdowns, the memory system implements a **Write-Ahead Log (WAL)**:
- **Process**: Every record is appended to `~/.qwen/memory/wal.jsonl` in a serialized JSON format *before* the attempt to upsert into Qdrant.
- **Recovery**: Upon boot, the `memory_daemon` scans the WAL and replays any pending records into the vector database, ensuring that no "remembered" fact is lost due to a process crash.

### Text Compaction
To maintain embedding quality and stay within semantic constraints, the system employs a **Compaction Strategy**:
- **Threshold**: Any text exceeding **1200 characters** is automatically compacted.
- **Strategy**: The system attempts to truncate at the nearest sentence boundary (. ! ?) or word boundary to preserve semantic meaning, rather than performing a hard character cut.
