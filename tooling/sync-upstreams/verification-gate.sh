#!/bin/bash
set -euo pipefail

# Sync Engine: Verification Gate
# This script verifies the quality and symmetry of the current branch.

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
    log_info "Entering Verification Gate verification..."

    # 1. Ruff Linting Check
    log_info "Running ruff linting check..."
    if ! ruff check .; then
        log_error "Ruff linting check failed. Please fix the issues."
        exit 1
    fi
    log_success "Ruff linting passed."

    # 2. Symmetry Check
    log_info "Running symmetry check (config <-> docs)..."
    if ! python3 tooling/symmetry-check.py; then
        log_error "Symmetry check failed. Config and documentation are out of sync."
        exit 1
    fi
    log_success "Symmetry check passed."

    echo -e "${GREEN}Verification Gate Passed${NC}"
}

main "$@"
