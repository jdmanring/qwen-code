# Skill: tmux Real User Testing

## 1. Skill Identity
**tmux Real User Testing** is a TUI-centric testing protocol that simulates real human interaction with the Qwen Code interface. Unlike headless tests, it uses a live `tmux` session to navigate dialogs and trigger commands, producing a "narrative artifact" (a readable log of screen snapshots) that allows maintainers to visually audit the user journey.

## 2. Trigger Logic
This skill is triggered by:
- **TUI Verification**: Requests to "test like a real user," "test slash command interactions," or "verify TUI rendering."
- **Narrative Reporting**: Requests for "readable logs," "TUI test reports," or "step-by-step snapshots."
- **Specific Phrases**: " tmux ", " tmux ", " TUI ".
- **Complex Flows**: Testing authentication, onboarding, or interactive error recovery where final state alone is insufficient.

## 3. Operational Workflow
The skill implements a "Capture-Pane" harness:
1. **Environment Setup**: Launches a `tmux` session with a large viewport (e.g., 200x50) and starts the application (e.g., `npm run dev`).
2. **Readiness Polling**: Instead of blind sleeping, the agent polls the pane for a known startup string to ensure the TUI is fully rendered.
3. **Interaction & Snapshotting**:
   - **Action**: Sends realistic keyboard sequences (`send-keys`) for typing and navigation (Arrow keys, Space, Enter).
   - **Capture**: After every meaningful state change, it executes `tmux capture-pane -p` to append a rendered frame of the screen to the log.
4. **Completion Polling**: Polls the screen for success or error strings (e.g., "Successfully configured") to determine when the flow has ended.
5. **Artifact Finalization**: Captures a final full-screen snapshot and generates a `report.md` summary.

## 4. Output Contract
The output is a timestamped directory in `tmp/<scenario>-tmux-YYYYMMDD-HHMMSS/` containing:
- **`tmux-readable-full.log`**: The primary artifact. A sequential log of labeled screen snapshots showing the entire journey.
- **`tmux-final-capture.log`**: A snapshot of the final screen state.
- **`current-pane.txt`**: A scratch file containing the last polled state.
- **`report.md`**: A summary including the scenario scope, PASS/FAIL result, and pointers to the logs.

## 5. Mirror Link
**Original Configuration**: [`../../../config/skills/tmux-real-user-testing/SKILL.md`](../../../config/skills/tmux-real-user-testing/SKILL.md)
