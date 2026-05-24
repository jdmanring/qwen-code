# MCP Transport Blueprint: Custom Transport Implementation Guide

## Introduction
The Model Context Protocol (MCP) SDK (v1.27.1) uses a transport-agnostic design. To implement a custom transport (e.g., Unix Domain Sockets, Named Pipes, Shared Memory), you must implement a **Transport Bridge** that translates raw bytes into the SDK's required **Object Stream** interface.

## 1. The Core Philosophy: Object Streams
The most critical architectural requirement is that MCP sessions do not communicate via byte streams. They communicate via **Object Streams**.

- **Incorrect Assumption**: The `read_stream` is a pipe of bytes that the SDK parses.
- **Correct Reality**: The `read_stream` is an **Asynchronous Iterator** that yields pre-parsed `mcp.shared.message.SessionMessage` objects.

Any custom transport must implement a "Framing Layer" that handles the conversion:
`Raw Bytes` $\rightarrow$ `Framing/Buffering` $\rightarrow$ `JSON Deserialization` $\rightarrow$ `SessionMessage Object` $\rightarrow$ `SDK Session`.

## 2. The Symmetric Interface Requirement
To be compatible with `mcp.BaseSession` (the parent of both `ClientSession` and `ServerSession`), a transport must implement a symmetric interface on both the read and write sides.

### The Read Stream Interface
The `read_stream` must implement:
1. **Async Iterator Protocol**:
   - `__aiter__()`: Must return an async iterator.
   - `__anext__()`: (Or be backed by an `anyio` memory stream) Must yield `SessionMessage` objects.
2. **Async Context Manager Protocol**:
   - `__aenter__()`: Must initialize the transport (e.g., start background read loops).
   - `__aexit__()`: Must clean up resources and signal EOF to the iterator.

### The Write Stream Interface
The `write_stream` must implement:
1. **The Send Method**:
   - `async def send(self, message: SessionMessage)`: Must serialize the `SessionMessage` and write the raw bytes to the transport.
2. **Async Context Manager Protocol**:
   - `__aenter__()`: Initialize the writer.
   - `__aexit__()`: Close the transport gracefully.

## 3. Implementation Blueprint: The "Bridge" Pattern

### The Framing Layer (Read)
Use a background worker task to decouple the raw socket reading from the SDK's consumption.
- **Producer**: A background task that reads raw bytes, buffers them until a frame (e.g., `\n`) is found, and pushes a `SessionMessage` into a memory queue.
- **Consumer**: The `__aiter__` method which simply yields from that memory queue.

### The Serialization Layer (Write)
The SDK provides `SessionMessage` wrappers. The bridge must:
1. Access the inner Pydantic model: `message.message`.
2. Use `.model_dump_json()` for high-performance, type-safe serialization.
3. Append the protocol's framing character (e.g., `\n`).

## 4. Lifecycle & Resource Management
Custom transports must be managed via `AsyncExitStack` or `async with` blocks to prevent resource leaks:
- **Socket Cleanup**: Always `unlink` UDS sockets before binding.
- **Task Cancellation**: Explicitly cancel background read loops in `__aexit__`.
- **Graceful Shutdown**: Await `writer.wait_closed()` to ensure all pending buffers are flushed.

## 5. Verification Checklist
- [ ] Does `read_stream` yield `SessionMessage` objects?
- [ ] Do both streams implement `__aenter__` and `__aexit__`?
- [ ] Does `write_stream` implement `async def send()`?
- [ ] Is the serialization using `.model_dump_json()` on the inner message?
- [ ] Does the `read_loop` handle `asyncio.CancelledError` without crashing the session?
- [ ] Does the "Data Loop" test (Ingest $\rightarrow$ Search $\rightarrow$ Assert) pass?
