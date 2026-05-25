#!/bin/bash
set -euo pipefail

# Upstream Contribution Tool
# Prepares a fix from this private monorepo for submission as a PR to the
# official qwen-code repository, without exposing any monorepo-specific history.
#
# How it works:
#   1. Creates a clean branch from upstream/main (no monorepo changes)
#   2. Cherry-picks your fix commit onto it (just the change, nothing else)
#   3. Pushes the branch to the fork (the 'upstream' remote = jdmanring/qwen-code)
#   4. Prints a direct link to open the PR against QwenLM/qwen-code
#
# The 'upstream' remote serves dual purpose: inbound sync source for the
# pipeline AND outbound PR channel. The fork is kept in sync with QwenLM
# via tooling/sync-upstreams/sync-fork-from-qwenlm.sh before running this.
#
# Usage:
#   ./tooling/sync-upstreams/contribute-upstream.sh <commit-hash> <branch-name>
#
# Example:
#   ./tooling/sync-upstreams/contribute-upstream.sh a1b2c3d fix/memory-leak-in-runner

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1" >&2; }
log_error()   { echo -e "${RED}[FAIL]${NC} $1" >&2; }

COMMIT_HASH="${1:-}"
BRANCH_NAME="${2:-}"

usage() {
    echo ""
    echo "Usage: $0 <commit-hash> <branch-name>"
    echo ""
    echo "  commit-hash   Hash of the fix to contribute (short or full)."
    echo "  branch-name   Short descriptive name for the PR branch."
    echo "                Convention: fix/<description> or feat/<description>"
    echo ""
    echo "Examples:"
    echo "  $0 a1b2c3d fix/memory-leak-in-runner"
    echo "  $0 HEAD~1  fix/typo-in-install-script"
    echo ""
    echo "Requires an 'upstream' remote pointing to your fork of qwen-code:"
    echo "  git remote add upstream https://github.com/jdmanring/qwen-code.git"
    echo ""
    exit 1
}

check_upstream_remote() {
    if ! git remote | grep -q "^upstream$"; then
        log_error "'upstream' remote is not configured."
        echo ""
        echo "  This tool needs the 'upstream' remote pointing to your fork of qwen-code."
        echo "  Your private monorepo cannot push directly to QwenLM/qwen-code."
        echo ""
        echo "  Set it up once:"
        echo "    git remote add upstream https://github.com/jdmanring/qwen-code.git"
        echo ""
        exit 1
    fi
}

main() {
    [ -z "$COMMIT_HASH" ] || [ -z "$BRANCH_NAME" ] && usage

    check_upstream_remote

    # Resolve to full hash and validate
    if ! FULL_HASH=$(git rev-parse "${COMMIT_HASH}^{commit}" 2>/dev/null); then
        log_error "Commit '${COMMIT_HASH}' not found in this repository."
        exit 1
    fi
    COMMIT_MSG=$(git log --format="%s" -1 "$FULL_HASH")
    PR_BRANCH="contribute/${BRANCH_NAME}"

    echo ""
    log_info "Commit : ${FULL_HASH:0:12} — ${COMMIT_MSG}"
    log_info "Branch : ${PR_BRANCH}"
    log_info "Target : upstream/main → upstream/${PR_BRANCH} → PR to QwenLM/qwen-code"
    echo ""

    # Fetch the latest upstream so we branch from current main, not a stale ref
    log_info "Fetching upstream/main..."
    git fetch upstream main

    # Create a clean branch with no monorepo history.
    # Starting from upstream/main means the PR diff will show only your fix.
    log_info "Creating clean branch from upstream/main..."
    git checkout -b "$PR_BRANCH" upstream/main

    # Cherry-pick the fix. If there's a conflict, we stop and let the user
    # resolve it — do not auto-resolve, as that could corrupt the upstream PR.
    log_info "Cherry-picking ${FULL_HASH:0:12}..."
    if ! git cherry-pick --no-edit "$FULL_HASH"; then
        echo ""
        log_warn "Cherry-pick conflict. Resolve manually, then run:"
        echo "  git cherry-pick --continue"
        echo "  git push upstream ${PR_BRANCH}"
        echo ""
        log_info "When the branch is pushed, open a PR at:"
        echo "  https://github.com/QwenLM/qwen-code/compare/main...YOUR_FORK:${PR_BRANCH}"
        exit 1
    fi

    # Push the clean branch to the fork (upstream remote = jdmanring/qwen-code)
    log_info "Pushing ${PR_BRANCH} to upstream fork..."
    git push upstream "$PR_BRANCH"

    # Build the PR URL from the upstream remote URL
    UPSTREAM_URL=$(git remote get-url upstream)
    # Normalise SSH → HTTPS for display
    UPSTREAM_URL=$(echo "$UPSTREAM_URL" | sed 's|git@github.com:|https://github.com/|; s|\.git$||')
    FORK_OWNER=$(echo "$UPSTREAM_URL" | sed 's|https://github.com/\([^/]*\)/.*|\1|')

    echo ""
    log_success "Branch pushed to your public fork."
    echo ""
    echo "  Open your PR here (click or copy):"
    echo "  https://github.com/QwenLM/qwen-code/compare/main...${FORK_OWNER}:${PR_BRANCH}"
    echo ""
    log_info "PR checklist:"
    echo "  [ ] Title matches the fix (upstream uses conventional commits)"
    echo "  [ ] Description explains the problem and links any related issue"
    echo "  [ ] No monorepo-specific files or imports are included in the diff"
    echo ""

    # Return to integration — the contribution branch stays local for amendments
    git checkout integration
    log_info "Returned to integration branch. ${PR_BRANCH} remains local for amendments."
    echo ""
}

main "$@"
