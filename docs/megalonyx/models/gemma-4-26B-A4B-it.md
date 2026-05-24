# Recipe: Primary Orchestrator (MoE)
**Model**: `google/gemma-4-26B-A4B-it`
**Version**: `1.0.0`
**Last Verified**: `2026-05-18`

## ⚙️ 1. Hyperparameters
- **Temperature**: `0.6`
- **Top_P**: `0.9`
- **Repetition_Penalty**: `1.2`
- **Max_Tokens**: `4096`
- **Stop Sequences**: `["<|end_of_turn|>", "### User:", "User:", "<|tool_response|>"]`

## 📐 2. Structural Blueprint
- **Tagging Strategy**: `XML-Hybrid` (Native Chat Roles + Semantic XML tags)
- **Instruction Positioning**: `Recency-Bias` (Heavily weight the end of the prompt)
- **Core Tags**: `<system_instructions>`, `<operational_law>`, `<capabilities>`, `<output_protocol>`, `<critical_reminders>`

## 🧠 3. Behavioral Mandates
- **Primary Objective**: Act as the high-throughput, responsive software engineering orchestrator, managing the ReAct loop with extreme efficiency.
- **Key Constraints**:
    - **Strict Reading**: Never assume a file is fully read; paginate until complete.
    - **No-Direct-Execution**: Never run the system from within the Blueprint directory.
    - **Algorithmic Skills**: Treat skills as deterministic protocols, not personas.
- **Known Failure Patterns**:
    - *Degenerate Looping* $\rightarrow$ Fixed by higher `repetition_penalty` (1.2) and explicit stop sequences.
    - *Instruction Drift* $\rightarrow$ Fixed by moving critical mandates to the bottom of the prompt.

## 🛠 4. Tooling & Skills
- **Allowed Tools**: All MCP tools (Filesystem, GitHub, Tavily, Memory).
- **Disallowed Tools**: None.
- **Primary Skills**: `codebase-mapper`, `refactor-safe`, `root-cause-hunter`, `system_optimizer`.

## 🧪 5. Validation Suite
- **Stress-Test Prompts**: See `docs/models/stability_benchmark.md`.
- **Success Criteria**: $\ge 90\%$ pass rate on Stability Benchmark Suite.
- **Baseline Comparison**: Compared against `gemma-4-31B-it` for throughput and latency.
---
