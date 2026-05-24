# Skill: generate-agent

## Skill Identity
The `generate-agent` skill enables the dynamic instantiation of new specialized agents. It transforms high-level descriptions of required expertise into fully configured agent personas with tailored toolsets and constraints.

## Trigger Logic
This skill is triggered by:
- Requests to "create a new agent" or "setup a specialized persona".
- The identification of a recurring task that would benefit from a dedicated agent.
- Descriptions of a new role (e.g., "I need an agent that specifically handles database migrations").

## Operational Workflow
1. **Persona Extraction**: Analyze the input description to define core expertise, primary responsibilities, and operational constraints.
2. **Tool Selection**: Determine the minimum viable set of tools required for the agent to fulfill its role without becoming a general-purpose agent.
3. **Agent Creation**: Invoke the `create_agent` tool to instantiate the agent with the extracted parameters.
4. **Verification**: Confirm that the agent was created successfully and its configuration matches the intended persona.

## Output Contract
The output must include:
1. **AGENT IDENTITY**: The name and description of the new agent.
2. **CONFIGURATION SUMMARY**: The specific tools and model assigned.
3. **VERIFICATION**: Confirmation of successful creation.
4. **CONFIDENCE**: A numerical value (0.0 - 1.0).

## Symmetry Link
Original configuration: [`config/skills/generate-agent/SKILL.md`](../../../config/skills/generate-agent/SKILL.md)
