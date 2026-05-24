# MCP UDS Transport Specification

## Overview
The UDS Transport layer implements the MCP `BaseSession` interface over Unix Domain Sockets. Since the MCP SDK expects a stream-like interface for reading and writing `SessionMessage` objects, the Sovereign Bridge implements custom stream wrappers that handle the translation between raw socket bytes and structured MCP messages.

## UDSReadStream
The `UDSReadStream` is responsible for converting a raw `asyncio.StreamReader` into an asynchronous iterator of `SessionMessage` objects.

### Architecture
To prevent the server from blocking while waiting for a message, `UDSReadStream` uses a producer-consumer pattern:
1. **The Read Loop (`_read_loop`)**: A background task that continuously calls `reader.readline()`.
2. **The Buffer**: Validated JSON messages are pushed into an `asyncio.Queue`.
3. **The Iterator**: The `__aiter__` method yields messages from the queue to the MCP server.

### Message Framing
The transport uses a **JSON-Lines** format. Each MCP message must be a single line of JSON followed by a newline character (`\n`). 
- **Deserialization Flow**: `Raw Bytes` $\to$ `UTF-8 Decode` $\to$ `json.loads()` $\to$ `JSONRPCMessage` $\to$ `SessionMessage`.
- **Error Handling**: If a line fails to deserialize, the error is logged, and the stream skips to the next line to maintain session stability.

## UDSWriteStream
The `UDSWriteStream` handles the serialization of `SessionMessage` objects back into the socket.

### Serialization Logic
The `send()` method ensures that all messages are compatible with the JSON-Lines requirement:
1. **Payload Extraction**: It extracts the inner `message` object from the `SessionMessage` wrapper.
2. **JSON Encoding**: It uses `model_dump_json()` (for Pydantic models) or `json.dumps()` to create a compact JSON string.
3. **Framing**: A newline character (`\n`) is appended to the end of the string.
4. **Transmission**: The resulting bytes are written to the `asyncio.StreamWriter` and `drain()` is called to ensure delivery.

## Technical Constraints
- **Max Queue Size**: The `UDSReadStream` queue is limited to 100 messages to prevent memory exhaustion during high-volume bursts.
- **Encoding**: All communication is strictly `UTF-8`.
- **Blocking**: Both streams are fully asynchronous, ensuring that the Memory Daemon can handle multiple concurrent client connections without stalling.
