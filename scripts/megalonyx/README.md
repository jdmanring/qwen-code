Megalonyx-specific shell scripts: installers and stack utilities.
These are owned by this repo and will not be overwritten on upstream sync.

Installers:
- install-megalonyx-stack.sh — installs the Python stack (uv workspace + Qdrant + bin wrappers)
- install-megalonyx-full.sh — installs Qwen Code CLI first, then the stack (compositor pattern)
- install-megalonyx-stack-legacy.sh — preserved from qwen_code_stack pre-monorepo; reference only, do not use

Other scripts are utilities carried over from qwen_code_stack migration.
All scripts must derive REPO_ROOT from BASH_SOURCE — no hardcoded paths or usernames.
