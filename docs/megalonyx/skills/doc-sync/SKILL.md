# Skill: Doc-Sync

## Skill Identity
**Doc-Sync** is a deterministic protocol designed to eliminate "Documentation Rot." It ensures that technical documentation remains a faithful representation of the actual implementation by synchronizing docs with the current state of the codebase.

## Trigger Logic
This skill is triggered when:
- A request is made to "sync docs with code" or "update documentation to match implementation."
- A feature has been implemented/changed, and the corresponding documentation needs verification.
- The orchestrator identifies a discrepancy between a doc's description and the actual code behavior.

## Operational Workflow
1. **Implementation Audit**: Use `read_file` and `grep` to analyze the current state of the target feature (API signatures, parameters, logic flow).
2. **Doc Discovery**: Use `glob` and `grep` to locate all documentation files (`.md`, `.txt`) referencing the target feature.
3. **Delta Analysis**: Compare the audit results with the current documentation to identify discrepancies.
4. **Synchronized Update**: Use `edit` to update the documentation to perfectly reflect the current implementation.
5. **Truth Verification**: Perform a side-by-side re-read of the updated documentation and the code to ensure 100% alignment.

## Output Contract
The Doc-Sync skill provides:
- **SYNC REPORT**: A comprehensive list of all documentation files and sections modified.
- **DELTA SUMMARY**: A "Before vs. After" summary of the changes made.
- **VERIFICATION**: Confirmation that all related symbols in the code were checked.
- **CONFIDENCE**: A score from `0.0` to `1.0`.

## Mirror Link
Original configuration: [`config/skills/doc-sync/SKILL.md`](../../config/skills/doc-sync/SKILL.md)
