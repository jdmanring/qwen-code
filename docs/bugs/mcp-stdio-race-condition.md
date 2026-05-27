# Bug: MCP Stdio Transport Premature Shutdown

## Status: Resolved

### 0. Solid Law of Operation
**NO BLIND ITERATION.**
The developer must not perform a loop of "guess-and-check" (blind iteration) unless specifically called for in a well-thought-out plan. Every change must be based on a verified root cause and a peer-reviewed architectural design.

### 1. Summary
The `MemoryDaemon` fails to deliver responses for tool calls when using the `stdio` transport if the client terminates the session (sends EOF on `stdin`) before the server has finished processing the request.

### 2. Root Cause Analysis (RCA)
The issue is a resource lifecycle mismatch between the MCP SDK and the `anyio` memory streams.

**The Failure Chain:**
1. **SDK Exit**: When `stdin` reaches EOF, the MCP SDK's `server.run()` returns.
2. **Destructive Cleanup**: As part of its exit logic, the SDK calls `.close()` on the `write_stream`.
3. **AnyIO Cascade**: In `anyio.create_memory_object_stream`, closing the `SendStream` immediately causes the `ReceiveStream` to raise `EndOfStream`.
4. **Writer Termination**: The `stdout_writer` (which consumes the `ReceiveStream`) crashes immediately upon receiving `EndOfStream`.
5. **Data Loss**: Because the writer dies *immediately* upon the SDK's exit, any responses still in the memory buffer are discarded. The client receives an abrupt EOF $\to$ `JSONDecodeError`.
6. **Shutdown Crash**: Our `ShutdownCoordinator` then tries to send a `SENTINEL_SHUTDOWN` to the already-closed stream $\to$ `ClosedResourceError`.

### 3. Engineered Solution: The Shielded Transport
To resolve this, we decouple the SDK's cleanup from the transport's actual lifetime.

**A. Ownership Decoupling (`CloseShieldSendStream`)**
We implement a proxy wrapper for the `outbound_send` stream. This proxy intercepts the `.close()` call from the SDK and ignores it, ensuring the stream remains open until the `ShutdownCoordinator` explicitly closes it.

**B. Protocol Compatibility (`StdioReadStream`)**
The SDK requires the `read_stream` to be an `AsyncContextManager`. We implement a hybrid class that satisfies both the `AsyncIterator` (for reading) and `AsyncContextManager` (for cleanup) protocols.

**C. Request Tracking (`RequestRegistry`)**
A registry using an `asyncio.Condition` tracks every active request via an async context manager. The server will not proceed to shutdown until `registry.wait_until_empty()` resolves.

**D. Deterministic Drain Sequence**
The `run_stdio_server_async` coordinator executes this strict sequence:
1. **Launch**: Start `stdin_reader` and `stdout_writer` in a `TaskGroup`.
2. **Execute**: `await server.run(read_stream=StdioReadStream, write_stream=CloseShieldSendStream)`.
3. **Quiesce**: `await registry.wait_until_empty()`.
4. **Signal**: `await outbound_send.send(SENTINEL_SHUTDOWN)`.
5. **Flush**: Exit `TaskGroup` to implicitly await the `stdout_writer` termination.
6. **Cleanup**: Explicitly close all streams.

### 4. Final Resolution & Implementation
The fix was implemented across the following files:
- `packages/memory/memory_transport.py`: Implemented `CloseShieldSendStream`, `StdioReadStream`, and the ID-based `RequestRegistry`. Updated `run_stdio_server_async` to follow the deterministic drain sequence.
- `packages/memory/memory_schema.py`: Updated `MemoryRecord` validation to allow the `"sync"` tier.
- `packages/memory/memory_embeddings.py`: Updated `embed` function to handle the `"sync"` tier (treating it as `local`).
- `packages/memory/memory_daemon.py`: Fixed `NameError` by importing `traceback`.

**Verification:**
- Passed `integration-tests/megalonyx/integration/test_lifecycle.py` with 0 `JSONDecodeErrors`.
- Verified graceful shutdown logs: `[REGISTRY] Registry is now empty. Proceeding with shutdown.` $\to$ `[DEBUG] Stdio server shut down gracefully`.

### 5. Lessons Learned (The Truths)
To prevent a recurrence of this failure mode, the following invariants are now established:

**Truth 1: The SDK Validation Layer is Invisible**
The `mcp` Python SDK performs automatic JSON Schema validation in its `call_tool` decorator *before* the request reaches the handler. If a "Input validation error" appears in logs but not in the project source, it is originating from the SDK's `lowlevel/server.py` using `jsonschema`.

**Truth 2: SDK Cleanup is Destructive**
The MCP SDK's exit logic assumes it owns the transport and closes it immediately. In `anyio` memory streams, this is a destructive operation that kills the reader. Transport ownership must be decoupled via proxies (`CloseShieldSendStream`) to ensure a controlled drain.

**Truth 3: RootModels require `.root`**
Pydantic `RootModel`s (like `JSONRPCMessage`) wrap their data. Attributes must be accessed via `.root` to avoid `AttributeError` or missing data.

**Truth 4: No Blind Iteration**
Guessing where an error originates (e.g., "maybe it's a dynamic string") is a waste of cycles. When a string is missing from the source but present in the logs, immediately audit the installed dependencies (e.g., using a `troubleshooter` agent) to find the exact line of code in `site-packages`.
