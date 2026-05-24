# Skill: System Optimizer

## 1. Skill Identity
The **System Optimizer** is a deterministic protocol for the meta-cognitive analysis of system failures. Its primary goal is to identify behavioral patterns that lead to errors (such as repetition loops or constraint violations) and institutionalize the fixes by updating the project's core operational laws in `QWEN.md`.

## 2. Trigger Logic
This skill is activated upon:
- **Behavioral Failures**: Detection of systemic errors, such as the agent entering a loop or repeatedly failing the same task.
- **Constraint Violations**: When the agent violates a mandate in `QWEN.md` or fails to follow a prescribed protocol.
- **Institutionalization Requests**: When a recurring problem is identified that requires a permanent behavioral rule to prevent future occurrences.

## 3. Operational Workflow
The Optimizer follows a strict institutionalization pipeline:
1. **Failure Reconstruction**: Analyzes logs and conversation history to map the exact sequence of tool calls and responses that led to the failure.
2. **Root Cause Identification**: Categorizes the failure into one of three types: *Lack of Constraint*, *Ambiguous Rule*, or *Tool Failure*.
3. **Behavioral Rule Drafting**: Drafts a new, prescriptive, and binary rule (e.g., "ALWAYS [Action] BEFORE [Action]").
4. **Conflict Check**: Reviews the existing `QWEN.md` to ensure the new rule does not contradict existing mandates.
5. **Institutionalization**: Applies the new rule to `QWEN.md` using the `edit` tool to ensure the fix is permanent and systemic.

## 4. Output Contract
The System Optimizer must provide the following in its report:
- **FAILURE ANALYSIS**: A description of the error pattern and its identified root cause.
- **PROPOSED RULE**: The exact text of the new behavioral rule to be added.
- **JUSTIFICATION**: An explanation of why this specific rule prevents the identified failure.
- **ACTION TAKEN**: Confirmation that `QWEN.md` has been updated.
- **CONFIDENCE**: A score from `0.0` to `1.0` regarding the effectiveness of the new rule.

## 5. Symmetry Link
**Original Configuration**: [`../../../config/skills/system_optimizer/SKILL.md`](../../../config/skills/system_optimizer/SKILL.md)
