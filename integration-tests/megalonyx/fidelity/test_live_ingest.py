import asyncio
import os

from control_plane_daemon.mcp_manager import MCPManager


async def main():
    mgr = MCPManager()
    cmd = [
        "python3",
        os.path.expanduser("~/.local/share/megalonyx/packages/memory/memory_daemon.py"),
    ]

    # Ingest a unique fact
    fact = "The secret code for the vault is 'BLUE-SQUIRREL-2026'."
    print(f"Ingesting fact: {fact}")
    result = await mgr.call_tool(
        "memory", cmd, "ingest", {"text": fact, "tier": "local"}
    )
    print(f"Ingest result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
