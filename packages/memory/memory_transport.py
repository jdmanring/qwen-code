import asyncio
import json
import os
import socket
import struct
import sys
import traceback
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any

import anyio
from mcp.server import Server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage, TextContent, Tool


class CloseShieldSendStream:
    """
    A proxy for a MemoryObjectSendStream that ignores close() calls.
    This prevents the MCP SDK from prematurely closing the transport.
    """

    def __init__(self, stream: anyio.streams.memory.MemoryObjectSendStream) -> None:
        self._stream = stream

    async def send(self, value: Any) -> None:
        await self._stream.send(value)

    def close(self) -> None:
        # Ignore close calls from the SDK.
        # The ShutdownCoordinator will close the stream explicitly.
        pass

    def __await__(self) -> Any:
        return self._stream.__await__()

    async def __aenter__(self) -> "CloseShieldSendStream":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


class StdioReadStream:
    """
    A hybrid stream that acts as both an AsyncIterator (for MCP session reading)
    and an AsyncContextManager (for MCP session cleanup).
    """

    def __init__(
        self, receive_stream: anyio.streams.memory.MemoryObjectReceiveStream[SessionMessage]
    ) -> None:
        self._receive_stream = receive_stream

    async def __aenter__(self) -> "StdioReadStream":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # The SDK calls this during shutdown.
        pass

    def __aiter__(self) -> AsyncIterator[SessionMessage]:
        return self._gen()

    async def _gen(self) -> AsyncGenerator[SessionMessage, None]:
        async with self._receive_stream:
            async for message in self._receive_stream:
                if message is SENTINEL_EOF:
                    return
                yield message


SENTINEL_EOF = object()
SENTINEL_SHUTDOWN = object()


class RequestRegistry:
    """
    Tracks active requests by their IDs to ensure graceful shutdown.
    """

    def __init__(self) -> None:
        self._active_ids: set[Any] = set()
        self._condition = asyncio.Condition()
        self._id = id(self)

    async def __aenter__(self) -> "RequestRegistry":
        # This is kept for compatibility but not used in the new ID-based flow.
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def inc(self, request_id: Any) -> None:
        """Synchronous increment for worker threads/readers."""
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(self._sync_inc, request_id)

    def dec(self, request_id: Any) -> None:
        """Synchronous decrement for worker threads/writers."""
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(self._sync_dec, request_id)

    def _sync_inc(self, request_id: Any) -> None:
        self._active_ids.add(request_id)
        sys.stderr.write(f"[REGISTRY] INC: ID={request_id}, Active={len(self._active_ids)}\n")
        sys.stderr.flush()

    def _sync_dec(self, request_id: Any) -> None:
        if request_id in self._active_ids:
            self._active_ids.remove(request_id)
            sys.stderr.write(f"[REGISTRY] DEC: ID={request_id}, Active={len(self._active_ids)}\n")
            sys.stderr.flush()
            asyncio.create_task(self._notify_condition())

    async def _notify_condition(self) -> None:
        async with self._condition:
            self._condition.notify_all()

    async def wait_until_empty(self, timeout: float = 5.0) -> bool:
        """Blocks until there are no active requests or timeout is reached."""
        sys.stderr.write(f"[REGISTRY] Waiting until empty... Active IDs={len(self._active_ids)}\n")
        sys.stderr.flush()
        try:
            async with asyncio.timeout(timeout):
                async with self._condition:
                    while len(self._active_ids) > 0:
                        await self._condition.wait()
            sys.stderr.write("[REGISTRY] Registry is now empty. Proceeding with shutdown.\n")
            sys.stderr.flush()
            return True
        except TimeoutError:
            sys.stderr.write(f"[REGISTRY] TIMEOUT reached! Pending IDs: {self._active_ids}\n")
            sys.stderr.flush()
            return False


