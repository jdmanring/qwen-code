# Skill: Docs-Update-From-Diff

## Skill Identity
**Docs-Update-From-Diff** is a specialized skill that reviews local code changes using `git diff` and updates the official documentation under `docs/` to match. It ensures that uncommitted work or recent refactors are immediately reflected in the documentation.

## Trigger Logic
This skill is triggered when the user asks to:
- Document current uncommitted work.
- Sync docs with local changes.
- Update docs after a feature implementation or refactor.
- Use phrases such as "git diff", "local changes", "update docs", or "official docs".

## Operational Workflow
1. **Build the Change Set**: Inspect `git status --short`, `git diff --stat`, and targeted `git diff` output to ground the delta in actual code changes.
2. **Derive the Docs Impact**: Extract user-facing or developer-facing facts (new commands, flags, config keys, etc.) from the diff.
3. **Find the Right Docs Location**: Map changes to the correct surface: `docs/users/**` for end-users, `docs/developers/**` for internals, or root `docs/**` for navigation.
4. **Write the Update**: Edit documentation to state current behavior (not history), using concrete paths and keys from the diff.
5. **Cross-check**: Verify the updated docs against the code diff to ensure no outdated examples or names remain.

## Output Contract
The deliverable for this skill is:
- **Docs Edits**: Modifications under `docs/` that make local changes understandable to a reader who has not seen the diff.
- **Summary**: A short report identifying exactly which pages were updated.

## Symmetry Link
Original configuration: [`config/skills/docs-update-from-diff/SKILL.md`](../../config/skills/docs-update-from-diff/SKILL.md)
