The agent_infra Python package. Shared utilities for the Megalonyx Python stack.

Modules:
- system_logger.py — SystemLogger: structured logging with consistent format across all packages
- git_worktree_manager.py — creates and cleans up git worktrees for isolated task execution
- cron_manager.py — schedules periodic background jobs (consolidation, pruning)

Import pattern: from agent_infra.system_logger import SystemLogger
Do not add application-specific logic here — only generic, reusable infrastructure.
