# Skill: Refactor Safe

## 1. Skill Identity
**Refactor Safe** is designed to execute systemic structural changes across multiple files while guaranteeing the absence of regressions. It prioritizes surgical precision and comprehensive verification over rapid implementation.

## 2. Trigger Logic
This skill is triggered when the task involves:
- **Structural Changes**: Modifying APIs, renaming symbols, or reorganizing module hierarchies.
- **Systemic Refactoring**: Changes that impact multiple call sites across the codebase.
- **Safe Migration**: Moving logic between components without breaking dependencies.
- **Keywords**: `refactor`, `structural change`, `safe rename`, `systemic update`.

## 3. Operational Workflow
1. **Surgical Discovery**: Uses `grep_search` and `glob` to identify every single occurrence of the target symbol or pattern, creating a definitive "Impacted Files" list.
2. **Impact Analysis**: Reads all impacted files to map dependencies and identify potential side effects, resulting in a detailed `todo_write` plan.
3. **Atomic Implementation**: Applies changes file-by-file. Each change follows a strict cycle: `read_file` $\rightarrow$ `edit` $\rightarrow$ `run_shell_command` (lint/typecheck).
4. **Global Verification**: Executes the full build process and the entire relevant test suite. If failures occur, it pivots to the "Root Cause Hunter" pattern.
5. **Final Reporting**: Synthesizes the results into a verification report.

## 4. Output Contract
The Refactor Safe skill adheres to the following output schema:
- **Refactor Summary**: A high-level explanation of what was changed and the rationale.
- **Impacted Files**: A complete list of all modified files.
- **Verification Evidence**: Raw output from the final successful build and test run.
- **Regression Log**: A detailed account of any issues encountered and resolved during the process.
- **Verdict**: `[SUCCESS / FAILED]`

## 5. Symmetry Link
Original Configuration: [`config/skills/refactor-safe/SKILL.md`](../../../config/skills/refactor-safe/SKILL.md)
