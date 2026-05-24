#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "========================================"
echo "       MEGALONYX STATUS          "
echo "========================================"
echo ""

# --------------------
# SERVICES
# --------------------

check_service() {
    local name=$1
    local pattern=$2
    if pgrep -f "$pattern" > /dev/null; then
        echo -e "[\033[0;32m OK \033[0m] $name"
    else
        echo -e "[\033[0;31m -- \033[0m] $name"
    fi
}

check_service "mega-db" "mega-db"
check_service "vLLM" "vllm"
check_service "Memory Daemon" "memory_daemon.py"

echo ""

# --------------------
# HEALTH CHECKS
# --------------------

echo "--- Health Checks ---"

# mega-db
if curl -s http://localhost:6333/health > /dev/null; then
    echo "[OK] mega-db API reachable"
else
    echo "[--] mega-db API UNREACHABLE"
fi

# Memory WAL
WAL_PATH="$HOME/.qwen/memory/wal.jsonl"
if [ -f "$WAL_PATH" ]; then
    LINE_COUNT=$(wc -l < "$WAL_PATH")
    echo "[OK] WAL exists ($LINE_COUNT pending entries)"
else
    echo "[--] WAL empty or missing"
fi

echo ""
echo "========================================"
