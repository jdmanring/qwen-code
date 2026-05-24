<skill_identity>
  Use this skill to dynamically create new specialized agents based on a description.
</skill_identity>

<deterministic_algorithm>
  1. **Persona Extraction**: Parse the input description to identify the core expertise, responsibilities, and constraints.
  2. **Tool Selection**: Identify the minimum set of tools required for the new agent to function.
  3. **Agent Creation**: Use `create_agent` to instantiate the new specialized agent with the extracted parameters.
  4. **Verification**: Confirm the agent creation was successful and that its configuration is correct.
</deterministic_algorithm>

<hard_constraints>
  - **No Manual File Creation**: Use the `create_agent` tool exclusively; do not attempt to write agent files directly.
  - **Scope Limitation**: Ensure the generated agent is specialized and doesn't become a "general-purpose" catch-all.
</hard_constraints>

<output_contract>
  1. **AGENT IDENTITY**: The name and description of the newly created agent.
  2. **CONFIGURATION SUMMARY**: The tools and model assigned to the agent.
  3. **VERIFICATION**: Confirmation of successful creation.
  4. **CONFIDENCE**: (0.0 - 1.0)
</output_contract>
