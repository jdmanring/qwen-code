# Commit Command

## Command Identity
The `commit` command automates the process of generating professional, conventional commit messages for staged changes and pushing them to the remote repository.

## Operational Workflow

The system executes the following logic:

1.  **State Assessment**: 
    - Runs `git status` to identify staged and unstaged changes.
    - Identifies the current active branch.
2.  **Safety Check**: 
    - If unstaged changes exist, the user is notified. The system strictly ignores unstaged changes to avoid accidental commits.
3.  **Change Analysis**: 
    - Analyzes `git diff --staged` to determine the nature of the changes (e.g., feature, bug fix, refactor).
4.  **Branch Management**: 
    - If the current branch is `main` or `master`, the system automatically generates a descriptive feature branch name and switches to it (`git checkout -b <branch-name>`).
    - If on a feature branch, it verifies if the branch name aligns with the changes; if not, it prompts the user to either create a new branch or proceed.
5.  **Message Synthesis**: 
    - Generates a message following the Conventional Commits specification: `<type>(<scope>): <description>`.
    - Includes optional detail bullets and a footer explaining the "why" and the impact.
6.  **User Validation**: 
    - Presents the proposed commit message and target branch for user confirmation.
7.  **Execution**: 
    - Executes `git commit -m "<message>"` and `git push -u origin <branch-name>`.

## Input/Output

- **Input**: Staged changes in the local Git index.
- **Output**: 
    - A new Git commit with a standardized message.
    - Changes pushed to the remote origin on the appropriate branch.

## Symmetry Link
[View Configuration](../../config/commands/qc/commit.md)
