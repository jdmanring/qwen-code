import asyncio
import json
import logging
import os
import sys
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from types import TracebackType
from typing import Any, Optional, TypedDict, cast

import anyio
import mcp.client.session as mcp_session
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.shared.message import SessionMessage
from mcp.types import ImageContent, JSONRPCMessage, TextContent

# Configure logging for the bridge
logger = logging.getLogger("mcp.transport.uds")


class MCPResponse(TypedDict):
    content: list[dict[str, Any]]
    error: str | None


class ServerConfig(TypedDict):
    command: list[str] | None
    socket_path: str | None
    env: dict[str, str] | None


class UDSReadStream:
    """
    UDS Read Stream that satisfies the MCP BaseSession interface.
    Uses an anyio memory object stream to buffer messages read from an asyncio.StreamReader.
    """

    def __init__(self, reader: asyncio.StreamReader) -> None:
        self._reader = reader
        self._send_stream, self._receive_stream = anyio.create_memory_object_stream(100)
        self._read_task: asyncio.Task | None = None

    async def __aenter__(self) -> "UDSReadStream":
        self._read_task = asyncio.create_task(self._read_loop())
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass

        await self._send_stream.aclose()
        await self._receive_stream.aclose()

    async def _read_loop(self) -> None:
        try:
            while True:
                try:
                    line = await self._reader.readline()
                except RuntimeError as e:
                    if "already waiting for incoming data" in str(e):
                        await asyncio.sleep(0.1)
                        continue
                    raise

                if not line:
                    break

                try:
                    data = json.loads(line.decode("utf-8"))
                    rpc_message = JSONRPCMessage(**data) if isinstance(data, dict) else data
                    message = SessionMessage(message=rpc_message)
                    await self._send_stream.send(message)
                except (
                    json.JSONDecodeError,
                    UnicodeDecodeError,
                    TypeError,
                    ValueError,
                ) as e:
                    logger.error(f"Failed to deserialize MCP message: {e}")
                    continue
        except asyncio.CancelledError:
            raise
        except (OSError, RuntimeError) as e:
            logger.exception(f"Unexpected error in UDS read loop: {e}")
        finally:
            await self._send_stream.aclose()

    def __aiter__(self) -> AsyncIterator[SessionMessage]:
        return cast(AsyncIterator[SessionMessage], self._receive_stream)

    async def __anext__(self) -> SessionMessage:
        return await self._receive_stream.receive()


class UDSWriteStream:
    """
    UDS Write Stream that satisfies the MCP BaseSession interface.
    Handles serialization of SessionMessages to JSON-lines format.
    """

    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self._writer = writer

    async def __aenter__(self) -> "UDSWriteStream":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if self._writer:
                self._writer.close()
                await self._writer.wait_closed()
        except (OSError, RuntimeError) as e:
            logger.error(f"Error closing UDS write stream: {e}")

    async def send(self, message: SessionMessage) -> None:
        try:
            serialized = message.message.model_dump_json()
            payload = (serialized + "\n").encode("utf-8")
            self._writer.write(payload)
            await self._writer.drain()
        except (OSError, RuntimeError, AttributeError) as e:
            logger.error(f"Failed to send MCP message: {e}")
            raise ConnectionError(f"UDS write failure: {e}") from e


@asynccontextmanager
async def socket_client(
    socket_path: str,
) -> AsyncIterator[tuple[UDSReadStream, UDSWriteStream]]:
    reader, writer = await asyncio.open_unix_connection(socket_path)
    read_stream = UDSReadStream(reader)
    write_stream = UDSWriteStream(writer)
    async with read_stream, write_stream:
        yield read_stream, write_stream


