# 🔌 MCP Implementation: The Connection Layer

This document describes the current implementation of the Model Context Protocol (MCP) in the Runtime Stack.

## 🛠️ The MCP Client

The system implements an MCP client in `packages/core/src/tools/mcp-client.ts`. This client is responsible for establishing connections, discovering tools/prompts, and managing the session lifecycle.

### 1. Supported Transports
The current implementation supports the following transport mechanisms:
- **Standard I/O (stdio)**: Used for local MCP servers spawned as child processes.
- **SSE (Server-Sent Events)**: Used for network-based MCP servers.
- **Streamable HTTP**: Used for high-performance HTTP-based MCP servers.

**Note**: Native Unix Domain Socket (UDS) support is not implemented in this client.

### 2. The Connection Lifecycle
1. **Transport Creation**: The `createTransport` function determines the correct transport based on the `MCPServerConfig`.
2. **Connection**: The client establishes a connection and registers its root capabilities (the current workspace directories).
3. **Discovery**: The `discover` method retrieves available tools and prompts from the server.
4. **Registration**: Discovered tools are wrapped in `DiscoveredMCPTool` instances and registered with the global `ToolRegistry`.

### 3. Authentication & OAuth
The system implements a sophisticated OAuth flow for network-based MCP servers:
- **Discovery**: If a 401 error is received, the system attempts to discover OAuth configuration via the `WWW-Authenticate` header or the server's base URL.
- **Authentication**: The `MCPOAuthProvider` manages the OAuth flow, storing tokens in `MCPOAuthTokenStorage`.
- **Token Injection**: Valid tokens are injected into the `Authorization` header of the transport.

---

## 🔄 Tool & Prompt Execution

### Tool Calling
When an MCP tool is invoked:
1. The `McpClient` sends a `tools/call` request to the server.
2. The response is parsed and returned to the LLM.
3. The system supports **Progress Notifications**, allowing MCP servers to send real-time updates on long-running tasks.

### Prompt Invocation
The system can invoke predefined prompts from an MCP server using the `prompts/get` method, allowing the server to provide structured, context-aware prompts to the LLM.

---

## ⚙️ Configuration
MCP servers are configured in `settings.json` with the following parameters:
- `command`/`args`: For stdio servers.
- `url`/`httpUrl`: For network servers.
- `timeout`: Connection and request timeout.
- `trust`: Whether the server is trusted for sensitive operations.
- `oauth`: OAuth configuration (enabled, authUrl, tokenUrl, scopes).
