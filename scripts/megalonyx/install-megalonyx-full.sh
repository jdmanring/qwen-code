#!/usr/bin/env bash
set -euo pipefail

# ======================================
# MEGALONYX FULL INSTALLER
# ======================================
#
# Installs the complete Megalonyx stack:
#   1. Upstream Qwen Code CLI (from scripts/installation/)
#   2. Megalonyx Python stack (uv workspace + Qdrant + bin wrappers)
#
# Run this on a clean machine. For stack-only updates (no Qwen Code
# reinstall needed), use install-megalonyx-stack.sh directly.
#
# Usage:
#   bash scripts/megalonyx/install-megalonyx-full.sh [OPTIONS]
#
# Options:
#   --skip-qwen          Skip Qwen Code installation (re-run stack only)
#   --force-config       Overwrite existing config files
#   --sync-deps          Force uv sync even if packages are importable
#   --verify-runtime     Run boot_verification.py after install
# ======================================

SKIP_QWEN=false
STACK_ARGS=()

for arg in "$@"; do
  case "$arg" in
    --skip-qwen)      SKIP_QWEN=true ;;
    --force-config)   STACK_ARGS+=("--force-config") ;;
    --sync-deps)      STACK_ARGS+=("--sync-deps") ;;
    --verify-runtime) STACK_ARGS+=("--verify-runtime") ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"
QWEN_INSTALLER="$REPO_ROOT/scripts/installation/install-qwen-standalone.sh"
STACK_INSTALLER="$REPO_ROOT/scripts/megalonyx/install-megalonyx-stack.sh"

echo ""
echo "=========================================="
echo " MEGALONYX FULL INSTALLER"
echo "=========================================="
echo ""

# ===
# STEP 1: QWEN CODE CLI
# ===

if [ "$SKIP_QWEN" = true ]; then
    echo "[1/2] Skipping Qwen Code installation (--skip-qwen)"
else
    echo "[1/2] Installing Qwen Code CLI..."
    if [ ! -f "$QWEN_INSTALLER" ]; then
        echo "ERROR: Upstream installer not found at $QWEN_INSTALLER"
        echo "This file is managed by the upstream sync pipeline."
        echo "Run: python3 tooling/sync-upstreams/upstream_ingest_pipeline.py"
        exit 1
    fi
    bash "$QWEN_INSTALLER"
    echo "[OK] Qwen Code installation complete."
fi

# ===
# STEP 2: MEGALONYX STACK
# ===

echo ""
echo "[2/2] Installing Megalonyx stack..."
bash "$STACK_INSTALLER" "${STACK_ARGS[@]+"${STACK_ARGS[@]}"}"

# ===
# DONE
# ===

echo ""
echo "=========================================="
echo " FULL INSTALLATION COMPLETE"
echo "=========================================="
echo ""
echo "Both the Qwen Code CLI and the Megalonyx stack are installed."
echo "See docs/megalonyx/installation.md for next steps."
echo "=========================================="
