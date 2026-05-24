import asyncio
import json
import os

import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Detect if we are running in the installed stack or the development directory
if os.environ.get("QWEN_STACK_ROOT"):
    STACK_ROOT = os.environ.get("QWEN_STACK_ROOT")
else:
    INSTALLED_STACK = os.path.expanduser("~/.local/share/megalonyx")
    LOCAL_STACK = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

    if os.path.exists(os.path.join(INSTALLED_STACK, "py/venv")):
        STACK_ROOT = INSTALLED_STACK
    else:
        STACK_ROOT = LOCAL_STACK

VENV_PYTHON = os.path.join(STACK_ROOT, "py/venv/bin/python3")
SERVICE_DAEMON = os.path.join(STACK_ROOT, "packages/memory/memory_daemon.py")
BIN_MEMORY = os.path.expanduser("~/.local/bin/mega-memory-manager")

# The command to launch our local MCP server for testing
MCP_COMMAND = [VENV_PYTHON, SERVICE_DAEMON]


async def get_session(env_override=None):
    """Helper to setup an MCP session."""
    env = os.environ.copy()
    if env_override:
        env.update(env_override)

    server_params = StdioServerParameters(
        command=MCP_COMMAND[0], args=MCP_COMMAND[1:], env=env
    )

    # Returns the async context managers for stdio and session
    # Note: In a real pytest environment, we'd use fixtures
    return stdio_client(server_params), server_params


@pytest.mark.asyncio
async def test_binary_connectivity():
    """
    Verify that the installed mega-memory-manager binary exists and is executable.
    """
    if not os.path.exists(BIN_MEMORY):
        pytest.fail(f"Installed binary not found at {BIN_MEMORY}")

    # Check if it can run a simple command
    import subprocess

    result = subprocess.run([BIN_MEMORY, "status"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Qdrant" in result.stdout
    print(f"[OK] Binary connectivity verified: {result.stdout.strip()}")


@pytest.mark.asyncio
async def test_memory_end_to_end():
    """
    End-to-end test: Ingest -> Search -> Reflect
    """
    if not os.path.exists(VENV_PYTHON):
        pytest.fail(f"Virtual environment python not found at {VENV_PYTHON}")

    server_params = StdioServerParameters(
        command=MCP_COMMAND[0],
        args=MCP_COMMAND[1:],
        env={**os.environ, "MCP_TRANSPORT": "stdio"},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize
            init_result = await session.initialize()
            assert init_result.serverInfo.name == "mega-memory-manager"
            assert init_result.protocolVersion is not None

            # 2. Test Ingestion
            test_text = "The quick brown fox jumps over the lazy dog."
            ingest_result = await session.call_tool(
                "ingest", {"text": test_text, "tier": "local"}
            )

            ingest_data = json.loads(ingest_result.content[0].text)
            assert ingest_data["status"] == "queued"

            # 3. Wait for background worker
            await asyncio.sleep(2)

            # 4. Test Search
            search_result = await session.call_tool(
                "search", {"query": "fox", "tier": "local"}
            )

            search_data = json.loads(search_result.content[0].text)
            assert len(search_data) > 0
            assert "error" not in search_data

            # 5. Test Reflect
            reflect_result = await session.call_tool("reflect", {"query": "fox"})
            reflect_data = json.loads(reflect_result.content[0].text)
            assert "error" not in reflect_data


@pytest.mark.asyncio
async def test_transport_stress():
    """
    Verify that the MCP transport can handle large payloads.
    """
    # Create a large text payload (approx 500KB)
    large_text = "Large payload test. " * 10000

    server_params = StdioServerParameters(
        command=MCP_COMMAND[0],
        args=MCP_COMMAND[1:],
        env={**os.environ, "MCP_TRANSPORT": "stdio"},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Ingest large text
            ingest_result = await session.call_tool(
                "ingest", {"text": large_text, "tier": "local"}
            )
            ingest_data = json.loads(ingest_result.content[0].text)
            assert ingest_data["status"] == "queued"

            await asyncio.sleep(3)

            # Search for a unique part of the large text
            search_result = await session.call_tool(
                "search", {"query": "Large payload test", "tier": "local"}
            )
            search_data = json.loads(search_result.content[0].text)
            assert len(search_data) > 0


@pytest.mark.asyncio
async def test_qdrant_connection_failure():
    """
    Verify that the server handles Qdrant connection failures gracefully.
    """
    # Use a non-existent Qdrant URL to force a connection error
    server_params = StdioServerParameters(
        command=MCP_COMMAND[0],
        args=MCP_COMMAND[1:],
        env={**os.environ, "QDRANT_LOCAL_URL": "http://localhost:9999"},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # The daemon will try to ensure_collections_exist() during start
            # which happens before run_stdio_server() is called in memory_daemon.py.
            # If it fails, the process might exit or the handshake will fail.
            try:
                await session.initialize()
            except (TimeoutError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
                # We expect an exception here because the daemon should crash
                # or fail the handshake when it can't connect to Qdrant.
                print(f"Caught expected failure: {e}")
                return

            # If it somehow initialized, tool calls should fail
            try:
                await session.call_tool("search", {"query": "test", "tier": "local"})
                pytest.fail("Search should have failed with invalid Qdrant URL")
            except (TimeoutError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
                print(f"Caught expected tool failure: {e}")


if __name__ == "__main__":
    # This allows running via 'python tests/integration_test_memory.py'
    # The installer uses this to verify a successful deployment.
    async def run_smoke_tests():
        print("Running Binary Connectivity Test...")
        await test_binary_connectivity()
        print("Running End-to-End Smoke Test...")
        await test_memory_end_to_end()
        print("Running Transport Stress Smoke Test...")
        await test_transport_stress()
        print("\n[OK] ALL SMOKE TESTS PASSED!")

    asyncio.run(run_smoke_tests())
