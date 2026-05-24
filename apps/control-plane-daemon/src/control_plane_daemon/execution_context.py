import copy
import os
from typing import Any, cast


class FileReadCache:
    """
    A cache for file contents to reduce I/O and token usage.
    Includes mtime validation to ensure cache coherence.
    """

    def __init__(self) -> None:
        self._cache: dict[str, dict[str, Any]] = {}

    def get(self, path: str) -> str | None:
        """Retrieves content if it exists and is still valid."""
        if path not in self._cache:
            return None

        entry = self._cache[path]
        try:
            current_mtime = os.path.getmtime(path)
            if current_mtime == entry["mtime"]:
                return cast(str, entry["content"])
        except OSError:
            return None

        return None

    def set(self, path: str, content: str) -> None:
        """Caches content with the current modification time."""
        try:
            mtime = os.path.getmtime(path)
            self._cache[path] = {"content": content, "mtime": mtime}
        except OSError:
            pass

    def clear(self) -> None:
        """Clears the entire cache."""
        self._cache.clear()


class ExecutionContext:
    """
    A container for ephemeral state that can be delegated to subagents.
    Implements the Prototype pattern to ensure strict isolation.
    """

    def __init__(self, config_overrides: dict[str, Any] | None = None) -> None:
        self.file_cache = FileReadCache()
        self.config = config_overrides or {}

    def clone(self) -> "ExecutionContext":
        """
        Creates a shallow copy of the context.
        Crucially, the file_cache is NOT copied to ensure subagents
        start with a clean slate (Prototype Isolation).
        """
        new_ctx = ExecutionContext(config_overrides=copy.deepcopy(self.config))
        # Subagents must perform their own reads to verify the actual state of the disk.
        return new_ctx

    def __repr__(self) -> str:
        return (
            f"ExecutionContext(cache_size={len(self.file_cache._cache)}, "
            f"config_keys={list(self.config.keys())})"
        )
