# MCP UDS Bridge: Conceptual Model

## Overview
The MCP UDS Bridge is a specialized transport layer that extends the Model Context Protocol (MCP) to support persistent, secure, and multi-client local daemons on Linux.

While the official MCP specification focuses on `stdio` (where a client spawns a server as a child process) and `SSE` (HTTP), the UDS Bridge implements a Unix Domain Socket (UDS) transport. This allows the memory system to exist as a standalone background service (the Daemon) that can be shared across multiple AI sessions and tools without the overhead of repeated process instantiation.

## The "Double-Bridge" Architecture

Because most MCP clients (e.g., Claude Desktop, IDE plugins) are hardcoded to communicate via `stdio`, the system employs a two-stage bridge:

### 1. The Memory Bridge (Proxy)
The Bridge is a lean CLI wrapper that acts as a translator.
- **Input**: It listens to `stdin` from the MCP Client.
- **Output**: It pipes those bytes directly into a Unix Domain Socket.
- **Role**: It satisfies the client's requirement for a `stdio` interface while delegating the actual work to a persistent background process.

### 2. The Memory Daemon (Server)
The Daemon is the authoritative source of truth for the stack's memory.
- **Input**: It listens on a UDS socket (`~/.local/share/megalonyx/sockets/megalonyx_memory.sock`).
- **Output**: It processes MCP requests and returns responses via the same socket.
- **Role**: It manages the `MemoryCore` logic, handles Qdrant connectivity, and maintains state across different AI sessions.

### Data Flow Diagram
`MCP Client` $\xrightarrow{\text{stdio}}$ `Memory Bridge` $\xrightarrow{\text{UDS Socket}}$ `Memory Daemon` $\xrightarrow{\text{Logic}}$ `Vector DB`

## Why This Approach?

### Persistence vs. Ephemerality
In a standard MCP `stdio` setup, the server dies when the client closes. By moving the logic to a UDS Daemon, the `MemoryCore` can perform background tasks (like the "Memory Refinement" pipeline for memory consolidation) independently of whether a user is currently chatting with the AI.

### Multi-Tenancy
A single UDS Daemon can handle multiple concurrent connections. This allows different agents (e.g., a `Researcher` and a `Developer`) to access and update the same semantic memory in real-time without conflicting process locks.

### Resource Efficiency
Spawning a full Python environment and initializing Qdrant connections for every session is expensive. The UDS model initializes the environment once and provides near-instantaneous connectivity via sockets.

## Comparison: Standard MCP vs. UDS Bridge

| Feature | Standard MCP (`stdio`) | UDS Bridge (UDS) |
| :--- | :--- | :--- |
| **Lifecycle** | Ephemeral (tied to client) | Persistent (Background Daemon) |
| **State** | Lost on session end | Preserved across sessions |
| **Connectivity** | 1:1 (Client $\to$ Server) | 1:N (Many Clients $\to$ 1 Server) |
| **Boot Time** | High (Process spawn) | Low (Socket connection) |
| **Security** | Process Isolation | OS-level Identity (`SO_PEERCRED`) |
