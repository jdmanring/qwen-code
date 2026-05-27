This directory contains internal development tools: the upstream sync pipeline, quality linters, smoke tests, and validators.
Nothing here is part of the installed stack -- it is all development and CI tooling.

Key tools:
- sync-upstreams/upstream_ingest_pipeline.py -- fetches QwenLM/qwen-code, runs quality gates, promotes to integration
- project_standards_linter.py -- enforces naming standards, config symmetry, and CODE rules
- symmetry_check.py -- verifies .qwen/config/ has a 1:1 mirror in docs/
- smoke-tests/ -- boot_verification.py and model_router_test.py; run after any package change
- validators/ -- deeper stack validators (Qdrant connectivity, vector indexing, installer)
- git-hooks/pre-commit -- the pre-commit hook source; install via tooling/install-hooks.sh
