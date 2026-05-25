#!/bin/bash
# sync-fork-from-qwenlm.sh
#
# Run this script INSIDE a local checkout of jdmanring/qwen-code (the fork).
# It fetches the latest commits from QwenLM/qwen-code, shows you what's coming
# in, and — only after you confirm — fast-forward merges and pushes to the fork.
#
# The fork (jdmanring/qwen-code) is the trusted inbound source for the
# megalonyx-monorepo pipeline. Review what you're absorbing before running this.
#
# Usage (run from inside your jdmanring/qwen-code checkout):
#   bash /path/to/megalonyx-monorepo/tooling/sync-upstreams/sync-fork-from-qwenlm.sh
#
# Requirements:
#   - You are inside a jdmanring/qwen-code checkout (not the monorepo).
#   - 'origin' remote points to QwenLM/qwen-code (standard fork setup).
#   - 'fork' remote points to jdmanring/qwen-code (your fork's remote).
#     If missing: git remote add fork https://github.com/jdmanring/qwen-code.git

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[FAIL]${NC} $1" >&2; }

# Verify we're in a git repo and have the expected remotes
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not inside a git repository."
    exit 1
fi

if ! git remote | grep -q "^origin$"; then
    log_error "'origin' remote not found. Expected: QwenLM/qwen-code"
    exit 1
fi

if ! git remote | grep -q "^fork$"; then
    log_error "'fork' remote not found."
    echo ""
    echo "  Add it with:"
    echo "    git remote add fork https://github.com/jdmanring/qwen-code.git"
    exit 1
fi

ORIGIN_URL=$(git remote get-url origin)
FORK_URL=$(git remote get-url fork)

echo ""
log_info "Upstream source : ${ORIGIN_URL}"
log_info "Fork target     : ${FORK_URL}"
echo ""

# Fetch latest from QwenLM
log_info "Fetching origin/main from QwenLM..."
git fetch origin main

# Count new commits
NEW_COUNT=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")

if [[ "${NEW_COUNT}" == "0" ]]; then
    log_success "Fork is already up to date with QwenLM/qwen-code."
    exit 0
fi

echo ""
log_warn "${NEW_COUNT} new commit(s) since last sync. Review before absorbing:"
echo ""
git log HEAD..origin/main --oneline --no-merges
echo ""

read -r -p "Absorb these commits into the fork? [y/N] " CONFIRM
if [[ "${CONFIRM}" != "y" && "${CONFIRM}" != "Y" ]]; then
    log_warn "Sync cancelled."
    exit 0
fi

# Fast-forward only — if this fails, divergence exists and manual review is required
log_info "Fast-forward merging origin/main..."
if ! git merge --ff-only origin/main; then
    log_error "Fast-forward failed — fork has diverged from QwenLM. Manual merge required."
    exit 1
fi

log_info "Pushing to fork (jdmanring/qwen-code)..."
git push fork main

log_success "Fork synced. The megalonyx-monorepo pipeline can now absorb these commits."
echo ""
echo "  Next: run the ingest pipeline from the monorepo:"
echo "    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py"
