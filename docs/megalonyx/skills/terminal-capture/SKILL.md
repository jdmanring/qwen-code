# Skill: Terminal Capture

## 1. Skill Identity
**Terminal Capture** is an automation skill that generates visual screenshots of CLI terminal interactions. It is used to provide empirical visual verification of TUI (Terminal User Interface) rendering, slash command execution, and general CLI output, bridging the gap between raw text logs and actual user experience.

## 2. Trigger Logic
This skill is triggered by:
- **PR Reviews**: When reviewing changes that modify CLI output or TUI layout.
- **Feature Testing**: Testing specific slash commands such as `/about`, `/context`, `/auth`, or `/export`.
- **Documentation**: Requests to generate visual examples or screenshots for documentation.
- **Keywords**: Mention of 'terminal screenshot', 'CLI test', 'visual test', or 'terminal-capture'.

## 3. Operational Workflow
The skill operates via a TypeScript-based configuration and execution engine:
1. **Scenario Configuration**: The agent creates or modifies a `.ts` file in `integration-tests/terminal-capture/scenarios/`. This file defines the `spawn` command, the `terminal` settings (cols, rows, theme), and the `flow` (a sequence of inputs and key presses).
2. **Execution**: The scenario is run using the `run.ts` entry point:
   `npx tsx integration-tests/terminal-capture/run.ts [scenario-path]`
3. **Interaction Cycle**:
   - **Input**: Sends text to the PTY $\rightarrow$ Captures state $\rightarrow$ Presses Enter $\rightarrow$ Waits for stable output $\rightarrow$ Captures result.
   - **Keys**: Sends specific key sequences (e.g., `ArrowDown`, `Tab`) for menu navigation.
   - **Streaming**: For long-running output, captures multiple frames at set intervals.
4. **Artifact Generation**: Screenshots are saved to `scenarios/screenshots/{name}/`.

## 4. Output Contract
The output consists of a structured directory of images:
- **Step-based Screenshots**: Pairs of images (`01-01.png` for input, `01-02.png` for result) for every interaction step.
- **Full-Flow Image**: A `full-flow.png` capturing the final state of the scrollback buffer.
- **Animated GIF**: (Optional) An animated GIF generated from `streaming` captures using `ffmpeg`.

## 5. Symmetry Link
**Original Configuration**: [`../../../config/skills/terminal-capture/SKILL.md`](../../../config/skills/terminal-capture/SKILL.md)
