import json
import os
import time
from typing import Any, cast


class StateManager:
    """
    Handles the persistence and retrieval of the global system state.
    This acts as the 'Blackboard' for the multi-agent system.
    """

    def __init__(self, state_file: str = ".qwen/state.json") -> None:
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> dict[str, Any]:
        """Loads state from disk or initializes a default state."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file) as f:
                    return cast(dict[str, Any], json.load(f))
            except (OSError, json.JSONDecodeError):
                pass

        return self._get_default_state()

    def _get_default_state(self) -> dict[str, Any]:
        """Defines the initial global state schema."""
        return {
            "active_phase": "PLANNING",
            "todo_list": [],
            "rag_context": {},
            "archive": [],
            "last_agent": None,
            "iteration_count": 0,
            "global_constraints": [],
            "metadata": {"session_start": None, "total_turns": 0},
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from the state."""
        return self.state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Updates a value in the state and persists it to disk."""
        self.state[key] = value
        self.save()

    def delete(self, key: str) -> None:
        """Removes a key from the state and persists it to disk."""
        if key in self.state:
            del self.state[key]
            self.save()

    def update_todo(self, todo_id: str, status: str) -> None:
        """Updates the status of a specific todo item."""
        for item in self.state.get("todo_list", []):
            if item["id"] == todo_id:
                item["status"] = status
                break
        self.save()

    def increment_iteration(self) -> None:
        """Increments the iteration count for the current phase."""
        self.state["iteration_count"] = self.state.get("iteration_count", 0) + 1
        self.save()

    def reset_iteration(self) -> None:
        """Resets the iteration count (usually called when phase changes)."""
        self.state["iteration_count"] = 0
        self.save()

    def archive_item(self, key: str) -> bool:
        """Moves an item from rag_context to the archive."""
        rag_context = self.state.get("rag_context", {})
        if key in rag_context:
            item = {"key": key, "content": rag_context[key], "timestamp": time.time()}
            self.state.setdefault("archive", []).append(item)
            del self.state["rag_context"][key]
            self.save()
            return True
        return False

    def save(self) -> None:
        """Persists the current state to the JSON file."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=4)
        except OSError:
            pass


if __name__ == "__main__":
    from agent_infra.system_logger import SystemLogger

    sm = StateManager()
    logger = SystemLogger()
    logger.info("state_manager_test", {"active_phase": sm.get("active_phase")})
    sm.set("active_phase", "IMPLEMENTATION")
    logger.info("state_manager_updated", {"active_phase": sm.get("active_phase")})
