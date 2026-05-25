#!/usr/bin/env bash
set -euo pipefail

# ======================================
# MEGALONYX STACK INSTALLER
# ======================================
#
# Sets up the Megalonyx Python stack in the current environment.
# Assumes the monorepo is already cloned. Does NOT install the
# upstream Qwen Code CLI — use install-megalonyx-full.sh for that.
#
# Usage:
#   bash scripts/megalonyx/install-megalonyx-stack.sh [OPTIONS]
#
# Options:
#   --force-config     Overwrite existing config files
#   --sync-deps        Force uv sync even if packages are importable
#   --verify-runtime   Run boot_verification.py after install
# ======================================

# ===
# ARGUMENTS & FLAGS
# ===
FORCE_CONFIG=false
FORCE_SYNC=false
VERIFY_RUNTIME=false
for arg in "$@"; do
  case "$arg" in
    --force-config)   FORCE_CONFIG=true ;;
    --sync-deps)      FORCE_SYNC=true ;;
    --verify-runtime) VERIFY_RUNTIME=true ;;
  esac
done

# ===
# PATH SETUP
# ===

# Derive repo root from script location — no hard-coded paths
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"

STACK_ROOT="$HOME/.local/share/megalonyx"       # XDG_DATA_HOME: application data
CONFIG_ROOT="$HOME/.config/megalonyx"          # XDG_CONFIG_HOME: Megalonyx config + secrets
QWEN_CONFIG_ROOT="$HOME/.config/qwen"          # XDG_CONFIG_HOME: Qwen Code CLI config
DATA_ROOT="$STACK_ROOT/data"
BIN_DIR="$HOME/.local/bin"
QDRANT_DIR="$STACK_ROOT/packages/infra/qdrant"
QDRANT_CONFIG="$CONFIG_ROOT/qdrant_config.yaml"

# ===
# PREREQUISITES
# ===

echo "[1/7] Checking prerequisites..."

command -v uv    >/dev/null || { echo "Missing uv — see https://docs.astral.sh/uv/getting-started/installation/"; exit 1; }
command -v curl  >/dev/null || { echo "Missing curl"; exit 1; }

echo "[OK] Prerequisites satisfied."

# ===
# DIRECTORY STRUCTURE
# ===

echo "[2/7] Preparing directory structure..."

mkdir -p \
  "$CONFIG_ROOT" \
  "$QWEN_CONFIG_ROOT" \
  "$DATA_ROOT/qdrant" \
  "$STACK_ROOT/logs" \
  "$STACK_ROOT/memory" \
  "$STACK_ROOT/tmp" \
  "$STACK_ROOT/packages" \
  "$BIN_DIR"

echo "[OK] Directory structure ready ($STACK_ROOT, $CONFIG_ROOT)"

# ===
# PYTHON WORKSPACE SYNC
# ===

echo "[3/7] Syncing Python workspace (uv)..."

if [ "$FORCE_SYNC" = true ] || ! uv run --project "$REPO_ROOT" python -c \
    "import agent_memory; import control_plane_daemon; import agent_infra" \
    >/dev/null 2>&1; then
    echo "Syncing all workspace packages..."
    uv sync --all-packages --project "$REPO_ROOT"
    echo "[OK] Workspace synced."
else
    echo "Workspace packages already importable. Use --sync-deps to force."
fi

# ===
# CONFIG TEMPLATES
# ===

echo "[4/7] Deploying config templates..."

# qdrant_config.yaml — rendered from template with actual data path
if [ ! -f "$QDRANT_CONFIG" ] || [ "$FORCE_CONFIG" = true ]; then
    cat > "$QDRANT_CONFIG" <<YAML
storage:
  path: "$DATA_ROOT/qdrant"
YAML
    echo "[OK] Created $QDRANT_CONFIG"
else
    echo "[OK] $QDRANT_CONFIG already exists."
fi

# .env — deployed to XDG_CONFIG_HOME/megalonyx/ (loaded at runtime by bin/mega-memory)
ENV_DEST="$CONFIG_ROOT/.env"
ENV_EXAMPLE="$REPO_ROOT/config/megalonyx/.env.example"
if [ ! -f "$ENV_DEST" ] || [ "$FORCE_CONFIG" = true ]; then
    if [ -f "$ENV_EXAMPLE" ]; then
        cp "$ENV_EXAMPLE" "$ENV_DEST"
        echo "[OK] Copied .env.example to $ENV_DEST — fill in API keys before running."
    else
        echo "WARNING: $ENV_EXAMPLE not found; $ENV_DEST not created."
    fi
else
    echo "[OK] $ENV_DEST already exists."
fi

# settings.json — deployed to XDG_CONFIG_HOME/qwen/ (read by Qwen Code CLI via QWEN_HOME)
SETTINGS_DEST="$QWEN_CONFIG_ROOT/settings.json"
SETTINGS_EXAMPLE="$REPO_ROOT/config/settings.example.json"
if [ ! -f "$SETTINGS_DEST" ] || [ "$FORCE_CONFIG" = true ]; then
    if [ -f "$SETTINGS_EXAMPLE" ]; then
        cp "$SETTINGS_EXAMPLE" "$SETTINGS_DEST"
        echo "[OK] Copied settings.example.json to $SETTINGS_DEST — review model providers before running."
    else
        echo "WARNING: $SETTINGS_EXAMPLE not found; $SETTINGS_DEST not created."
    fi
else
    echo "[OK] $SETTINGS_DEST already exists."
fi

# Shell profile — export QWEN_HOME so the CLI finds config in ~/.config/qwen/
QWEN_HOME_EXPORT="export QWEN_HOME=\"\$HOME/.config/qwen\""
SHELL_RC=""
FISH_RC=""
case "${SHELL:-}" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
    */fish) FISH_RC="$HOME/.config/fish/conf.d/megalonyx.fish" ;;
