# Skill: Structured Debugging

## 1. Skill Identity
**Structured Debugging** is a hypothesis-driven methodology designed for resolving non-trivial, "impossible," or flaky bugs. It replaces the intuitive "guess-and-fix" approach with a disciplined cycle of hypothesis, instrumentation, and verification, ensuring that the root cause is identified and proven before any code changes are applied.

## 2. Trigger Logic
This skill is triggered by:
- **Contextual Indicators**: Investigation of non-trivial bugs, unexpected behavior, or flaky tests.
- **Failure Patterns**: When a first attempt at a fix fails, or when behavior contradicts the internal model of the system.
- **External Attribution**: When there is a temptation to blame external systems (APIs, libraries, LLMs) without empirical evidence.
- **Explicit Keywords**: Requests for "deep dive debugging," "root cause analysis," or "structured investigation."

## 3. Operational Workflow
The skill follows a recursive 6-step cycle:
1. **Hypothesize**: Formulate a specific, testable theory about the failure. Document the expected state at each step in an investigation journal (side note file).
2. **Design Instrumentation**: Identify 2-3 critical decision points and add targeted logs or assertions. Focus on *data values* (payloads, return codes) rather than *presence checks* (function calls).
3. **Verify Data Collection**: Confirm that the instrumentation output is actually captured (e.g., checking for `2>/dev/null` or flush issues) to avoid wasted runs.
4. **Run and Observe**: Execute the test and read the output verbatim. If data contradicts the hypothesis, the data is treated as the ground truth.
5. **Document Findings**: Update the investigation journal with specific log quotes, confirming what was proven or disproved.
6. **Iterate**: Refine the hypothesis based on new evidence and return to Step 2.

## 4. Output Contract
The debugging process concludes only when the root cause is proven. The final output must include:
- **Root Cause**: A detailed description of the specific mechanism causing the bug.
- **Evidence**: Specific log lines or data captures that confirm the root cause.
- **Fix**: A description of the change being made and why it directly addresses the proven root cause.

## 5. Symmetry Link
**Original Configuration**: [`../../../config/skills/structured-debugging/SKILL.md`](../../../config/skills/structured-debugging/SKILL.md)
