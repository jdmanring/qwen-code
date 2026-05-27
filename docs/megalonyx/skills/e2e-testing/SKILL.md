# Skill: e2e-testing

## Skill Identity
The `e2e-testing` skill provides a comprehensive framework for running end-to-end tests of the Qwen Code CLI. It is designed to verify the entire pipeline--from model API calls and tool validation to final execution--ensuring that the system behaves correctly in real-world scenarios. It solves the problem of gaps in unit testing by allowing for headless execution, raw API traffic inspection, and interactive TUI verification.

## Trigger Logic
This skill is triggered by requests or mentions of:
- **E2E Testing**: General end-to-end verification.
- **Headless Testing**: Non-interactive execution with structured (JSON) output.
- **MCP Tool Testing**: Verifying the integration and execution of MCP servers.
- **Issue Reproduction**: Using the CLI to reproduce user-reported bugs.

## Operational Workflow
1. **Binary Selection**: 
   - Use the global `qwen` command to reproduce bugs (matches user environment).
   - Use `node dist/cli.js` (after `npm run build && npm run bundle`) to verify local fixes.
2. **Execution Mode**:
   - **Headless Mode**: Execute with `--output-format json` and `--approval-mode yolo` for automated, structured output.
   - **Interactive Mode**: Use `tmux` to simulate a real user session, sending keys and capturing pane output for TUI verification.
3. **Traffic Inspection**: Enable `--openai-logging` and specify a logging directory to capture raw request/response JSON payloads for debugging model behavior.
4. **MCP Verification**: Utilize specialized MCP testing templates and servers to validate tool schemas and execution.
5. **Analysis**: Use `scripts/token-stats.py` to analyze token usage and cache hit rates from API logs.

## Output Contract
- **Headless Output**: A stream of JSON objects containing `system` (init), `assistant` (model output), `user` (tool results), and `result` (final output) types.
- **Interactive Output**: Rendered TUI frames captured via `tmux capture-pane`.
- **API Logs**: JSON files containing `request.messages` and `response.choices`.

## Mirror Link
Original configuration: [`config/skills/e2e-testing/SKILL.md`](../../../config/skills/e2e-testing/SKILL.md)
