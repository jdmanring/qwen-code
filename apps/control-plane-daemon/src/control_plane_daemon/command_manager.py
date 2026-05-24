import os
from pathlib import Path
from typing import Any

import yaml


class CommandManager:
    def __init__(self, commands_dir: str | None = None) -> None:
        if commands_dir is None:
            # 1. Check for project-local commands directory
            project_root = os.path.abspath(
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    "..",
                )
            )
            local_commands_dir = os.path.join(project_root, "config", "commands")

            if os.path.exists(local_commands_dir):
                commands_dir = local_commands_dir
            else:
                # 2. Fallback to default user commands directory
                commands_dir = os.path.expanduser("~/.qwen/commands")

        self.commands_dir = commands_dir
        self.commands: dict[str, dict[str, Any]] = {}
        self.load_commands()

    def load_commands(self) -> None:
        """Loads all command workflows from the commands directory."""
        # Search for all .md files recursively in the commands directory
        command_files = list(Path(self.commands_dir).rglob("*.md"))
        for file_path in command_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            # Parse YAML frontmatter
                            meta = yaml.safe_load(parts[1])
                            workflow_body = parts[2].strip()

                            if meta and "description" in meta:
                                # Use the filename (without extension) as the command ID
                                # e.g., bugfix.md -> bugfix
                                cmd_id = file_path.stem
                                self.commands[cmd_id] = {
                                    "name": cmd_id,
                                    "description": meta["description"],
                                    "workflow": workflow_body,
                                    "path": str(file_path),
                                }
            except (OSError, UnicodeDecodeError, yaml.YAMLError):
                pass

    def get_command(self, cmd_id: str) -> dict[str, Any] | None:
        """Returns the workflow for a given command ID."""
        return self.commands.get(cmd_id)

    def list_commands(self) -> list[str]:
        """Returns a list of all registered commands."""
        return list(self.commands.keys())


if __name__ == "__main__":
    import sys

    # For debugging: allow overriding the commands directory
    cmd_dir = None
    if len(sys.argv) > 1:
        cmd_dir = sys.argv[1]

    manager = CommandManager(commands_dir=cmd_dir)
    print(f"Loaded commands: {manager.list_commands()}")
    for cmd in manager.list_commands():
        cmd_info = manager.get_command(cmd)
        if cmd_info:
            print(f"\nCommand: {cmd}")
            print(f"Description: {cmd_info['description']}")
        # print(f"Workflow: {manager.get_command(cmd)['workflow'][:100]}...")
