import asyncio
import json
import os
import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Environment Setup
# Force use of the monorepo for testing
LOCAL_STACK = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
STACK_ROOT = LOCAL_STACK

VENV_PYTHON = os.path.join(STACK_ROOT, ".venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "packages/memory/memory_daemon.py")
MCP_COMMAND = [VENV_PYTHON, SERVICE_DAEMON]


async def execute_action(tool_name, arguments):
    """Helper to run a single tool call in a fresh session."""
    env = os.environ.copy()
    env["MCP_TRANSPORT"] = "stdio"
    
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=env
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.call_tool(tool_name, arguments)
            return json.loads(res.content[0].text)


@pytest.mark.asyncio
async def test_minimal_ingest():
    unique_fact = "Minimal test fact"
    print(f"Ingesting: {unique_fact}")
    res = await execute_action("ingest", {"text": unique_fact, "tier": "local"})
    print(f"Result: {res}")
    assert res["status"] == "queued"

if __name__ == "__main__":
    asyncio.run(test_minimal_ingest())
