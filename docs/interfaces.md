# Interface Specification

This document defines the communication protocols and data schemas used between the Qwen Code CLI and the Megalonyx Control Plane Daemon.

## 1. Communication Transport

The system supports two primary transport mechanisms for communication between the CLI (Client) and the Daemon (Server).

### Unix Domain Sockets (UDS)
The primary transport for persistent daemon communication. 
- **Socket Path**: Defined in configuration, typically `megalonyx_memory.sock`.
- **Security**: Implements `SO_PEERCRED` verification to ensure that only the user who started the daemon can connect to the socket.
- **Usage**: Used by the CLI to forward user prompts and by the Daemon to coordinate with the Memory MCP server.

### Standard I/O (stdio)
Used as a fallback or for direct process-to-process communication during initial boot or specific tool executions.
- **Protocol**: Line-delimited JSON.

---

## 2. Request/Response Schemas

### Task Intake Request
When the CLI forwards a user prompt to the Control Plane, it uses the following structure:

```json
{
  "sessionId": "string",
  "prompt": "string",
  "context": {
    "current_file": "string | null",
    "selected_text": "string | null",
    "cwd": "string"
  },
  "options": {
    "force_decomposition": "boolean",
    "risk_profile": "string"
  }
}
```

### Task Intake Response
The Control Plane responds with the classified intent and the decomposed job sequence:

```json
{
  "sessionId": "string",
  "intent": {
    "type": "string", 
    "confidence": "float",
    "risk_level": "low | medium | high"
  },
  "jobs": [
    {
      "id": "string",
      "skill": "string",
      "params": {
        "key": "value"
      },
      "verification_criteria": "string",
      "status": "pending | in_progress | completed | failed"
    }
  ],
  "status": "processing | complete | error",
  "error": "string | null"
}
```

---

## 3. Agent Memory MCP Contract

The `agent-memory` service implements the Model Context Protocol (MCP). The following tools are exposed to the Control Plane.

### `ingest`
Stores a piece of semantic memory.
- **Arguments**:
  - `text` (string): The content to be remembered.
  - `metadata` (object): Optional tags or source information.
- **Returns**: `success: boolean`

### `search`
Retrieves the most relevant memories based on semantic similarity.
- **Arguments**:
  - `query` (string): The search string.
  - `limit` (integer): Number of results to return.
- **Returns**: `results: Array<{text: string, score: float, metadata: object}>`

### `reflect`
Synthesizes a high-level summary of existing memories to provide broad context.
- **Arguments**:
  - `query` (string): The topic to reflect upon.
- **Returns**: `summary: string`
