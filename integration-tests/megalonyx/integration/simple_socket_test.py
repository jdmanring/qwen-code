import asyncio
import json
import os


async def test():
    socket_path = os.path.expanduser("~/.local/share/megalonyx/tmp/qwen_memory.sock")
    print(f"Connecting to {socket_path}...")
    reader, writer = await asyncio.open_unix_connection(socket_path)

    # Send initialize request
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }
    print("Sending initialize...")
    writer.write((json.dumps(req) + "\n").encode())
    await writer.drain()

    resp = await reader.readline()
    print(f"Response: {resp.decode()}")
    writer.close()
    await writer.wait_closed()


asyncio.run(test())
