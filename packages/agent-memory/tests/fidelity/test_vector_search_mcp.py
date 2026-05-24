import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Derive repo root from script location for portability
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))

MCP_COMMAND = ["uv", "run", "--project", REPO_ROOT, "python", "-m", "agent_memory.memory_daemon"]


async def test_cloud_rag():
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0],
        args=MCP_COMMAND[1:],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            test_text = "Cloud memory testing text: The dragon flies over the mountain."
            print(f"[Test] Ingesting to cloud: '{test_text}'")

            ingest_result = await session.call_tool(
                "ingest", arguments={"text": test_text, "tier": "cloud"}
            )
            print(f"[Test] Ingest Response: {ingest_result}")

            print("[Test] Waiting 5 seconds for background ingestion...")
            await asyncio.sleep(5)

            print("[Test] Searching from cloud with query: 'dragon'")
            search_result = await session.call_tool(
                "search", arguments={"query": "dragon", "tier": "cloud"}
            )
            print(f"[Test] Search Response: {search_result}")

            import json

            try:
                content = search_result.content[0].text
                data = json.loads(content)

                cloud_results = data.get("cloud", [])
                print(f"[Test] Found {len(cloud_results)} results in cloud tier.")

                if len(cloud_results) > 0:
                    found = any(test_text in r["payload"]["text"] for r in cloud_results)
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
