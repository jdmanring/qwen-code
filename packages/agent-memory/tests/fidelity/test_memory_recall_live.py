import asyncio

from control_plane_daemon.mcp_manager import MCPManager

DAEMON_CMD = ["uv", "run", "python", "-m", "agent_memory.memory_daemon"]


async def main():
    mgr = MCPManager()

    query = "What is the secret code for the vault?"
    print(f"Searching for: {query}")
    result = await mgr.call_tool("memory", DAEMON_CMD, "search", {"query": query, "tier": "local"})
    print(f"Search result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
