#!/usr/bin/env bash
set -euo pipefail

# ======================================
# MEGALONYX STACK INSTALLER (RUNTIME STACK)
# ======================================
#
# Sets up the Megalonyx Python stack as a Runtime Stack on the Machine.
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
BIN_STACK_DIR="$STACK_ROOT/bin"
APPS_STACK_DIR="$STACK_ROOT/apps"
QDRANT_DIR="$STACK_ROOT/packages/infra/qdrant"
QDRANT_CONFIG="$CONFIG_ROOT/qdrant_config.yaml"

# ===
# PREREQUISITES
# ===
echo "[1/9] Checking prerequisites..."
command -v uv    >/dev/null || { echo "Missing uv"; exit 1; }
command -v curl  >/dev/null || { echo "Missing curl"; exit 1; }
echo "[OK] Prerequisites satisfied."

# ===
# DIRECTORY STRUCTURE
# ===
echo "[2/9] Preparing directory structure..."
mkdir -p \
  "$CONFIG_ROOT" \
  "$QWEN_CONFIG_ROOT" \
  "$DATA_ROOT/qdrant" \
  "$STACK_ROOT/logs" \
  "$STACK_ROOT/memory" \
  "$STACK_ROOT/tmp" \
  "$STACK_ROOT/packages" \
  "$BIN_STACK_DIR" \
  "$APPS_STACK_DIR" \
  "$BIN_DIR"
echo "[OK] Directory structure ready ($STACK_ROOT)"

# ===
# PHYSICAL DEPLOYMENT (Blueprint -> Machine)
# ===
echo "[3/9] Physically deploying Blueprint to Machine..."
if [ -d "$REPO_ROOT/packages" ]; then
    cp -r "$REPO_ROOT/packages/"* "$STACK_ROOT/packages/"
    echo "[OK] Core packages deployed to $STACK_ROOT/packages"
else
    echo "ERROR: Blueprint packages directory not found at $REPO_ROOT/packages"
    exit 1
fi

if [ -d "$REPO_ROOT/apps" ]; then
    cp -r "$REPO_ROOT/apps/"* "$APPS_STACK_DIR/"
    echo "[OK] Apps deployed to $APPS_STACK_DIR"
else
    echo "WARNING: Blueprint apps directory not found at $REPO_ROOT/apps"
fi

if [ -d "$REPO_ROOT/bin" ]; then
    cp -r "$REPO_ROOT/bin/"* "$BIN_STACK_DIR/"
    echo "[OK] Binaries deployed to $BIN_STACK_DIR"
else
    echo "WARNING: Blueprint bin directory not found at $REPO_ROOT/bin"
fi

# ===
# RUNTIME ENVIRONMENT (The Body)
# ===
echo "[4/9] Creating Runtime Python environment..."
if [ "$FORCE_SYNC" = true ] || [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv at $VENV_DIR..."
    uv venv --clear "$VENV_DIR"

    echo "Installing dependencies from Blueprint..."
    # Install from requirements first
    uv pip install --python "$VENV_DIR/bin/python" -r "$REPO_ROOT/requirements.txt" 2>/dev/null || true

    # Install specific packages from the monorepo to the local venv
    uv pip install --python "$VENV_DIR/bin/python" "$REPO_ROOT/packages/agent-infra"
    uv pip install --python "$VENV_DIR/bin/python" "$REPO_ROOT/packages/agent-memory"
    uv pip install --python "$VENV_DIR/bin/python" "$REPO_ROOT/apps/control-plane-daemon"
    echo "[OK] Runtime environment ready."
else
    echo "[OK] Existing venv found at $VENV_DIR."
fi

# ===
# CONFIG TEMPLATES
# ===
echo "[5/9] Deploying config templates..."
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
echo "[6/9] Configuring runtime wrappers in $BIN_DIR..."

# mega-run-py — RUNTIME: resolves relative paths against the Machine root
cat > "$BIN_DIR/mega-run-py" <<EOF
#!/usr/bin/env bash
set -euo pipefail
S_ROOT="$HOME/.local/share/megalonyx"
cd "\$S_ROOT"
exec "\$S_ROOT/py/venv/bin/python" "\$@"
EOF
chmod +x "$BIN_DIR/mega-run-py"
echo "[OK] mega-run-py (runtime)"

# mega-db
cat > "$BIN_DIR/mega-db" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$DATA_ROOT"
export QDRANT__STORAGE__PATH="."
exec "$QDRANT_DIR/bin/qdrant" --config-path "$QDRANT_CONFIG"
EOF
chmod +x "$BIN_DIR/mega-db"

# ===
# QDRANT
# ===
echo "[7/9] Installing Qdrant..."
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
echo "[8/9] Verifying deployment readiness..."
if ! "$VENV_DIR/bin/python" -c "import agent_memory; import control_plane_daemon; import agent_infra" 2>/dev/null; then
    echo "ERROR: Packages not importable in Runtime venv."
    exit 1
fi
echo "[OK] Deployment is ready and functional."
echo "=========================================="
