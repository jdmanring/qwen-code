# Installation

## What gets installed

The Megalonyx stack has two components that install independently:

| Component | What it is | Installed by |
|---|---|---|
| Qwen Code CLI | Node.js terminal AI agent (upstream) | `install-qwen-standalone.sh` |
| Megalonyx stack | Python services: memory daemon, control plane, infra | `install-megalonyx-stack.sh` |

Both together: `install-megalonyx-full.sh`.

---

## Quick start (full install)

```bash
# Clone the repo
git clone <repo-url> megalonyx-monorepo
cd megalonyx-monorepo
git checkout develop

# Install everything
bash scripts/megalonyx/install-megalonyx-full.sh
```

This runs the upstream Qwen Code installer first, then the Megalonyx stack installer.

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

1. Checks prerequisites: `uv`, `curl`
2. Creates `~/.local/share/megalonyx/` with `config/`, `data/`, `logs/`, `memory/`, `tmp/`
3. Runs `uv sync --all-packages` — installs `agent-memory`, `control-plane-daemon`, `agent-infra` as editable packages
4. Writes `~/.local/share/megalonyx/config/qdrant_config.yaml` (points at local data dir)
5. Copies `config/megalonyx/.env.example` → `~/.local/share/megalonyx/.env` (if missing)
6. Copies `config/settings.example.json` → `~/.qwen/settings.json` (if missing)
7. Creates symlinks: `mega-memory`, `mega-status`, `mega-tasks` → `~/.local/bin/`
8. Writes wrappers: `mega-db`, `mega-run-py`, `mega-reboot` in `~/.local/bin/`
9. Downloads the Qdrant binary to `~/.local/share/megalonyx/packages/infra/qdrant/bin/qdrant`
10. Verifies Python packages are importable

---

## Post-install configuration

After install, two files need to be filled in before running the stack:

**`~/.local/share/megalonyx/.env`** — API keys and runtime paths:
- `QDRANT_LOCAL_URL` — default `http://localhost:6333`, change if Qdrant is remote
- `QDRANT_CLOUD_URL` and `QDRANT_API_KEY` — only if using Qdrant Cloud
- `GEMINI_API_KEY` — for Google Gemini embeddings
- `OPENAI_API_KEY` — for OpenAI-compatible LLM providers
- `GITHUB_TOKEN` — for GitHub Models / Copilot

**`~/.qwen/settings.json`** — model provider selection. Review the providers section and set your preferred LLM backend.

---

## Starting the stack

```bash
# Start Qdrant (required for memory)
mega-db &

# Start the memory daemon
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
| `mega-run-py` | Run a Python script in the uv workspace context |
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

## Legacy installer

`scripts/megalonyx/install-megalonyx-stack-legacy.sh` preserves the original `qwen_code_stack/install.sh` from before the monorepo migration. It is kept as a reference for the standalone (non-uv-workspace) install path. Do not use it for new installations.
