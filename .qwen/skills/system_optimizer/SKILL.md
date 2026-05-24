<skill_identity>
  A deterministic protocol for meta-cognitive analysis of system failures and institutionalizing behavioral fixes in QWEN.md.
</skill_identity>

<deterministic_algorithm>
  1. **Failure Reconstruction**: Analyze the logs and the conversation history to identify the exact sequence of tool calls and responses that led to the failure (e.g., a repetition loop).
  2. **Root Cause Identification**: Determine if the failure was caused by: (Lack of Constraint, Ambiguous Rule, or Tool Failure).
  3. **Behavioral Rule Drafting**: Create a new, prescriptive, and actionable rule to prevent the failure (e.g., "ALWAYS [Action] BEFORE [Action]" or "NEVER [Action] when [Condition]").
  4. **Conflict Check**: Read the existing `QWEN.md` to ensure the new rule does not contradict existing mandates.
  5. **Institutionalization**: Use `edit` to apply the new rule to the project's `QWEN.md`.
</deterministic_algorithm>

<hard_constraints>
  - **Prescriptive Only**: No vague advice. Rules must be binary and actionable.
  - **Evidence-Backed**: Every rule MUST be linked to a specific failure instance from the logs.
  - **No Code Modification**: The System Optimizer is STRICTLY PROHIBITED from modifying application code.
</hard_constraints>

<output_contract>
  1. **FAILURE ANALYSIS**: Description of the error pattern and its root cause.
  2. **PROPOSED RULE**: The exact text of the new behavioral rule.
  3. **JUSTIFICATION**: Why this rule prevents the failure.
  4. **ACTION TAKEN**: Confirmation of the update to `QWEN.md`.
  5. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
