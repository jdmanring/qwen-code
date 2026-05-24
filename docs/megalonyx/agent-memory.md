# Agent Memory Service

The agent-memory service stores and retrieves memory for AI agents. It runs as a background
process, accepts ingest requests, and answers search queries using vector similarity against
a Qdrant database.

Location: `packages/agent-memory/`  
Entry point: `packages/agent-memory/src/agent_memory/memory_daemon.py`  
Package name: `agent-memory` (installed as `agent_memory`)  
Start: `mega-memory`

---

## What it does

The service provides two core operations:

**Store**: take a piece of text, embed it (convert to a vector), write it to Qdrant, and append to the WAL (write-ahead log) for crash recovery.

**Search**: take a query string, embed it, find the most similar vectors in Qdrant, return the matching text records.

It also runs two background maintenance tasks:
- **Pruning**: periodically deletes records older than a configured age
- **Compaction**: summarizes records whose text exceeds 1200 characters, replacing verbose records with compact summaries

---

## Modules

### `memory_daemon.py`

The daemon orchestrator. Runs an ingest queue, a search dispatcher, and a background maintenance cycle. Exposes the ingest and search API. All other modules are called from here.

### `memory_mcp_server.py`

An MCP (Model Context Protocol) server. Exposes `store_memory` and `search_memory` as tools that any MCP-compatible client (including the Qwen Code CLI) can call. Handles JSON-RPC serialization.

Transport: stdio (subprocess pipe) or Unix domain socket, controlled by `MCP_TRANSPORT` in `.env`.

### `memory_embeddings.py`

Converts text to embedding vectors. Supports two providers:

| Provider | Model | When to use |
|---|---|---|
| Local (SentenceTransformer) | `all-MiniLM-L6-v2` | No API key needed; runs on-device; lower quality |
| Cloud (Google Gemini) | Gemini embedding endpoint | Higher quality; requires `GEMINI_API_KEY` |

Batches requests and retries on transient API errors.

### `memory_ingest.py`

The write path:
1. Receive text + metadata
2. Call `memory_embeddings.py` to get the vector
3. Upsert the record to Qdrant (creates collection if it doesn't exist)
4. Append to `~/.local/share/megalonyx/memory/wal.jsonl` for crash recovery
5. Handle local-tier vs. cloud-tier routing (see `memory_ingest_filter.py`)

### `memory_search.py`

The read path:
1. Receive query text
2. Call `memory_embeddings.py` to embed the query
3. Run a similarity search against the Qdrant collection
4. Return ranked results with scores and metadata

Includes health checks and latency diagnostics.

### `memory_ingest_filter.py`

A gatekeeper that classifies each ingest request into one of three routing decisions:
- `local` — store in `agent_memory_local` collection only
- `cloud` — store in both `agent_memory_local` and `agent_memory_cloud`
- `ignore` — discard (reduces noise from low-value content)

Classification is based on content heuristics — length, pattern matching, source metadata.

### `memory_pruner.py`

Background task. Deletes records older than `max_age_days` from both collections. All deletions are logged via `SystemLogger`.

### `memory_compact.py` (memory compaction)

Background task. Finds records whose text exceeds 1200 characters and summarizes them via an LLM call, replacing the verbose record with a compact version. This keeps the vector database dense and search results relevant.

### `memory_schema.py`

Defines the `MemoryRecord` data structure: text, tier (local/cloud), timestamp, record ID. Handles serialization/deserialization.

---

## Qdrant collections

| Collection | What it stores |
|---|---|
| `agent_memory_local` | Records for this machine only; fast local search |
| `agent_memory_cloud` | Records flagged for cloud sync; replicated to Qdrant Cloud |

Both collections use the same vector dimension (determined by the embedding model). If the
collection doesn't exist, `memory_ingest.py` creates it on first write.

---

## Configuration

Set in `~/.local/share/megalonyx/.env` (see `docs/megalonyx/.env.md`):

| Variable | What it controls |
|---|---|
| `QDRANT_LOCAL_URL` | URL of the local Qdrant instance (default: `http://localhost:6333`) |
| `QDRANT_CLOUD_URL` | Qdrant Cloud URL (empty = no cloud sync) |
| `QDRANT_API_KEY` | Qdrant Cloud authentication key |
| `GEMINI_API_KEY` | Required if using Gemini embeddings |
| `MCP_TRANSPORT` | `stdio` or `socket` (default: `socket`) |

---

## Tests

Lifecycle tests: `packages/agent-memory/tests/lifecycle/test_dreaming.py`

Run: `uv run pytest packages/agent-memory/tests/`

---

## WAL recovery

If the service crashes mid-write, the WAL (`wal.jsonl`) contains the unconfirmed records.
On next startup, the daemon replays any WAL entries that are not in Qdrant. This prevents
silent data loss from crashes.
