The upstream sync pipeline: fetches changes from QwenLM/qwen-code, runs quality gates, and promotes to the integration branch.
This is how upstream bug fixes and features enter the monorepo without overwriting Megalonyx work.

Key files:
- upstream_ingest_pipeline.py — main pipeline: fetch → gate (ruff, mypy, symmetry, boot) → promote
- gate_failure_tests.py — verifies all three gate failure modes correctly block promotion

Usage:
  uv run python3 tooling/sync-upstreams/upstream_ingest_pipeline.py           # full sync
  uv run python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run # gates only, no git ops
  uv run python3 tooling/sync-upstreams/gate_failure_tests.py                 # verify gates block failures

See docs/meta/pipeline-runbook.md for failure recovery procedures.
