# Skill: Critic

## Skill Identity
The **Critic** is a deterministic protocol designed for progress verification, loop detection, and stagnation analysis. It serves as the system's internal quality gate, ensuring that the agent is moving toward a solution rather than circling in a repetitive failure loop or stagnating due to a flawed approach.

## Trigger Logic
This skill is triggered when:
- The orchestrator requires a formal verification of progress after a series of iterations.
- Stagnation is suspected (e.g., the same error persists across multiple attempts).
- A "progress check" or "loop analysis" is explicitly requested.
- The agent has failed to achieve a milestone within a predefined number of steps.

## Operational Workflow
1. **State Snapshot Analysis**: Compare the current system state (files, test results, todo list) with the state from $N$ steps ago.
2. **Progress Quantification**: Identify concrete changes, such as new tests passing, new files created, or todo items completed.
3. **Loop Detection**: Analyze tool calls to check if the agent is repeating the same arguments or producing identical errors.
4. **Stagnation Diagnosis**: If no progress is detected, analyze tool outputs to determine the root cause (e.g., "wrong approach," "missing dependency," "hallucinated path").
5. **Course Correction**: Propose a specific "Pivot" (e.g., "Stop using grep, try glob" or "Re-read the API docs") to break the cycle and resume progress.

## Output Contract
The Critic must provide the following structured output:
- **VERDICT**: A binary/ternary classification: `[PROGRESSING / STAGNATED / LOOPING]`.
- **EVIDENCE**: A detailed comparison of state snapshots showing progress or repetition.
- **DIAGNOSIS**: The root cause of stagnation or the loop (if applicable).
- **PIVOT RECOMMENDATION**: A specific, actionable change in strategy to resume progress.
- **CONFIDENCE**: A score from `0.0` to `1.0`.

## Symmetry Link
Original configuration: [`config/skills/critic/SKILL.md`](../../config/skills/critic/SKILL.md)
