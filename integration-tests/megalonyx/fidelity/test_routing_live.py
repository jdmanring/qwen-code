import asyncio
import os

from control_plane_daemon.mcp_manager import MCPManager


async def main():
    mgr = MCPManager()
    cmd = [
        "python3",
        os.path.expanduser("~/.local/share/megalonyx/packages/memory/memory_daemon.py"),
    ]

    # 1. Ingest to LOCAL
    print("Ingesting local fact...")
    await mgr.call_tool(
        "memory",
        cmd,
        "ingest",
        {"text": "This is a local-only secret.", "tier": "local"},
    )

    # 2. Ingest to CLOUD
    print("Ingesting cloud fact...")
    await mgr.call_tool(
        "memory",
        cmd,
        "ingest",
        {"text": "This is a global architecture policy.", "tier": "cloud"},
    )

    # 3. Search LOCAL only
    print("\nSearching LOCAL tier...")
    local_res = await mgr.call_tool(
        "memory", cmd, "search", {"query": "local secret", "tier": "local"}
    )
    print(f"Local search result: {local_res}")

    # 4. Search CLOUD only
    print("\nSearching CLOUD tier...")
    cloud_res = await mgr.call_tool(
        "memory", cmd, "search", {"query": "architecture policy", "tier": "cloud"}
    )
    print(f"Cloud search result: {cloud_res}")


if __name__ == "__main__":
    asyncio.run(main())
