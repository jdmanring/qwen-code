# Megalonyx Stack Architecture

The Megalonyx stack consists of three Python packages that work together to extend the Qwen Code
CLI with persistent memory and structured task handling. This document describes what each
component does, how they communicate, and where the data lives.

---

## Components

```
User / CLI session
       |
       | task or question
       v
control-plane-daemon          apps/control-plane-daemon/
  ├── IntentClassifier         classify what kind of task this is
  ├── TaskDecomposer           break it into atomic jobs
  ├── JobStateManager          track job lifecycle (pending → done)
  ├── ExecutionProfileSelector pick the right model and tool config
  ├── ModelRouter              assign a specific model to each job
  └── ToolExecutor             call the model, handle retries, return result
       |
       | memory read/write (via MCP over stdio or Unix socket)
       v
agent-memory                  packages/agent-memory/
  ├── MemoryMCPServer          MCP server: exposes store/search as tools
  ├── MemoryIngest             write path: embed → upsert to Qdrant → WAL
  ├── MemorySearch             read path: embed query → similarity search
  ├── MemoryPruner             background: delete old records
  └── MemoryCompact            background: summarize oversized records
       |
       | Qdrant API calls
       v
Qdrant (external process)
  ├── agent_memory_local       collection for this machine's working memory
  └── agent_memory_cloud       collection synced to Qdrant Cloud (optional)
```

The third component, `agent-infra`, provides shared utilities used by both services:

```
agent-infra                   packages/agent-infra/
  ├── SystemLogger             structured JSON logging to ~/.local/share/megalonyx/logs/
  ├── CronManager              schedule periodic tasks (pruning, health checks)
  └── GitWorktreeManager       create isolated git worktrees for agent work
```

---

## Dependency chain

```
agent-infra   ←   agent-memory   ←   control-plane-daemon
```

`agent-infra` has no Megalonyx dependencies. `agent-memory` imports `agent-infra` for logging.
`control-plane-daemon` imports both.

All three are members of the `uv` workspace. `uv sync` installs the full chain.

---

## Data flow: task submission to result

1. A task arrives (from CLI session, API call, or test harness)
2. `IntentClassifier` assigns a taxonomy: Exploratory, Surgical Fix, Feature Synthesis, Structural Evolution, Adversarial Review, or Knowledge Sync
3. `TaskDecomposer` breaks the task into one or more atomic jobs with dependency ordering
4. `ExecutionProfileSelector` loads the matching profile from `.qwen/agents/` based on file context and task keywords
5. `ModelRouter` reads the profile and assigns a specific model (from `settings.json` provider list) to each job
6. `ToolExecutor` calls the model with a resolved system prompt and context; handles retries and fallback models
7. Results flow back through `JobStateManager` to the caller

If any job needs to read or write memory, it calls the `agent-memory` MCP server via the
MCP tool registered in the session.

---

## Where data lives on disk

| Data | Path |
|---|---|
| Logs | `~/.local/share/megalonyx/logs/megalonyx_system.log` |
| WAL (write-ahead log for memory) | `~/.local/share/megalonyx/memory/wal.jsonl` |
| Runtime environment | `~/.local/share/megalonyx/.env` |
| Settings (Qwen Code runtime config) | `config/settings.json` (not committed) |
| Qdrant data | Wherever Qdrant is configured to store it (local default: `~/.local/share/qdrant/`) |

---

## Communication between components

**control-plane-daemon → agent-memory:**
The daemon calls the memory service via MCP. The transport is configurable via `MCP_TRANSPORT`
in the `.env` file:
- `stdio` — the daemon spawns the memory server as a subprocess and communicates via stdin/stdout
- `socket` — the memory server runs as a background daemon; the control plane connects via Unix socket at `~/.local/share/megalonyx/megalonyx_memory.sock`

The socket mode is preferred for production because it avoids spawning a new process per session.

**agent-memory → Qdrant:**
Standard HTTP API calls to `QDRANT_LOCAL_URL` (default `http://localhost:6333`) and optionally
`QDRANT_CLOUD_URL`. Qdrant must be running independently — neither service starts it.

---

## Boot order

1. Start Qdrant (if not already running): `~/.local/share/megalonyx/bin/qdrant`
2. Start `agent-memory`: `mega-memory` (runs `python -m agent_memory.memory_daemon`)
3. Start `control-plane-daemon` or launch a Qwen Code CLI session — either will connect to memory on first use

Check status with `mega-status`.
