# Skill: Root Cause Hunter

## 1. Skill Identity
The **Root Cause Hunter** is a specialized debugging protocol designed to rapidly isolate the cause of non-trivial bugs, such as race conditions, state leaks, or complex integration failures.

## 2. Trigger Logic
This skill is triggered when:
- **Non-Trivial Bugs**: The cause of a bug is not immediately obvious from the stack trace.
- **Heisenbugs**: Bugs that are intermittent or hard to reproduce.
- **Complex Failures**: Failures involving state corruption or concurrency.
- **Keywords**: `root cause`, `isolate bug`, `debug`, `hunt bug`, `race condition`.

## 3. Operational Workflow
1. **Evidence Analysis**: Analyzes error logs and bug descriptions to identify the "Failure Point" and searches for similar error patterns in the codebase.
2. **MRE Construction**: Develops a Minimal Reproducible Example (MRE) in `tests/debug/`. The MRE must be a standalone script that consistently triggers the bug.
3. **Isolation (The Hunt)**: Employs a binary search approach (systematic code isolation) and print debugging to narrow the failure window and formulate a hypothesis.
4. **Hypothesis Verification**: Applies a targeted fix to the MRE. The root cause is only confirmed once the MRE passes.
5. **Global Fix & Validation**: Applies the verified fix to the main codebase and runs the full project test suite to ensure no regressions.

## 4. Output Contract
The Root Cause Hunter provides a technical post-mortem:
- **Root Cause**: A clear, technical explanation of why the bug occurred.
- **Evidence**: Log snippets or `file:line` references proving the cause.
- **MRE Status**: The path to the MRE script and its final result (Failing $\rightarrow$ Passing).
- **Fix Verification**: Evidence that the global fix works and tests pass.
- **CONFIDENCE**: A numerical value `(0.0 - 1.0)`.

## 5. Symmetry Link
Original Configuration: [`config/skills/root-cause-hunter/SKILL.md`](../../../config/skills/root-cause-hunter/SKILL.md)
