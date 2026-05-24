<skill_identity>
  A deterministic protocol for eliminating "dark logic" by forcing execution of every conditional branch and edge case.
</skill_identity>

<deterministic_algorithm>
  1. **Control Flow Analysis**: Use `read_file` and `grep` to identify all conditional branches (`if`, `switch`, `try-catch`, `ternaries`) in the target function.
  2. **Boundary Mapping**: For every branch, define the input values (boundary conditions, nulls, overflows, empty collections) required to trigger it.
  3. **Test Generation**: Use `edit` or `write_file` to create a test suite that targets each identified boundary condition.
  4. **Execution & Coverage Audit**: Run the tests using `shell` and use a coverage tool (e.g., `pytest-cov`, `istanbul`, `gocov`) to identify remaining uncovered lines.
  5. **Iterative Filling**: Repeat steps 2-4 until branch coverage reaches 100% or a technical impossibility is proven.
</deterministic_algorithm>

<hard_constraints>
  - **No Happy-Path Only**: Tests focusing only on the "success" case are considered insufficient.
  - **Zero-Assumption**: NEVER assume a branch is "unreachable" without proving it via static analysis or tool output.
  - **Isolation**: Each edge case MUST be tested in an isolated test function.
</hard_constraints>

<output_contract>
  1. **COVERAGE METRIC**: % increase in line/branch coverage.
  2. **EDGE CASES COVERED**: List of specific boundary conditions tested.
  3. **NEW TESTS**: List of added test files/functions.
  4. **UNREACHABLE PATHS**: Justification for any paths that could not be covered.
  5. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
