# Universal Agent Recipe Template

This template is used to standardize the optimization of all agents within the Qwen Code stack. Every agent must have a corresponding recipe card following this format to ensure consistency, reproducibility, and token efficiency.

---

##  Recipe: [Agent Name]
**Model**: `[model_id]`
**Version**: `[SemVer]`
**Last Verified**: `[YYYY-MM-DD]`

###  1. Hyperparameters
*The precise sampling settings required for this agent's role.*
- **Temperature**: `[value]` (Reasoning vs Creativity balance)
- **Top_P**: `[value]` (Nucleus sampling)
- **Repetition_Penalty**: `[value]` (Loop prevention)
- **Max_Tokens**: `[value]` (Response length limit)
- **Stop Sequences**: `[list of tokens/strings]`

###  2. Structural Blueprint
*The prompt architecture used to guide the model.*
- **Tagging Strategy**: `[e.g., XML-Hybrid / Native-Only / Compressed]`
- **Instruction Positioning**: `[e.g., Primacy-Recency / Recency-Only / Top-Heavy]`
- **Core Tags**: `[List of specific tags used, e.g., <persona>, <constraints>, <context>]`

###  3. Behavioral Mandates
*The core logic that defines the agent's "Law".*
- **Primary Objective**: `[One-sentence definition of the agent's ultimate goal]`
- **Key Constraints**: 
    - `[Constraint 1]`
    - `[Constraint 2]`
    - `[Constraint 3]`
- **Known Failure Patterns**:
    - `[Pattern A]` $\rightarrow$ `[Prompt-level Fix]`
    - `[Pattern B]` $\rightarrow$ `[Prompt-level Fix]`

###  4. Tooling & Skills
*The functional capabilities of the agent.*
- **Allowed Tools**: `[list of MCP tools]`
- **Disallowed Tools**: `[list of blocklisted tools]`
- **Primary Skills**: `[List of SKILL.md references]`

###  5. Validation Suite
*How to verify that this recipe is performing as expected.*
- **Stress-Test Prompts**: `[Link to benchmark prompts or specific examples]`
- **Success Criteria**: `[Quantitative or qualitative markers of a correct response]`
- **Baseline Comparison**: `[Which model/recipe this was compared against]`
---
