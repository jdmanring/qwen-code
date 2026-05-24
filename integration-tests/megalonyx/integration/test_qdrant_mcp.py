import json
import os
import subprocess

# Add project root to path
import sys
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from docs.skills.rag_tool import VectorSearchTool

# --- Test 1: qwencode.sh injection logic ---


def test_qwencode_rag_injection_logic(tmp_path):
    """Tests the python logic used in qwencode.sh to inject MCP configuration."""
    # Setup dummy settings.json
    settings_file = tmp_path / "settings.json"
    initial_settings = {"mcpServers": {}}
    settings_file.write_text(json.dumps(initial_settings))

    # The exact python logic used in qwencode.sh
    # We use a generic path to ensure it's location-agnostic
    mock_python_path = "/usr/bin/python3"
    python_logic = f"""
import json
import os
d = json.load(open('{settings_file}'))
d.setdefault('mcpServers', {{}})['mega-db'] = {{
    'command': '{mock_python_path}',
    'args': ['-m', 'qdrant_mcp.server', '--qdrant-url', 'http://localhost:6333',
             '--embedding-provider', 'sentence-transformers', '--embedding-model', 'all-MiniLM-L6-v2']
}}
open('{settings_file}', 'w').write(json.dumps(d, indent=2) + '\\n')
"""
    # Run the logic
    subprocess.run(["python3", "-c", python_logic], check=True)

    # Verify
    with open(settings_file) as f:
        updated_settings = json.load(f)

    assert "mega-db" in updated_settings["mcpServers"]
    qdrant_config = updated_settings["mcpServers"]["mega-db"]
    assert qdrant_config["command"] == mock_python_path
    assert "-m" in qdrant_config["args"]
    assert "qdrant_mcp.server" in qdrant_config["args"]
    assert "--embedding-provider" in qdrant_config["args"]
    assert "sentence-transformers" in qdrant_config["args"]
    assert "--embedding-model" in qdrant_config["args"]
    assert "all-MiniLM-L6-v2" in qdrant_config["args"]


# --- Test 2: rag_tool.py MCP communication ---


def test_rag_tool_mcp_call():
    """Tests that VectorSearchTool correctly calls the MCP server via stdio."""
    # Mocking the MCP client components
    with (
        patch("docs.skills.rag_tool.stdio_client") as mock_stdio,
        patch("docs.skills.rag_tool.ClientSession") as mock_session,
    ):
        # Setup mock session
        mock_session_instance = AsyncMock()
        # Mock the async context manager behavior
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        # Mock the stdio_client context manager behavior
        mock_stdio.return_value.__aenter__.return_value = (MagicMock(), MagicMock())

        # Mock the tool call result
        mock_result = MagicMock()
        mock_result.content = "Found some relevant code chunks."
        mock_session_instance.call_tool.return_value = mock_result

        rag = VectorSearchTool()
        # Use the synchronous wrapper which handles the event loop
        result = rag.semantic_search("test query")

        # Verify
        mock_session_instance.initialize.assert_called_once()
        mock_session_instance.call_tool.assert_called_once_with(
            "mega-db-find-memories", arguments={"query": "test query"}
        )
        assert result == "Found some relevant code chunks."


def test_rag_tool_error_handling():
    """Tests that VectorSearchTool handles MCP communication errors gracefully."""
    with (
        patch("docs.skills.rag_tool.stdio_client") as mock_stdio,
        patch("docs.skills.rag_tool.ClientSession") as mock_session,
    ):
        mock_session_instance = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        mock_stdio.return_value.__aenter__.return_value = (MagicMock(), MagicMock())

        # Simulate an exception during the tool call
        mock_session_instance.call_tool.side_effect = Exception("Connection failed")

        rag = VectorSearchTool()
        result = rag.semantic_search("test query")

        assert "error" in result
        assert "MCP Semantic search failed: Connection failed" in result["error"]