class MCPManager:
    """
    Intuitive MCP Manager.
    Handles multiple MCP server connections with qualified tool naming.
    """

    _instance: Optional["MCPManager"] = None

    def __new__(cls) -> "MCPManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Guard to prevent re-initialization in singleton
        if hasattr(self, "sessions"):
            return
        self.sessions: dict[
            str, dict[str, Any]
        ] = {}  # server_name -> {session, stack: AsyncExitStack, config: ServerConfig}
        self.server_configs: dict[str, ServerConfig] = {}

    def register_server(
        self,
        server_name: str,
        command: list[str] | None = None,
        socket_path: str | None = None,
    ) -> None:
        """Registers a server configuration without connecting immediately."""
        self.server_configs[server_name] = {
            "command": command,
            "socket_path": socket_path,
            "env": os.environ.copy(),
        }

    async def _get_session(self, server_name: str) -> Any:
        """Gets an existing session or creates a new one based on registered config."""
        if server_name in self.sessions:
            return self.sessions[server_name]["session"]

        if server_name not in self.server_configs:
            raise ValueError(
                f"Server '{server_name}' is not registered. Call register_server first."
            )

        config = self.server_configs[server_name]
        stack = AsyncExitStack()
        try:
            if config["socket_path"]:
                read, write = await stack.enter_async_context(socket_client(config["socket_path"]))
            elif config["command"]:
                server_params = StdioServerParameters(
                    command=config["command"][0],
                    args=config["command"][1:],
                    env=config["env"],
                )
                read, write = await stack.enter_async_context(stdio_client(server_params))
            else:
                raise ValueError(
                    f"No valid connection method configured for server '{server_name}'"
                )

            session = await stack.enter_async_context(
                mcp_session.ClientSession(cast(Any, read), cast(Any, write))
            )
            await session.initialize()

            self.sessions[server_name] = {
                "session": session,
                "stack": stack,
                "config": config,
            }
            return session
        except (OSError, RuntimeError, ValueError) as e:
            await stack.aclose()
            raise e

    async def list_tools(self, server_name: str) -> list[dict[str, Any]]:
        """Lists available tools on a registered MCP server."""
        session = await self._get_session(server_name)
        tools_result = await session.list_tools()
        return [{"name": t.name, "description": t.description} for t in tools_result.tools]

    async def call_tool(
        self, server_name: str, tool_name: str, arguments: dict[str, Any]
    ) -> MCPResponse:
        """Calls a specific tool on a registered MCP server."""
        session = await self._get_session(server_name)
        result = await session.call_tool(tool_name, arguments)

        formatted_result: MCPResponse = {"content": [], "error": None}
        for content in result.content:
            if isinstance(content, TextContent):
                formatted_result["content"].append({"type": "text", "text": content.text})
            elif isinstance(content, ImageContent):
                formatted_result["content"].append(
                    {
                        "type": "image",
                        "data": content.data,
                        "mimeType": content.mimeType,
                    }
                )

        return formatted_result

    async def read_resource(self, server_name: str, uri: str) -> str:
        """Reads a resource from a registered MCP server."""
        session = await self._get_session(server_name)
        resource = await session.read_resource(uri)
        return resource.contents[0].text if resource.contents else ""

    async def close_all(self) -> None:
        """Closes all active MCP sessions."""
        for _, data in self.sessions.items():
            await data["stack"].aclose()
        self.sessions.clear()


if __name__ == "__main__":

    async def test() -> None:
        mgr = MCPManager()
        try:
            # Register the everything server
            mgr.register_server(
                "everything",
                command=["npx", "-y", "@modelcontextprotocol/server-everything"],
            )

            print("Listing tools...", file=sys.stderr)
            tools = await mgr.list_tools("everything")
            print(f"Found {len(tools)} tools.", file=sys.stderr)

            if tools:
                print(f"\nCalling tool: {tools[0]['name']}...", file=sys.stderr)
                res = await mgr.call_tool(
                    "everything", tools[0]["name"], {"message": "Hello Monorepo MCP!"}
                )
                print(res, file=sys.stderr)
        finally:
            print("\nClosing all sessions...", file=sys.stderr)
            await mgr.close_all()

    asyncio.run(test())
