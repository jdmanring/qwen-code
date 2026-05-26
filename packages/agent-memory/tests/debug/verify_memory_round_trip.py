import asyncio
import json
import os
import sys
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any

import anyio
from control_plane_daemon.mcp_manager import MCPManager
from mcp.client.session import ClientSession
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage


@asynccontextmanager
async def socket_client(socket_path):
    """Connects to a Unix socket and wraps it in MCP-compatible streams."""
    read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
    write_stream, write_stream_reader = anyio.create_memory_object_stream(0)

    reader, writer = await asyncio.open_unix_connection(socket_path)

    async def read_loop():
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                try:
                    message = JSONRPCMessage.model_validate_json(line.decode())
                    await read_stream_writer.send(SessionMessage(message))
                except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
                    await read_stream_writer.send(e)
        except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
            await read_stream_writer.send(e)
        finally:
            await read_stream.aclose()
            await read_stream_writer.aclose()

    async def write_loop():
        try:
            async for session_message in write_stream_reader:
                json_str = session_message.message.model_dump_json(by_alias=True, exclude_none=True)
                writer.write((json_str + "\n").encode())
                await writer.drain()
        except (RuntimeError, ValueError, TypeError, AttributeError, OSError):
            pass
        finally:
            writer.close()
            await writer.wait_closed()
            await write_stream.aclose()
            await write_stream_reader.aclose()

    async with anyio.create_task_group() as tg:
        tg.start_soon(read_loop)
        tg.start_soon(write_loop)
        try:
            yield read_stream, write_stream
        finally:
            await write_stream.aclose()
            await read_stream.aclose()


class SocketMCPManager(MCPManager):
    async def _get_session(
        self,
        server_name: str,
        command: list[str] | None = None,
        socket_path: str | None = None,
    ) -> Any:
        if server_name in self.sessions:
            return self.sessions[server_name]["session"]

        stack = AsyncExitStack()
        try:
            if socket_path:
                read, write = await stack.enter_async_context(socket_client(socket_path))
            elif command:
                from mcp.client.stdio import stdio_client
                from mcp.types import StdioServerParameters

                server_params = StdioServerParameters(
                    command=command[0], args=command[1:], env=os.environ
                )
                read, write = await stack.enter_async_context(stdio_client(server_params))
            else:
                raise ValueError("Either command or socket_path must be provided")

            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            self.sessions[server_name] = {
                "session": session,
                "stack": stack,
                "command": command,
                "socket_path": socket_path,
            }
            return session
        except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
            await stack.aclose()
            raise e


async def main():
    socket_path = os.path.expanduser("~/.local/share/megalonyx/tmp/megalonyx_memory.sock")
    verification_string = f"VERIFY_MEMORY_LOOP_{os.getpid()}_{int(asyncio.get_event_loop().time())}"
    server_name = "memory_daemon"

    print(f"Testing connection to memory daemon at: {socket_path}")
    print(f"Verification string: {verification_string}")

    mgr = SocketMCPManager()
    try:
        print("\nStep 1: Ingesting verification string...")
        ingest_res = await mgr.call_tool(
            server_name,
            socket_path=socket_path,
            tool_name="ingest",
            arguments={"text": verification_string, "tier": "local"},
        )
        print(f"Ingest response: {ingest_res}")

        print("Waiting for ingestion worker to process...")
        await asyncio.sleep(2)

        print("\nStep 2: Searching for verification string...")
        search_res = await mgr.call_tool(
            server_name,
            socket_path=socket_path,
            tool_name="search",
            arguments={"query": verification_string, "tier": "local"},
        )
        print(f"Search response: {search_res}")

        content_list = search_res.get("content", [])
        if not content_list:
            raise RuntimeError("No content returned from search tool")

        recall_data = json.loads(content_list[0]["text"])

        found = False
        if isinstance(recall_data, list):
            for point in recall_data:
                if point.get("payload", {}).get("text") == verification_string:
                    found = True
                    break

        if found:
            print("\nSUCCESS: Verification string found in memory!")
        else:
            print("\nFAILURE: Verification string NOT found in memory.")
            print(f"Recall data received: {recall_data}")
            sys.exit(1)

    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"\nERROR during verification loop: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await mgr.close_all()


if __name__ == "__main__":
    try:
        anyio.run(main)
    except SystemExit as e:
        sys.exit(e.code)
