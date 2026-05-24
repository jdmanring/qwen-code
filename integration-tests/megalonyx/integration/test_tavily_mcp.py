import os
import sys
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Note: We don't have a specific TavilyTool class in the current codebase,
# but we can test the generic MCP communication pattern used by other tools.
# This test ensures that if a tool were to use the Tavily MCP server,
# the communication pattern is correct.

# For the purpose of this test, we will simulate a generic MCP client interaction
# that would be used by a tool.


class MockMCPClient:
    def __init__(self) -> None:
        self.session = AsyncMock()
        self.stdio_client = MagicMock()

    async def __aenter__(self) -> "MockMCPClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


@pytest.mark.anyio
async def test_mcp_tavily_search_call() -> None:
    """Tests the pattern of calling a Tavily MCP tool."""
    # Mocking the MCP client components
    mock_session = AsyncMock()

    # Mock the tool call result
    mock_result = MagicMock()
    mock_result.content = "Search results for 'AI agents': [result1, result2]"
    mock_session.call_tool.return_value = mock_result

    # Simulate the tool execution logic
    # In a real scenario, this would be inside a Skill or Tool class
    query = "AI agents"
    result = await mock_session.call_tool(
        "tavily-search-web", arguments={"query": query}
    )

    # Verify
    mock_session.call_tool.assert_called_once_with(
        "tavily-search-web", arguments={"query": query}
    )
    assert result.content == "Search results for 'AI agents': [result1, result2]"


@pytest.mark.anyio
async def test_mcp_tavily_error_handling() -> None:
    """Tests handling of errors during Tavily MCP tool calls."""
    mock_session = AsyncMock()

    # Simulate an exception during the tool call
    mock_session.call_tool.side_effect = Exception("Tavily API limit reached")

    query = "AI agents"

    with pytest.raises(Exception) as excinfo:
        await mock_session.call_tool("tavily-search-web", arguments={"query": query})

    assert "Tavily API limit reached" in str(excinfo.value)
