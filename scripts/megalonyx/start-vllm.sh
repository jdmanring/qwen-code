#!/usr/bin/env bash
set -euo pipefail

VENV="$HOME/.local/share/megalonyx/py/venv"
# Log file located in persistent logs dir to avoid /tmp space limits
LOG="$HOME/.qwen/logs/vllm.log"

source "$VENV/bin/activate"

echo "[vllm] starting..."

python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-Coder-7B-Instruct-AWQ \
  --host 127.0.0.1 \
  --port 8000 \
  > "$LOG" 2>&1
