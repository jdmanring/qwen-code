import asyncio
import json
import os

import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Import the simulation logic
from sim_agent import SimAgent

# Environment Setup
if os.environ.get("QWEN_STACK_ROOT"):
    STACK_ROOT = os.environ.get("QWEN_STACK_ROOT")
else:
    INSTALLED_STACK = os.path.expanduser("~/.local/share/megalonyx")
    LOCAL_STACK = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    STACK_ROOT = (
        INSTALLED_STACK
        if os.path.exists(os.path.join(INSTALLED_STACK, "py/venv"))
        else LOCAL_STACK
    )

VENV_PYTHON = os.path.join(STACK_ROOT, "py/venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "packages/memory/memory_daemon.py")

MCP_COMMAND = [VENV_PYTHON, SERVICE_DAEMON]


@pytest.mark.asyncio
async def test_proactive_ingestion():
    """
    Verify that the agent correctly identifies a 'remember' prompt
    and calls the ingest tool with the right tier.
    """
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = SimAgent(session)

            # Prompt for Cloud tier
            prompt = "Remember that the project architecture uses a 4-layer model."
            res = await agent.handle_prompt(prompt)

            data = json.loads(res.content[0].text)
            assert data["status"] == "queued"
            assert data["tier"] == "cloud"

            # Prompt for Local tier
            prompt_local = "Remember that I prefer using async/await."
            res_local = await agent.handle_prompt(prompt_local)

            data_local = json.loads(res_local.content[0].text)
            assert data_local["status"] == "queued"
            assert data_local["tier"] == "local"


@pytest.mark.asyncio
async def test_contextual_recall():
    """
    Verify that the agent correctly identifies a 'recall' prompt
    and retrieves the previously stored fact.
    """
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = SimAgent(session)

            # 1. Ingest fact
            fact = "The secret project code is 'BLUE-SQUIRREL'."
            await agent.handle_prompt(f"Remember that {fact}")
            await asyncio.sleep(2)

            # 2. Recall fact
            res = await agent.handle_prompt("What is the secret project code?")
            await asyncio.sleep(1)
            data = json.loads(res.content[0].text)

            assert len(data) > 0
            assert any("BLUE-SQUIRREL" in r["payload"]["text"] for r in data)


if __name__ == "__main__":

    async def main():
        print("Running Agentic Usage Tests...")
        try:
            await test_proactive_ingestion()
            print("[OK] Proactive ingestion verified.")
            await test_contextual_recall()
            print("[OK] Contextual recall verified.")
            print("\nALL AGENTIC TESTS PASSED!")
        except (
            AssertionError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            OSError,
        ) as e:
            print(f"\n[FAIL] Tests failed: {e}")
            import sys

            sys.exit(1)

    asyncio.run(main())
