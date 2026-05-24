#!/usr/bin/env bash
set -euo pipefail

# ======================================
# MEGALONYX STACK — LEGACY STANDALONE INSTALLER
# ======================================
#
# Preserved from qwen_code_stack/install.sh (standalone deployment, pre-monorepo).
# Kept as a reference for the standalone (non-monorepo) install path and as
# the basis for install-megalonyx-stack.sh (the current monorepo installer).
#
# DO NOT USE for new installations — use install-megalonyx-stack.sh instead.
#
# Changes from original vs monorepo layout (marked [UPDATED] inline):
#   - venv removed; Python deps now managed by uv workspace (uv sync --all-packages)
#   - STACK_MANAGER path moved: scripts/memory_manager.py
#                             → uv run python -m agent_memory.memory_daemon
#   - memory package location: $STACK_ROOT/packages/memory/
#                             → packages/agent-memory/src/agent_memory/
#   - mega-run-py wrapper → uv run python (workspace-aware, no venv path needed)
#   - mega-memory-manager wrapper → delegates to bin/mega-memory (repo bin/)
#   - Readiness check: memory_daemon.py file check → python import check via uv
# ======================================

# ===
# ARGUMENTS & FLAGS
# ===
FORCE_CONFIG=false
FORCE_VENV=false    # [UPDATED] kept for interface compat; venv is replaced by uv workspace
FORCE_SYNC=false
VERIFY_RUNTIME=false
INSTALL_TESTS=false
for arg in "$@"; do
  if [ "$arg" == "--force-config" ]; then
    FORCE_CONFIG=true
  elif [ "$arg" == "--force-venv" ]; then
    FORCE_VENV=true
  elif [ "$arg" == "--sync-deps" ]; then
    FORCE_SYNC=true
  elif [ "$arg" == "--verify-runtime" ]; then
    VERIFY_RUNTIME=true
  elif [ "$arg" == "--install-tests" ]; then
    INSTALL_TESTS=true
  fi
done

# ===
# ROOT CONFIG
# ===

# [UPDATED] PyTorch/vLLM venv removed — sentence-transformers installed via uv workspace
# TARGET_TORCH_VERSION="2.12.0+cu130"

STACK_ROOT="$HOME/.local/share/megalonyx"
TMP_DIR="$STACK_ROOT/tmp"
# [UPDATED] PY_ROOT / VENV_ROOT removed — using uv workspace managed by the monorepo root
DATA_ROOT="$STACK_ROOT/data"
SERVICE_ROOT="$STACK_ROOT/packages"
BIN_DIR="$HOME/.local/bin"
QDRANT_DIR="$STACK_ROOT/packages/infra/qdrant"

# [UPDATED] STACK_MANAGER: was $STACK_ROOT/scripts/memory_manager.py
# Now launched via: uv run python -m agent_memory.memory_daemon
# (see mega-memory-manager wrapper below)

# SOURCE OF TRUTH (BUILD LAYER) — derived from script location for portability
INSTALL_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"

# ===
# CREATE DIRECTORY STRUCTURE
# ===

echo "[1/9] Preparing directory structure..."

mkdir -p \
  "$STACK_ROOT" \
  "$STACK_ROOT/scripts" \
  "$STACK_ROOT/validators" \
  "$STACK_ROOT/config" \
  "$STACK_ROOT/docs" \
  "$STACK_ROOT/bin" \
  "$DATA_ROOT/qdrant" \
  "$SERVICE_ROOT" \
  "$BIN_DIR" \
  "$TMP_DIR"

# ===
# SANITY CHECKS
# ===

command -v python3 >/dev/null || { echo "Missing python3"; exit 1; }
command -v git >/dev/null || { echo "Missing git"; exit 1; }
command -v curl >/dev/null || { echo "Missing curl"; exit 1; }
# [UPDATED] added uv check — replaces standalone venv requirement
command -v uv >/dev/null || { echo "Missing uv (see https://docs.astral.sh/uv/getting-started/installation/)"; exit 1; }

# ===
# PYTHON WORKSPACE SYNC
# ===

# [UPDATED] replaces the standalone venv + pip install section.
# The monorepo uses uv workspace — all three Python packages (agent-infra,
# agent-memory, control-plane-daemon) are installed as editable packages.
echo "[4/9] Syncing Python workspace (uv)..."

if [ "$FORCE_SYNC" = true ] || ! uv run python -c "import agent_memory; import control_plane_daemon; import agent_infra" >/dev/null 2>&1; then
    echo "Syncing all workspace packages..."
    uv sync --all-packages --project "$INSTALL_SRC"
    echo "[OK] Workspace synced."
