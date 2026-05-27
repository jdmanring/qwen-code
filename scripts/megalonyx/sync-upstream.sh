#!/bin/bash

# Mega Code Upstream Sync Script
# This script updates the 'Lab' source to the latest upstream version
# to allow verifying patches against the evolving kernel.

LAB_DIR="${LAB_DIR:-$HOME/Projects/labs/qwen-code}"

echo "Updating Mega Code Upstream Kernel..."

if [ -d "$LAB_DIR/.git" ]; then
  cd "$LAB_DIR"
  git fetch origin
  git reset --hard origin/main
  echo " Upstream kernel updated to latest version."
else
  echo " Error: Lab directory not found or not a git repository."
  exit 1
fi
