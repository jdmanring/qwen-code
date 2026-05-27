#!/usr/bin/env bash
set -euo pipefail

# Use the project venv
VENV_PYTHON="$(cd "$(dirname "$0")" && pwd)/../tests/venv/bin/python3"

echo " Running Code Linting (Ruff)..."

# Ensure ruff is installed in the venv
if ! "$VENV_PYTHON" -m pip show ruff >/dev/null 2>&1; then
    echo "Installing ruff in venv..."
    "$VENV_PYTHON" -m pip install ruff
fi

# Run ruff on the packages directory
if "$VENV_PYTHON" -m ruff check packages/; then
    echo " Code style is clean."
else
    echo " Linting errors found. Please fix them."
    exit 1
fi

exit 0
