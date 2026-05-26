# Transport Comparison: Standard MCP vs. UDS Bridge

## Engineering Justification
The decision to implement a custom UDS Bridge instead of using the official MCP `stdio` transport was driven by three primary engineering requirements: **Persistence**, **Concurrency**, and **Security**.

## Detailed Comparison

### 1. Lifecycle & State
- **Standard MCP**: The server is a child process of the client. When the client (e.g., Claude Desktop) is closed, the server is killed. Any in-memory state, cached embeddings, or active background tasks are lost.
- **UDS Bridge**: The server is a system daemon. It exists independently of any client. This enables "The Dreaming Pipeline"—a background process that consolidates memories while the user is offline.

### 2. Connection Topology
- **Standard MCP**: 1:1 Relationship. One client $\to$ One server process. If you have three different AI tools using the same memory, you must spawn three identical server processes, tripling the RAM usage.
- **UDS Bridge**: 1:N Relationship. Many clients $\to$ One server daemon. All tools share a single, efficient connection pool to the vector database.

### 3. Performance Overhead
- **Standard MCP**: Every session start requires a full Python interpreter boot, environment variable loading, and Qdrant connection handshake.
- **UDS Bridge**: The daemon is already running. The "Bridge" is a lightweight byte-proxy. Connection time is reduced from seconds to milliseconds.

### 4. Security Model
- **Standard MCP**: Relies on process isolation. The client has full control over the server's environment.
- **UDS Bridge**: Implements kernel-level identity verification. By using `SO_PEERCRED`, the daemon can prove exactly who is connecting to it, providing a higher level of assurance for shared local environments.

## Summary Matrix

| Metric | Standard `stdio` | UDS Bridge | Winner |
| :--- | :--- | :--- | :--- |
| **Boot Latency** | High (Process Spawn) | Low (Socket Connect) | **UDS Bridge** |
| **Memory Footprint** | Linear (per client) | Constant (one daemon) | **UDS Bridge** |
| **State Persistence** | Ephemeral | Permanent | **UDS Bridge** |
| **Implementation Complexity** | Low (SDK Native) | High (Custom Proxy) | **Standard** |
| **Local Security** | Basic | Hardened (`SO_PEERCRED`) | **UDS Bridge** |

## Conclusion
While the standard MCP transport is sufficient for simple tool-use, it is inadequate for a professional AI memory stack. The UDS Bridge is a necessary architectural investment to support the persistence and efficiency required for a production-grade agentic system.