esac
if [ -n "$FISH_RC" ]; then
    mkdir -p "$(dirname "$FISH_RC")"
    if ! grep -qF 'QWEN_HOME' "$FISH_RC" 2>/dev/null; then
        echo "# Qwen Code CLI: use XDG config dir instead of ~/.qwen" >> "$FISH_RC"
        echo "set -Ux QWEN_HOME \$HOME/.config/qwen" >> "$FISH_RC"
        echo "[OK] Added QWEN_HOME to $FISH_RC — restart your shell"
    else
        echo "[OK] QWEN_HOME already set in $FISH_RC"
    fi
elif [ -n "$SHELL_RC" ]; then
    if ! grep -qF 'QWEN_HOME' "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# Qwen Code CLI: use XDG config dir instead of ~/.qwen" >> "$SHELL_RC"
        echo "$QWEN_HOME_EXPORT" >> "$SHELL_RC"
        echo "[OK] Added QWEN_HOME to $SHELL_RC — restart your shell or: source $SHELL_RC"
    else
        echo "[OK] QWEN_HOME already set in $SHELL_RC"
    fi
else
    echo "[ACTION REQUIRED] Add to your shell profile: $QWEN_HOME_EXPORT"
fi

# ===
# BIN WRAPPERS
# ===

echo "[5/7] Configuring runtime wrappers in $BIN_DIR..."

# mega-memory, mega-status, mega-tasks — symlinks to repo bin/ (stay current with repo)
for script in mega-memory mega-status mega-tasks; do
    target="$REPO_ROOT/bin/$script"
    link="$BIN_DIR/$script"
    chmod +x "$target"
    # Only create symlink if not already pointing to the right place
    if [ ! -L "$link" ] || [ "$(readlink "$link")" != "$target" ]; then
        ln -sf "$target" "$link"
    fi
    echo "[OK] $script → $target"
done

# mega-run-py — delegates to uv run python in the workspace context
cat > "$BIN_DIR/mega-run-py" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec uv run --project "$REPO_ROOT" python "\$@"
EOF
chmod +x "$BIN_DIR/mega-run-py"
echo "[OK] mega-run-py (uv-backed)"

# mega-db — Qdrant launcher
cat > "$BIN_DIR/mega-db" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$DATA_ROOT"
export QDRANT__STORAGE__PATH="."
exec "$QDRANT_DIR/bin/qdrant" \\
  --config-path "$QDRANT_CONFIG"
EOF
chmod +x "$BIN_DIR/mega-db"
echo "[OK] mega-db"

# mega-reboot — kill and restart all services, then print status
cat > "$BIN_DIR/mega-reboot" <<EOF
#!/usr/bin/env bash
set -euo pipefail
echo "[reboot] Stopping stack services..."
pkill -f "agent_memory.memory_daemon" 2>/dev/null || true
pkill -f "qdrant" 2>/dev/null || true
sleep 1
echo "[reboot] Starting stack services..."
"$BIN_DIR/mega-db" &
"$BIN_DIR/mega-memory" &
sleep 2
echo "[reboot] Verifying health..."
"$BIN_DIR/mega-status"
EOF
chmod +x "$BIN_DIR/mega-reboot"
echo "[OK] mega-reboot"

# ===
# QDRANT
# ===

echo "[6/7] Installing Qdrant..."

if [ -f "$QDRANT_DIR/bin/qdrant" ]; then
    echo "Qdrant already installed at $QDRANT_DIR/bin/qdrant. Skipping download."
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
    echo "[OK] Qdrant $QDRANT_VERSION installed at $QDRANT_DIR/bin/qdrant"
fi

# ===
# VERIFICATION
# ===

echo "[7/7] Verifying deployment readiness..."

READINESS_OK=true

if ! uv run --project "$REPO_ROOT" python -c \
    "import agent_memory; import control_plane_daemon; import agent_infra" \
    >/dev/null 2>&1; then
    echo "ERROR: Python packages not importable. Run with --sync-deps to re-sync."
    READINESS_OK=false
fi

if [ ! -x "$BIN_DIR/mega-db" ]; then
    echo "ERROR: mega-db not found or not executable in $BIN_DIR"
    READINESS_OK=false
fi

if [ ! -f "$QDRANT_CONFIG" ]; then
    echo "ERROR: qdrant_config.yaml missing at $QDRANT_CONFIG"
    READINESS_OK=false
fi

if [ "$READINESS_OK" = false ]; then
    exit 1
fi

echo "[OK] Deployment is ready."

if [ "$VERIFY_RUNTIME" = true ]; then
    echo "[Validation] Running full boot verification..."
    uv run --project "$REPO_ROOT" python3 "$REPO_ROOT/tooling/smoke-tests/boot_verification.py" --skip-memory
fi

# ===
# DONE
# ===

echo ""
echo "=========================================="
echo " INSTALLATION COMPLETE"
echo "=========================================="
echo ""
echo "CONFIG:       $CONFIG_ROOT"
echo "DATA:         $STACK_ROOT"
echo "BIN:          $BIN_DIR"
echo ""
echo "COMMANDS:"
echo "  mega-memory          start the memory daemon"
echo "  mega-db              start Qdrant"
echo "  mega-status          show service health"
echo "  mega-tasks           manage active tasks"
echo "  mega-reboot          restart all services"
echo ""
echo "Next steps:"
echo "  1. Fill in $ENV_DEST (API keys)"
echo "  2. Review $SETTINGS_DEST (model providers)"
echo "  3. Restart your shell (or: source your shell RC) so QWEN_HOME takes effect"
echo "  4. Start Qdrant:  mega-db"
echo "  5. Start memory:  mega-memory"
echo "=========================================="
