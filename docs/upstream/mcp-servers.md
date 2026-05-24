# Bundled MCP Servers

MCP (Model Context Protocol) is a standard for connecting AI models to external tools and data
sources. Each MCP server is a subprocess that the CLI starts and communicates with via JSON-RPC.
The model can call any tool the server advertises.

Servers are configured in `config/settings.json` under `mcpServers`. The example file at
`config/settings.example.json` shows the full configuration.

---

## Servers in use

### filesystem

```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
}
```

**What it does:** Exposes read and write access to the local filesystem as tools. The `.`
argument scopes it to the current working directory. The model uses this to read files,
write files, list directories, and search for patterns.

**Package:** `@modelcontextprotocol/server-filesystem` (official MCP server)

---

### memory

```json
"memory": {
  "command": "mega-memory",
  "args": []
}
```

**What it does:** Runs the Megalonyx `agent-memory` service as an MCP server over stdio.
The model can call `store_memory` to save information and `search_memory` to retrieve
relevant records by semantic similarity.

**Implementation:** `packages/agent-memory/src/agent_memory/memory_mcp_server.py`  
**Bin script:** `bin/mega-memory`

This replaces the original `memory_bridge.py` stub that referenced a non-existent path
in the qwen_code_stack layout. The Megalonyx version is a full implementation.

---

### github

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
}
```

**What it does:** Provides tools for GitHub operations — reading issues, creating PRs,
searching code, listing commits. Requires a personal access token in `GITHUB_TOKEN`.

**Package:** `@modelcontextprotocol/server-github` (official MCP server)

---

### internet-search

```json
"internet-search": {
  "command": "npx",
  "args": ["-y", "tavily-mcp"],
  "env": { "TAVILY_API_KEY": "$TAVILY_API_KEY" }
}
```

**What it does:** Provides web search tools via the Tavily search API. The model uses this
to look up current information, documentation, or anything not in its training data.

**Package:** `tavily-mcp`  
**Requires:** `TAVILY_API_KEY`

---

### code-index

```json
"code-index": {
  "command": "uvx",
  "args": ["code-index-mcp"]
}
```

**What it does:** Indexes the codebase for fast semantic and structural search. Useful
for large repos where the model needs to find symbol definitions or usage patterns across
many files without reading each one.

**Package:** `code-index-mcp` (installed via `uvx`, no prior install needed)

---

## How the CLI handles MCP servers

All MCP connections are managed by `McpClientManager` in `packages/core/`. On session start,
it starts each configured server as a subprocess and discovers its tools via the MCP handshake.

If a server advertises a tool with the same name as a built-in CLI tool, the MCP tool is
renamed to `mcp__servername__toolname` to avoid collision.

The manager enforces a budget cap on tool calls per server. It warns at 75% of the cap and
re-arms the warning at 37.5% — this prevents runaway tool loops from exhausting API credits.

---

## Adding a new MCP server

Add an entry to `config/settings.json` under `mcpServers`:

```json
"my-server": {
  "command": "npx",
  "args": ["-y", "my-mcp-package"],
  "env": { "MY_API_KEY": "$MY_API_KEY" }
}
```

The CLI will start it on next launch and add its tools to the registry automatically.
For a Python-based server using `uv run`, use `"command": "uv"` with `"args": ["run", "python", "-m", "my.module"]`.
