from unittest.mock import MagicMock, patch

import pytest
from agent_memory.memory_daemon import MemoryDaemon


def test_dreaming_deduplication() -> None:
    """
    Verify that the Dreaming pipeline removes redundant memories based on content.
    """
    core = MemoryDaemon()

    # Mock the Qdrant client
    mock_client = MagicMock()

    # Simulate 3 points: 2 are identical, 1 is unique
    mock_points = [
        MagicMock(id="1", payload={"text": "Unique memory A"}),
        MagicMock(id="2", payload={"text": "Duplicate memory B"}),
        MagicMock(id="3", payload={"text": "Duplicate memory B"}),
    ]

    # Mock scroll to return these points
    mock_client.scroll.return_value = (mock_points, None)

    # Patch the local_qdrant and cloud_qdrant in memory_daemon
    with (
        patch("agent_memory.memory_daemon.local_qdrant", mock_client),
        patch("agent_memory.memory_daemon.cloud_qdrant", mock_client),
    ):
        core.dream()

        # Verify that delete was called for the duplicate (id "3")
        # Note: The first seen hash is kept, the second is deleted.
        mock_client.delete.assert_called()
        args, kwargs = mock_client.delete.call_args
        assert "3" in kwargs["points_selector"] or "3" in args[1]


def test_dreaming_empty_collection() -> None:
    """Verify that dreaming handles empty collections gracefully."""
    core = MemoryDaemon()
    mock_client = MagicMock()
    mock_client.scroll.return_value = ([], None)

    with (
        patch("agent_memory.memory_daemon.local_qdrant", mock_client),
        patch("agent_memory.memory_daemon.cloud_qdrant", mock_client),
    ):
        core.dream()
        mock_client.delete.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__])
