import asyncio
import json
import os

import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Environment Setup
if os.environ.get("QWEN_STACK_ROOT"):
    STACK_ROOT = os.environ.get("QWEN_STACK_ROOT")
else:
    INSTALLED_STACK = os.path.expanduser("~/.local/share/megalonyx")
    LOCAL_STACK = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    STACK_ROOT = (
        INSTALLED_STACK
        if os.path.exists(os.path.join(INSTALLED_STACK, "py/venv"))
        else LOCAL_STACK
    )

VENV_PYTHON = os.path.join(STACK_ROOT, "py/venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "packages/memory/memory_daemon.py")

MCP_COMMAND = [VENV_PYTHON, SERVICE_DAEMON]


async def execute_action(tool_name, arguments):
    """Helper to run a single tool call in a fresh session."""
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=os.environ.copy()
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.call_tool(tool_name, arguments)
            return json.loads(res.content[0].text)


@pytest.mark.asyncio
async def test_cross_session_persistence():
    """
    Verify that facts persist across completely different MCP server sessions.
    """
    unique_fact = f"Cross-session secret: {os.urandom(8).hex()}"

    # Session 1: Ingest
    print(f"[Session 1] Ingesting: {unique_fact}")
    res1 = await execute_action("ingest", {"text": unique_fact, "tier": "local"})
    assert res1["status"] == "queued"

    # Wait for async ingestion to hit Qdrant
    await asyncio.sleep(2)

    # Session 2: Recall
    print(f"[Session 2] Recalling: {unique_fact[:20]}...")
    res2 = await execute_action("search", {"query": unique_fact[:20], "tier": "local"})

    assert len(res2) > 0
    assert any(unique_fact in r["payload"]["text"] for r in res2), (
        "Fact did not persist across sessions!"
    )


@pytest.mark.asyncio
async def test_cold_start_recovery():
    """
    Verify that the system recovers correctly from the WAL after a 'crash'.
    """
    # Note: We can't easily 'crash' the process and then check it here without
    # manipulating files. We'll simulate a WAL entry.
    wal_path = os.path.expanduser("~/.qwen/memory/wal.jsonl")
    os.makedirs(os.path.dirname(wal_path), exist_ok=True)

    # Create a fake WAL entry manually
    fake_record = {
        "id": "00000000-0000-0000-0000-000000000001",
        "text": "WAL recovery test fact",
        "tier": "local",
        "source": "test",
        "importance": 5,
        "metadata": {},
        "created_at": 1000.0,
        "updated_at": 1000.0,
        "schema_version": "1.0",
    }
    with open(wal_path, "a") as f:
        f.write(json.dumps(fake_record) + "\n")

    # Now launch the server. It should run recover() and ingest the record.
    await asyncio.sleep(1)
    res = await execute_action("search", {"query": "WAL recovery", "tier": "local"})

    assert len(res) > 0
    assert any("WAL recovery test fact" in r["payload"]["text"] for r in res)


if __name__ == "__main__":

    async def main():
        print("Running Lifecycle Tests...")
        try:
            await test_cross_session_persistence()
            print("[OK] Cross-session persistence verified.")
            await test_cold_start_recovery()
            print("[OK] Cold start WAL recovery verified.")
            print("\nALL LIFECYCLE TESTS PASSED!")
        except (
            AssertionError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            OSError,
        ) as e:
            print(f"\n[FAIL] Tests failed: {e}")
            import sys

            sys.exit(1)

    asyncio.run(main())
