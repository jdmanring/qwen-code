import json
import os
from datetime import UTC, datetime
from typing import Any, cast

from rich.console import Console
from rich.theme import Theme


class SystemLogger:
    """
    Provides structured JSON logging for the entire agent stack.
    Logs are stored in a JSONL format for easy parsing and post-mortem analysis.
    Integrates with ~/.qwen/settings.json for dynamic level filtering and path management.
    Also provides color-coded, human-readable terminal output via `rich`.
    """

    LEVEL_MAP = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40, "CRITICAL": 50}

    # Define a custom theme for the terminal output
    THEME = Theme(
        {
            "log.debug": "dim cyan",
            "log.info": "green",
            "log.warn": "yellow",
            "log.error": "bold red",
            "log.critical": "bold red underline",
            "log.event": "bold magenta",
        }
    )

    def __init__(self, log_file: str | None = None) -> None:
        self.console = Console(theme=self.THEME)
        self.settings = self._load_settings()

        # Priority: 1. Constructor arg, 2. settings.json, 3. Default fallback (Persistent Log Dir)
        if log_file:
            self.log_file = log_file
        else:
            default_log = os.path.join(os.path.expanduser("~/.qwen/logs"), "qwen_system.log")
            self.log_file = self.settings.get("logging", {}).get("log_path", default_log)

        # Ensure absolute path
        if not os.path.isabs(self.log_file):
            self.log_file = os.path.expanduser(self.log_file)

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.current_level = self.settings.get("logging", {}).get("log_level", "INFO").upper()
        self.enable_trace = self.settings.get("logging", {}).get("enable_trace", False)

    def _load_settings(self) -> dict[str, Any]:
        """Loads settings from the machine's config directory."""
        settings_path = os.path.expanduser("~/.qwen/settings.json")
        try:
            if os.path.exists(settings_path):
                with open(settings_path, encoding="utf-8") as f:
                    return cast(dict[str, Any], json.load(f))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"WARNING: Failed to load settings for logger: {e}")
        return {}

    def log(self, event_type: str, data: dict[str, Any], level: str = "INFO") -> None:
        """Logs a structured event if the level meets the configured threshold."""
        level = level.upper()
        config_level = self.current_level if self.current_level in self.LEVEL_MAP else "INFO"

        if self.LEVEL_MAP.get(level, 20) < self.LEVEL_MAP.get(config_level, 20):
            return

        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": level,
            "event": event_type,
            "data": data,
        }

        # 1. Write to JSONL log file (for machine parsing)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\\n")
        except OSError as e:
            print(f"CRITICAL: Failed to write to system log: {e}")

        # 2. Print to terminal (for human readability)
        self._print_to_terminal(entry)

    def _print_to_terminal(self, entry: dict[str, Any]) -> None:
        """Prints a color-coded, human-readable version of the log entry."""
        level = entry["level"]
        event = entry["event"]
        data = entry["data"]
        timestamp = entry["timestamp"]

        # Map level to theme color
        theme_color = f"log.{level.lower()}"
        if level not in self.LEVEL_MAP:
            theme_color = "white"

        # Build the message
        # Format: [TIMESTAMP] [LEVEL] [EVENT] | DATA
        msg = f"[{timestamp}] [{level}] [{event}] | {data}"

        # For very large data dicts, we'll just print the keys to keep the terminal clean
        if len(str(data)) > 200:
            msg = f"[{timestamp}] [{level}] [{event}] | Keys: {list(data.keys())}"

        self.console.print(f"[{theme_color}]{msg}[/{theme_color}]")

    def trace(self, category: str, raw_data: Any) -> None:
        """
        Writes high-verbosity raw data to a transient trace log in ~/.qwen/tmp/.
        This is used for debugging raw MCP I/O and LLM prompts.
        """
        if not self.enable_trace:
            return

        # Trace files are timestamped per session to prevent massive file growth
        # We use a daily rotation for trace logs
        date_str = datetime.now().strftime("%Y-%m-%d")
        trace_dir = os.path.expanduser("~/.qwen/tmp")
        os.makedirs(trace_dir, exist_ok=True)

        trace_file = os.path.join(trace_dir, f"trace_{date_str}.log")

        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "category": category,
            "payload": raw_data,
        }

        try:
            with open(trace_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\\n")
        except OSError as e:
            print(f"WARNING: Failed to write to trace log: {e}")

    def debug(self, event: str, data: dict[str, Any]) -> None:
        self.log(event, data, "DEBUG")

    def info(self, event: str, data: dict[str, Any]) -> None:
        self.log(event, data, "INFO")

    def warn(self, event: str, data: dict[str, Any]) -> None:
        self.log(event, data, "WARN")

    def error(self, event: str, data: dict[str, Any]) -> None:
        self.log(event, data, "ERROR")

    def critical(self, event: str, data: dict[str, Any]) -> None:
        self.log(event, data, "CRITICAL")

    def exception(self, event: str, data: dict[str, Any]) -> None:
        """Logs an error along with the current exception context."""
        import traceback

        data["traceback"] = traceback.format_exc()
        self.log(event, data, "ERROR")


if __name__ == "__main__":
    # Simple test
    logger = SystemLogger()
    logger.debug("debug_test", {"message": "This should only appear in DEBUG mode"})
    logger.info("test_event", {"message": "Hello World", "status": "ok"})
    logger.trace("mcp_io", {"request": "initialize", "response": "success"})
    print(f"Log written to {logger.log_file} with level {logger.current_level}")
