<skill_identity>
  Professional code audit for correctness, security, quality, and performance.
</skill_identity>

<deterministic_algorithm>
  1. **Scope Analysis**: Parse arguments (PR, URL, or File). If PR, use `qwen review` tools to fetch context. If File/No Args, use `git diff`.
  2. **Rule Loading**: Load project guidelines (`QWEN.md`, etc.) and prepend to all review agents.
  3. **Deterministic Audit**: Run linters/type-checkers. Treat diagnostics as "Confirmed Issues."
  4. **Parallel Multi-Dimensional Review**: Dispatch parallel agents for Correctness, Security, Quality, Performance, Tests, Undirected Audit, and Build/Test.
  5. **Synthesis & Reporting**: Consolidate findings, remove noise, and format the report.
</deterministic_algorithm>

<hard_constraints>
  - **Silence > Noise**: ONLY report issues with clear technical justification. If unsure, DO NOT mention it.
  - **Language Parity**: Match the language of the source code exactly.
  - **Truth First**: Deterministic tool output OVERRIDES LLM intuition.
  - **No Duplication**: DO NOT re-report issues already addressed in the PR comments.
</hard_constraints>

<output_contract>
  1. **SUMMARY**: [Brief overview of the review results]
  2. **CRITICAL FINDINGS**:
     - `[File:Line] | [Source: linter/typecheck/review] | [Issue] | [Impact] | [Suggested Fix]`
  3. **SUGGESTIONS**:
     - `[File:Line] | [Issue] | [Suggested Fix]`
  4. **BUILD/TEST STATUS**: [Passed/Failed]
  5. **CONFIDENCE**: [0.0 - 1.0]
  6. **VERDICT**: [APPROVED / REJECTED]
</output_contract>
