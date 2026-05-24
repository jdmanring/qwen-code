# Model Comparison: Gemma 4 Orchestration

This document analyzes the trade-offs between the dense and MoE variants of Gemma 4 specifically for the role of the Qwen Code Orchestrator.

## 1. Comparative Matrix

| Metric | gemma-4-31B-it (Dense) | gemma-4-26B-A4B-it (MoE) | Orchestrator Impact |
| :--- | :--- | :--- | :--- |
| **Inference Speed** | Baseline | $\sim 2\text{--}4\times$ Faster | MoE reduces "agent lag" in multi-turn loops. |
| **Reasoning Depth** | Maximum | High (Competitive) | Dense is safer for complex architectural pivots. |
| **Instruction Adherence**| Extremely High | High | MoE may require slightly more explicit tagging. |
| **VRAM Pressure** | High | Moderate | MoE allows for larger context windows on limited HW. |
| **Loop Stability** | Stable | Prone to "degenerate" loops | MoE requires tighter stop-sequence control. |

## 2. Deployment Strategy (The "Routing" Rule)

To maximize the efficiency of the stack, we should adopt a **Dynamic Routing** strategy:

### Case A: The "Deep Think" (Use 31B Dense)
**Trigger**: Tasks involving `architect`, `developer` (initial implementation), or `security_auditor` skills.
**Reasoning**: These tasks require maximum precision and a holistic understanding of the codebase. The cost of a mistake is high, and the latency of a dense model is acceptable.

### Case B: The "Rapid Loop" (Use 26B-A4B MoE)
**Trigger**: Tasks involving `general-purpose` research, `codebase-mapper` iterations, or high-frequency tool-calling loops.
**Reasoning**: These tasks are iterative. The orchestrator acts as a router. High throughput allows the agent to "fail fast" and correct itself without frustrating the user.

## 3. Final Recommendation for Primary Model
If only one model can be the "Default Primary," **gemma-4-31B-it** is recommended for the Blueprint to ensure the highest baseline of stability and correctness. However, the infrastructure should support a seamless switch to **gemma-4-26B-A4B-it** for "Performance Mode."
