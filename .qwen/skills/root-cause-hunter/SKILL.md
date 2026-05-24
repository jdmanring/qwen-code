<skill_identity>
  Rapidly isolate the cause of non-trivial bugs (race conditions, state leaks, etc.).
</skill_identity>

<deterministic_algorithm>
  1. **Evidence Analysis**: Read the error log/bug description. Identify the "Failure Point." Use `grep_search` to find all occurrences of the error message.
  2. **MRE Construction**: Create a Minimal Reproducible Example (MRE) in `tests/debug/`. The MRE must be a standalone script that triggers the bug consistently. Verify the MRE fails as expected.
  3. **Isolation (The Hunt)**: Use a "Binary Search" approach (commenting out code/print debugging) to narrow the failure window. Formulate a hypothesis: "The bug is caused by X at line Y."
  4. **Hypothesis Verification**: Apply a targeted fix to the MRE. Run the MRE. If it passes, the root cause is confirmed. If it fails, refine the hypothesis and return to Step 3.
  5. **Global Fix & Validation**: Apply the verified fix to the main codebase. Run the project's test suite to ensure the fix works and introduces no regressions.
</deterministic_algorithm>

<hard_constraints>
  - **EVIDENCE-BASED**: NEVER guess the root cause. Every conclusion MUST be backed by a log snippet or a failing MRE.
  - **MRE REQUIREMENT**: No bug is considered "fixed" until a failing MRE has been turned into a passing one.
  - **MINIMALISM**: The fix must be the smallest possible change that resolves the root cause.
</hard_constraints>

<output_contract>
  1. **Root Cause**: [Clear, technical explanation of the bug]
  2. **Evidence**: [Log snippet or file:line reference proving the cause]
  3. **MRE Status**: [Path to the MRE script and its final result]
  4. **Fix Verification**: [Evidence that the fix works and tests pass]
  5. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
