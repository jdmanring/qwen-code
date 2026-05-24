# Megalonyx Monorepo — Roadmap

Tracks the evolution of the Megalonyx stack. Distinguishes what is fully implemented and
verified from what is an architectural target not yet in code.

---

## Implemented and verified

### Persistent semantic memory
- Tiered storage: local and cloud Qdrant collections with keyword-based routing via `MemoryAuthority`
- Async ingestion: write-ahead log (`wal.jsonl`) and background worker for non-blocking memory updates
- Recall: core MCP tools for semantic retrieval (`memory_search.py`)
- Memory compaction and pruning: background consolidation pass (`memory_compact.py`, `memory_pruner.py`)

### MCP integration
- Memory daemon: MCP server providing memory tools via `stdio` and `socket` transports (`memory_mcp_server.py`)
- MCP manager: client-side orchestrator for managing multiple MCP server sessions (`mcp_manager.py`)

### Orchestration plane
- Intent classifier: classifies user prompt into one of six intent types (`intent_classifier.py`)
- Policy engine: evaluates intent + risk profile against configured rules (`policy_engine.py`)
- Task decomposer: breaks compound intents into atomic jobs (`task_decomposer.py`)
- Job state manager: tracks job lifecycle from creation through completion (`job_state_manager.py`)
- Execution profile selector: scores and ranks agent profiles for a given intent (`execution_profile_selector.py`)

### Agent execution
- Tool executor: bridges classified intent to subprocess skill execution (`tool_executor.py`)
- Agent generator: synthesizes structured system prompts from execution profiles (`agent_generator.py`)
- Vector search tool: RAG lookup via Qdrant MCP server (`vector_search_tool.py`)

### Reproducible deployment
- uv workspace: all three Python packages installed as editable deps via `uv sync --all-packages`
- Lifecycle management: `bin/mega-memory`, `bin/mega-status`, `bin/mega-tasks`
- Installer: `scripts/megalonyx/install-megalonyx-stack.sh`

### Structural integrity
- Config/docs symmetry: 1:1 mirror of `config/` to `docs/` verified by `tooling/symmetry_check.py`
- Upstream sync pipeline: automated fetch -> gate -> promote for QwenLM/qwen-code updates
- Boot verification: `tooling/smoke-tests/boot_verification.py` covers imports, instantiation, profile selection, memory round-trip

---

## In progress — Phase 3

- Installer unification: `install-megalonyx-stack.sh`, `install-megalonyx-full.sh`, `docs/megalonyx/installation.md`
- Remaining test migration: `tests/fidelity/`, `tests/debug/`, `tests/validators/` from qwen_code_stack

---

## Future work

### Advanced memory consolidation
- Semantic clustering during consolidation: move beyond hash-based deduplication to content-aware merging of related memories
- Automated pattern extraction: distill recurring patterns from ingested code during the consolidation pass

### Enhanced ingestion
- Automated cognitive mapping: move from structural mirroring to semantic mapping of external repositories on ingest
- Runtime artifact isolation: strict separation of transient artifacts (`tmp/`), persistent audit logs (`logs/`), and ephemeral trace data — prevents tmpfs exhaustion and improves portability

### Context compression (CEAP v2)
- Skeleton-first discovery: `read_skeleton` capability returning only structural metadata (imports, signatures) before implementation
- Semantic state checkpointing: periodic high-density session checkpoints compressing conversational history into summaries
- Contextual pruning: "local neighborhood" loading — only the target function and its immediate dependencies
- Hierarchical context loading: enforce top-down protocol (Blueprint -> Module -> Implementation)
- Token-aware search: search results ranked by semantic proximity rather than textual match count

### Platform

- T3 GUI: web interface for task management, memory inspection, and service health
- Public release repo: separate repository with upstream content stripped, internal tooling excluded
- Full Qwen Code rebrand: complete renaming of inherited upstream identifiers

---

## Maintenance notes

- Do not modify `ci.yml` — upstream content, overwritten on sync
- Do not commit `config/settings.json` or `config/megalonyx/.env` — contain live API keys
- Upstream sync runs against `QwenLM/qwen-code` via `tooling/sync-upstreams/upstream_ingest_pipeline.py`
