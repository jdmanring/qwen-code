# Skill: Test Coverage Max

## 1. Skill Identity
**Test Coverage Max** is a deterministic protocol designed to eliminate "dark logic"--untested code paths that may hide critical bugs. It forces the execution of every conditional branch and edge case within a target function, ensuring that the test suite is comprehensive and that no branch is left unverified.

## 2. Trigger Logic
This skill is activated when:
- **Coverage Goals**: The user requests 100% branch or line coverage for a specific module.
- **Edge Case Hardening**: The goal is to ensure a function is robust against nulls, overflows, or empty collections.
- **Regression Prevention**: A bug was found in a previously "tested" area, indicating a gap in the coverage.
- **Explicit Keywords**: Requests for "maximum coverage," "branch analysis," or "edge case testing."

## 3. Operational Workflow
The skill employs a systematic iterative process:
1. **Control Flow Analysis**: Uses `read_file` and `grep` to identify all conditional branches (`if`, `switch`, `try-catch`, ternaries) within the target code.
2. **Boundary Mapping**: For every identified branch, the agent defines the specific input values (boundary conditions, nulls, overflows, empty collections) required to trigger that path.
3. **Test Generation**: Creates isolated test functions for each boundary condition using `edit` or `write_file`.
4. **Execution & Coverage Audit**: Runs the tests and utilizes coverage tools (e.g., `pytest-cov`, `istanbul`) to pinpoint remaining uncovered lines.
5. **Iterative Filling**: Repeats the mapping and generation steps until branch coverage reaches 100% or a technical impossibility is formally proven.

## 4. Output Contract
The final report must include:
- **COVERAGE METRIC**: The percentage increase in line and branch coverage.
- **EDGE CASES COVERED**: A list of the specific boundary conditions that were successfully tested.
- **NEW TESTS**: A list of the new test files or functions added to the suite.
- **UNREACHABLE PATHS**: A technical justification for any paths that could not be covered.
- **CONFIDENCE**: A score from `0.0` to `1.0` regarding the completeness of the coverage.

## 5. Mirror Link
**Original Configuration**: [`../../../config/skills/test-coverage-max/SKILL.md`](../../../config/skills/test-coverage-max/SKILL.md)
