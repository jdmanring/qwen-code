#!/usr/bin/env bash
set -euo pipefail

# ======================================
# MEGALONYX FULL INSTALLER
# ======================================
#
# Builds the Qwen Code CLI from monorepo source using the upstream esbuild
# pipeline and installs the Megalonyx Python stack.
#
# Build pipeline (CLI):
#   1. pnpm install
#   2. node packages/web-templates/build.mjs   (generate TS assets)
#   3. node scripts/build_package.js            (tsc --build each internal dep)
#   4. node esbuild.config.js                   (bundle → dist/cli.js)
#   5. node scripts/copy_bundle_assets.js       (vendor, skills, locales → dist/)
#
# Prerequisites: node 22+, pnpm 11+, uv, curl
#
# Usage:
#   bash scripts/megalonyx/install-megalonyx-full.sh [OPTIONS]
#
# Options:
#   --skip-cli           Skip the Node.js CLI build (re-run stack only)
#   --force-config       Overwrite existing config files
#   --sync-deps          Force uv sync even if packages are importable
#   --verify-runtime     Run boot_verification.py after install
# ======================================

SKIP_CLI=false
STACK_ARGS=()

for arg in "$@"; do
  case "$arg" in
    --skip-cli)       SKIP_CLI=true ;;
    --force-config)   STACK_ARGS+=("--force-config") ;;
    --sync-deps)      STACK_ARGS+=("--sync-deps") ;;
    --verify-runtime) STACK_ARGS+=("--verify-runtime") ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"
STACK_INSTALLER="$REPO_ROOT/scripts/megalonyx/install-megalonyx-stack.sh"
BUILD_PACKAGE_SCRIPT="$REPO_ROOT/scripts/build_package.js"
BIN_DIR="$HOME/.local/bin"
CLI_BUNDLE="$REPO_ROOT/dist/cli.js"

# ===
# Helpers
# ===

die() { echo "ERROR: $*" >&2; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "$1 is required. ${2:-}"
}

# Remove the root dist/ if a build step fails mid-run, so the next run starts
# clean rather than from an inconsistent partial state.
_cli_build_started=false
_cleanup_partial_dist() {
  if [ "$_cli_build_started" = true ] && [ -d "$REPO_ROOT/dist" ]; then
    echo "Cleaning partial dist/ after build failure." >&2
    rm -rf "$REPO_ROOT/dist"
  fi
}
trap '_cleanup_partial_dist' ERR

# Run a build step with a label; exit non-zero if the command fails.
run_step() {
  local label="$1"; shift
  echo "  → $label"
  if ! "$@"; then
    die "Step failed: $label"
  fi
}

verify_file() {
  local path="$1" label="$2"
  [[ -f "$path" ]] || die "Expected output missing: $path ($label)"
}

echo ""
echo "=========================================="
echo " MEGALONYX FULL INSTALLER"
echo "=========================================="
echo ""

# ===
# STEP 1: QWEN CODE CLI (build from source)
# ===

if [ "$SKIP_CLI" = true ]; then
    echo "[1/2] Skipping CLI build (--skip-cli)"
else
    echo "[1/2] Building Qwen Code CLI from source..."

    # --- Prerequisite checks ---
    require_cmd node  "Install from https://nodejs.org/ (v22+ required)"
    require_cmd pnpm  "Install: npm install -g pnpm"

    NODE_MAJOR=$(node -e "process.stdout.write(String(process.versions.node.split('.')[0]))")
    (( NODE_MAJOR >= 22 )) || die "Node.js 22+ required (found $(node --version))"

    PNPM_MAJOR=$(pnpm --version | cut -d. -f1)
    (( PNPM_MAJOR >= 10 )) || die "pnpm 10+ required (found $(pnpm --version))"

    echo "  node $(node --version)  pnpm $(pnpm --version)"

    _cli_build_started=true

    # --- 1a. Install Node.js dependencies ---
    run_step "pnpm install" \
        pnpm install --dir "$REPO_ROOT" --config.dangerouslyAllowAllBuilds=true

    # Make workspace-local binaries (tsc, etc.) available to child processes
    export PATH="$REPO_ROOT/node_modules/.bin:$PATH"

    # --- 1b. Full build via pnpm ---
    # Runs: generate-git-commit-info → nx build (web-templates, tsc for all
    # packages via project references) → esbuild bundle → copy bundle assets.
    run_step "pnpm build" \
        pnpm --dir "$REPO_ROOT" build

    verify_file "$CLI_BUNDLE" "esbuild output"

    # --- 1f. Smoke-test the bundle ---
    echo "  → verifying bundle runs"
    CLI_VERSION=$(node "$CLI_BUNDLE" --version 2>&1) \
        || die "'node dist/cli.js --version' failed — check build output above"
    echo "  [OK] dist/cli.js reports version: $CLI_VERSION"

    # --- 1g. Install wrapper into PATH ---
    mkdir -p "$BIN_DIR"
    cat > "$BIN_DIR/qwen" <<EOF
#!/usr/bin/env bash
exec node "$CLI_BUNDLE" "\$@"
EOF
    chmod +x "$BIN_DIR/qwen"
    echo "  [OK] installed qwen → $CLI_BUNDLE"

    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo ""
        echo "  NOTE: $BIN_DIR is not on your PATH."
        echo "  Add this to your shell RC file:"
        echo "    export PATH=\"$BIN_DIR:\$PATH\""
    fi

    echo "[OK] Qwen Code CLI build complete (v${CLI_VERSION})"
fi

# ===
# STEP 2: MEGALONYX STACK
# ===

echo ""
echo "[2/2] Installing Megalonyx stack..."
bash "$STACK_INSTALLER" "${STACK_ARGS[@]+"${STACK_ARGS[@]}"}"

# ===
# STEP 3: GIT REMOTES
# ===

echo ""
echo "[3/3] Configuring git remotes..."

UPSTREAM_SSH="git@github.com:jdmanring/qwen-code.git"
UPSTREAM_HTTPS="https://github.com/jdmanring/qwen-code.git"

if git -C "$REPO_ROOT" remote get-url upstream >/dev/null 2>&1; then
    CURRENT_URL="$(git -C "$REPO_ROOT" remote get-url upstream)"
    if [ "$CURRENT_URL" = "$UPSTREAM_HTTPS" ]; then
        git -C "$REPO_ROOT" remote set-url upstream "$UPSTREAM_SSH"
        echo "  [OK] upstream remote corrected: HTTPS → SSH"
    else
        echo "  [OK] upstream remote already configured: $CURRENT_URL"
    fi
else
    git -C "$REPO_ROOT" remote add upstream "$UPSTREAM_SSH"
    echo "  [OK] upstream remote added: $UPSTREAM_SSH"
fi

# ===
# DONE
# ===

echo ""
echo "=========================================="
echo " FULL INSTALLATION COMPLETE"
echo "=========================================="
echo ""
echo "CLI:    qwen (bundled from packages/cli/ via esbuild)"
echo "Stack:  mega-stack {start|stop|restart|status}  — manage Qdrant + memory daemon"
echo "        mega-db                                  — start Qdrant directly"
echo ""
echo "Restart your shell (or source your RC file) so QWEN_HOME takes effect."
echo "See docs/megalonyx/installation.md for next steps."
echo "=========================================="
