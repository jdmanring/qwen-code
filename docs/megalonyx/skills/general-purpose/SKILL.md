# Skill: general-purpose

## Skill Identity
The `general-purpose` skill serves as the deterministic fallback protocol for handling miscellaneous tasks and providing coordination when no specialized skill is applicable. It ensures that basic operations are performed reliably and transparently without overreaching into complex architectural changes.

## Trigger Logic
This skill is triggered when:
- A request does not match the trigger criteria of any specialized skill.
- A task requires basic file manipulation, search, or environment exploration.
- General coordination between other agents is needed for a simple sequence of actions.

## Operational Workflow
1. **Intent Classification**: Analyze the request to see if it can be delegated to a specialized skill.
2. **Environment Exploration**: Use `glob` or `grep_search` to identify the necessary files and context.
3. **Atomic Execution**: Execute the task using the most direct and efficient tool sequence.
4. **Verification**: Perform a post-action check (e.g., reading a file after writing) to ensure success.
5. **Technical Summary**: Report the actions taken and the final result.

## Output Contract
The output must follow this structure:
1. **ACTION SUMMARY**: A concise description of what was performed.
2. **RESULT**: The final outcome or finding.
3. **CONFIDENCE**: A numerical value (0.0 - 1.0) representing the certainty of the result.

## Mirror Link
Original configuration: [`config/skills/general-purpose/SKILL.md`](../../../config/skills/general-purpose/SKILL.md)