async def stdin_reader(
    send_stream: anyio.streams.memory.MemoryObjectSendStream[SessionMessage | Exception | object],
    registry: RequestRegistry,
) -> None:
    """Reads from stdin and sends messages to the send stream."""
    try:
        while True:
            # Use to_thread to avoid blocking the event loop with sys.stdin.readline
            line = await anyio.to_thread.run_sync(sys.stdin.readline)
            if not line:
                await send_stream.send(SENTINEL_EOF)
                break

            try:
                message = JSONRPCMessage.model_validate_json(line)
                root = message.root
                # Increment registry for every request that requires a response (has an ID)
                if hasattr(root, "id") and root.id is not None:
                    registry.inc(root.id)

                session_message = SessionMessage(message=message)
                await send_stream.send(session_message)
            except Exception as exc:
                await send_stream.send(exc)
    except Exception as e:
        sys.stderr.write(f"Error in stdin_reader: {e}\n")
        sys.stderr.flush()
    # No close() here. Stream closure is managed by the ShutdownCoordinator.


async def stdout_writer(
    receive_stream: anyio.streams.memory.MemoryObjectReceiveStream[SessionMessage | object],
    registry: RequestRegistry,
) -> None:
    """Reads from the receive stream and writes messages to stdout."""
    try:
        while True:
            try:
                session_message = await receive_stream.receive()
            except (anyio.ClosedResourceError, anyio.EndOfStream):
                # Stream closed. This is expected during graceful shutdown.
                break

            if session_message is SENTINEL_SHUTDOWN:
                break

            # Extract the actual message payload
            if hasattr(session_message, "message"):
                payload_obj = session_message.message
            elif isinstance(session_message, dict) and "message" in session_message:
                payload_obj = session_message["message"]
            else:
                payload_obj = session_message

            # Serialize to JSON
            if hasattr(payload_obj, "model_dump_json"):
                serialized = payload_obj.model_dump_json(by_alias=True, exclude_none=True)
            else:
                serialized = json.dumps(payload_obj)

            sys.stderr.write(f"[WRITER] Sending: {serialized}\n")
            sys.stderr.flush()

            # Use print with flush=True to ensure the message is sent immediately
            print(serialized, flush=True)

            # Decrement registry ONLY if this was a response to a request
            # The payload_obj is a JSONRPCMessage (RootModel), so we access
            # the wrapped object via .root
            if hasattr(payload_obj, "root"):
                root = payload_obj.root
                if hasattr(root, "id") and root.id is not None:
                    registry.dec(root.id)
            elif hasattr(payload_obj, "id") and payload_obj.id is not None:
                registry.dec(payload_obj.id)
    except Exception:
        sys.stderr.write(f"[ERROR] stdout_writer failure: {traceback.format_exc()}\n")
        sys.stderr.flush()


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
        if self._read_task is None or self._read_task.done():
            self._read_task = asyncio.create_task(self._read_loop())
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass
        await self._queue.put(None)

    async def _read_loop(self) -> None:
        try:
            buffer = bytearray()
            while True:
                chunk = await self._reader.read(4096)
                if not chunk:
                    break

                buffer.extend(chunk)

                while True:
                    try:
                        start = buffer.find(b"{")
                        if start == -1:
                            break

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
                            break

                        line = buffer[start:end]
                        del buffer[:end]

                        try:
                            data = json.loads(line.decode("utf-8"))
                            rpc_message = JSONRPCMessage(**data) if isinstance(data, dict) else data
                            message = SessionMessage(message=rpc_message)
                            await self._queue.put(message)
                        except (
                            json.JSONDecodeError,
                            UnicodeDecodeError,
                            TypeError,
                            ValueError,
                        ) as e:
                            sys.stderr.write(f"Failed to deserialize MCP message: {e}\n")
                            sys.stderr.flush()
                            continue

                    except Exception as e:
                        sys.stderr.write(f"Unexpected error during buffer parsing: {e}\n")
                        sys.stderr.flush()
                        break
        except asyncio.CancelledError:
            raise
        except (OSError, RuntimeError) as e:
            sys.stderr.write(f"Unexpected error in UDS read loop: {e}\n")
            sys.stderr.flush()
        finally:
            await self._queue.put(None)

    def __aiter__(self) -> AsyncIterator[SessionMessage]:
        async def _gen() -> AsyncGenerator[SessionMessage, None]:
            while True:
                item = await self._queue.get()
                if item is None:
                    break
                yield item

        return _gen()

    async def __anext__(self) -> SessionMessage:
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
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if self._writer:
                self._writer.close()
                await self._writer.wait_closed()
        except (OSError, RuntimeError) as e:
            sys.stderr.write(f"Error closing UDS write stream: {e}\n")
            sys.stderr.flush()

    async def send(self, message: SessionMessage) -> None:
        try:
            if hasattr(message, "message"):
                payload_obj = message.message
            elif isinstance(message, dict) and "message" in message:
                payload_obj = message["message"]
            else:
                payload_obj = message

            if hasattr(payload_obj, "model_dump_json"):
                serialized = payload_obj.model_dump_json()
            else:
                serialized = json.dumps(payload_obj)

            payload = (serialized + "\n").encode("utf-8")
            self._writer.write(payload)
            await self._writer.drain()
        except (OSError, RuntimeError, AttributeError) as e:
            sys.stderr.write(f"Failed to send MCP message: {e}\n")
            sys.stderr.flush()
            raise ConnectionError(f"UDS write failure: {e}") from e


