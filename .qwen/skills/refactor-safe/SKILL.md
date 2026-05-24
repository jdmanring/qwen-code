<skill_identity>
  Execute systemic structural changes across multiple files without introducing regressions.
</skill_identity>

<deterministic_algorithm>
  1. **Surgical Discovery**: Use `grep_search` and `glob` to find every occurrence of the target. Generate an "Impacted Files" list.
  2. **Impact Analysis**: Read all impacted files to understand call sites/dependencies. Identify side effects. Create a `todo_write` list.
  3. **Atomic Implementation**: Apply changes file-by-file. For each: `read_file` $\rightarrow$ `edit` $\rightarrow$ `run_shell_command` (local lint/typecheck). Fix errors immediately.
  4. **Global Verification**: Run the full build command and the relevant test suite. If tests fail, use the "Root Cause Hunter" pattern.
  5. **Final Reporting**: Synthesize the report based on the Output Contract.
</deterministic_algorithm>

<hard_constraints>
  - **NO GUESSING**: NEVER assume a symbol is unused; always verify with `grep_search`.
  - **ATOMICITY**: One change per `edit` call. Do not group unrelated changes.
  - **VERIFICATION FIRST**: No refactor is "complete" until the full test suite passes.
  - **DRY RUN**: IF `--dry-run` is specified $\rightarrow$ only perform Steps 1 and 2 and report planned changes.
</hard_constraints>

<output_contract>
  1. **Refactor Summary**: [What was changed and why]
  2. **Impacted Files**: [List of all modified files]
  3. **Verification Evidence**: [Output of the final build and test run]
  4. **Regression Log**: [Any issues found and fixed during the process]
  5. **Verdict**: [SUCCESS / FAILED]
</output_contract>
