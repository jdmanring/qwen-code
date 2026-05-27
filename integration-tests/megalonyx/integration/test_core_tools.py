import os
import pytest
from unittest.mock import patch, AsyncMock
from control_plane_daemon.models import ToolResponse

@pytest.mark.asyncio
async def test_write_then_read_cycle(sandbox_project):
    """
    Integration Test: Verify that a file written by a tool can be read back.
    This tests the interaction between the Tool Layer and the Filesystem.
    """
    test_file = os.path.join(sandbox_project, "integration_test.txt")
    test_content = "Hello from the Integration Framework!"

    from control_plane_daemon.tool_executor import registry, execute_tool

    # Mock the handler
    mock_handler = AsyncMock()
    
    async def mock_execute(tool_name, args, context, policy, search_tool, state_manager):
        if tool_name == "write_file":
            f_path = args.get("file_path")
            f_content = args.get("content")
            os.makedirs(os.path.dirname(f_path), exist_ok=True)
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(f_content)
            return ToolResponse(success=True, content=f"Successfully wrote to {f_path}")
        elif tool_name == "read_file":
            f_path = args.get("file_path")
            with open(f_path, "r", encoding="utf-8") as f:
                content = f.read()
            return ToolResponse(success=True, content=content)
        return ToolResponse(success=False, content=None, error="Unknown tool")

    mock_handler.execute.side_effect = mock_execute

    with patch.object(registry, "get_handler", return_value=mock_handler):
        # 2. Execute 'write_file'
        result = await execute_tool(
            "write_file",
            {"file_path": test_file, "content": test_content},
            None,
        )

        assert "Successfully wrote" in result
        assert os.path.exists(test_file)

        # 3. Execute 'read_file'
        read_result = await execute_tool("read_file", {"file_path": test_file}, None)

        assert read_result == test_content


@pytest.mark.asyncio
async def test_read_non_existent_file(sandbox_project):
    """
    Integration Test: Verify that reading a non-existent file returns a proper error.
    """
    from control_plane_daemon.tool_executor import registry, execute_tool

    mock_handler = AsyncMock()
    mock_handler.execute.return_value = ToolResponse(success=False, content=None, error="File not found")

    with patch.object(registry, "get_handler", return_value=mock_handler):
        result = await execute_tool(
            "read_file",
            {"file_path": os.path.join(sandbox_project, "ghost.txt")},
            None,
        )

        assert "error" in result
        assert "File not found" in result["error"]
