The upstream sync tooling manages bidirectional code flow between QwenLM/qwen-code and
the monorepo via the jdmanring/qwen-code fork. This is how upstream bug fixes enter the
monorepo without overwriting Megalonyx work, and how our fixes reach QwenLM as PRs.

Key files:
- fork_sync_pipeline.py       -- fork manager: --status, --sync (inbound), --contribute (outbound)
- upstream_ingest_pipeline.py -- monorepo pipeline: fetch fork -> gate (boot/lint/symmetry) -> promote
- gate_failure_tests.py       -- verifies all three monorepo gate failure modes block correctly
- fork_sync_pipeline_tests.py -- verifies all advisory and isolation gate functions

Usage:

  # See where the fork stands relative to QwenLM and integration
  python3 tooling/sync-upstreams/fork_sync_pipeline.py --status

  # Absorb new QwenLM commits into the fork (inbound -- run this first)
  python3 tooling/sync-upstreams/fork_sync_pipeline.py --sync
  python3 tooling/sync-upstreams/fork_sync_pipeline.py --sync --dry-run

  # Push a monorepo fix to the fork as an upstream PR branch (outbound)
  python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <branch-name>
  python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <branch-name> --dry-run

  # Absorb fork changes into integration (run after --sync)
  python3 tooling/sync-upstreams/upstream_ingest_pipeline.py
  python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run

  # Verify gate tests
  python3 tooling/sync-upstreams/fork_sync_pipeline_tests.py
  python3 tooling/sync-upstreams/gate_failure_tests.py

Standard inbound workflow:
  1. python3 tooling/sync-upstreams/fork_sync_pipeline.py --status
  2. python3 tooling/sync-upstreams/fork_sync_pipeline.py --sync
  3. python3 tooling/sync-upstreams/upstream_ingest_pipeline.py

Standard outbound workflow:
  1. python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <branch>
  2. Open the PR URL printed by the script

See docs/meta/pipeline-runbook.md for failure recovery procedures.
See docs/upstream/upstream-pr-guide.md for the full upstream contribution guide.
