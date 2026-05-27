#  Memory System Technical Map

This document provides a comprehensive technical mapping of the Mega Code memory system, detailing the responsibilities, data flows, and logic of each component.

## 1. High-Level Architecture

The memory system is a **Dual-Tier RAG (Retrieval Augmented Generation)** implementation. It separates transient, project-specific information from long-term, global architectural knowledge.

### Data Flow Diagrams

#### Ingestion Flow
`User/Agent` $\rightarrow$ `memory_transport.py` (MCP) $\rightarrow$ `memory_daemon.py` (Orchestration) $\rightarrow$ `memory_authority.py` (Filter/Route) $\rightarrow$ `memory_daemon.py` (Compaction) $\rightarrow$ `memory_ingest.py` (WAL $\rightarrow$ Embed $\rightarrow$ Qdrant).

#### Retrieval Flow
`User/Agent` $\rightarrow$ `memory_transport.py` (MCP) $\rightarrow$ `memory_daemon.py` (Orchestration) $\rightarrow$ `memory_embeddings.py` (Query Vectorization) $\rightarrow$ `memory_search.py` (Qdrant Query) $\rightarrow$ `memory_daemon.py` (Filter/Format) $\rightarrow$ `User/Agent`.

---

## 2. Component Breakdown

### `memory_daemon.py` (The Orchestrator)
**Responsibility**: The central hub coordinating all memory operations.
- **Key Logic**:
    - **Ingest Coordination**: Checks `MemoryAuthority` for storage permission, determines the tier, and queues the record for the background worker.
    - **Recall/Reflect**: Manages search requests across local and cloud tiers.
    - **Worker Thread**: A background thread that processes the ingestion queue to ensure the MCP interface remains responsive.
- **Dependencies**: `memory_authority`, `memory_compact`, `memory_ingest`, `memory_search`, `memory_transport`.

### `memory_authority.py` (The Gatekeeper)
**Responsibility**: Enforces the memory policy and determines *if* and *where* data is stored.
- **Key Logic**:
    - **Noise Filtering**: Rejects trivial input (e.g., "Ok", "Thanks") using a word-set check.
    - **Deduplication**: Maintains a bounded window (default 1000) of SHA-256 hashes to prevent redundant entries.
    - **Tier Routing**: Classifies text as `cloud` if it contains "signals" (e.g., "architecture", "policy", "standard"), otherwise defaults to `local`.
- **Dependencies**: `hashlib`, `json`, `collections.deque`.

### `memory_ingest.py` (The Writer)
**Responsibility**: Handles the physical persistence of memory records.
- **Key Logic**:
    - **WAL (Write-Ahead Log)**: Every record is appended to `~/.qwen/memory/wal.jsonl` before attempting a Qdrant upsert.
    - **Recovery**: On boot, the daemon replays the WAL to recover any records that weren't successfully committed to the DB.
    - **Upsert**: Performs idempotent updates to Qdrant using the record's UUID.
- **Dependencies**: `qdrant_client`, `memory_embeddings`, `memory_schema`.

### `memory_search.py` (The Reader)
**Responsibility**: Manages semantic retrieval and collection health.
- **Key Logic**:
    - **Collection Bootstrapping**: Ensures `qwen_local_memory` and `qwen_cloud_memory` exist with correct dimensions.
    - **Similarity Search**: Performs vector queries with a `min_score` threshold to filter out irrelevant results.
    - **Connectivity**: Implements exponential backoff for Qdrant connection attempts.
- **Dependencies**: `qdrant_client`.

### `memory_embeddings.py` (The Vectorizer)
**Responsibility**: Converts text into semantic vectors.
- **Key Logic**:
    - **Local Provider**: Uses `all-MiniLM-L6-v2` (384 dimensions).
    - **Cloud Provider**: Uses `gemini-embedding-2` (3072 dimensions) via API.
    - **Caching**: Implements an in-memory cache for cloud embeddings to reduce API latency and cost.
- **Dependencies**: `sentence_transformers`, `requests`.

### `memory_gc.py` (The Janitor)
**Responsibility**: Manages storage growth and data retention.
- **Key Logic**:
    - **Age-Based Pruning**: Deletes records older than a specified threshold (default 90 days) using a Qdrant range filter on `created_at`. See [Memory Maintenance & GC](memory-gc.md) for more details.
- **Dependencies**: `qdrant_client`.

### `memory_transport.py` (The Interface)
**Responsibility**: Implements the MCP stdio protocol.
- **Key Logic**:
    - **Tool Mapping**: Maps MCP `tools/call` requests to `MemoryCore` methods (`ingest`, `recall`, `reflect`).
    - **JSON-RPC**: Handles the request/response cycle for the MCP handshake.
- **Dependencies**: `json`, `sys`.

### `memory_schema.py` (The Definition)
**Responsibility**: Defines the structure of a memory record.
- **Key Logic**:
    - **MemoryRecord**: A dataclass containing text, tier, source, importance, and timestamps. See [Memory Record Schema](memory-schema.md) for field details.
    - **Serialization**: Provides `serialize` and `deserialize` helpers for JSON/Qdrant payload compatibility.
- **Dependencies**: `dataclasses`, `uuid`, `time`.

---

## 3. Operational Constants

| Constant | Value | Location | Description |
| :--- | :--- | :--- | :--- |
| `MAX_COMPACT_CHARS` | 1200 | `memory_compact.py` | Maximum length of a memory record before truncation. |
| `DEDUP_WINDOW_SIZE` | 1000 | `memory_authority.py` | Number of hashes kept for deduplication. |
| `GC_MAX_AGE_DAYS` | 90 | `memory_gc.py` | Retention period for memory records. |
| `LOCAL_DIM` | 384 | `memory_search.py` | Vector dimensions for local tier. |
| `CLOUD_DIM` | 3072 | `memory_search.py` | Vector dimensions for cloud tier. |
