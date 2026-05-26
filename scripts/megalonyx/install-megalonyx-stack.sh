#!/usr/bin/env bash
set -euo pipefail

# ======================================
# MEGALONYX STACK INSTALLER (SOVEREIGN)
# ======================================
#
# Sets up the Megalonyx Python stack as a standalone entity on the Machine.
# Decouples the runtime from the monorepo Blueprint.
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
        *)                ;;
    esac
done

# ===
# PATH SETUP
# ===
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"
STACK_ROOT="$HOME/.local/share/megalonyx"
CONFIG_ROOT="$HOME/.config/megalonyx"
QWEN_CONFIG_ROOT="$HOME/.config/qwen"
DATA_ROOT="$STACK_ROOT/data"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$STACK_ROOT/py/venv"
QDRANT_DIR="$STACK_ROOT/packages/infra/qdrant"
QDRANT_CONFIG="$CONFIG_ROOT/qdrant_config.yaml"

# ===
# PREREQUISITES
# ===
echo "[1/8] Checking prerequisites..."
command -v uv    >/dev/null || { echo "Missing uv"; exit 1; }
command -v curl  >/dev/null || { echo "Missing curl"; exit 1; }
echo "[OK] Prerequisites satisfied."

# ===
# DIRECTORY STRUCTURE
# ===
echo "[2/8] Preparing directory structure..."
mkdir -p \
  "$CONFIG_ROOT" \
  "$QWEN_CONFIG_ROOT" \
  "$DATA_ROOT/qdrant" \
  "$STACK_ROOT/logs" \
  "$STACK_ROOT/memory" \
  "$STACK_ROOT/tmp" \
  "$STACK_ROOT/packages" \
  "$BIN_DIR"
echo "[OK] Directory structure ready ($STACK_ROOT)"

# ===
# STANDALONE ENVIRONMENT (The Body)
# ===
echo "[3/8] Creating standalone Python environment..."
if [ "$FORCE_SYNC" = true ] || [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv at $VENV_DIR..."
    uv venv --clear "$VENV_DIR"
    
    echo "Installing dependencies from Blueprint..."
    # Install specific packages from the monorepo to avoid setuptools flat-layout errors
    uv pip install --python "$VENV_DIR/bin/python" -r "$REPO_ROOT/requirements.txt" 2>/dev/null || true
    uv pip install --python "$VENV_DIR/bin/python" "$REPO_ROOT/packages/agent-memory"
    uv pip install --python "$VENV_DIR/bin/python" "$REPO_ROOT/apps/control-plane-daemon"
    uv pip install --python "$VENV_DIR/bin/python" "$REPO_ROOT/packages/agent-infra"
    echo "[OK] Standalone environment ready."
else
    echo "[OK] Existing venv found at $VENV_DIR."
fi

# ===
# SCRIPT DEPLOYMENT (Blueprint -> Machine)
# ===
echo "[4/8] Deploying scripts to the Machine..."
# Copy core packages to ensure the Machine is self-sufficient
if [ -d "$REPO_ROOT/packages" ]; then
    cp -r "$REPO_ROOT/packages/"* "$STACK_ROOT/packages/"
    echo "[OK] Core packages deployed to $STACK_ROOT/packages"
else
    echo "ERROR: Blueprint packages directory not found at $REPO_ROOT/packages"
    exit 1
fi

# Explicitly deploy the bridge relay from apps/ to packages/ for runtime consistency
BRIDGE_SRC="$REPO_ROOT/apps/control-plane-daemon/src/control_plane_daemon/stdio_socket_relay.py"
BRIDGE_DEST="$STACK_ROOT/packages/core/src/stdio_socket_relay.py"
if [ -f "$BRIDGE_SRC" ]; then
    mkdir -p "$(dirname "$BRIDGE_DEST")"
    cp "$BRIDGE_SRC" "$BRIDGE_DEST"
    echo "[OK] Bridge relay deployed to $BRIDGE_DEST"
else
    echo "WARNING: Bridge relay not found at $BRIDGE_SRC"
fi

# ===
# CONFIG TEMPLATES
# ===
echo "[5/8] Deploying config templates..."
if [ ! -f "$QDRANT_CONFIG" ] || [ "$FORCE_CONFIG" = true ]; then
    cat > "$QDRANT_CONFIG" <<YAML
storage:
  path: "$DATA_ROOT/qdrant"
YAML
    echo "[OK] Created $QDRANT_CONFIG"
fi

ENV_DEST="$CONFIG_ROOT/.env"
ENV_EXAMPLE="$REPO_ROOT/config/megalonyx/.env.example"
if [ ! -f "$ENV_DEST" ] || [ "$FORCE_CONFIG" = true ]; then
    [ -f "$ENV_EXAMPLE" ] && cp "$ENV_EXAMPLE" "$ENV_DEST" && echo "[OK] Copied .env.example"
fi

SETTINGS_DEST="$QWEN_CONFIG_ROOT/settings.json"
SETTINGS_EXAMPLE="$REPO_ROOT/config/settings.example.json"
if [ ! -f "$SETTINGS_DEST" ] || [ "$FORCE_CONFIG" = true ]; then
    [ -f "$SETTINGS_EXAMPLE" ] && cp "$SETTINGS_EXAMPLE" "$SETTINGS_DEST" && echo "[OK] Copied settings.example.json"
fi

# Shell profile
QWEN_HOME_EXPORT="export QWEN_HOME=\"\$HOME/.config/qwen\""
SHELL_RC=""
FISH_RC=""
case "${SHELL:-}" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
    */fish) FISH_RC="$HOME/.config/fish/conf.d/megalonyx.fish" ;;
