<skill_identity>
  A deterministic protocol for generating professional, atomic, and descriptive git commits following the Conventional Commits standard.
</skill_identity>

<deterministic_algorithm>
  1. **Diff Analysis**: Use `git diff HEAD` (and `git diff --staged`) to analyze the exact changes made to the codebase.
  2. **Atomic Decomposition**: Determine if the changes represent a single logical unit. IF multiple unrelated changes are found $\rightarrow$ request the user to split the commit.
  3. **Type Selection**: Assign a Conventional Commit type based on the change: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
  4. **Message Drafting**: Construct the message:
     - **Subject**: Imperative mood, present tense, no period.
     - **Body**: Explain the "Why" and "How" (the reasoning), not the "What" (the diff).
     - **Footer**: Reference issue numbers (e.g., `Fixes #123`).
  5. **Staging & Execution**: Use `git add` for the specific files and `git commit -m "..."` to finalize.
</deterministic_algorithm>

<hard_constraints>
  - **No "Fixed bug"**: Subject lines MUST be descriptive (e.g., `fix: resolve null pointer in UserAuth.ts`).
  - **Atomic Only**: NEVER commit multiple unrelated features in one commit.
  - **Imperative Mood**: ALWAYS use "Add feature" not "Added feature" or "Adds feature".
</hard_constraints>

<output_contract>
  1. **COMMIT MESSAGE**: The exact string used for the commit.
  2. **FILES STAGED**: List of absolute paths included in the commit.
  3. **CONVENTIONAL TYPE**: The type used (e.g., `feat`, `fix`).
  4. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
