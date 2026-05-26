# 🧪 Testing Framework: Verification and Validation

This document describes the current testing infrastructure of the Runtime Stack.

## 🏗️ The Testing Pyramid

The project employs a multi-tiered testing strategy to ensure stability across the stack.

### 1. Unit Tests
- **Location**: Co-located with source files (e.g., `*.test.ts`).
- **Framework**: Vitest.
- **Focus**: Testing atomic logic, utility functions, and individual tool implementations in isolation.

### 2. Integration Tests (`integration-tests/`)
These tests verify the interaction between multiple components of the system.

#### A. Terminal Capture (TUI Testing)
A specialized suite that tests the actual terminal output and interaction.
- **Mechanism**: Spawns the CLI in a controlled environment and captures the output stream.
- **Scenarios**: Tests complex flows like the `/loop` skill, markdown rendering, and subagent flicker regressions.

#### B. CLI & SDK Tests
Tests the end-to-end behavior of the CLI and the TypeScript SDK, ensuring that API calls result in the expected system state changes.

#### C. MCP Daemon Tests
Verifies the lifecycle of MCP servers, including connection, discovery, and disconnection.

### 3. Fidelity Tests (`tests/fidelity/`)
High-fidelity tests that run against live providers to verify the "real-world" behavior of the system.
- **Routing Tests**: Verifies that the system correctly routes prompts to the intended models.
- **Recall Tests**: Tests the accuracy of memory retrieval from the vector store.
- **Ingest Tests**: Verifies that facts are correctly extracted and stored in memory.

---

## 🛠️ Running Tests

Tests are executed using the following commands:
- `npm test`: Runs all tests.
- `npm test -- <pattern>`: Runs tests matching the pattern.

## 📈 Verification Standards
A feature is considered "Verified" only when:
1. Its unit tests pass.
2. Its integration tests pass in the `terminal-capture` environment.
3. (For core logic) It passes a fidelity test against a live model.
