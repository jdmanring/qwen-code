import asyncio
import os

from control_plane_daemon.mcp_manager import MCPManager


async def main():
    mgr = MCPManager()
    cmd = [
        "python3",
        os.path.expanduser("~/.local/share/megalonyx/packages/memory/memory_daemon.py"),
    ]

    # Search for the secret code
    query = "What is the secret code for the vault?"
    print(f"Searching for: {query}")
    result = await mgr.call_tool(
        "memory", cmd, "search", {"query": query, "tier": "local"}
    )
    print(f"Search result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
