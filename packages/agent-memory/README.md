The agent-memory package provides persistent semantic memory for the Megalonyx stack.
It stores and retrieves text via vector embeddings in Qdrant, exposes memory tools over MCP (stdio and socket transports), and runs background consolidation and pruning passes.
Python package: agent_memory — importable via the uv workspace after uv sync --all-packages.
Requires a running Qdrant instance (default: http://localhost:6333). Start with: mega-db.
