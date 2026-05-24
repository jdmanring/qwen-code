import asyncio
import os
import subprocess
from pathlib import Path

import pytest

# --- PATH HACK ---
# -----------------
# Import MCPManager from the project
# We'll need to ensure PYTHONPATH is set correctly
from control_plane_daemon.mcp_manager import MCPManager  # noqa: E402


@pytest.mark.asyncio
async def test_full_stack_flow():
    """
    Verifies the end-to-end flow:
    1. Start stack
    2. Verify health
    3. Perform a memory turn (Ingest -> Search -> Reflect)
    4. Stop stack
    """
    # 1. Start the stack
    print("Starting stack via mega-memory-manager...")
    # Use the actual script path since the bin/ wrapper is created during installation
    project_root = Path(__file__).resolve().parent.parent.parent
    stack_manager = project_root / "scripts" / "mega-memory-manager.py"

    # We run it via the venv python
    python_bin = Path("sys.executable")

    env = os.environ.copy()
    env["PYTHONPATH"] = (
        f"{project_root}:{project_root}/packages/memory:{env.get('PYTHONPATH', '')}"
    )

    start_proc = subprocess.run(
        [str(python_bin), str(stack_manager), "start"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert start_proc.returncode == 0, f"Failed to start stack: {start_proc.stderr}"
    print("Stack started successfully.")

    # Give the daemon time to initialize and create the socket
    print("Waiting for daemon initialization...")
    await asyncio.sleep(5)

    # 2. Verify health
    print("Verifying stack health...")
    qwen_status = project_root / "bin" / "mega-status"

    status_proc = subprocess.run(
        [str(python_bin), str(qwen_status)], env=env, capture_output=True, text=True
    )
    assert status_proc.returncode == 0, f"mega-status failed: {status_proc.stderr}"
    print("Stack health verified.")
    # 3. Perform a Memory Turn
    # Derive the socket path from the user's home directory to remain location-agnostic
    stack_root = Path(os.path.expanduser("~/.local/share/megalonyx"))
    socket_path = stack_root / "tmp" / "qwen_memory.sock"
    print(f"Using derived socket path: {socket_path}")

    mgr = MCPManager()
    try:
        # A. Ingest
        print("Executing Ingest...")
        ingest_res = await mgr.call_tool(
            "memory",
            tool_name="ingest",
            arguments={
                "text": "The quick brown fox jumps over the lazy dog.",
                "tier": "local",
            },
            socket_path=str(socket_path),
        )
        assert (
            ingest_res["content"][0]["text"] == '{"status": "queued", "tier": "local"}'
        )
        print("Ingest successful.")

        # B. Search
        print("Executing Search...")
        # Give it a moment to "process" (even though it's just queued)
        await asyncio.sleep(1)
        search_res = await mgr.call_tool(
            "memory",
            tool_name="search",
            arguments={"query": "brown fox"},
            socket_path=str(socket_path),
        )
        # The search result might be empty if it's purely in-memory and not yet indexed,
        # but it should at least return a valid structure.
        assert "content" in search_res
        print("Search successful.")

        # C. Reflect
        print("Executing Reflect...")
        reflect_res = await mgr.call_tool(
            "memory",
            tool_name="reflect",
            arguments={"query": "What did the fox do?"},
            socket_path=str(socket_path),
        )
        assert "content" in reflect_res
        print("Reflect successful.")

    finally:
        # 4. Stop the stack
        print("Stopping stack...")
        stop_proc = subprocess.run(
            [str(python_bin), str(stack_manager), "stop"],
            env=env,
            capture_output=True,
            text=True,
        )
        assert stop_proc.returncode == 0, f"Failed to stop stack: {stop_proc.stderr}"
        print("Stack stopped successfully.")
        await mgr.close_all()


if __name__ == "__main__":
    asyncio.run(test_full_stack_flow())