else
    echo "Workspace packages already importable. Skipping sync."
fi

# ===
# DEPLOY CONFIG TEMPLATES
# ===

echo "[2.5/9] Deploying config templates..."

QDRANT_CONFIG="$STACK_ROOT/config/qdrant_config.yaml"
if [ ! -f "$QDRANT_CONFIG" ] || [ "$FORCE_CONFIG" = true ]; then
    mkdir -p "$(dirname "$QDRANT_CONFIG")"
    cat > "$QDRANT_CONFIG" <<YAML
storage:
  path: "$STACK_ROOT/data/qdrant"
YAML
    echo "[OK] Created $QDRANT_CONFIG"
else
    echo "[OK] $QDRANT_CONFIG already exists."
fi

# Deploy .env if missing
ENV_DEST="$STACK_ROOT/.env"
ENV_EXAMPLE="$INSTALL_SRC/config/megalonyx/.env.example"
if [ ! -f "$ENV_DEST" ] && [ -f "$ENV_EXAMPLE" ]; then
    cp "$ENV_EXAMPLE" "$ENV_DEST"
    echo "[OK] Copied .env.example to $ENV_DEST — fill in API keys before running."
elif [ ! -f "$ENV_DEST" ]; then
    echo "WARNING: No .env.example found; $ENV_DEST not created."
fi

# Deploy settings.json if missing
SETTINGS_DEST="$HOME/.qwen/settings.json"
SETTINGS_EXAMPLE="$INSTALL_SRC/config/settings.example.json"
if [ ! -f "$SETTINGS_DEST" ] && [ -f "$SETTINGS_EXAMPLE" ]; then
    mkdir -p "$HOME/.qwen"
    cp "$SETTINGS_EXAMPLE" "$SETTINGS_DEST"
    echo "[OK] Copied settings.example.json to $SETTINGS_DEST — review model providers before running."
elif [ ! -f "$SETTINGS_DEST" ]; then
    echo "WARNING: No settings.example.json found; $SETTINGS_DEST not created."
fi

# ===
# RUNTIME WRAPPERS
# ===

echo "[5/9] Configuring runtime wrappers in $BIN_DIR..."

# mega-status — symlink to the repo bin/ script (stays current with repo)
if [ -L "$BIN_DIR/mega-status" ] || [ ! -f "$BIN_DIR/mega-status" ]; then
    ln -sf "$INSTALL_SRC/bin/mega-status" "$BIN_DIR/mega-status"
fi
chmod +x "$INSTALL_SRC/bin/mega-status"
echo "[OK] mega-status → $INSTALL_SRC/bin/mega-status"

# mega-memory — symlink to repo bin/mega-memory (runs memory daemon via uv)
if [ -L "$BIN_DIR/mega-memory" ] || [ ! -f "$BIN_DIR/mega-memory" ]; then
    ln -sf "$INSTALL_SRC/bin/mega-memory" "$BIN_DIR/mega-memory"
fi
chmod +x "$INSTALL_SRC/bin/mega-memory"
echo "[OK] mega-memory → $INSTALL_SRC/bin/mega-memory"

# mega-tasks — symlink to repo bin/mega-tasks
if [ -L "$BIN_DIR/mega-tasks" ] || [ ! -f "$BIN_DIR/mega-tasks" ]; then
    ln -sf "$INSTALL_SRC/bin/mega-tasks" "$BIN_DIR/mega-tasks"
fi
chmod +x "$INSTALL_SRC/bin/mega-tasks"
echo "[OK] mega-tasks → $INSTALL_SRC/bin/mega-tasks"

# [UPDATED] mega-run-py: was $VENV_ROOT/bin/python3; now delegates to uv run
cat > "$BIN_DIR/mega-run-py" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec uv run --project "$INSTALL_SRC" python "\$@"
EOF
chmod +x "$BIN_DIR/mega-run-py"
echo "[OK] mega-run-py (uv-backed)"

# mega-db — Qdrant launcher
cat > "$BIN_DIR/mega-db" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "$QDRANT_DIR/bin/qdrant" \\
  --config-path "$QDRANT_CONFIG"
EOF
chmod +x "$BIN_DIR/mega-db"
echo "[OK] mega-db"

