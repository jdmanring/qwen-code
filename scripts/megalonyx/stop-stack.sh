#!/usr/bin/env bash
set -euo pipefail

echo "[stack] stopping services..."

pkill -f mega-db || true
pkill -f memory_daemon.py || true
pkill -f vllm || true

echo "[stack] stopped"
