# Skill: Qwen Code Claw

## 1. Skill Identity
**Qwen Code Claw** serves as a high-capability Code Agent specialized in deep code understanding, project generation, feature implementation, bug fixing, and systemic refactoring. It leverages the Qwen Code engine via the Agent Client Protocol (ACP) to perform complex development tasks.

## 2. Trigger Logic
This skill is triggered by requests involving:
- **Codebase Exploration**: Understanding existing logic or asking questions about source code.
- **Project Scaffolding**: Generating new projects or adding significant new features.
- **Code Review**: Auditing pull requests or specific modules.
- **Maintenance**: Fixing bugs or refactoring existing code.
- **Automation**: Executing programming tasks like documentation generation or test writing.
- **Keywords**: `qwen code`, `acpx`, `generate feature`, `analyze codebase`.

## 3. Operational Workflow
1. **Environment Setup**: Verifies authentication via `qwen auth status` and ensures the `BAILIAN_CODING_PLAN_API_KEY` is configured.
2. **ACPX Integration**: Utilizes `acpx` to interface with the Qwen Code agent, avoiding raw PTY scraping for better stability.
3. **Task Execution**:
    - **Persistent Sessions**: For iterative tasks (e.g., "inspect tests" $\rightarrow$ "apply fix").
    - **One-Shot Execution**: For immediate, single-purpose tasks (e.g., "summarize repo").
    - **Parallel Streams**: Using named sessions (`-s`) for concurrent task management.
4. **Permission Management**: Operates under specific approval modes (`--approve-all`, `--approve-reads`, `--deny-all`) to control tool execution.

## 4. Output Contract
The output format varies by invocation mode:
- **Interactive/Text**: Standard conversational responses and code blocks.
- **Machine-Readable**: JSON format (`--format json`) for orchestration and automation.
- **Quiet**: Minimal output for CI/CD integration.

## 5. Mirror Link
Original Configuration: [`config/skills/qwen-code-claw/SKILL.md`](../../../config/skills/qwen-code-claw/SKILL.md)