# [UPDATED] mega-memory-manager: was $VENV_ROOT/bin/python3 $STACK_MANAGER
# Now delegates to bin/mega-memory which uses uv run
cat > "$BIN_DIR/mega-memory-manager" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "$BIN_DIR/mega-memory" "\$@"
EOF
chmod +x "$BIN_DIR/mega-memory-manager"
echo "[OK] mega-memory-manager (delegates to mega-memory)"

# mega-reboot
cat > "$BIN_DIR/mega-reboot" <<EOF
#!/usr/bin/env bash
set -euo pipefail
echo "[reboot] Restarting stack services..."
"$BIN_DIR/mega-memory-manager" restart
echo "[reboot] Verifying health..."
"$BIN_DIR/mega-status"
EOF
chmod +x "$BIN_DIR/mega-reboot"
echo "[OK] mega-reboot"

# ===
# QDRANT INSTALL
# ===

echo "[6/9] Installing Qdrant..."

if [ -f "$QDRANT_DIR/bin/qdrant" ]; then
    echo "Qdrant already installed. Skipping download."
else
    ARCH="$(uname -m)"
    OS="$(uname -s)"
    case "$OS-$ARCH" in
        Linux-x86_64)  QDRANT_ASSET="qdrant-x86_64-unknown-linux-gnu.tar.gz" ;;
        Linux-aarch64) QDRANT_ASSET="qdrant-aarch64-unknown-linux-gnu.tar.gz" ;;
        Darwin-x86_64) QDRANT_ASSET="qdrant-x86_64-apple-darwin.tar.gz" ;;
        Darwin-arm64)  QDRANT_ASSET="qdrant-aarch64-apple-darwin.tar.gz" ;;
        *) echo "ERROR: unsupported platform $OS-$ARCH"; exit 1 ;;
    esac

    QDRANT_VERSION=$(curl -sf --max-time 10 \
      "https://api.github.com/repos/qdrant/qdrant/releases/latest" \
      | grep '"tag_name"' | head -n 1 | cut -d '"' -f4)

    echo "Downloading Qdrant $QDRANT_VERSION ($QDRANT_ASSET)..."
    mkdir -p "$QDRANT_DIR/bin"
    curl -L \
      "https://github.com/qdrant/qdrant/releases/download/${QDRANT_VERSION}/${QDRANT_ASSET}" \
      -o "$QDRANT_DIR/qdrant.tar.gz"
    tar -xzf "$QDRANT_DIR/qdrant.tar.gz" -C "$QDRANT_DIR/bin"
    rm "$QDRANT_DIR/qdrant.tar.gz"
    chmod +x "$QDRANT_DIR/bin/qdrant"
    echo "[OK] Qdrant $QDRANT_VERSION installed."
fi

# ===
# VALIDATION
# ===

echo "[8/9] Verifying deployment readiness..."

readiness_check() {
    echo "[Validation] Running readiness check..."

    # [UPDATED] was: check for $SERVICE_ROOT/memory/memory_daemon.py
    # Now: check importability via uv workspace
    if ! uv run --project "$INSTALL_SRC" python -c \
        "import agent_memory; import control_plane_daemon; import agent_infra" \
        >/dev/null 2>&1; then
        echo "ERROR: One or more Python packages not importable. Run: uv sync --all-packages"
        return 1
    fi

    if [ ! -x "$BIN_DIR/mega-db" ]; then
        echo "ERROR: mega-db not found in $BIN_DIR"
        return 1
    fi

    if [ ! -f "$QDRANT_CONFIG" ]; then
        echo "ERROR: qdrant_config.yaml missing at $QDRANT_CONFIG"
        return 1
    fi

    echo "[OK] Deployment is ready."
    return 0
}

if ! readiness_check; then
    exit 1
fi

if [ "$VERIFY_RUNTIME" = true ]; then
    echo "[Validation] Starting full runtime verification..."
    uv run --project "$INSTALL_SRC" python3 tooling/smoke-tests/boot_verification.py --skip-memory
fi

# ===
# DONE
# ===

echo ""
echo "=========================================="
echo " INSTALLATION COMPLETE"
echo "=========================================="
echo ""
echo "STACK DATA:   $STACK_ROOT"
echo "BIN WRAPPERS: $BIN_DIR"
echo ""
echo "COMMANDS:"
echo "  mega-memory          start the memory daemon"
echo "  mega-db              start Qdrant"
echo "  mega-status          show service health"
echo "  mega-tasks           manage active tasks"
echo "  mega-reboot          restart all services"
echo ""
echo "Next: fill in $ENV_DEST (API keys) and $SETTINGS_DEST (model providers)."
echo "=========================================="
