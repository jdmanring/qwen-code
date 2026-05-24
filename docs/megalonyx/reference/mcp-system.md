# MCP System

## Overview

MCP (Model Context Protocol) provides tool access for Qwen Code. It allows the agent to interact with the external environment through a standardized interface.

---

## Registered MCP Servers

- **filesystem**: Local file system access.
- **github**: Repository and issue management.
- **memory (Unified Authority)**: Semantic long-term context.
- **tavily-search**: Real-time web research.
- **code-index**: Deep codebase symbol indexing.

---

## Memory Authority Layer

The separate `qdrant-local` and `qdrant-cloud` servers have been replaced by a unified **Memory Authority Layer**.

### Unified Authority: `mega-memory-manager`
The `mega-memory-manager` MCP server acts as the single entry point for all semantic memory operations. It delegates requests to the `memory_daemon.py` which handles the dual-tier routing.

#### 1. Orchestration & Transport
- **`memory_daemon.py`**: The central hub. Coordinates ingestion, search, and manages the connection to the vector store.
- **`memory_transport.py`**: Implements the JSON-RPC server for MCP compatibility, allowing the orchestrator to communicate with the daemon.
- **`mega-memory-manager` (bin)**: A bash process manager that ensures the daemon is running in the correct virtual environment and implements exponential backoff for restarts.

#### 2. The Data Pipeline
- **`memory_authority.py`**: The "Brain" of the memory system. Decides whether a piece of data should be stored and routes it to the appropriate tier (Local vs. Cloud) based on importance and sensitivity.
- **`memory_embeddings.py`**: Converts raw text into high-dimensional vectors using `sentence-transformers`.
- **`memory_compact.py`**: Optimizes memory usage by compressing texts longer than 1200 characters before storage.
- **`memory_ingest.py`**: Handles the atomic insertion of records into the vector database.

#### 3. Storage & Retrieval
- **`memory_search.py`**: Manages Qdrant collections and performs vector similarity searches to retrieve relevant context.
- **`memory_schema.py`**: Defines the `MemoryRecord` structure (ID, text, tier, importance, metadata), ensuring consistency.
- **`memory_gc.py`**: Garbage Collector. Periodically cleans up stale, low-importance, or redundant memories to maintain search quality.

#### 4. Tiers
- **Local Tier**:
  - Logic: `embed_local()`
  - Storage: Qdrant local
  - Purpose: Fast memory, offline retrieval, highly sensitive data.

- **Cloud Tier**:
  - Logic: `embed_google()`
  - Storage: Qdrant cloud
  - Purpose: Durable memory, high-quality retrieval, shared across environments.

---

## Rule

MCP does NOT decide embeddings.

Only `memory_embeddings.py` (via the daemon) does.
