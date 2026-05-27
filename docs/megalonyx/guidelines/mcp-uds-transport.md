# MCP Unix Domain Socket (UDS) Transport Bridge

## Overview
The `mcp` SDK (v1.27.1) is designed around a "stream" abstraction. However, these streams are **not raw byte streams**. They are high-level **Object Streams** that yield parsed MCP messages.

The "Disconnected" state in the UI often occurs when a transport is implemented as a byte pipe, but the SDK expects an object iterator.

## The "A-ha" Moment: Object Streams vs. Byte Streams
The most critical realization when building UDS support is:
**`mcp.client.session.ClientSession` and `mcp.server.Server` expect their read streams to be asynchronous iterators of `mcp.shared.message.SessionMessage` objects, not bytes.**

If you provide a raw byte stream, the SDK will fail with a `TypeError` because it attempts to iterate over the stream (`async for message in self._read_stream`) and expects the resulting objects to have MCP-specific attributes.

## Architecture of the UDS Bridge

### 1. Framing Layer
The MCP protocol uses **newline-delimited JSON (`\n`)** for its raw transport. The bridge must:
- Read bytes from the UDS socket.
- Buffer bytes until a newline is encountered.
- Decode the line to UTF-8.
- Parse the JSON using `mcp.types.JSONRPCMessage.model_validate_json()`.
- Wrap the result in a `mcp.shared.message.SessionMessage`.

### 2. Stream Wrappers
Because the SDK expects specific interfaces, the bridge implements:
- **Read Stream**: An async iterator (`__aiter__`) that yields `SessionMessage` objects.
- **Write Stream**: A wrapper that takes a `SessionMessage`, serializes it to JSON, appends a newline, and writes the bytes to the socket.

#### Critical Serialization Detail
`SessionMessage` is a dataclass wrapper. To send it over the wire, you must serialize the **inner message** (a Pydantic model) using `.model_dump_json()`. 
**Wrong:** `json.dumps(session_message)` $\rightarrow$ `TypeError`
**Right:** `session_message.message.model_dump_json()`

### 3. Lifecycle Management
UDS sockets are files on disk. The bridge must:
- **Server-side**: Unlink (delete) any existing socket file at the path before starting to avoid "Address already in use" errors.
- **Client-side**: Ensure the connection is closed gracefully via an `AsyncExitStack` or async context manager to prevent socket leaks.

## Error Handling and Lifecycle Semantics

The `mcp` SDK's transport layer is designed for robustness in the face of connection instability. Understanding its error propagation model is critical for debugging transport-level issues.

### 1. Task Lifecycle via `anyio.TaskGroup`
The `Server.run` method manages the server's internal lifecycle using an `anyio.TaskGroup`. This group encapsulates several concurrent tasks:
- **The Main Receive Loop**: Continuously reads messages from the transport.
- **Background Task Workers**: Handles the execution of tools, resources, and prompts.

### 2. Error Propagation with `ExceptionGroup`
Because multiple tasks run concurrently within the `TaskGroup`, the SDK uses Python's `ExceptionGroup` to propagate failures. If a background task (e.g., a tool execution) fails or a transport error occurs, the `anyio.TaskGroup` will collect all resulting exceptions and raise them as a single `ExceptionGroup`. This ensures that a failure in one part of the server doesn't silently leave other tasks hanging.

### 3. Swallowing Connection Errors during Writes
To prevent transient network or socket errors from causing unnecessary server crashes, the SDK implements specific handling for write operations. When attempting to send a response, the SDK explicitly catches and "swallows" the following errors:
- `BrokenPipeError`
- `ConnectionResetError`

By swallowing these, the SDK allows the transport layer to handle the disconnection gracefully through the main receive loop, rather than crashing the entire server process immediately upon a failed write.

### 4. Graceful Exit on Transport Error
When a critical transport error occurs (e.g., the socket is closed or becomes unreadable), the following sequence is triggered:
1. The **Main Receive Loop** encounters the error (e.g., an EOF or a `ConnectionError`).
2. The loop exits, which triggers the cancellation of the `anyio.TaskGroup`.
3. All active background tasks are cancelled.
4. The `TaskGroup` finishes, and any remaining errors are propagated via an `ExceptionGroup`.
5. This ensures a clean shutdown of all server components.

## Implementation Pattern


### Server Side
```python
# Use asyncio.start_unix_server
# Wrap the connection in a bridge that yields SessionMessages
# Pass the bridge to server.run(read_stream, write_stream, ...)
```

### Client Side
```python
# Use asyncio.open_unix_connection
# Wrap the connection in a bridge that yields SessionMessages
# Pass the bridge to ClientSession(read, write)
```

## Verification
A successful UDS bridge is verified when:
1. The daemon process is healthy and listening on the `.sock` file.
2. The client can initialize a `ClientSession` without `TypeError` or `ImportError`.
3. A "Data Loop" test (Ingest $\rightarrow$ Search $\rightarrow$ Assert) completes successfully.

---

##  Lessons Learned: The "Broken Pipe" Pitfall

During the implementation of the Memory MCP, we discovered a critical failure mode in the Bridge's I/O implementation.

### The "Greedy Buffer" Problem
If the bridge uses a blocking `read(n)` call (e.g., `await asyncio.to_thread(stdin.read, 4096)`), it will wait until the buffer is full or EOF is reached. 

Because MCP `initialize` requests are small, the bridge sits idle, the UI times out, and the connection is reported as "Offline."

### The Fix: Event-Driven, Non-Blocking I/O
To ensure "instant" connectivity, the bridge **must not** use `readline()` or large `read(n)` calls. Instead, it must use an event-driven model:
1. Set `stdin` to non-blocking mode (`os.set_blocking(sys.stdin.fileno(), False)`).
2. Use `loop.add_reader(sys.stdin.fileno(), ...)` to trigger a callback as soon as *any* byte arrives.
3. Forward the chunk immediately to the UDS socket.

This ensures the bridge is a "zero-latency" proxy that satisfies the strict timing requirements of the MCP handshake.
