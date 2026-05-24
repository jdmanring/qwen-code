# MCP Test Server Implementation Documentation

## Purpose
This file is a reference for `mcp-test-server.js`, a zero-dependency template used to create mock MCP (Model Context Protocol) servers for E2E testing.

## Logic & Structure
The script implements a basic JSON-RPC 2.0 server over `stdin`/`stdout`:
- **Configuration Section**:
    - `TOOL_DEFINITIONS`: An array of objects defining the tools the server provides, including names, descriptions, and JSON Schema `inputSchema`.
    - `handleToolCall()`: A switch-case function that implements the actual logic for each tool (e.g., the `echo` tool).
- **Protocol Handling**:
    - `initialize`: Handles the initial MCP handshake, returning server info and capabilities.
    - `tools/list`: Returns the list of available tools defined in `TOOL_DEFINITIONS`.
    - `tools/call`: Dispatches tool calls to `handleToolCall()` and returns the result or an error.
- **Transport**: Uses the Node.js `readline` module to process requests line-by-line from `stdin`.

## Usage
- **Testing**: Developers copy this file to create a custom test server, modify the tools, and point to it in `.qwen/settings.json`.
- **Manual Verification**: The server can be tested without the CLI by piping JSON-RPC strings directly into the process.

## Original File
[config/skills/e2e-testing/scripts/mcp-test-server.js](../../config/skills/e2e-testing/scripts/mcp-test-server.js)
