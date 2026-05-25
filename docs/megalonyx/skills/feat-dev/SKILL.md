# Skill: feat-dev

## Skill Identity
The `feat-dev` skill defines a rigorous, phased end-to-end workflow for implementing non-trivial features within the qwen-code ecosystem. It ensures that features are well-investigated, architecturally sound, and verified against a concrete test plan before being merged, reducing regressions and design drift.

## Trigger Logic
This skill is triggered when:
- A new feature request is received that requires coordinated changes across multiple files.
- A complex behavioral change is needed that necessitates a design document.
- Implementation requires a formal verification process (E2E testing) beyond simple unit tests.

## Operational Workflow
The workflow follows a strict linear progression where each phase produces a required artifact:
1. **Investigate**: Explore existing implementation, runtime wiring, and constraints.
2. **Design Doc**: Create a document in `.qwen/design/<feature>.md` covering the problem statement, proposed changes, and scope.
3. **Test Plan**: Define E2E test groups and expected behaviors in `.qwen/e2e-tests/<feature>.md`.
4. **Dry-Run**: Validate the test plan against the current baseline to establish a "failure" state.
5. **Implement**: Execute changes using ESM/TypeScript, ensuring Prettier formatting and collocated unit tests.
6. **Verify**: Run the E2E test plan against the local build and iterate until all tests pass.
7. **Code Review**: Use `/review` to triage findings and apply necessary fixes.
8. **Wrap Up**: Commit using Conventional Commits and create a PR with E2E results.

## Output Contract
- **Planning Artifacts**: Markdown files located in `.qwen/design/` and `.qwen/e2e-tests/`.
- **Implementation**: TypeScript source code and corresponding unit tests.
- **Verification Report**: E2E results appended to the test plan.

## Mirror Link
Original configuration: [`config/skills/feat-dev/SKILL.md`](../../../config/skills/feat-dev/SKILL.md)
