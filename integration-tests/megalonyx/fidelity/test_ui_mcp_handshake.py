import asyncio
import json
import subprocess
import sys


async def test_ui_handshake():
    print("\n--- SIMULATING UI MCP HANDSHAKE ---")

    # 1. Setup paths
    python_bin = "sys.executable"
    bridge_script = (
        "stdio_socket_relay"
    )

    # Ensure daemon is running
    subprocess.run(["mega-memory-manager", "start"], check=True)
    print("Daemon started.")

    # 2. Spawn the bridge as the UI would
    # We use a subprocess with pipes for stdin and stdout
    process = await asyncio.create_subprocess_exec(
        python_bin,
        bridge_script,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    print(f"Bridge spawned (PID: {process.pid})")

    try:
        # 3. Send the MCP 'initialize' request
        # This is the exact first message the UI sends
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "qwen-code-ui-sim", "version": "1.0.0"},
            },
        }

        print("Sending initialize request...")
        payload = (json.dumps(init_request) + "\n").encode("utf-8")
        process.stdin.write(payload)
        await process.stdin.drain()

        # 4. Wait for the response on stdout
        print("Waiting for response on stdout...")
        # Use a timeout to prevent hanging
        response_bytes = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)

        if not response_bytes:
            print("❌ FAILURE: Bridge closed stdout without responding.")
            return False

        response_text = response_bytes.decode("utf-8").strip()
        print(f"Received: {response_text}")

        try:
            response_json = json.loads(response_text)
            if response_json.get("id") == 1 and "result" in response_json:
                print("✅ SUCCESS: MCP Handshake complete. UI should see 'Connected'.")
                return True
            else:
                print(f"❌ FAILURE: Invalid MCP response: {response_json}")
                return False
        except json.JSONDecodeError:
            print(f"❌ FAILURE: Response was not valid JSON: {response_text}")
            return False

    except TimeoutError:
        print("❌ FAILURE: Bridge timed out. No response to initialize request.")
        # Capture stderr to see why it failed
        stderr_data = await process.stderr.read()
        print(f"Bridge Stderr: {stderr_data.decode()}")
        return False
    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False
    finally:
        process.terminate()
        await process.wait()


if __name__ == "__main__":
    if not asyncio.run(test_ui_handshake()):
        sys.exit(1)
    sys.exit(0)
