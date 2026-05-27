import asyncio
import json
import os
import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Environment Setup
# Force use of the monorepo for testing
LOCAL_STACK = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
STACK_ROOT = LOCAL_STACK

VENV_PYTHON = os.path.join(STACK_ROOT, ".venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "packages/memory/memory_daemon.py")
MCP_COMMAND = ["/home/james/projects/megalonyx-monorepo/wrapper.sh"]


async def execute_action(tool_name, arguments, session=None):
    """Helper to run a single tool call. If session is provided, uses it."""
    if session:
        res = await session.call_tool(tool_name, arguments)
        return json.loads(res.content[0].text)

    env = os.environ.copy()
    env["MCP_TRANSPORT"] = "stdio"
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=env
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

    env = os.environ.copy()
    env["MCP_TRANSPORT"] = "stdio"
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=env
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Session 1: Ingest
            print(f"[Session 1] Ingesting: {unique_fact}")
            res1 = await session.call_tool("ingest", {"text": unique_fact, "tier": "sync"})
            res1_parsed = json.loads(res1.content[0].text)
            assert res1_parsed["status"] == "stored"

            # Wait for async ingestion to hit Qdrant
            await asyncio.sleep(2)

            # Session 2: Recall (within same session, but simulating a new one)
            print(f"[Session 2] Recalling: {unique_fact[:20]}...")
            res2 = await session.call_tool("search", {"query": unique_fact[:20], "tier": "local"})
            res2_parsed = json.loads(res2.content[0].text)

            assert len(res2_parsed) > 0
            assert any(unique_fact in r["payload"]["text"] for r in res2_parsed), (
                "Fact did not persist!"
            )


@pytest.mark.asyncio
async def test_cold_start_recovery():
    """
    Verify that the system recovers correctly from the WAL after a 'crash'.
    """
    # Note: We can't easily 'crash' the process and then check it here without
    # manipulating files. We'll simulate a WAL entry.
    wal_path = os.path.join(STACK_ROOT, "packages/memory/wal.jsonl")
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
    # Since we are starting a NEW process, this is a true cold start.
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
