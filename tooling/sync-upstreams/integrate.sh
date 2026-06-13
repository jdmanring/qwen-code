#!/bin/bash
set -euo pipefail

# Sync Engine: Integrate
# This script merges 'upstream-mirror' into the current branch.
# REQUIREMENT: Caller must be on the 'integration' branch.

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
    # 1. Context Verification (Fail-Fast)
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [ "$CURRENT_BRANCH" != "integration" ]; then
        log_error "Invalid Context: This script must be run from the 'integration' branch."
        log_error "Current branch: $CURRENT_BRANCH"
        exit 1
    fi

    log_info "Starting integration: upstream-mirror -> integration"

    # 2. Ghost Change Purge
    log_info "Purging ghost modifications..."
    git reset --hard HEAD

    # 3. Idempotency Check
    if git merge-base --is-ancestor upstream-mirror integration; then
        log_success "Integration branch is already up-to-date with upstream-mirror. Nothing to do."
        exit 0
    fi

    # 4. Merge Execution
    log_info "Merging upstream-mirror into integration..."
    if ! git merge upstream-mirror; then
        # Check if the only conflict is the problematic .bat file
        if git status | grep -q "scripts/installation/install-qwen-standalone.bat"; then
            log_info "Resolving modify/delete conflict for problematic .bat file..."
            git rm -f scripts/installation/install-qwen-standalone.bat
            if git commit -m "fix: resolve merge conflict by purging problematic .bat file"; then
                log_success "Conflict resolved by purging .bat file."
            else
                log_error "Failed to commit conflict resolution."
                exit 1
            fi
        else
            log_error "Critical merge conflict detected in other files!"
            log_error "Please resolve conflicts manually and commit the result before retrying."
            exit 1
        fi
    fi

    # 5. Post-Merge Purge
    log_info "Performing post-merge purge of problematic files..."
    rm -f scripts/installation/install-qwen-standalone.bat

    log_success "Successfully merged upstream-mirror into integration."
}

main "$@"
