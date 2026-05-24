import asyncio

from control_plane_daemon.mcp_manager import MCPManager

DAEMON_CMD = ["uv", "run", "python", "-m", "agent_memory.memory_daemon"]


async def main():
    mgr = MCPManager()

    # 1. Test Deduplication
    fact = "This is a duplicate fact that should only be stored once."
    print(f"Ingesting duplicate fact 3 times: {fact}")
    for _ in range(3):
        await mgr.call_tool("memory", DAEMON_CMD, "ingest", {"text": fact, "tier": "local"})

    # 2. Test Noise Filtering
    noise = "Ok, thanks!"
    print(f"Ingesting noise: {noise}")
    await mgr.call_tool("memory", DAEMON_CMD, "ingest", {"text": noise, "tier": "local"})

    # 3. Verify results
    print("\nSearching for duplicate fact...")
    dup_res = await mgr.call_tool(
        "memory", DAEMON_CMD, "search", {"query": "duplicate fact", "tier": "local"}
    )
    print(f"Duplicate search result: {dup_res}")

    print("\nSearching for noise...")
    noise_res = await mgr.call_tool(
        "memory", DAEMON_CMD, "search", {"query": "Ok, thanks!", "tier": "local"}
    )
    print(f"Noise search result: {noise_res}")


if __name__ == "__main__":
    asyncio.run(main())
