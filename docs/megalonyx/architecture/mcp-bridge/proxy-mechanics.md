# MCP Bridge Proxy Mechanics

## Overview
The `memory_bridge.py` is a high-performance proxy designed to translate `stdio` (Standard Input/Output) traffic into Unix Domain Socket (UDS) traffic. This allows the system to present a standard MCP server interface to clients while delegating the actual logic to a persistent background daemon.

## Non-Blocking Stdin Handling
A primary challenge in `stdio` proxies is that `sys.stdin.read()` is a blocking operation. If the bridge simply waited for input, it would freeze the entire `asyncio` event loop, preventing the bridge from piping responses from the UDS socket back to the client.

### The `StdioReader` Implementation
To solve this, the bridge implements a custom `StdioReader`:
1. **Non-Blocking Mode**: It calls `os.set_blocking(sys.stdin.fileno(), False)` to ensure that reads return immediately even if no data is available.
2. **Event Loop Integration**: It uses `loop.add_reader(sys.stdin.fileno(), callback)`, telling the `asyncio` loop to trigger the `_handle_read` callback only when the OS signals that data is actually available on the stdin file descriptor.
3. **Queueing**: Data is pushed into an `asyncio.Queue`, allowing the `pipe_stdio_to_uds` loop to `await` new input without blocking other tasks.

## The Piping Logic
The bridge runs two concurrent asynchronous loops:

### 1. Stdin $\to$ UDS (`pipe_stdio_to_uds`)
- Awaits data from the `StdioReader`.
- Writes the raw bytes directly to the UDS `asyncio.StreamWriter`.
- This is a "transparent pipe"—the bridge does not inspect or modify the MCP messages; it simply moves the bytes.

### 2. UDS $\to$ Stdout (`pipe_uds_to_stdio`)
- Awaits data from the UDS `asyncio.StreamReader`.
- Writes the bytes directly to `sys.stdout.buffer`.
- Uses `stdout_buffer.flush()` to ensure that the MCP client receives the response immediately without buffering delays.

## Process Lifecycle & Safety
Because the bridge is spawned as a child process of an MCP client (e.g., Claude Desktop), it is susceptible to "orphanage" if the client crashes without properly closing the process.

### Parent Death Signal (`pdeathsig`)
The bridge uses a Linux-specific kernel feature to ensure it never becomes a zombie process:
- **Mechanism**: It calls `libc.prctl(PR_SET_PDEATHSIG, SIGTERM)`.
- **Effect**: The Linux kernel is instructed to send a `SIGTERM` signal to the bridge process the moment its parent process terminates.
- **Result**: The bridge cleans up its socket connections and exits immediately when the client dies, ensuring system resources are reclaimed.

## Summary of the Proxy Flow
`Client Stdin` $\to$ `StdioReader (non-blocking)` $\to$ `UDS Writer` $\to$ `Daemon` $\to$ `UDS Reader` $\to$ `Stdout Buffer` $\to$ `Client Stdout`
