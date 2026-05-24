# Create PR Command

## Command Identity
The `create-pr` command automates the creation of a structured Pull Request (PR) for staged code changes, ensuring all necessary context and metadata are included.

## Operational Workflow

The system executes the following steps:

1.  **Change Review**: 
    - Analyzes `git diff --staged` to understand the scope and impact of the modifications.
2.  **Repository Alignment**: 
    - Ensures the changes are on a dedicated feature branch (creating one if currently on `main`).
    - Commits all staged changes and pushes the branch to the remote repository.
3.  **PR Description Synthesis**: 
    - Populates the project's PR template.
    - Summarizes changes, provides motivation/context, and lists breaking changes.
    - Links related issues or marks as "No linked issues".
    - Appends the mandatory AI attribution: `🤖 Generated with [Qwen Code](https://github.com/QwenLM/qwen-code)`.
4.  **Submission**: 
    - Constructs the PR title and body.
    - Executes `gh pr create`.
    - **Authentication**: If a `GH_TOKEN` is provided in the user's message, it is used for the session; otherwise, it relies on default `gh` authentication.

## Input/Output

- **Input**: Staged code changes in the local repository.
- **Output**: 
    - A pushed feature branch.
    - A submitted GitHub Pull Request with a professional description.

## Symmetry Link
[View Configuration](../../config/commands/qc/create-pr.md)
