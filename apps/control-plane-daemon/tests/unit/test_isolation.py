import os

import pytest
from control_plane_daemon.execution_context import ExecutionContext


def test_runtime_context_isolation() -> None:
    """
    Verify that cloning a ExecutionContext creates a new, empty FileReadCache
    to prevent 'Self-Grading' bias between agents.
    """
    # 1. Create root context and populate cache
    root_ctx = ExecutionContext()

    # Create a dummy file to cache
    test_file = "isolation_test.txt"
    with open(test_file, "w") as f:
        f.write("Original Content")

    # Simulate a read and cache it
    root_ctx.file_cache.set(test_file, "Original Content")
    assert root_ctx.file_cache.get(test_file) == "Original Content"

    # 2. Clone the context for a subagent
    sub_ctx = root_ctx.clone()

    # 3. Verify that the sub-agent's cache is EMPTY
    # This is the critical check for Prototype Isolation
    assert sub_ctx.file_cache.get(test_file) is None, "Subagent should NOT inherit the root cache"

    # 4. Verify that updating sub-agent cache doesn't affect root
    sub_ctx.file_cache.set(test_file, "Subagent Content")
    assert sub_ctx.file_cache.get(test_file) == "Subagent Content"
    assert root_ctx.file_cache.get(test_file) == "Original Content"

    # Cleanup
    os.remove(test_file)


def test_config_inheritance() -> None:
    """
    Verify that configuration overrides ARE inherited during cloning,
    as they represent shared project policies.
    """
    root_ctx = ExecutionContext(config_overrides={"project_name": "MegaCode", "strict_mode": True})
    sub_ctx = root_ctx.clone()

    assert sub_ctx.config["project_name"] == "MegaCode"
    assert sub_ctx.config["strict_mode"] is True

    # Verify that modifying sub-config doesn't affect root (deep copy check)
    sub_ctx.config["strict_mode"] = False
    assert root_ctx.config["strict_mode"] is True


if __name__ == "__main__":
    pytest.main([__file__])
