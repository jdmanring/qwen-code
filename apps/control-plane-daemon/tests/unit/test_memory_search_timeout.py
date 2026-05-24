import asyncio
import time
from unittest.mock import patch

import pytest
from control_plane_daemon.vector_search_tool import VectorSearchTool


@pytest.mark.asyncio
async def test_recall_race_timeout():
    """
    Verify that the VectorSearchTool enforces the 2.5s deadline.
    """
    rag = VectorSearchTool()

    # Mock the _perform_mcp_search to simulate a slow response (3 seconds)
    async def slow_search(query, limit):
        await asyncio.sleep(3.0)
        return "This should not be returned"

    with patch.object(VectorSearchTool, "_perform_mcp_search", side_effect=slow_search):
        start_time = time.time()
        result = await rag._async_semantic_search("Any query", limit=5)
        duration = time.time() - start_time

        # Verify that it timed out around 2.5s, not 3.0s
        assert duration < 3.0
        assert duration >= 2.4
        assert "Recall Race Timeout" in result["error"]


@pytest.mark.asyncio
async def test_recall_race_success():
    """Verify that fast responses are returned normally."""
    rag = VectorSearchTool()

    async def fast_search(query, limit):
        await asyncio.sleep(0.1)
        return "Fast result"

    with patch.object(VectorSearchTool, "_perform_mcp_search", side_effect=fast_search):
        result = await rag._async_semantic_search("Any query", limit=5)
        assert result == "Fast result"


if __name__ == "__main__":
    asyncio.run(pytest.main([__file__]))
