Skill definitions loaded by the Qwen Code CLI as slash commands and agent capabilities.
Each subdirectory is one skill: name matches the directory name, prompt.md contains the skill instructions.

Skills are invoked by the tool executor (control_plane_daemon/tool_executor.py) when dispatching jobs.
The skill name in a job matches the directory name here.

Do not put execution profiles here — those belong in .qwen/agents/.
