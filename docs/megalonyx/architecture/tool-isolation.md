 
# Tool Isolation: WASM Sandboxing

This document defines the technical specification for the isolation of tool execution within the `qwen_code_stack` using WebAssembly (WASM).

## 1. Objective
To prevent "Execution Plane" escapes and ensure that AI-invoked tools cannot modify the host system or the Blueprint directory unless explicitly authorized.

## 2. The Isolation Architecture

The system implements a **Sandbox-by-Default** policy. Every tool call is executed within a lightweight, non-persistent WASM runtime.

### 2.1 The Sandbox Lifecycle
1. **Instantiation**: When a tool is called, the `MCPManager` spawns a fresh WASM instance.
2. **Capability Injection**: The instance is granted a minimal set of capabilities (e.g., read-only access to specific files, network access to a specific endpoint).
3. **Execution**: The tool logic runs within the WASM VM.
4. **Teardown**: Upon completion or timeout, the entire instance is destroyed, wiping all transient state.

### 2.2 Security Boundaries
- **File System**: Tools cannot access the host file system directly. They interact with a virtual file system (VFS) provided by the sandbox.
- **Network**: All network calls are intercepted by a proxy that enforces a strict allow-list of domains.
- **Memory**: The WASM VM provides a hard memory limit to prevent Denial-of-Service (DoS) attacks via memory exhaustion.

## 3. Integration with the MCP Bridge

The `MCPManager` acts as the sandbox orchestrator:
- **WASM Wrapper**: It wraps standard Python/Rust tools in a WASM-compatible binary.
- **Resource Accounting**: It tracks the CPU and memory usage of each tool call, providing telemetry to the Orchestrator.

## 4. Implementation Status
- **[Current]**: Tools run in the same process or via standard subprocesses with limited environment variables.
- **[Target]**: Full WASM-based isolation for all `S-EXEC` tools, providing a mathematically provable security boundary.
