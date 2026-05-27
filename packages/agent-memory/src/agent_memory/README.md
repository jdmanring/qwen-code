The agent_memory Python package. All modules importable as agent_memory.<module>.

Key modules:
- memory_daemon.py -- MemoryDaemon: top-level service; start() opens MCP server, ingest/recall API
- memory_mcp_server.py -- MCP server: exposes ingest and search as MCP tools over stdio or socket
- memory_ingest.py -- writes text to the write-ahead log (wal.jsonl) and queues background embedding
- memory_search.py -- semantic search via Qdrant; ensure_collections_exist() initializes collections
- memory_embeddings.py -- embedding generation (sentence-transformers, Gemini, or Ollama)
- memory_compact.py -- background consolidation: deduplication and clustering pass
- memory_pruner.py -- background pruning: removes low-relevance entries
- memory_schema.py -- Qdrant collection schema definitions (field names, vector config)
- memory_ingest_filter.py -- noise filtering: rejects trivial or duplicate ingest candidates

Tiers: "local" (private) and "cloud" (shared). Routing is controlled by MemoryAuthority.
