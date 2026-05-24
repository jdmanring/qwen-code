import asyncio
import json
import subprocess
import sys


async def test_ui_handshake():
    print("\n--- SIMULATING UI MCP HANDSHAKE ---")

    # Start the memory daemon via the bin/ wrapper
    subprocess.run(["mega-memory", "start"], check=True)
    print("Daemon started.")

    # Spawn mega-memory in MCP server mode (stdio transport)
    process = await asyncio.create_subprocess_exec(
        "mega-memory",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    print(f"Bridge spawned (PID: {process.pid})")

    try:
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

        print("Waiting for response on stdout...")
        response_bytes = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)

        if not response_bytes:
            print("FAILURE: Bridge closed stdout without responding.")
            return False

        response_text = response_bytes.decode("utf-8").strip()
        print(f"Received: {response_text}")

        try:
            response_json = json.loads(response_text)
            if response_json.get("id") == 1 and "result" in response_json:
                print("SUCCESS: MCP Handshake complete.")
                return True
            else:
                print(f"FAILURE: Invalid MCP response: {response_json}")
                return False
        except json.JSONDecodeError:
            print(f"FAILURE: Response was not valid JSON: {response_text}")
            return False

    except TimeoutError:
        print("FAILURE: Bridge timed out. No response to initialize request.")
        stderr_data = await process.stderr.read()
        print(f"Bridge Stderr: {stderr_data.decode()}")
        return False
    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"UNEXPECTED ERROR: {e}")
        return False
    finally:
        process.terminate()
        await process.wait()


if __name__ == "__main__":
    if not asyncio.run(test_ui_handshake()):
        sys.exit(1)
    sys.exit(0)
