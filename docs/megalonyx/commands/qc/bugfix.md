# Bugfix Command

## Command Identity
The `bugfix` command triggers a rigorous, reproduce-first workflow to resolve bugs reported via GitHub issues. It ensures that a bug is fully understood and reproducible before any code changes are made, and verified by an independent agent before completion.

## Operational Workflow

The system executes the following sequence:

1.  **Issue Capture**: 
    - Reads the GitHub issue using the `gh` CLI.
    - Creates a local tracking file at `.qwen/issues/issue-<number>.md`. This file serves as the single source of truth to maintain context and minimize token usage.
2.  **Reproduction**: 
    - Spawns the `test-engineer` agent.
    - The agent analyzes the issue file and attempts to reproduce the bug.
    - The `test-engineer` updates the issue file with a **Reproduction Report**.
    - If the bug is not reproduced, the process halts.
3.  **Localization and Fix**: 
    - The system analyzes the reproduction report to identify the root cause.
    - Applies the fix to the codebase.
    - For complex bugs, the `structured-debugging` skill is employed to systematically test hypotheses.
4.  **Verification**: 
    - Spawns the `test-engineer` agent again.
    - The agent verifies the fix by re-running reproduction steps or executing a newly written test script.
    - The issue file is updated with a **Verification Report**.
    - If the status remains `STILL_BROKEN`, the system loops back to the Fix stage.
5.  **Regression Testing**: 
    - Runs existing unit tests for modified packages.
    - Ensures the reproduction test passes.
    - Adds new unit or integration tests to prevent future regressions.

## Input/Output

- **Input**: A GitHub issue URL or issue number.
- **Output**: 
    - A verified code fix committed to the repository.
    - A completed `.qwen/issues/issue-<number>.md` file containing both reproduction and verification reports.
    - Passing test suite (including new regression tests).

## Symmetry Link
[View Configuration](../../config/commands/qc/bugfix.md)
