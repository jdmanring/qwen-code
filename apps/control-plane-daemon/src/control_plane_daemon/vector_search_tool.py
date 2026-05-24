import asyncio
import json
import os
from typing import Any, cast

import requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"

# MCP Server Configuration
MCP_SERVER_PARAMS = StdioServerParameters(
    command=os.getenv(
        "QDRANT_MCP_PYTHON",
        os.path.expanduser("~/.local/share/megalonyx/venvs/mcp-server-qdrant/bin/python"),
    ),
    args=["-m", "qdrant_mcp.server"],
    env=None,
)


class VectorSearchTool:
    def __init__(self) -> None:
        # Ensure an event loop exists for the synchronous wrapper
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def get_embedding(self, text: str) -> list[float] | None:
        """Fetches embedding from Ollama."""
        try:
            response = requests.post(OLLAMA_URL, json={"model": EMBEDDING_MODEL, "prompt": text})
            response.raise_for_status()
            return cast(list[float], response.json()["embedding"])
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Embedding Error: {e}")
            return None

    async def _async_semantic_search(self, query: str, limit: int = 5) -> Any:
        """Internal async method to handle MCP communication with a strict deadline."""
        try:
            # Implement the 'Recall Race' pattern: 2.5s deadline to prevent UI latency
            return await asyncio.wait_for(self._perform_mcp_search(query, limit), timeout=2.5)
        except TimeoutError:
            return {
                "error": (
                    "Recall Race Timeout: Semantic search exceeded 2.5s deadline. "
                    "Returning partial/empty results to maintain latency."
                )
            }
        except (OSError, RuntimeError) as e:
            return {"error": f"MCP Semantic search failed: {str(e)}"}

    async def _perform_mcp_search(self, query: str, limit: int) -> Any:
        """The actual MCP communication logic."""
        async with stdio_client(MCP_SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Call the specialized MCP tool
                result = await session.call_tool(
                    "mega-db-find-memories", arguments={"query": query}
                )

                # The MCP server returns a list of content blocks
                if hasattr(result, "content"):
                    return result.content
                return result

    def semantic_search(self, query: str, limit: int = 5) -> Any:
        """
        Performs a semantic search via the MCP Server.
        Returns a list of relevant code chunks.
        """
        # Run the async MCP call in the current event loop
        try:
            return self.loop.run_until_complete(self._async_semantic_search(query, limit))
        except RuntimeError as e:
            return {"error": f"VectorSearchTool execution failed: {str(e)}"}


if __name__ == "__main__":
    # Simple test
    tool = VectorSearchTool()
    query = "How is the state managed in the orchestrator?"
    print(f"Searching for: {query}")
    results = tool.semantic_search(query)
    print(f"Results: {results}")
