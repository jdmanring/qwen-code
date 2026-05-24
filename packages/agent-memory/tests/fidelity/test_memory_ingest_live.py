import asyncio

from control_plane_daemon.mcp_manager import MCPManager

DAEMON_CMD = ["uv", "run", "python", "-m", "agent_memory.memory_daemon"]


async def main():
    mgr = MCPManager()

    fact = "The secret code for the vault is 'BLUE-SQUIRREL-2026'."
    print(f"Ingesting fact: {fact}")
    result = await mgr.call_tool("memory", DAEMON_CMD, "ingest", {"text": fact, "tier": "local"})
    print(f"Ingest result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
