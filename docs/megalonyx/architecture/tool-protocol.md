#  The Tool Protocol: Atomic Execution

This document describes the tool system, the interface between the LLM's reasoning and the underlying operating system and filesystem.

##  Tool Definition & Registry

The Runtime Stack uses a centralized dispatch model for tool execution.

### 1. The Dispatcher
Tool logic is implemented in a hardcoded dispatch block within the `execute_tool` function in `packages/core/src/skill_bridge.py`. This ensures that every tool call passes through a single, auditable point of execution.

### 2. Tool Schema
Tools are Python functions that follow a consistent signature:
- **Input**: A `tool_name` (string) and an `args` dictionary.
- **Output**: A string representation of the result, which is then appended to the LLM's conversation history.

---

##  The Execution Protocol

Every tool call follows a strict security and verification pipeline:

1. **Call Generation**: The LLM outputs a structured JSON-like string: `{"tool": "tool_name", "args": {...}}`.
2. **Parsing**: The `run_job_execution` loop uses a regular expression to extract this JSON from the model's response.
3. **Policy Check**: Before execution, the `PolicyEngine` verifies:
    - **Authorization**: Is this tool permitted for the current `agent_name` and `intent`?
    - **Mutation Guard**: If the tool is a mutation tool (`edit`, `write_file`), does the current mode allow `can_write = True`?
    - **Path Guard**: Is the target file path within the allowed workspace boundaries?
4. **Execution**: The tool logic is executed.
5. **Result Integration**: The output is fed back to the LLM as a `tool` role message.

---

##  MCP (Model Context Protocol) Integration

To extend capabilities beyond the hardcoded Python tools, the Runtime Stack implements the **Model Context Protocol (MCP)**.

### The MCP Manager
The `MCPManager` (`packages/core/src/mcp_manager.py`) allows the system to connect to external MCP servers via:
- **Standard I/O (stdio)**: For local processes.
- **Unix Domain Sockets (UDS)**: For local services.

### Dynamic Tool Discovery
When an MCP server is connected:
1. The system queries the server for its `list_tools` capability.
2. The discovered tools are added to the available toolset for the current session.
3. Tool calls to MCP servers are routed through the `MCPManager`, which handles the JSON-RPC communication with the server.

---

##  Runtime Context & Caching

To optimize token usage and performance, the system employs a `RuntimeContext`:
- **Result Caching**: The results of expensive tools (e.g., `grep_search` on a large codebase) are cached.
- **Context Injection**: The `RuntimeContext` tracks which files have been read, allowing the system to avoid redundant reads in the same turn loop.
