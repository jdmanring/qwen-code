import asyncio
import json
import os


async def test_socket():
    socket_path = os.path.expanduser("~/.local/share/megalonyx/tmp/megalonyx_memory.sock")
    print(f"Connecting to {socket_path}...")

    try:
        reader, writer = await asyncio.open_unix_connection(socket_path)
        print("Successfully connected to socket.")

        # MCP Initialize Request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "debug-test-client", "version": "1.0.0"},
            },
        }

        payload = (json.dumps(init_request) + "\n").encode("utf-8")
        print(f"Sending: {json.dumps(init_request)}")
        writer.write(payload)
        await writer.drain()

        # Wait for response
        try:
            response = await asyncio.wait_for(reader.readline(), timeout=5.0)
            if response:
                print(f"Received response: {response.decode('utf-8').strip()}")
            else:
                print("Received EOF (empty response).")
        except TimeoutError:
            print("Timed out waiting for response from daemon.")

        writer.close()
        await writer.wait_closed()

    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    asyncio.run(test_socket())
