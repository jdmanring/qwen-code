Megalonyx-specific shell scripts: installers and stack utilities.
These are owned by this repo and will not be overwritten on upstream sync.

Installers:
- install-megalonyx-full.sh -- full install: builds Qwen Code CLI from packages/cli/ source, then runs the stack installer
- install-megalonyx-stack.sh -- Python stack only: uv workspace sync, Qdrant, config templates, bin wrappers (use when CLI is already installed)

Other scripts are utilities carried over from qwen_code_stack migration.
All scripts must derive REPO_ROOT from BASH_SOURCE -- no hardcoded paths or usernames.
