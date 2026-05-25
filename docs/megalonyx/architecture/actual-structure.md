# 🗺️ Actual Project Structure

This document provides a factual map of the current filesystem state of the `megalonyx-monorepo`.

## 📂 Directory Map

### 1. Root Level
- `config/`: Contains static blueprints for agents and skills.
- `docs/`: All technical and user documentation.
- `packages/`: The core implementation of the system.
- `scripts/`: Utility scripts for maintenance and scaffolding.
- `integration-tests/`: End-to-end and TUI tests.
- `tests/`: Unit and fidelity tests.

### 2. The Core Package (`packages/core`)
The `core` package is the central logic hub.
- `src/core/`: Orchestration logic, LLM clients, and the tool scheduler.
- `src/tools/`: Implementations of atomic tools (e.g., `read-file.ts`, `shell.ts`) and the MCP client.
- `src/memory/`: Logic for the memory bridge and vector store interaction.
- `src/permissions/`: Permission evaluation and classifier logic.
- `src/utils/`: Shared utility functions and schema validators.

### 3. Other Packages
- `packages/cli/`: The command-line interface implementation.
- `packages/sdk-typescript/`: The TypeScript SDK for programmatic access.
- `packages/acp-bridge/`: The bridge between the ACP protocol and the internal core.
- `packages/webui/`: The web-based user interface.

---

## 🔗 Dependency Flow (Actual)

The current flow of dependencies is:
**`packages/cli` / `packages/webui`** $\to$ **`packages/core`** $\to$ **`System / OS`**

MCP servers are treated as external extensions and are connected dynamically via the `McpClient` in `packages/core/src/tools/`.
