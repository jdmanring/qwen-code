# Tmux Real-User Logging Utility Documentation

## Purpose
This file is a reference for `tmux-real-user-log.sh`, a bash helper script designed to automate the recording of interactive user sessions in `tmux` for testing and debugging purposes.

## Logic & Structure
The script provides a set of commands to control a `tmux` session and capture its state:
- **`start`**: Launches a new detached `tmux` session with a specific command and sets up an output directory for logs.
- **`snapshot`**: Captures the current pane content (including scrollback) and appends it to a readable log file with a label.
- **`send` / `type-submit`**: Programmatically sends keystrokes or text+Enter to the `tmux` session to simulate user interaction.
- **`wait-for`**: Polls the `tmux` pane until a specific regex pattern appears in the output, facilitating automated E2E tests.
- **`finish`**: Performs a final full-pane capture and kills the session.

## Usage
- **E2E Testing**: Use this script to create "headless but interactive" tests where the agent can simulate a user in a real terminal and verify the output.
- **Bug Reproduction**: Record the exact sequence of keys and resulting output in a `tmux` session to provide a high-fidelity reproduction log.

## Original File
[config/skills/tmux-real-user-testing/scripts/tmux-real-user-log.sh](../../config/skills/tmux-real-user-testing/scripts/tmux-real-user-log.sh)