esac
if [ -n "$FISH_RC" ]; then
    echo "set -Ux QWEN_HOME \$HOME/.config/qwen" >> "$FISH_RC"
elif [ -n "$SHELL_RC" ]; then
    grep -qF 'QWEN_HOME' "$SHELL_RC" || echo "$QWEN_HOME_EXPORT" >> "$SHELL_RC"
fi

# ===
# BIN WRAPPERS
# ===
echo "[6/8] Configuring runtime wrappers in $BIN_DIR..."

# mega-memory, mega-status, mega-tasks
for script in mega-memory mega-status mega-tasks; do
    target="$REPO_ROOT/bin/$script"
    link="$BIN_DIR/$script"
    chmod +x "$target"
    ln -sf "$target" "$link"
done

# mega-run-py — NOW SOVEREIGN: uses local venv, not monorepo project
cat > "$BIN_DIR/mega-run-py" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "$VENV_DIR/bin/python" "\$@"
EOF
chmod +x "$BIN_DIR/mega-run-py"
echo "[OK] mega-run-py (standalone)"

# mega-db
cat > "$BIN_DIR/mega-db" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$DATA_ROOT"
export QDRANT__STORAGE__PATH="."
exec "$QDRANT_DIR/bin/qdrant" --config-path "$QDRANT_CONFIG"
EOF
chmod +x "$BIN_DIR/mega-db"

# mega-reboot
cat > "$BIN_DIR/mega-reboot" <<EOF
#!/usr/bin/env bash
set -euo pipefail
echo "[reboot] Stopping stack services..."
pkill -f "memory_daemon" 2>/dev/null || true
pkill -f "qdrant" 2>/dev/null || true
sleep 1
echo "[reboot] Starting stack services..."
"$BIN_DIR/mega-db" &
"$BIN_DIR/mega-memory" &
sleep 2
"$BIN_DIR/mega-status"
EOF
chmod +x "$BIN_DIR/mega-reboot"

# ===
# QDRANT
# ===
echo "[7/8] Installing Qdrant..."
if [ ! -f "$QDRANT_DIR/bin/qdrant" ]; then
    ARCH="$(uname -m)"; OS="$(uname -s)"
    case "$OS-$ARCH" in
        Linux-x86_64)  QDRANT_ASSET="qdrant-x86_64-unknown-linux-gnu.tar.gz" ;;
        Linux-aarch64) QDRANT_ASSET="qdrant-aarch64-unknown-linux-gnu.tar.gz" ;;
        *) echo "ERROR: unsupported platform"; exit 1 ;;
    esac
    QDRANT_VERSION=$(curl -sf "https://api.github.com/repos/qdrant/qdrant/releases/latest" | grep '"tag_name"' | head -n 1 | cut -d '"' -f4)
    mkdir -p "$QDRANT_DIR/bin"
    curl -L "https://github.com/qdrant/qdrant/releases/download/${QDRANT_VERSION}/${QDRANT_ASSET}" -o "$QDRANT_DIR/qdrant.tar.gz"
    tar -xzf "$QDRANT_DIR/qdrant.tar.gz" -C "$QDRANT_DIR/bin"
    rm "$QDRANT_DIR/qdrant.tar.gz"
    chmod +x "$QDRANT_DIR/bin/qdrant"
fi

# ===
# VERIFICATION
# ===
echo "[8/8] Verifying deployment readiness..."
if ! "$VENV_DIR/bin/python" -c "import agent_memory; import control_plane_daemon; import agent_infra" 2>/dev/null; then
    echo "ERROR: Packages not importable in standalone venv."
    exit 1
fi
echo "[OK] Deployment is ready and sovereign."
echo "=========================================="
