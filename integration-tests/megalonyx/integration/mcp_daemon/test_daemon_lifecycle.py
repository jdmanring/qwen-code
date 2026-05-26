import asyncio
import os
import sys
from pathlib import Path

# --- PATH HACK ---
# -----------------
# Import MCPManager from the project
# We'll need to ensure PYTHONPATH is set correctly
from control_plane_daemon.mcp_manager import MCPManager  # noqa: E402


def test_daemon_lifecycle() -> None:
    """
    Verifies that the Memory Daemon can be started, responds to MCP commands,
    and can be stopped gracefully.
    """

    async def _run_test():
        mgr = None
        # 1. Setup: Use a fixed path in /tmp/ to avoid tmpdir permission issues
        socket_path = Path("/tmp/test_megalonyx_memory.sock")
        if socket_path.exists():
            os.remove(socket_path)

        # We'll use a custom runner script to avoid modifying the original daemon code.
        # This script will import the necessary components and run the server on our test socket.
        runner_code = (
            "import os, sys; "
            "print(f'Subprocess sys.path: {sys.path}', file=sys.stderr); "
            "from agent_memory.memory_daemon import MemoryCore, run_socket_server; "
            "core = MemoryCore(); "
            "run_socket_server(core, sys.argv[1])"
        )

        # 2. Start the Daemon as a subprocess
        # We must set PYTHONPATH to include the project root so the subprocess can find 'packages'
        env = os.environ.copy()
        env["PYTHONPATH"] = (
            f"{os.getcwd()}:{os.getcwd()}/packages/memory:{env.get('PYTHONPATH', '')}"
        )
        # Set MCP_TRANSPORT to socket (though run_socket_server handles it)
        env["MCP_TRANSPORT"] = "socket"

        print("Starting daemon subprocess...")
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-c",
            runner_code,
            str(socket_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        try:
            # 3. Wait for the socket to be created
            import time

            start_time = time.time()
            print(f"Waiting for socket at {socket_path}...")
            while not socket_path.exists():
                if process.returncode is not None:
                    stderr_data = await process.stderr.read()
                    print(
                        f"Daemon exited with code {process.returncode}. stderr: {stderr_data.decode()}",
                        file=sys.stderr,
                    )
                    raise RuntimeError(
                        f"Daemon exited prematurely with code {process.returncode}"
                    )

                if time.time() - start_time > 10:
                    # Let's capture stderr to see why it failed
                    stderr_data = await process.stderr.read()
                    print(f"Daemon stderr: {stderr_data.decode()}", file=sys.stderr)
                    raise TimeoutError("Daemon failed to create socket in time.")
                await asyncio.sleep(0.5)

            print("Socket created successfully.")

            # 4. Use MCPManager to interact with the daemon
            print("Initializing MCPManager...")
            mgr = MCPManager()

            # Verify connection by listing tools
            # Note: We pass the socket_path to the manager
            print("Listing tools...")
            tools = await mgr.list_tools("memory", socket_path=str(socket_path))
            print(f"Tools found: {[t['name'] for t in tools]}")

            # Check if we got the expected tools
            tool_names = [t["name"] for t in tools]
            assert "ingest" in tool_names, f"Expected 'ingest' tool, got {tool_names}"
            assert "search" in tool_names, f"Expected 'search' tool, got {tool_names}"
            assert "reflect" in tool_names, f"Expected 'reflect' tool, got {tool_names}"

            # Test a simple tool call (ingest)
            print("Calling 'ingest' tool...")
            ingest_res = await mgr.call_tool(
                "memory",
                tool_name="ingest",
                arguments={"text": "Hello from the integration test!", "tier": "local"},
                socket_path=str(socket_path),
            )
            print(f"Ingest result: {ingest_res}")
            assert (
                ingest_res["content"][0]["text"]
                == '{"status": "queued", "tier": "local"}'
            )

            # 5. Cleanup: Stop the daemon
            print("Stopping daemon...")
            process.terminate()
            await process.wait()

        finally:
            # Ensure the process is dead
            if process.returncode is None:
                print("Killing daemon process...")
                process.kill()
                await process.wait()

            # Close all MCP sessions in the manager
            if mgr:
                print("Closing MCP sessions...")
                await mgr.close_all()

            # Clean up the socket file
            if socket_path.exists():
                print(f"Removing socket file {socket_path}")
                os.remove(socket_path)

    asyncio.run(_run_test())


if __name__ == "__main__":
    test_daemon_lifecycle()
