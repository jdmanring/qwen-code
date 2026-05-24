Smoke tests that verify the stack boots correctly without requiring live external services (except where noted).
Run after any change to the Python packages.

Tests:
- boot_verification.py — imports all three packages, instantiates ControlPlane, optionally runs Qdrant round-trip
- model_router_test.py — tests ExecutionProfileSelector routing for all 6 intent types without a live LLM call

Usage:
  uv run python3 tooling/smoke-tests/boot_verification.py
  uv run python3 tooling/smoke-tests/boot_verification.py --skip-memory
  uv run python3 tooling/smoke-tests/model_router_test.py
