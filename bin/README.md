Shell entry points for the Megalonyx stack. These are symlinked to ~/.local/bin/ by the installer.

Scripts:
- mega-memory — starts the memory MCP daemon (uv run python -m agent_memory.memory_daemon)
- mega-status — prints service health: Qdrant, memory daemon, WAL
- mega-tasks — CLI for the job state manager (list/add/done/clear)

The installer also creates bin wrappers that are NOT in this directory:
- mega-db (in ~/.local/bin/) — starts Qdrant using the installed config
- mega-run-py (in ~/.local/bin/) — runs a Python script via uv run in the workspace context
- mega-reboot (in ~/.local/bin/) — restarts all services

Do not put upstream Qwen Code scripts here. This directory is for Megalonyx-owned entry points only.
