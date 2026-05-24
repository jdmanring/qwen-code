import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Detect if we are running in the installed stack or the development directory
STACK_ROOT = os.environ.get(
    "QWEN_STACK_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
)
VENV_PYTHON = os.path.join(STACK_ROOT, "py/venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "services/memory_daemon.py")

# The command to launch our local MCP server for testing
MCP_COMMAND = [VENV_PYTHON, SERVICE_DAEMON]


async def test_cloud_rag():
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0],
        args=MCP_COMMAND[1:],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            test_text = "Cloud memory testing text: The dragon flies over the mountain."
            print(f"[Test] Ingesting to cloud: '{test_text}'")

            # 1. Ingest to cloud
            ingest_result = await session.call_tool(
                "ingest", arguments={"text": test_text, "tier": "cloud"}
            )
            print(f"[Test] Ingest Response: {ingest_result}")

            # 2. Wait for background ingestion
            print("[Test] Waiting 5 seconds for background ingestion...")
            await asyncio.sleep(5)

            # 3. Search from cloud
            print("[Test] Searching from cloud with query: 'dragon'")
            search_result = await session.call_tool(
                "search", arguments={"query": "dragon", "tier": "cloud"}
            )
            print(f"[Test] Search Response: {search_result}")

            # 4. Verification
            import json

            try:
                content = search_result.content[0].text
                data = json.loads(content)

                cloud_results = data.get("cloud", [])
                print(f"[Test] Found {len(cloud_results)} results in cloud tier.")

                if len(cloud_results) > 0:
                    # Check if any result contains our text
                    found = any(
                        test_text in r["payload"]["text"] for r in cloud_results
                    )
                    if found:
                        print("[Test] SUCCESS: Cloud RAG is working!")
                    else:
                        print(
                            "[Test] FAILURE: Cloud RAG returned results, but none match the test text."
                        )
                        sys.exit(1)
                else:
                    print("[Test] FAILURE: Cloud RAG returned no results.")
                    sys.exit(1)

            except (json.JSONDecodeError, IndexError, AttributeError) as e:
                print(f"[Test] Error during verification: {e}")
                print(f"Raw search result: {search_result}")
                sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_cloud_rag())
