#  Testing Pyramid

This document defines the multi-layered testing strategy for the Qwen Code project. We employ a "Testing Pyramid" approach to ensure high confidence in system stability, from individual component logic to full end-to-end user workflows.

##  The Pyramid Structure

The testing suite is organized into four distinct levels, each with increasing scope and fidelity.

| Level | Type | Focus | Environment | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Unit** | Individual functions, classes, and pure logic. | Isolated (No I/O) | Low |
| **2** | **Integration** | Interactions between modules and external services (e.g., MCP, Qdrant). | Controlled (Mocked/Local) | Medium |
| **3** | **Fidelity** | Real-world execution of core services (e.g., daemons) in a sandbox. | Sandbox (Real I/O) | High |
| **4** | **Chaos/E2E** | Full system lifecycle and resilience to failure. | Production-like | Very High |

---

##  Level Details

### 1. Unit Tests
*   **Goal**: Verify the correctness of isolated algorithms and logic.
*   **Scope**: Pure functions, data models, and utility classes.
* **Example**: Testing the parsing logic of a configuration file or a mathematical calculation in a core module.
* **Tooling**: `pytest`.

### 2. Integration Tests
*   **Goal**: Ensure that different modules within the stack communicate correctly.
*   **Scope**: MCP bridge connectivity, database schema migrations, and inter-module dependency resolution.
* **Environment**: Uses mocks or lightweight, local versions of services (e.g., a local SQLite database or a mocked MCP server).
* **Example**: Verifying that the `MCPManager` can correctly discover tools from a mock MCP server.

### 3. Fidelity Tests
*   **Goal**: Verify that the actual service implementations (the "daemons") function correctly in a real environment.
* **Scope**: Lifecycle management (start/stop), socket communication, and actual interaction with local infrastructure (e.g., a local Qdrant instance).
* **Environment**: A controlled sandbox (e.g., using `tempfile` and `sys.path` manipulation) that mimics the production environment without affecting the host system.
* **Example**: Launching the `MemoryDaemon` as a subprocess and verifying it creates a UDS socket and responds to MCP requests.

### 4. Chaos & E2E Tests
*   **Goal**: Validate the entire system from a user's perspective and test its resilience.
* **Scope**: Full installation/uninstallation cycles, complete user "turns" (Ingest $\rightarrow$ Search $\rightarrow$ Reflect), and system recovery from service failures.
* **Environment**: The actual host environment or a high-fidelity replica.
* **Example**: Running `install.sh`, starting the stack via `mega-memory-manager`, performing a full RAG workflow, and then stopping the stack.

---

##  Testing Standards

To maintain high quality, all new features must be accompanied by tests that adhere to these standards:

1.  **Test-Driven Development (TDD) Preferred**: Define the expected behavior through tests before implementing the logic.
2.  **Observability**: Tests must provide clear, descriptive error messages when they fail.
3.  **Independence**: Each test must be idempotent and independent of others. No test should rely on the state left by a previous test.
4.  **Verification Rule**: Every test must follow the `S-VERIFY` protocol: `Action` $\rightarrow$ `Verification Tool` $\to$ `Pass/Fail`.
5.  **Coverage**: Aim for high coverage of critical paths, especially in the `mcp_bridge`, `mcp_daemon`, and `core` modules.
