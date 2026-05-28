# MCP Daemon Lifecycle

## Overview
The Memory Daemon is the persistent core of the Qwen Code stack. It manages the lifecycle of the `MemoryDaemon` and the MCP transport layer, ensuring that semantic memory is available and consistent across all AI sessions.

## Boot Sequence
The daemon follows a strict startup sequence to ensure that dependencies are ready before the transport layer begins accepting connections.

### 1. Core Initialization
The `MemoryDaemon` is instantiated, setting up:
- **MemoryAuthority**: The logic for tier classification and storage rules.
- **Internal Queue**: A thread-safe queue for asynchronous ingestion.
- **Dream Interval**: Configuration for the periodic memory consolidation process.

### 2. Infrastructure Verification
Before starting the MCP server, the daemon verifies the health of the vector database:
- It attempts to connect to Qdrant and ensure required collections exist.
- **Retry Logic**: It implements a 30-second retry loop to allow Qdrant to boot up (essential for containerized environments).

### 3. Background Worker Deployment
Two daemon threads are launched to handle asynchronous tasks without blocking the MCP server:
- **Ingestion Worker**: Pulls text from the internal queue and writes it to the vector DB.
- **Dream Worker**: Triggers the `dream()` pipeline every hour to deduplicate and prune memories.

### 4. Transport Activation
Finally, the daemon starts the MCP server. Based on the `MCP_TRANSPORT` environment variable, it chooses between:
- **Socket Mode**: Starts the UDS server with `SO_PEERCRED` verification.
- **Stdio Mode**: Starts a standard `stdio` server for direct client interaction.

## Socket Management & Cleanup
Unix Domain Sockets persist as files on the disk even after the process terminates. To prevent "Address already in use" errors on restart, the daemon implements an explicit cleanup phase.

### Cleanup Logic
Before binding to the socket path, the daemon checks for the existence of the socket file:
```python
if os.path.exists(socket_path):
    os.unlink(socket_path)
```
This ensures that the daemon always starts with a fresh socket, regardless of how the previous session ended (e.g., crash, power failure).

## Process Termination
The daemon is designed to be managed by a process manager or a simple shell script. It handles `KeyboardInterrupt` and `SIGTERM` gracefully, ensuring that the `MemoryDaemon` can flush any pending ingestion tasks to the database before exiting.
