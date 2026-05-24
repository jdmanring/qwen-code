import pytest
from control_plane_daemon.tool_executor import strip_orphaned_user_entries


def test_strip_orphaned_user_entries_basic() -> None:
    """Verify that simple failure notifications followed by logs are removed."""
    history = [
        {"role": "assistant", "content": "I have implemented the fix."},
        {"role": "user", "content": "No, you failed. Please fix it."},
        {
            "role": "user",
            "content": "VERIFICATION FAILURE LOGS: Traceback... line 42: IndexError",
        },
    ]

    cleaned = strip_orphaned_user_entries(history)

    # Should remove the "No, you failed" entry but keep the logs
    assert len(cleaned) == 2
    assert cleaned[0]["role"] == "assistant"
    assert "VERIFICATION FAILURE LOGS" in cleaned[1]["content"]


def test_strip_orphaned_user_entries_no_orphans() -> None:
    """Verify that normal conversation is not stripped."""
    history = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "Can you help me with this file?"},
    ]

    cleaned = strip_orphaned_user_entries(history)
    assert len(cleaned) == 3
    assert cleaned == history


def test_strip_orphaned_user_entries_multiple_orphans() -> None:
    """Verify that multiple orphaned entries are handled."""
    history = [
        {"role": "assistant", "content": "Attempt 1"},
        {"role": "user", "content": "Incorrect. Fix it."},
        {"role": "user", "content": "VERIFICATION FAILURE LOGS: Error A"},
        {"role": "assistant", "content": "Attempt 2"},
        {"role": "user", "content": "Still not correct."},
        {"role": "user", "content": "VERIFICATION FAILURE LOGS: Error B"},
    ]

    cleaned = strip_orphaned_user_entries(history)

    # Should remove both "Incorrect. Fix it." and "Still not correct."
    assert len(cleaned) == 4
    assert "VERIFICATION FAILURE LOGS: Error A" in cleaned[1]["content"]
    assert "VERIFICATION FAILURE LOGS: Error B" in cleaned[3]["content"]


def test_strip_orphaned_user_entries_empty() -> None:
    """Verify handling of empty history."""
    assert strip_orphaned_user_entries([]) == []
    assert strip_orphaned_user_entries(None) == []


if __name__ == "__main__":
    pytest.main([__file__])
