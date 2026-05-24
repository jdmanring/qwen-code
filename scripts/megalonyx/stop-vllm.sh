#!/usr/bin/env bash
set -euo pipefail

echo "[vllm] stopping..."

pkill -f "vllm.entrypoints.openai.api_server" || true

echo "[vllm] stopped"
