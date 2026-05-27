#!/bin/bash
# DEPRECATED -- superseded by the Upstream Ingest Pipeline.
#
# This script used the old branch name 'upstream-main' (now 'upstream-mirror')
# and performed no verification before merging. It is retained only for
# historical reference and will exit with an error if invoked.
#
# Use instead:
#   python3 tooling/sync-upstreams/upstream_ingest_pipeline.py            # full sync
#   python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run  # gates only

echo "[FAIL] merge-upstream.sh is deprecated." >&2
echo "       Use: python3 tooling/sync-upstreams/upstream_ingest_pipeline.py" >&2
exit 1
