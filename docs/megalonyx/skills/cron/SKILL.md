# Skill: Cron

## Skill Identity
The **Cron** skill is responsible for the scheduling and management of recurring tasks and automation jobs within the environment. It ensures that periodic maintenance, synchronization, or reporting tasks are executed reliably without manual intervention.

## Trigger Logic
This skill is triggered when:
- The user requests the creation of a recurring task or scheduled job.
- There is a need to list, modify, or delete existing automation schedules.
- Phrases like "schedule a task", "run every X hours", or "set up a cron job" are used.

## Operational Workflow
1. **Task Analysis**: Determine the required frequency, timing, and dependencies of the requested task.
2. **Schedule Creation**: Utilize the `cron_create` tool to establish the recurring job.
3. **Verification**: Use the `cron_list` tool to confirm that the job is correctly scheduled and active.

## Output Contract
The Cron skill adheres to the following output format:
- **SCHEDULE SUMMARY**: Detailed information regarding the created, deleted, or listed jobs.
- **VERIFICATION**: Confirmation of the schedule as retrieved from `cron_list`.
- **CONFIDENCE**: A score from `0.0` to `1.0`.

## Mirror Link
Original configuration: [`config/skills/cron/SKILL.md`](../../config/skills/cron/SKILL.md)
