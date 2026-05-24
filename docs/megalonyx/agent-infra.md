# Agent Infrastructure Library

`agent-infra` is a shared Python library used by both `agent-memory` and `control-plane-daemon`.
It provides utilities that would otherwise be duplicated across both services.

Location: `packages/agent-infra/`  
Package name: `agent-infra` (installed as `agent_infra`)

This package has no Megalonyx-specific dependencies — it only depends on standard library
and third-party packages. It is the foundation of the dependency chain.

---

## Modules

### `system_logger.py`

Structured logging for the Megalonyx stack.

Output format: JSONL (one JSON object per line) written to `~/.local/share/megalonyx/logs/megalonyx_system.log`.

Terminal output: color-coded rich text (INFO=blue, WARNING=yellow, ERROR=red, DEBUG=dim).

Usage:
```python
from agent_infra.system_logger import SystemLogger

logger = SystemLogger.get_logger(__name__)
logger.info("Service started")
logger.debug("Processing record %s", record_id)
logger.error("Failed to connect to Qdrant: %s", str(e))
```

Configuration is read from `~/.qwen/settings.json` at startup: `logging.log_level`,
`logging.log_path`, `logging.enable_trace`.

This module is the single source of truth for logging across the stack. Do not use
`print()` statements in production code — they bypass log routing and make operational
debugging difficult.

### `cron_manager.py`

Manages periodic background tasks. Services register tasks with a name, interval, and
callable. The manager runs each task on its schedule using a background thread.

```python
cron = CronManager()
cron.register("memory-prune", interval_seconds=3600, fn=pruner.run)
cron.start()
```

Used by `agent-memory` for the pruning and compaction cycles.

### `git_worktree_manager.py`

Automates creation of isolated git worktrees. An agent that needs to work on a feature
branch without disrupting the main working tree can use this to create a temporary worktree,
do its work, and clean up.

```python
manager = GitWorktreeManager(repo_root="/path/to/repo")
worktree_path = manager.create("feature-xyz", base_branch="develop")
# ... do work in worktree_path ...
manager.remove("feature-xyz")
```

---

## Adding to agent-infra

If you add a utility that both services need, put it here rather than duplicating it.
The rule: if it's pure infrastructure with no business logic tied to memory or task handling,
it belongs in `agent-infra`.

Do not add Qdrant, MCP, or model-provider dependencies to this package — keep it minimal
so it can be imported without pulling in the full ML stack.
