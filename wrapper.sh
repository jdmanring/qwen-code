#!/bin/bash
# wrapper.sh
echo "[wrapper] Starting MemoryDaemon..." >&2
/home/james/projects/megalonyx-monorepo/.venv/bin/python3 packages/memory/memory_daemon.py
EXIT_CODE=$?
echo "[wrapper] MemoryDaemon exited with code $EXIT_CODE" >&2
exit $EXIT_CODE
