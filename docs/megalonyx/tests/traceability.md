#  Test-to-Requirement Traceability Matrix

This document maps the core functional requirements of the Mega Code stack to their corresponding verification tests. This ensures that every critical architectural mandate is validated and provides a gap analysis for future testing efforts.

## 1. Traceability Matrix

| Req ID | Requirement Description | Primary Test Suite | Specific Test File(s) | Status |
| :--- | :--- | :--- | :--- | :---: |
| **REQ-01** | **Intent Classification & Decomposition**: Ability to process prompts into managed job sets. | Unit / E2E | `tests/unit/test_decomposer.py`, `tests/e2e/test_golden_paths.py` |  |
| **REQ-02** | **Job Execution Loop**: Deterministic Act $\to$ Observe $\to$ Verify $\to$ Correct cycle. | Fidelity / E2E | `tests/fidelity/test_control_plane_live.py`, `tests/e2e/test_golden_paths.py` |  |
| **REQ-03** | **S-VERIFY (Verification)**: Contract-based validation of job outcomes. | Unit / Fidelity | `tests/unit/test_contracts.py`, `tests/fidelity/test_control_plane_simulation.py` |  |
| **REQ-04** | **S-CORRECT (Correction)**: Automated retry/pivot logic upon verification failure. | E2E / Fidelity | `tests/e2e/test_golden_paths.py`, `tests/fidelity/test_control_plane_live.py` |  |
| **REQ-05** | **A-PERM (Boundaries)**: Strict enforcement of Project Root and permission matrices. | Unit / Fidelity | `tests/unit/test_isolation.py`, `tests/fidelity/test_policy_enforcement.py` |  |
| **REQ-06** | **CSF-SYNC (Symmetry)**: 1:1 mirroring between `.qwen/config/` and `docs/`. | Tooling | `tooling/symmetry_check.py` |  |
| **REQ-07** | **Performance Baselines**: Latency gates for orchestration overhead. | Performance | `tests/performance/latency_bench.py` |  |
| **REQ-08** | **Resilience**: Fault tolerance against daemon crashes and transport failures. | Adversarial | `tests/adversarial/test_state_failures.py`, `tests/adversarial/test_transport_failures.py`, `tests/adversarial/test_process_failures.py` |  |
| **REQ-09** | **Resilience (Stochastic)**: Ability to recover from randomized, unpredictable faults. | Adversarial | `tests/adversarial/test_resilience_stress.py` |  |

## 2. Coverage Analysis

### Verified Domains
- **Golden Paths**: Fully covered via E2E scenarios for Bugfixes, Features, and Refactors.
- **Failure Domains**: State, Transport, and Process failures are systematically validated.
- **Performance**: Baselines established for the critical path of the orchestration loop.

### Identified Gaps & Future Work
- **Chaos Testing**: While adversarial tests cover specific failures, a randomized chaos monkey for the Control Plane is not yet implemented.
- **Cross-Platform Fidelity**: Tests are currently optimized for Linux. Windows/macOS specific boundary tests are pending.
- **Concurrent Job Stress**: Testing the `JobStateManager` under high-concurrency loads (multiple simultaneous agents) is not yet covered.

## 3. Maintenance Protocol

This matrix must be updated whenever:
1.  A new requirement is added to `QWEN.md`.
2.  A new test suite is introduced.
3.  A critical bug is found that reveals a "blind spot" in the current test coverage.
