#!/bin/bash
set -euo pipefail

# Sync Engine: Raw Inline
# Resets upstream-mirror to a clean snapshot of upstream/main and commits
# the removal of any Windows-only artifacts (.bat files).
#
# This is the low-level step called by the orchestrator. Running it standalone
# is safe — it only modifies the upstream-mirror branch.
#
# Usage:
#   ./tooling/sync-upstreams/raw-inline.sh

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_error()   { echo -e "${RED}[FAIL]${NC} $1" >&2; }

MIRROR_BRANCH="upstream-mirror"

main() {
    log_info "Starting raw-inline sync: upstream/main → ${MIRROR_BRANCH}"

    # 1. Fetch latest from upstream
    log_info "Fetching upstream/main..."
    if ! git fetch upstream main; then
        log_error "Failed to fetch from upstream remote."
        exit 1
    fi

    # 2. Switch to mirror branch (create if missing)
    log_info "Switching to ${MIRROR_BRANCH}..."
    if ! git checkout -f "$MIRROR_BRANCH" 2>/dev/null; then
        log_info "${MIRROR_BRANCH} not found — creating from upstream/main..."
        if ! git checkout -B "$MIRROR_BRANCH" upstream/main; then
            log_error "Failed to create ${MIRROR_BRANCH}."
            exit 1
        fi
    fi

    # 3. Reset to upstream/main
    log_info "Hard-resetting ${MIRROR_BRANCH} to upstream/main..."
    if ! git reset --hard upstream/main; then
        log_error "Failed to reset ${MIRROR_BRANCH}."
        exit 1
    fi

    # 4. Purge Windows-only artifacts and commit the removal.
    #    Using `git ls-files` instead of `find` ensures we only touch tracked
    #    files, and committing the removal means downstream merges never see
    #    a modify/delete conflict on these files.
    log_info "Checking for upstream Windows artifacts..."
    BAT_FILES=$(git ls-files -- '*.bat' || true)
    if [ -n "$BAT_FILES" ]; then
        log_info "Purging: ${BAT_FILES//$'\n'/, }"
        # shellcheck disable=SC2086
        git rm -f -- $BAT_FILES
        git commit -m "chore(mirror): purge upstream Windows artifacts"
        log_success "Artifacts purged and committed."
    else
        log_info "No Windows artifacts found."
    fi

    log_success "${MIRROR_BRANCH} is now a clean mirror of upstream/main."
}

main "$@"
