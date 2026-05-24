Execution profile definitions loaded by ExecutionProfileSelector (control_plane_daemon/execution_profile_selector.py).
Each .md file defines one agent persona: name, description, intent affinity, tool permissions, and system prompt.

The intent_profile_map in execution_profile_selector.py assigns canonical profiles to each intent type:
- Feature Synthesis → developer
- Surgical Correction → developer, troubleshooter
- Structural Evolution → architect
- Adversarial Review → code-reviewer, security-auditor
- Exploratory Analysis → scout, Explore
- Knowledge Sync → doc-expert, documentation-writer

Profile scoring uses keyword overlap with the prompt plus intent affinity bonuses.
Add new profiles by creating a new .md file here — the selector loads all files in this directory.
