# Bug: MCP Stdio Transport Premature Shutdown

## Status: Open / Under Investigation

### 1. Summary
The `MemoryDaemon` fails to deliver responses for tool calls when using the `stdio` transport if the client terminates the session (sends EOF on `stdin`) before the server has finished processing the request.

### 2. Root Cause Analysis (RCA)
The issue stems from the interaction between the `mcp` library's session lifecycle and the asynchronous nature of the `MemoryDaemon`'s tool handlers.

**The Failure Chain:**
1. **Request Initiation:** The client sends a `CallToolRequest`. The `mcp` server spawns an async task to handle this request.
2. **Offloading:** The handler offloads heavy CPU work (embedding generation) to a `ThreadPoolExecutor` via `asyncio.to_thread` or `run_in_executor`.
3. **Client EOF:** The client closes the `stdin` stream (EOF).
4. **Aggressive Cancellation:** The `mcp` library's `Server.run` loop detects the EOF and immediately calls `tg.cancel_scope.cancel()` on its internal task group.
5. **Handler Termination:** The tool handler task is cancelled. Even if the underlying thread is still working, the coroutine awaiting that thread is terminated.
6. **Transport Closure:** The `stdio_server` context manager exits, closing the `stdout` stream.
7. **Result Loss:** The result of the embedding work is never sent to the client. The client receives an empty response, leading to a `JSONDecodeError`.

### 3. Observed Symptoms
- `integration-tests/megalonyx/integration/test_lifecycle.py` fails with `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.
- Server logs show `[DEBUG] Stdio server shut down gracefully` immediately after `Processing request of type CallToolRequest`, but before the actual work (e.g., Qdrant HTTP requests) completes.

### 4. Impact
- High: The `stdio` transport is unreliable for any tool that takes significant time to execute.
- Low: The Unix Domain Socket (UDS) transport is unaffected as it does not rely on `stdin` EOF for session termination.

### 5. Proposed Resolution Path
- **Phase 1:** Document the failure and map the current system.
- **Phase 2:** Evaluate architectural fixes (e.g., `GracefulServer` override, `asyncio.shield` with a blocking shutdown gate, or process isolation).
- **Phase 3:** Implement the approved fix and verify via regression testing.
