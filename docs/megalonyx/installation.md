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

1. Checks prerequisites: `uv`, `curl`
2. Creates `~/.local/share/megalonyx/` (data) and `~/.config/megalonyx/` + `~/.config/qwen/` (config)
3. Runs `uv sync --all-packages` — installs `agent-memory`, `control-plane-daemon`, `agent-infra` as editable packages
4. Writes `~/.config/megalonyx/qdrant_config.yaml` (points at `~/.local/share/megalonyx/data/qdrant`)
5. Copies `config/megalonyx/.env.example` → `~/.config/megalonyx/.env` (if missing)
6. Copies `config/settings.example.json` → `~/.config/qwen/settings.json` (if missing)
6a. Adds `export QWEN_HOME="$HOME/.config/qwen"` to your shell RC so the CLI finds its config dir
7. Creates symlinks: `mega-memory`, `mega-status`, `mega-tasks` → `~/.local/bin/`
8. Writes wrappers: `mega-db`, `mega-run-py`, `mega-reboot` in `~/.local/bin/`
9. Downloads the Qdrant binary to `~/.local/share/megalonyx/packages/infra/qdrant/bin/qdrant`
10. Verifies Python packages are importable

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

## Rebuilding the CLI after source changes

The `qwen` wrapper in `~/.local/bin/qwen` runs directly from `packages/cli/dist/`. After modifying TypeScript source, rebuild with:

```bash
npm run build --prefix packages/core
npm run build --prefix packages/cli
```

No reinstall needed — the wrapper picks up the new build automatically.
