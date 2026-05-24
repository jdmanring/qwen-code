import os

import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


@pytest.mark.asyncio
async def test_write_then_read_cycle(sandbox_project, memory_server):
    """
    Integration Test: Verify that a file written by a tool can be read back.
    This tests the interaction between the Tool Layer and the Filesystem.
    """
    # 1. Setup: Create a test file in the sandbox
    test_file = os.path.join(sandbox_project, "integration_test.txt")
    test_content = "Hello from the Integration Framework!"

    # We simulate the tool call by calling the logic directly or via MCP.
    # Since we are testing the INTEGRATION, we use the MCP session.

    server_params = StdioServerParameters(
        command=memory_server[0], args=memory_server[1:], env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. Execute 'write_file'
            # Note: In the Blueprint, write_file is a built-in tool.
            # Here we test if the tool logic (which we'll eventually move to a package) works.
            # For now, we'll use the actual tool implementation if available.

            # Since write_file is a core tool, we test it via the MCP interface
            # if the server supports it, or by calling the internal function.

            # Let's use the internal function for a "unit-integration" hybrid
            # until the MCP server is fully updated to expose all core tools.
            from control_plane_daemon.tool_executor import execute_tool

            # We need a mock rag_tool for execute_tool
            class MockRag:
                def semantic_search(self, q, limit):
                    return []

            result = execute_tool(
                "write_file",
                {"file_path": test_file, "content": test_content},
                MockRag(),
            )

            assert "Successfully wrote" in result
            assert os.path.exists(test_file)

            # 3. Execute 'read_file'
            read_result = execute_tool("read_file", {"file_path": test_file}, MockRag())

            assert read_result == test_content


@pytest.mark.asyncio
async def test_read_non_existent_file(sandbox_project):
    """
    Integration Test: Verify that reading a non-existent file returns a proper error.
    """
    from control_plane_daemon.tool_executor import execute_tool

    class MockRag:
        def semantic_search(self, q, limit):
            return []

    result = execute_tool(
        "read_file",
        {"file_path": os.path.join(sandbox_project, "ghost.txt")},
        MockRag(),
    )

    assert "error" in result
    assert "File not found" in result["error"]
