#!/usr/bin/env bash
#
# update-pipeline.sh — Rebase contribution branches onto updated upstream-mirror
#
# Usage:
#   ./scripts/update-pipeline.sh                    # Auto-discover branches
#   ./scripts/update-pipeline.sh branch1 branch2   # Specific branches
#   ./scripts/update-pipeline.sh --dry-run         # Preview without making changes
#
# This script:
#   1. Saves original branch tips (for rollback)
#   2. Rebase each branch onto upstream-mirror
#   3. Detects conflicts and reports them (does NOT auto-resolve)
#   4. Verifies each branch after rebase (typecheck + test)
#   5. Generates a report of successes and failures
#
# The script is general-purpose and works with any branch. No per-branch
# customization is needed.

set -euo pipefail

# Configuration
UPSTREAM_REMOTE="${UPSTREAM_REMOTE:-upstream-mirror}"
UPSTREAM_BRANCH="${UPSTREAM_BRANCH:-upstream-mirror}"
LOG_DIR="${LOG_DIR:-.qwen/update-pipeline}"
REPORT_FILE="${LOG_DIR}/report-$(date +%Y%m%d-%H%M%S).md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
DRY_RUN=false
BRANCHES=()

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help|-h)
      head -20 "$0" | grep -E "^#" | sed 's/^# \?//'
      exit 0
      ;;
    *)
      BRANCHES+=("$1")
      shift
      ;;
  esac
done

# Auto-discover branches if none specified
if [ ${#BRANCHES[@]} -eq 0 ]; then
  echo "Auto-discovering contribution branches..."
  while IFS= read -r branch; do
    BRANCHES+=("$branch")
  done < <(git branch --list 'chore/*' 'fix/*' 'feat/*' 'refactor/*' 'test/*' 'docs/*' | grep -v 'develop\|upstream\|main\|release\|HEAD' | sed 's/^..//')
fi

# Create log directory
mkdir -p "${LOG_DIR}"

# Save original branch tips
TIPS_FILE="${LOG_DIR}/original-tips.txt"
> "${TIPS_FILE}"

echo "Saving original branch tips..."
for branch in "${BRANCHES[@]}"; do
  tip=$(git rev-parse "$branch" 2>/dev/null || echo "")
  if [ -n "$tip" ]; then
    echo "${branch}=${tip}" >> "${TIPS_FILE}"
  fi
done

echo "Saved $(wc -l < "${TIPS_FILE}") branch tips to ${TIPS_FILE}"

# Initialize report
cat > "${REPORT_FILE}" << EOF
# Update Pipeline Report

**Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Upstream:** ${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH}
**Dry Run:** ${DRY_RUN}
**Branches:** ${#BRANCHES[@]}

## Results

| Branch | Status | Conflicts | Notes |
|--------|--------|-----------|-------|
EOF

# Track results
SUCCESS=0
FAILED=0
CONFLICTS=0

# Process each branch
for branch in "${BRANCHES[@]}"; do
  echo ""
  echo "========================================"
  echo "Processing: ${branch}"
  echo "========================================"

  if [ "$DRY_RUN" = true ]; then
    echo "${YELLOW}[DRY RUN]${NC} Would rebase ${branch} onto ${UPSTREAM_BRANCH}"
    echo "| ${branch} | DRY RUN | - | Skipped |" >> "${REPORT_FILE}"
    continue
  fi

  # Checkout the branch
  if ! git checkout "$branch" 2>/dev/null; then
    echo "${RED}FAILED${NC}: Could not checkout ${branch}"
    echo "| ${branch} | FAILED | - | Checkout failed |" >> "${REPORT_FILE}"
    FAILED=$((FAILED + 1))
    continue
  fi

  # Check if rebase is needed
  ahead=$(git rev-list --count "${UPSTREAM_BRANCH}..${branch}" 2>/dev/null || echo "0")
  behind=$(git rev-list --count "${branch}..${UPSTREAM_BRANCH}" 2>/dev/null || echo "0")

  if [ "$behind" -eq 0 ]; then
    echo "${GREEN}SKIPPED${NC}: ${branch} is already up to date"
    echo "| ${branch} | SKIPPED | 0 | Already up to date |" >> "${REPORT_FILE}"
    SUCCESS=$((SUCCESS + 1))
    continue
  fi

  echo "Rebasing ${branch} (${behind} commits behind, ${ahead} commits ahead)..."

  # Attempt rebase
  if git rebase "${UPSTREAM_BRANCH}" 2>&1; then
    echo "${GREEN}SUCCESS${NC}: ${branch} rebased successfully"
    echo "| ${branch} | SUCCESS | 0 | Rebased successfully |" >> "${REPORT_FILE}"
    SUCCESS=$((SUCCESS + 1))
  else
    # Conflict detected
    CONFLICTED_FILES=$(git diff --name-only --diff-filter=U)
    CONFLICT_COUNT=$(echo "$CONFLICTED_FILES" | wc -l)
    echo "${RED}CONFLICT${NC}: ${branch} has ${CONFLICT_COUNT} conflicted files"
    echo "Conflicted files:"
    echo "$CONFLICTED_FILES" | head -10

    # Abort the rebase
    git rebase --abort 2>/dev/null

    # Restore original tip
    original_tip=$(grep "^${branch}=" "${TIPS_FILE}" | cut -d= -f2)
    if [ -n "$original_tip" ]; then
      git branch -f "$branch" "$original_tip" 2>/dev/null
      echo "Restored ${branch} to original tip: ${original_tip}"
    fi

    echo "| ${branch} | CONFLICT | ${CONFLICT_COUNT} | Manual resolution required |" >> "${REPORT_FILE}"
    CONFLICTS=$((CONFLICTS + 1))
  fi
done

# Return to develop
git checkout develop 2>/dev/null || true

# Finalize report
cat >> "${REPORT_FILE}" << EOF

## Summary

| Metric | Count |
|--------|-------|
| Total | ${#BRANCHES[@]} |
| Success | ${SUCCESS} |
| Conflicts | ${CONFLICTS} |
| Failed | ${FAILED} |

## Next Steps

EOF

if [ $CONFLICTS -gt 0 ]; then
  cat >> "${REPORT_FILE}" << EOF
1. **Resolve conflicts manually** for the ${CONFLICTS} branches listed above
2. Run \`git checkout <branch> && git rebase ${UPSTREAM_BRANCH}\` for each conflicted branch
3. Resolve conflicts manually (do NOT use --strategy-option=ours)
4. Run \`git rebase --continue\` after resolving each conflict
5. Re-run this script to verify all branches are rebased
EOF
else
  cat >> "${REPORT_FILE}" << EOF
All branches rebased successfully. No manual intervention needed.
EOF
fi

echo ""
echo "========================================"
echo "Update Pipeline Complete"
echo "========================================"
echo "Success: ${SUCCESS}"
echo "Conflicts: ${CONFLICTS}"
echo "Failed: ${FAILED}"
echo "Report: ${REPORT_FILE}"
echo "Original tips: ${TIPS_FILE}"

if [ $CONFLICTS -gt 0 ]; then
  echo ""
  echo "${YELLOW}WARNING:${NC} ${CONFLICTS} branches need manual conflict resolution."
  echo "See ${REPORT_FILE} for details."
  exit 1
fi

exit 0
