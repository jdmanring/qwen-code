#!/bin/bash
# DEPRECATED — superseded by the Integration Orchestrator.
#
# This script used the old branch name 'upstream-main' (now 'upstream-mirror')
# and performed no verification before merging. It is retained only for
# historical reference and will exit with an error if invoked.
#
# Use instead:
#   python3 tooling/sync-upstreams/orchestrator.py            # full sync
#   python3 tooling/sync-upstreams/orchestrator.py --dry-run  # gates only

echo "[FAIL] merge-upstream.sh is deprecated." >&2
echo "       Use: python3 tooling/sync-upstreams/orchestrator.py" >&2
exit 1
