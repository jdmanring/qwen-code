# ⏱️ Latency Baselines

This document records the performance baselines for the Control Plane orchestration loop. These metrics are used to detect performance regressions during development.

## 1. Measurement Methodology

Latency is measured using the `latency_bench.py` tool, which simulates the "Golden Path" scenarios. We measure three distinct phases of a user turn:

1.  **Decomposition Latency**: Time from receiving a prompt to completing the Intent Classification and Task Decomposition.
2.  **Execution Latency**: Time to execute the first job in the sequence.
3.  **Total Latency**: The sum of the above, representing the time until the user sees the first meaningful action.

**Environment**:
- Model: `gemini-2.5-flash-lite`
- Iterations: 5 per scenario (averaged)
- Mocked: LLM responses and Tool Executions (to isolate orchestration overhead from network/LLM latency).

## 2. Baseline Metrics

| Scenario | Decomposition (s) | Execution (s) | Total (s) |
| :--- | :---: | :---: | :---: |
| **Targeted Bugfix** | 0.0303 | 0.0013 | 0.0316 |
| **Feature Implementation** | 0.0017 | 0.0040 | 0.0057 |
| **Architectural Refactor** | 0.0017 | 0.0013 | 0.0030 |

## 3. Performance Gates

Any change to the `ControlPlane` or `TaskDecomposer` must not increase the **Total Latency** by more than **20%** of the baseline.

**Verification Command**:
```bash
python apps/control-plane-daemon/tests/performance/latency_bench.py
```