def create_memory_server(core: Any, registry: RequestRegistry) -> Server:
    """
    Creates and configures an MCP server for memory operations.
    """
    server = Server("mega-memory-manager")

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        async with registry:
            return [
                Tool(
                    name="ingest",
                    description="Ingest text into semantic memory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The text"},
                            "tier": {
                                "type": "string",
                                "enum": ["local", "cloud", "auto", "sync"],
                                "description": "The storage tier",
                            },
                        },
                        "required": ["text"],
                    },
                ),
                Tool(
                    name="search",
                    description="Search memory using semantic recall",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The query"},
                            "tier": {
                                "type": "string",
                                "enum": ["local", "cloud", "auto", "sync"],
                                "description": "The storage tier",
                            },
                        },
                        "required": ["query"],
                    },
                ),
                Tool(
                    name="reflect",
                    description="Reflect on a query for high-level context",
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

        try:
            if name == "ingest":
                text = arguments.get("text")
                if text is None:
                    raise ValueError("Missing required argument: 'text'")
                tier = arguments.get("tier", "auto")
                res = await core.ingest(text, tier)
                sys.stderr.write(f"[DEBUG] ingest result: {res}\n")
                sys.stderr.flush()
                return [TextContent(type="text", text=json.dumps(res))]

            elif name == "search":
                query = arguments.get("query")
                if query is None:
                    raise ValueError("Missing required argument: 'query'")
                tier = arguments.get("tier", "auto")
                res = await core.recall(query, tier)
                sys.stderr.write(f"[DEBUG] search result: {res}\n")
                sys.stderr.flush()
                return [TextContent(type="text", text=json.dumps(res))]

            elif name == "reflect":
                query = arguments.get("query")
                if query is None:
                    raise ValueError("Missing required argument: 'query'")
                res = await core.reflect(query)
                sys.stderr.write(f"[DEBUG] reflect result: {res}\n")
                sys.stderr.flush()
                return [TextContent(type="text", text=json.dumps(res))]

            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            sys.stderr.write(f"[ERROR] Tool failed: {traceback.format_exc()}\n")
            sys.stderr.flush()
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

    return server


async def run_socket_server_async(core: Any, socket_path: str) -> None:
    """
    Starts a Unix Domain Socket server using asyncio.start_unix_server.
    """
    registry = RequestRegistry()
    core.registry = registry
    server = create_memory_server(core, registry)

    async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            sock = writer.get_extra_info("socket")
            if sock:
                creds = sock.getsockopt(
                    socket.SOL_SOCKET,
                    socket.SO_PEERCRED,
                    struct.calcsize("iii"),
                )
                pid, uid, gid = struct.unpack("iii", creds)
                current_uid = os.getuid()
                if uid != current_uid:
                    sys.stderr.write(f"Unauthorized connection attempt from UID {uid}.\n")
                    sys.stderr.flush()
                    writer.close()
                    await writer.wait_closed()
                    return
        except (OSError, RuntimeError) as e:
            sys.stderr.write(f"Peer verification failed: {e}\n")
            sys.stderr.flush()
            writer.close()
            await writer.wait_closed()
            return

        client_address = writer.get_extra_info("peername") or "unknown"
        sys.stderr.write(f"New UDS connection established from {client_address}\n")
        sys.stderr.flush()

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
        except BaseException:
            sys.stderr.write(f"Session Error: {traceback.format_exc()}\n")
            sys.stderr.flush()
        finally:
            try:
                client_address = writer.get_extra_info("peername") or "unknown"
                sys.stderr.write(f"Closing connection from {client_address}\n")
                sys.stderr.flush()
            except (OSError, RuntimeError):
                pass

    if os.path.exists(socket_path):
        try:
            os.unlink(socket_path)
            sys.stderr.write(f"Removed existing socket file at {socket_path}\n")
            sys.stderr.flush()
        except OSError as e:
            sys.stderr.write(f"Could not remove socket file: {e}\n")
            sys.stderr.flush()
            raise

    server_instance = await asyncio.start_unix_server(handle_connection, path=socket_path)
    os.chmod(socket_path, 0o600)
    sys.stderr.write(f"MCP UDS Server listening on {socket_path} (Permissions: 0600)\n")
    sys.stderr.flush()

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
    """
    Robust async implementation of the MCP server over Stdio.
    Follows a deterministic shutdown sequence to ensure all requests are completed
    and all output is flushed before exiting.
    """
    registry = RequestRegistry()
    core.registry = registry
    server = create_memory_server(core, registry)
    sys.stderr.write("[DEBUG] Stdio server listening on stdin/stdout\n")
    sys.stderr.flush()

    # 1. Setup transport streams
    inbound_send, inbound_receive = anyio.create_memory_object_stream(100)
    outbound_send, outbound_receive = anyio.create_memory_object_stream(100)

    read_stream = StdioReadStream(inbound_receive)

    # 2. Unified Lifecycle Management
    async with anyio.create_task_group() as tg:
        # Launch transport tasks within the group
        tg.start_soon(stdin_reader, inbound_send, registry)
        tg.start_soon(stdout_writer, outbound_receive, registry)

        try:
            # Execute the MCP protocol
            await server.run(
                read_stream=read_stream,
                write_stream=CloseShieldSendStream(outbound_send),
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
        finally:
            sys.stderr.write("[DEBUG] Server.run() returned. Starting graceful shutdown...\n")
            sys.stderr.flush()

            # A. Close the outbound send stream to signal the writer that
            # no more messages will be sent.
            # This allows the stdout_writer to drain the queue and call
            # registry.dec() for all pending responses.
            outbound_send.close()

            # B. Wait for the writer to finish processing all pending responses.
            await registry.wait_until_empty(timeout=2.0)

            # C. Signal the writer to stop finally.
            # Note: outbound_send is already closed, but we send this to be
            # explicit if the stream supports it.
            try:
                await outbound_send.send(SENTINEL_SHUTDOWN)
            except Exception:
                pass

            # The anyio task group will now implicitly await the stdout_writer
            # to finish its work before exiting this block.

    sys.stdout.flush()
    sys.stderr.write("[DEBUG] Stdio server shut down gracefully\n")
    sys.stderr.flush()
    # Final cleanup of streams
    inbound_send.close()
    outbound_send.close()


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
