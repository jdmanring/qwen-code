# Skill: Commit

## 1. Skill Identity
The **Commit** skill is a deterministic protocol for generating professional, atomic, and descriptive git commits. It solves the problem of poor commit history (e.g., "fixed bug," "updates") by enforcing the **Conventional Commits** standard.

## 2. Trigger Logic
This skill is triggered when:
- The agent has completed a task and needs to commit changes.
- The user requests to "commit the changes" or "finalize the feature."
- A request is made to stage and commit specific files.

## 3. Operational Workflow
The Commit skill follows a strict five-step sequence:
1. **Diff Analysis**: Analyzes exact changes using `git diff HEAD` and `git diff --staged`.
2. **Atomic Decomposition**: Verifies if changes represent a single logical unit. If multiple unrelated changes exist, it requests a split.
3. **Type Selection**: Assigns a Conventional Commit type (e.g., `feat`, `fix`, `docs`, `refactor`, `chore`).
4. **Message Drafting**: Constructs the message using the imperative mood and present tense.
   - **Subject**: Descriptive, no period.
   - **Body**: Focuses on "Why" and "How," not "What."
   - **Footer**: References issue numbers (e.g., `Fixes #123`).
5. **Staging & Execution**: Executes `git add` for specific files and `git commit -m`.

## 4. Output Contract
The skill must provide the following details for every commit:
- **COMMIT MESSAGE**: The exact string used for the commit.
- **FILES STAGED**: A list of absolute paths included in the commit.
- **CONVENTIONAL TYPE**: The assigned type (e.g., `feat`).
- **CONFIDENCE**: A score from 0.0 to 1.0.

## 5. Mirror Link
Original Configuration: [`config/skills/commit/SKILL.md`](../../../config/skills/commit/SKILL.md)
