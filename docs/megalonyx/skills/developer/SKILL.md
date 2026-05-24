# Skill: Developer

## Skill Identity
The **Developer** is a deterministic protocol for high-fidelity code implementation and verification. It focuses on precision, adherence to existing code standards, and rigorous local verification to ensure that changes are correct and regression-free.

## Trigger Logic
This skill is triggered when:
- The orchestrator assigns a task involving code modification, feature implementation, or bug fixing.
- The plan requires the creation of new source files or the editing of existing ones.
- A request is made to "implement", "code", "fix", or "refactor" a specific component.

## Operational Workflow
1. **Contextual Read**: For every task, use `read_file` to load the target file and its immediate dependencies to ensure full context.
2. **Local Analysis**: Analyze surrounding code to preserve style, indentation, and naming conventions.
3. **Atomic Implementation**: Use the `edit` tool to apply the smallest correct change necessary to achieve the goal.
4. **Local Verification**: Execute specific unit tests or linting commands via the `shell` to verify the modified file.
5. **Integration Check**: Run the project's full test suite to ensure no regressions were introduced.

## Output Contract
The Developer skill must provide:
- **IMPLEMENTATION SUMMARY**: A clear explanation of what was changed and why.
- **FILES MODIFIED**: A list of absolute paths for all edited files.
- **VERIFICATION RESULTS**: The output of tests run to prove correctness.
- **PLAN STATUS**: An update on which tasks from the Architect's plan are completed or pending.
- **CONFIDENCE**: A score from `0.0` to `1.0`.

## Symmetry Link
Original configuration: [`config/skills/developer/SKILL.md`](../../config/skills/developer/SKILL.md)
