🏛️ 
# 🛣️ Routing Plane: The Strategic Triage System

The **Routing Plane** is the second layer of the Mega Code 4-Layer Architecture. While the Control Plane determines **WHAT** needs to be done, the Routing Plane determines **WHICH** specialized agent (Skill) is best equipped to execute the task based on the current system state, intent, and context.

## 🎯 Objective
To eliminate "ego-agent" behavior by replacing linear chat with a deterministic, state-aware triage system that maps requests to the most precise specialized tool in the agentic swarm.

---

## ⚙️ The Triage Pipeline

The Routing Plane operates as a sequential pipeline that transforms a raw user prompt into a structured **Job Contract**.

### 1. Intent Classification
The process begins with the `IntentClassifier`. It analyzes the prompt to extract:
- **Intent Name**: The high-level category of the request (e.g., `feature-implementation`, `bug-fix`, `architectural-audit`).
- **Risk Profile**: An assessment of the potential impact of the task (e.g., `Low`, `Medium`, `High`, `Critical`).
- **Suggested Tool Chain**: A preliminary list of tools required to fulfill the intent.

### 2. State-Aware Skill Selection
The `SkillOrchestrator` then evaluates all available skills using a weighted scoring algorithm (inspired by STRMAC). It considers three primary dimensions:

#### A. Capability Match (Weight: +2.0)
The orchestrator scans the prompt for keywords defined in the skill's `triggers`. A direct keyword match provides the strongest signal for agent selection.

#### B. Phase Alignment (Weight: +1.5)
The system tracks the current **Active Phase** via the `StateManager`. Skills are prioritized based on their role in the lifecycle:
- **PLANNING**: $\to$ `architect`, `scout`, `researcher`
- **IMPLEMENTATION**: $\to$ `developer`
- **VERIFICATION**: $\to$ `reviewer`, `qa_lead`
- **OPTIMIZATION**: $\to$ `system_optimizer`

#### C. Contextual Anchors (Weight: +0.5)
If a file is currently open or targeted, the orchestrator checks the file extension against the skill's `file_extensions` trigger. (e.g., `.py` $\to$ `python-expert`).

#### D. Reviewer Boost (+1.0 to +3.0)
To ensure quality, the `reviewer` agent receives a priority boost if:
- The system is in the `VERIFICATION` phase.
- A previous sub-agent's report indicates low confidence ($< 0.7$) or explicitly requests a review.

### 3. The Job Contract
The final output of the Routing Plane is a machine-readable **Job Contract**. This contract serves as the authoritative instruction for the Execution Plane.

**Contract Schema:**
```json
{
  "job_contract": {
    "intent": "string",
    "risk_profile": "string",
    "recommended_skill": "string",
    "suggested_tool_chain": ["string"],
    "reason": "string"
  },
  "model": "string"
}
```

---

## 📂 Skill Discovery & Configuration

Skills are treated as "plugins" and are discovered dynamically from the `~/.qwen/skills` directory.

### Supported Formats
The Routing Plane supports two configuration formats:
1. **YAML (`.yaml`)**: Pure configuration files.
2. **Markdown (`SKILL.md`)**: Human-readable documentation with a YAML frontmatter block for the orchestrator.

### Configuration Anatomy
A skill definition includes:
- **Name**: Unique identifier used in the Job Contract.
- **Triggers**: Keywords and file extensions that trigger the skill.
- **Model**: The specific LLM to use (or `inherit` to use the global default).
- **Persona**: The system prompt and reporting schema that define the agent's behavior.

---

## 🛠️ How to Extend the Routing Plane

To add a new specialized agent to the swarm:

1. **Create a Skill Definition**: Add a `SKILL.md` file to `~/.qwen/skills/your-skill-name/`.
2. **Define Triggers**: Add keywords that uniquely identify the tasks this agent should handle.
3. **Set the Persona**: Define a strict system prompt that enforces the `S-READ` and `S-VERIFY` protocols.
4. **Verify**: Run the `skill_selector.py` check command to ensure your skill is being triggered correctly:
   ```bash
   python3 packages/core/src/skill_selector.py check_prompt "Your test prompt here"
   ```
