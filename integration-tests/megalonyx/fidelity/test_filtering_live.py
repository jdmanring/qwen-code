import asyncio
import os

from control_plane_daemon.mcp_manager import MCPManager


async def main():
    mgr = MCPManager()
    cmd = [
        "python3",
        os.path.expanduser("~/.local/share/megalonyx/packages/memory/memory_daemon.py"),
    ]

    # 1. Test Deduplication
    fact = "This is a duplicate fact that should only be stored once."
    print(f"Ingesting duplicate fact 3 times: {fact}")
    for i in range(3):
        await mgr.call_tool("memory", cmd, "ingest", {"text": fact, "tier": "local"})

    # 2. Test Noise Filtering
    noise = "Ok, thanks!"
    print(f"Ingesting noise: {noise}")
    await mgr.call_tool("memory", cmd, "ingest", {"text": noise, "tier": "local"})

    # 3. Verify results
    print("\nSearching for duplicate fact...")
    dup_res = await mgr.call_tool(
        "memory", cmd, "search", {"query": "duplicate fact", "tier": "local"}
    )
    print(f"Duplicate search result: {dup_res}")

    print("\nSearching for noise...")
    noise_res = await mgr.call_tool(
        "memory", cmd, "search", {"query": "Ok, thanks!", "tier": "local"}
    )
    print(f"Noise search result: {noise_res}")


if __name__ == "__main__":
    asyncio.run(main())
