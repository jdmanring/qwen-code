import asyncio
import json
import logging
import os
import socket
import struct
import sys
import traceback
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any

from mcp.server import Server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage, TextContent, Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp.transport.uds")


class UDSReadStream:
    """
    UDS Read Stream that satisfies the MCP BaseSession interface.
    Uses an asyncio.Queue to buffer messages read from an asyncio.StreamReader.
    """

    def __init__(self, reader: asyncio.StreamReader) -> None:
        self._reader = reader
        self._queue: asyncio.Queue[SessionMessage | None] = asyncio.Queue(maxsize=100)
        self._read_task: asyncio.Task | None = None

    async def __aenter__(self) -> "UDSReadStream":
        """Start the background read loop upon entering the context, ensuring it only runs once."""
        if self._read_task is None or self._read_task.done():
            self._read_task = asyncio.create_task(self._read_loop())
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Ensure the background task is cancelled and queue is closed."""
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass
        # Signal EOF to the consumer
        await self._queue.put(None)

    async def _read_loop(self) -> None:
        """
        Background loop that reads raw bytes from the UDS socket,
        deserializes them into SessionMessages, and pushes them into the queue.
        """
        try:
            buffer = bytearray()
            while True:
                chunk = await self._reader.read(4096)
                if not chunk:
                    # Socket closed
                    break

                buffer.extend(chunk)

                # Attempt to extract complete JSON objects from the buffer
                while True:
                    try:
                        # Find the first '{' and last '}' to attempt to isolate a JSON object
                        # This is a simplified approach; a robust one would track brace nesting
                        start = buffer.find(b"{")
                        if start == -1:
                            break

                        # Try to find the matching closing brace
                        # We use a simple brace counter to find the end of the object
                        brace_count = 0
                        end = -1
                        for i in range(start, len(buffer)):
                            if buffer[i] == ord("{"):
                                brace_count += 1
                            elif buffer[i] == ord("}"):
                                brace_count -= 1
                                if brace_count == 0:
                                    end = i + 1
                                    break

                        if end == -1:
                            # Incomplete object, wait for more data
                            break

                        # Extract the object and remove it from the buffer
                        line = buffer[start:end]
                        del buffer[:end]

                        try:
                            data = json.loads(line.decode("utf-8"))
                            rpc_message = JSONRPCMessage(**data) if isinstance(data, dict) else data
                            message = SessionMessage(message=rpc_message)
                            await self._queue.put(message)
                        except (  # noqa: E501 - kept for readability
                            json.JSONDecodeError,
                            UnicodeDecodeError,
                            TypeError,
                            ValueError,
                        ) as e:
                            logger.error(f"Failed to deserialize MCP message: {e}")
                            continue

                    except Exception as e:
                        logger.error(f"Unexpected error during buffer parsing: {e}")
                        break
        except asyncio.CancelledError:
            raise
        except (OSError, RuntimeError) as e:
            logger.exception(f"Unexpected error in UDS read loop: {e}")
        finally:
            await self._queue.put(None)

    def __aiter__(self) -> AsyncIterator[SessionMessage]:
        """Returns an async generator that yields messages from the queue."""

        async def _gen() -> AsyncGenerator[SessionMessage, None]:
            while True:
                item = await self._queue.get()
                if item is None:
                    break
                yield item

        return _gen()

    async def __anext__(self) -> SessionMessage:
        """Implementation for compatibility with older async iterator patterns."""
        item = await self._queue.get()
        if item is None:
            raise StopAsyncIteration
        return item


class UDSWriteStream:
    """
    UDS Write Stream that satisfies the MCP BaseSession interface.
    Handles serialization of SessionMessages to JSON-lines format.
    """

    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self._writer = writer

    async def __aenter__(self) -> "UDSWriteStream":
        """Enter context; essentially a no-op but required for symmetry."""
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Ensure the writer is properly closed."""
        try:
            if self._writer:
                self._writer.close()
                await self._writer.wait_closed()
        except (OSError, RuntimeError) as e:
            logger.error(f"Error closing UDS write stream: {e}")

    async def send(self, message: SessionMessage) -> None:
        """
        Serializes the SessionMessage to JSON and writes it to the socket.
        """
        try:
            # Robust payload extraction to avoid AttributeError
            if hasattr(message, "message"):
                payload_obj = message.message
            elif isinstance(message, dict) and "message" in message:
                payload_obj = message["message"]
            else:
                payload_obj = message

            # Use .model_dump_json() if it's a Pydantic model, otherwise fallback to json.dumps
            if hasattr(payload_obj, "model_dump_json"):
                serialized = payload_obj.model_dump_json()
            else:
                serialized = json.dumps(payload_obj)

            payload = (serialized + "\n").encode("utf-8")

            self._writer.write(payload)
            await self._writer.drain()
        except (OSError, RuntimeError, AttributeError) as e:
            logger.error(f"Failed to send MCP message: {e}")
            raise ConnectionError(f"UDS write failure: {e}") from e


