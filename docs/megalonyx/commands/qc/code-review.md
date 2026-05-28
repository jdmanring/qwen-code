---
name: code-review
description: Invokes an expert reviewer persona to analyze Pull Requests (PRs).
category: qc
---

# Code Review Command

## Command Identity
The `code-review` command invokes an expert reviewer persona to analyze Pull Requests (PRs). It focuses on code correctness, project conventions, performance, security, and test coverage.

## Operational Workflow

The system follows these steps:

1.  **PR Identification**:
    - If a PR number is provided in the arguments, it is used directly.
    - Otherwise, the system executes `gh pr list` to identify open PRs for the user to choose from.
2.  **Data Acquisition**:
    - Fetches PR metadata using `gh pr view <number>`.
    - Retrieves the full code diff using `gh pr diff <number>`.
3.  **Technical Analysis**:
    - Analyzes the diff against project standards.
    - Evaluates the logic for potential edge cases, performance bottlenecks, or security vulnerabilities.
    - Checks if the changes are sufficiently covered by tests.
4.  **Review Generation**:
    - Synthesizes the findings into a structured report.

## Input/Output

- **Input**: (Optional) A GitHub PR number.
- **Output**: A comprehensive code review report containing:
    - **Overview**: Summary of the PR's purpose.
    - **Quality Analysis**: Evaluation of style and implementation.
    - **Suggestions**: Specific, actionable improvements.
    - **Risks**: Identification of potential issues or regressions.

## Symmetry Link
[View Configuration](../../config/commands/qc/code-review.md)
