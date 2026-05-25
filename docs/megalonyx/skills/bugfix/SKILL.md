# Skill: Bugfix

## 1. Skill Identity
The **Bugfix** skill is a specialized workflow for resolving GitHub issues. It solves the problem of "blind fixing" (fixing without reproduction) by enforcing a strict **reproduce-first** methodology, ensuring that fixes are complete and do not introduce regressions.

## 2. Trigger Logic
This skill is triggered by:
- Provision of a GitHub issue URL or issue number.
- User requests to "fix a bug," "investigate an issue," or "debug a reported problem."

## 3. Operational Workflow
The Bugfix skill follows a rigorous six-step lifecycle:
1. **Read The Issue**: Fetches the issue via `gh` CLI and creates a local artifact in `.qwen/issues/issue-<number>.md`.
2. **Reproduce**: Spawns a `test-engineer` agent to create a reproduction report. If the bug is not reproduced, the process stops.
3. **Fix**: Implements the fix based on the reproduction report. Uses `structured-debugging` for complex failures.
4. **Verify**: Builds the project and spawns the `test-engineer` again to verify the fix. Iterates until status is `VERIFIED_FIXED`.
5. **Tests**: Runs existing unit tests and adds new regression tests for the failure scenario.
6. **Code Review**: Executes `/review` to triage changes. Valid issues are fixed and re-verified.

## 4. Output Contract
The output of a successful Bugfix operation includes:
- **Modified Source Code**: The actual fix applied to the codebase.
- **Updated Issue Artifact**: The `.qwen/issues/` file containing both the Reproduction and Verification reports.
- **Regression Tests**: New or updated test cases confirming the fix.

## 5. Mirror Link
Original Configuration: [`config/skills/bugfix/SKILL.md`](../../../config/skills/bugfix/SKILL.md)
