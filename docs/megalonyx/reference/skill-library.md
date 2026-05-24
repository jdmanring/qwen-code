# Gold Standard Service Library

This library defines the "Engineering Macros" available to the `qwen_code_stack` agents. These services transform basic tool use into repeatable, professional engineering workflows.

## 🛠️ Core Engineering Services

| Service | Goal | Primary Workflow | Multiplier Effect |
| :--- | :--- | :--- | :--- |
| `refactor-safe` | Systemic Refactoring | Impact Analysis $\rightarrow$ Topological Plan $\rightarrow$ Incremental Apply $\rightarrow$ Regression Sweep | 0% regression rate on large-scale changes. |
| `test-coverage-max` | Edge-Case Testing | Branch Mapping $\rightarrow$ Boundary Analysis $\rightarrow$ Iterative Generation $\rightarrow$ Gap Filling | Eliminates "dark logic" and unseen bugs. |
| `codebase-mapper` | Semantic Discovery | Symbol Extraction $\rightarrow$ Call-Graph $\rightarrow$ Hierarchical Summary $\rightarrow$ Semantic Query | Drastic reduction in hallucinated dependencies. |
| `root-cause-hunter` | Bug Isolation | MRE $\rightarrow$ Hypothesis $\rightarrow$ Instrumentation $\rightarrow$ Bisection $\rightarrow$ Verification | Moves from "guessing" to "proving" the root cause. |
| `doc-sync` | Documentation Truth | Delta Detection $\rightarrow$ Doc Mapping $\rightarrow$ Conflict Analysis $\rightarrow$ Automated Update | Ensures docs are a truthful reflection of code. |

## 📋 Implementation Standard
All services in this library are implemented as **Unified Agentic Services** in `config/services/`. They adhere to the **ReAct Loop**:
`Thought (Analyze/Justify) $\rightarrow$ Action (Tool) $\rightarrow$ Observation (Analyze $\rightarrow$ Update)`

They must also follow the **Professional Constraints**:
- **No Big Bangs**: Incremental changes only.
- **Evidence-Based**: No assumptions; verify via tools.
- **Truth First**: Code is the source of truth.
