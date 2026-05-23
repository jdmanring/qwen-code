#!/bin/bash
set -euo pipefail

# Sync Engine: Raw Inline
# This script updates the 'upstream-mirror' branch to be a perfect mirror of 'upstream/main'.

# Colors for logging
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

main() {
    log_info "Starting raw-inline sync: upstream/main -> upstream-mirror"

    # 1. Fetch latest from upstream
    log_info "Fetching latest changes from upstream..."
    if ! git fetch upstream; then
        log_error "Failed to fetch from upstream remote."
        exit 1
    fi

    # 2. Checkout upstream-mirror (Forced)
    log_info "Checking out upstream-mirror branch (forced)..."
    if ! git checkout -f upstream-mirror; then
        log_error "Failed to checkout upstream-mirror branch. Attempting to create it..."
        if ! git checkout -B upstream-mirror upstream/main; then
            log_error "Failed to create upstream-mirror branch from upstream/main."
            exit 1
        fi
    fi

    # 3. Hard reset to upstream/main
    log_info "Hard resetting upstream-mirror to upstream/main..."
    if ! git reset --hard upstream/main; then
        log_error "Failed to hard reset upstream-mirror to upstream/main."
        exit 1
    fi

    # 4. Purge problematic files
    log_info "Purging problematic installation files from mirror..."
    rm -f scripts/installation/install-qwen-standalone.bat

    log_success "upstream-mirror is now a perfect mirror of upstream/main (cleaned)."
}

main "$@"
