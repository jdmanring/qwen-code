# Installation

## What gets installed

The Megalonyx stack has two components that install independently:

| Component | What it is | Installed by |
|---|---|---|
| Qwen Code CLI | Node.js terminal AI agent (built from `packages/cli/`) | `install-megalonyx-full.sh` |
| Megalonyx stack | Python services: memory daemon, control plane, infra | `install-megalonyx-stack.sh` |

Both together: `install-megalonyx-full.sh` (recommended for new installs).

---

## Quick start (full install)

```bash
# Clone the repo
git clone <repo-url> megalonyx-monorepo
cd megalonyx-monorepo
git checkout develop

# Install everything (builds CLI from source + Python stack)
bash scripts/megalonyx/install-megalonyx-full.sh
```

This builds the Qwen Code CLI from `packages/cli/` (requires Node.js 22+), then installs the Megalonyx Python stack.

---

## Stack-only install

If Qwen Code is already installed (or you only need the Python stack):

```bash
bash scripts/megalonyx/install-megalonyx-stack.sh
```

Options:

| Flag | Effect |
|---|---|
| `--force-config` | Overwrite existing config files (`.env`, `settings.json`, `qdrant_config.yaml`) |
| `--sync-deps` | Force `uv sync` even if packages are already importable |
| `--verify-runtime` | Run `tooling/smoke-tests/boot_verification.py` after install |

---

## What the stack installer does

The installer transforms the monorepo Blueprint into a standalone **Runtime Stack** on your machine, ensuring that the services can function independently of the source code repository.

1. **Prerequisite Check**: Verifies `uv` and `curl` are installed.
2. **Infrastructure Setup**: Creates the stack root at `~/.local/share/megalonyx/`, including dedicated directories for `sockets/`, `packages/`, `logs/`, and `data/`.
3. **Physical Deployment**: Performs a physical copy of all core packages, apps, and scripts from the monorepo to the stack root. This eliminates reliance on symlinks.
4. **Workspace Initialization**: Creates a minimal `pyproject.toml` at the stack root to define a UV workspace, allowing internal packages to resolve each other.
5. **Isolated Environment**: Creates a dedicated Python virtual environment at `~/.local/share/megalonyx/py/venv`.
6. **Local Installation**: Installs `agent-infra`, `agent-memory`, and `control-plane-daemon` into the venv using the physical copies deployed in step 3.
7. **Configuration**: Deploys `.env`, `settings.json`, and `qdrant_config.yaml` templates to their respective config directories.
8. **Environment Integration**: Adds `QWEN_HOME` to your shell profile (bash/zsh/fish) so the CLI can locate its configuration.
9. **Runtime Wrappers**: Installs essential wrappers in `~/.local/bin/` (e.g., `mega-run-py`, `mega-db`) that resolve paths against the stack root.
10. **Qdrant Deployment**: Downloads and installs the correct Qdrant binary for your architecture.
11. **Verification**: Performs a final import check to ensure the isolated environment is fully functional.

---

## Post-install configuration

After install, two files need to be filled in before running the stack:

**`~/.config/megalonyx/.env`** — API keys and runtime paths for the Python stack:
- `QDRANT_LOCAL_URL` — default `http://localhost:6333`, change if Qdrant is remote
- `QDRANT_CLOUD_URL` and `QDRANT_API_KEY` — only if using Qdrant Cloud
- `GEMINI_API_KEY` — for Google Gemini embeddings
- `OPENAI_API_KEY` — for OpenAI-compatible LLM providers
- `GITHUB_TOKEN` — for GitHub Models / Copilot

**`~/.config/qwen/settings.json`** — Qwen Code CLI config: model provider selection, MCP servers. Review the providers section and set your preferred LLM backend.

---

## Starting the stack

```bash
# Start Qdrant (required for memory)
mega-db &

# Start the memory daemon (via stack manager or direct module execution)
# The daemon listens on ~/.local/share/megalonyx/sockets/megalonyx_memory.sock
mega-memory &

# Check status
mega-status
```

---

## Commands installed

| Command | What it does |
|---|---|
| `mega-memory` | Start/restart the memory MCP daemon |
| `mega-db` | Start Qdrant with the installed config |
| `mega-status` | Show service health (Qdrant, memory daemon, WAL) |
| `mega-tasks` | Manage active tasks in the job state manager |
| `mega-run-py` | Run a Python script in the isolated UV workspace context |
| `mega-reboot` | Restart all services and print status |

---

## Updating

The stack installer is idempotent. Re-running it will:
- Skip uv sync if packages are already importable (use `--sync-deps` to force)
- Skip config file deployment if they already exist (use `--force-config` to overwrite)
- Skip Qdrant download if the binary already exists

To update just the Python packages after a code change:

```bash
uv sync --all-packages
```

---

## Rebuilding the CLI after source changes

The `qwen` wrapper in `~/.local/bin/qwen` runs directly from `packages/cli/dist/`. After modifying TypeScript source, rebuild with:

```bash
npm run build --prefix packages/core
npm run build --prefix packages/cli
```

No reinstall needed — the wrapper picks up the new build automatically.
