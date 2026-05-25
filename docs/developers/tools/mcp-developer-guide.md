# MCP Developer Guide: Building Model Context Protocol Servers

This guide provides the technical blueprint for building your own MCP (Model Context Protocol) servers to extend Qwen Code. While built-in tools are integrated into the core, MCP servers allow you to create decoupled, language-agnostic capabilities that can be shared across different AI clients.

---

## 1. MCP Architecture Overview

The Model Context Protocol is a standardized JSON-RPC 2.0 based protocol that separates the **AI Client** (Qwen Code) from the **Tool Provider** (Your MCP Server).

### The Communication Loop
1. **Discovery**: Upon connection, the client calls `list_tools`. The server returns a list of available tools and their JSON Schemas.
2. **Invocation**: When the model decides to use a tool, the client calls `call_tool` with the tool name and arguments.
3. **Response**: The server executes the logic and returns a `CallToolResult` containing text, images, or other content.

### Transport Layers
Qwen Code supports three primary transport mechanisms:
- **Stdio**: The most common. The server is spawned as a subprocess; communication happens via `stdin` and `stdout`.
- **SSE (Server-Sent Events)**: The server runs as a web service; the client connects via HTTP.
- **Streamable HTTP**: A specialized HTTP streaming transport for high-performance data.

---

## 2. Implementation Blueprint

The most efficient way to build an MCP server is using the official SDKs.

### Recommended SDKs
- **TypeScript/JavaScript**: `@modelcontextprotocol/sdk`
- **Python**: `mcp` (Python SDK)

### Core Development Steps

#### Step 1: Define Your Tool Schemas
Every tool must have a name, a description, and a JSON Schema for its parameters.
- **Name**: Use alphanumeric characters and underscores (e.g., `get_weather_data`).
- **Description**: Be extremely descriptive. The LLM uses this to decide whether to call the tool.
- **Schema**: Use standard JSON Schema (e.g., `type: 'object'`, `properties: { ... }`).

#### Step 2: Implement the Tool Handler
Your server must implement a handler that:
1. Validates the incoming arguments.
2. Executes the business logic (API calls, DB queries, shell commands).
3. Returns a `CallToolResult` (typically a list of content blocks).

#### Step 3: Configure the Server
Set up the transport layer. For a local tool, Stdio is recommended.

---

## 3. Minimal Working Example (TypeScript)

Here is a blueprint for a simple "Note Taker" MCP server.

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { 
  CallToolRequestSchema, 
  ListToolsRequestSchema 
} from "@modelcontextprotocol/sdk/types.js";

// 1. Initialize the Server
const server = new Server(
  { name: "note-taker", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// 2. Define Available Tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "save_note",
      description: "Saves a text note to the local store",
      inputSchema: {
        type: "object",
        properties: {
          content: { type: "string", description: "The text of the note" },
          title: { type: "string", description: "Title of the note" }
        },
        required: ["content", "title"]
      }
    }
  ]
}));

// 3. Implement Tool Logic
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "save_note") {
    const { content, title } = request.params.arguments as { content: string, title: string };
    // Logic to save the note goes here...
    return {
      content: [{ type: "text", text: `Note "${title}" saved successfully!` }]
    };
  }
  throw new Error("Tool not found");
});

// 4. Connect via Stdio
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 4. Deployment and Integration

Once your server is built, you must integrate it into Qwen Code via `settings.json`.

### Local Deployment (Stdio)
For a Node.js server:
```json
"mcpServers": {
  "my-notes": {
    "command": "node",
    "args": ["/path/to/your/server/index.js"],
    "cwd": "/path/to/your/server"
  }
}
```

### Containerized Deployment (Docker)
To ensure dependency isolation, package your server as a Docker image:
```json
"mcpServers": {
  "my-notes-docker": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "my-notes-server:latest"]
  }
}
```

---

## 5. Advanced MCP Patterns

### Rich Content Responses
MCP supports more than just text. You can return:
- **Images**: Using `type: "image"`.
- **Embedded Resources**: Linking to specific files or data URIs.
- **Multi-part responses**: Combining a summary text block with a detailed data block.

### Resource Templates
Instead of just tools, servers can expose **Resources** (read-only data) using URI templates (e.g., `notes://{id}`). This allows the AI to "read" specific data points without executing a tool.

### Security & Trust
- **Trust Mode**: In `settings.json`, setting `"trust": true` for a server bypasses all confirmation prompts for its tools. Use this only for servers you fully control.
- **Environment Variables**: Pass sensitive API keys via the `env` object in the server config to avoid hardcoding them in the server source.

---

## 6. Verification Checklist

- [ ] **Protocol Compliance**: Does the server respond correctly to `list_tools`?
- [ ] **Schema Precision**: Are the input schemas restrictive enough to prevent LLM hallucinations?
- [ ] **Error Handling**: Does the server return clear error messages in the `CallToolResult` instead of crashing?
- [ ] **Transport Stability**: Does the server handle `SIGTERM` and close connections gracefully?
- [ ] **Qwen Integration**: Does the tool appear and execute correctly when verified via the `/mcp` command in the CLI?