def create_memory_server(core: Any) -> Server:
    """
    Creates and configures an MCP server for memory operations.
    """
    server = Server("mega-memory-manager")

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return [
            Tool(
                name="ingest",
                description="Ingest text into semantic memory",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The text to ingest"},
                        "tier": {
                            "type": "string",
                            "enum": ["local", "cloud", "auto"],
                            "description": "The storage tier",
                        },
                    },
                    "required": ["text"],
                },
            ),
            Tool(
                name="search",
                description="Search memory for relevant context using semantic recall",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query"},
                        "tier": {
                            "type": "string",
                            "enum": ["local", "cloud", "auto"],
                            "description": "The storage tier to search in",
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="reflect",
                description="Reflect on a query to get high-level context from multiple tiers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to reflect on",
                        }
                    },
                    "required": ["query"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None = None
    ) -> list[TextContent]:
        if not arguments:
            arguments = {}

        if name == "ingest":
            text = arguments.get("text")
            if text is None:
                raise ValueError("Missing required argument: 'text'")
            tier = arguments.get("tier", "auto")
            res = core.ingest(text, tier)
            return [TextContent(type="text", text=json.dumps(res))]

        elif name == "search":
            query = arguments.get("query")
            if query is None:
                raise ValueError("Missing required argument: 'query'")
            tier = arguments.get("tier", "auto")
            res = core.recall(query, tier)
            return [TextContent(type="text", text=json.dumps(res))]

        elif name == "reflect":
            query = arguments.get("query")
            if query is None:
                raise ValueError("Missing required argument: 'query'")
            res = core.reflect(query)
            return [TextContent(type="text", text=json.dumps(res))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    return server


async def run_socket_server_async(core: Any, socket_path: str) -> None:
    """
    Starts a Unix Domain Socket server using asyncio.start_unix_server.
    """
    server = create_memory_server(core)

    async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        # ----------------------------------------------------------------------
        # SECURITY: Peer Verification (SO_PEERCRED)
        # ----------------------------------------------------------------------
        # Verify that the process connecting to the UDS has the same UID as the daemon.
        try:
            sock = writer.get_extra_info("socket")
            if sock:
                # SO_PEERCRED returns a binary struct (pid, uid, gid)
                # On Linux, this is typically 3 integers (4 bytes each)
                creds = sock.getsockopt(
                    socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("iii")
                )
                pid, uid, gid = struct.unpack("iii", creds)
                current_uid = os.getuid()
                if uid != current_uid:
                    logger.warning(
                        f"Unauthorized connection attempt from UID {uid}. Expected {current_uid}."
                    )
                    writer.close()
                    await writer.wait_closed()
                    return
        except (OSError, RuntimeError) as e:
            logger.error(f"Peer verification failed: {e}")
            writer.close()
            await writer.wait_closed()
            return

        client_address = writer.get_extra_info("peername") or "unknown"
        logger.info(f"New UDS connection established from {client_address}")

        try:
            async with (
                UDSReadStream(reader) as read_stream,
                UDSWriteStream(writer) as write_stream,
            ):
                await server.run(
                    read_stream=read_stream,
                    write_stream=write_stream,
                    initialization_options=InitializationOptions(
                        server_name="mega-memory-manager",
                        server_version="1.0.0",
                        capabilities=server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                        client_capabilities=None,
                    ),
                )
        except BaseException as e:
            logger.error(f"Session Error ({type(e).__name__}): {traceback.format_exc()}")
        finally:
            try:
                client_address = writer.get_extra_info("peername") or "unknown"
                logger.info(f"Closing connection from {client_address}")
            except (OSError, RuntimeError):
                pass

    # 1. Socket Cleanup
    if os.path.exists(socket_path):
        try:
            os.unlink(socket_path)
            logger.info(f"Removed existing socket file at {socket_path}")
        except OSError as e:
            logger.error(f"Could not remove existing socket file: {e}")
            raise

    # 2. Standard asyncio server
    server_instance = await asyncio.start_unix_server(handle_connection, path=socket_path)

    # 3. Hardened Permissions (0o600)
    # Only the owner can read/write to the socket
    os.chmod(socket_path, 0o600)

    logger.info(f"MCP UDS Server listening on {socket_path} (Permissions: 0600)")

    async with server_instance:
        await server_instance.serve_forever()


def run_socket_server(core: Any, socket_path: str) -> None:
    """
    Runs the MCP server over a Unix Domain Socket.
    """
    try:
        asyncio.run(run_socket_server_async(core, socket_path))
    except KeyboardInterrupt:
        pass
    except (OSError, RuntimeError) as e:
        sys.stderr.write(f"[ERROR] Socket server error: {e}\n")
        raise


async def run_stdio_server_async(core: Any) -> None:
    """Async implementation of the MCP server over Standard Input/Output."""
    server = create_memory_server(core)
    sys.stderr.write("[DEBUG] Stdio server listening on stdin/stdout\n")
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


def run_stdio_server(core: Any) -> None:
    """
    Runs the MCP server over Standard Input/Output (Stdio).
    """
    try:
        asyncio.run(run_stdio_server_async(core))
    except KeyboardInterrupt:
        pass
    except (OSError, RuntimeError) as e:
        sys.stderr.write(f"[ERROR] Stdio server error: {e}\n")
        raise
