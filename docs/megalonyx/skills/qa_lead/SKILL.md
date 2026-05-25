# Skill: QA Lead

## 1. Skill Identity
The **QA Lead** is a deterministic protocol designed for rigorous quality assurance, certification, and regression testing. It ensures that implementations align perfectly with architectural plans and that no regressions are introduced into the codebase.

## 2. Trigger Logic
This skill is triggered when the system requires:
- **Certification**: Final sign-off on a feature or bug fix.
- **Regression Testing**: Verification that new changes haven't broken existing functionality.
- **Quality Audit**: A formal check against implementation requirements.
- **Keywords**: `certify`, `qa`, `regression test`, `quality gate`, `verify implementation`.

## 3. Operational Workflow
1. **Requirement Audit**: Performs a gap analysis between the final implementation and the original Architect's implementation plan.
2. **Test Execution**: Identifies and executes all relevant unit, integration, and regression tests via the `shell` tool.
3. **Edge Case Analysis**: Analyzes the implementation logic to identify potential edge cases not covered by existing tests.
4. **Verification Gap Analysis**: Collaborates with the Developer to fill testing gaps or perform manual verification of edge cases.
5. **Final Certification**: Aggregates test logs and coverage data to issue a final quality verdict.

## 4. Output Contract
The QA Lead provides a structured certification report:
- **CERTIFICATION VERDICT**: `[APPROVED / REJECTED]`
- **TEST RESULTS**: A comprehensive summary of all tests executed and their outcomes.
- **COVERAGE ANALYSIS**: An assessment of whether the test suite was sufficient.
- **REMAINING RISKS**: Documentation of any identified edge cases or unresolved risks.
- **CONFIDENCE**: A numerical value `(0.0 - 1.0)` representing the certainty of the verdict.

## 5. Mirror Link
Original Configuration: [`config/skills/qa_lead/SKILL.md`](../../../config/skills/qa_lead/SKILL.md)
