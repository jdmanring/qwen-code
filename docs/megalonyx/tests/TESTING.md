# Testing & Validation Strategy

This document outlines the testing and validation framework for the Qwen Code project, ensuring stability across the Source Repository and the Runtime Environment.

## 1. Validation Philosophy

The Qwen Code project employs a **Production-First Validation** approach. Rather than relying solely on isolated unit tests, the system validates its health by performing a real deployment and executing "Smoke Tests" against the installed binaries.

### The Validation Pipeline
The primary entry point for validation is the `install.sh` script. During the `[8/9] Verifying deployment` phase, the installer performs the following checks:

1.  **Environment Sanity**: Verifies core files (e.g., `memory_daemon.py`) and critical Python dependencies (`qdrant_client`, `sentence_transformers`) are present in the isolated virtual environment.
2.  **Service Orchestration**: Launches the background services (Qdrant and Memory Daemon) via `mega-memory-manager`.
3.  **Transport Verification**: Explicitly checks for the existence of the Unix Domain Socket (`/tmp/megalonyx_memory.sock`) to ensure the production transport layer is operational.
4.  **End-to-End Smoke Tests**: Executes the `tests/integration_test_memory.py` suite to verify the functional path from the orchestrator to the vector store.

---

## 2. The Integration Test Suite

The core validation logic resides in `tests/integration_test_memory.py`. This suite is divided into two distinct categories of tests:

### A. Positive Smoke Tests (The "Happy Path")
These tests verify that the system is operational and meets the minimum functional requirements for a successful deployment.
- **Binary Connectivity Test**: Launches the installed `mega-memory-manager` binary and performs an MCP `initialize` handshake. This verifies the wrapper, venv, and `.env` loading.
- **End-to-End Flow**: Executes a full `Ingest` $\rightarrow$ `Search` $\rightarrow$ `Reflect` sequence.
- **Transport Stress Test**: Pushes large payloads (approx 500KB) through the MCP pipe to ensure no truncation or buffer overflows.

### B. Negative Edge-Case Tests (Resilience)
These tests verify that the system handles failures gracefully. They are used for development and regression testing but are separated from the primary "Smoke" path to avoid false negatives during installation.
- **Qdrant Connection Failure**: Forces a connection error by providing an invalid Qdrant URL to ensure the daemon crashes or reports the error correctly.

---

## 3. How to Run Tests

### Full Stack Validation (Recommended)
To verify the entire installation from scratch:
```bash
./install.sh
```

### Targeted Integration Tests
To run the memory integration tests independently (requires the stack to be installed):
```bash
# Using pytest (Recommended for development)
pytest tests/integration_test_memory.py

# Using raw python (Used by the installer)
python3 tests/integration_test_memory.py
```

## 4. Adding New Tests

When adding new functionality to the stack, follow these guidelines:
1. **Add to Smoke Suite**: If the feature is critical for system boot, add a test case to the `run_smoke_tests()` function in `tests/integration_test_memory.py`.
2. **Isolate Edge Cases**: Place resilience and error-handling tests in separate `@pytest.mark` functions to keep the installer's validation path clean.
3. **Verify the Binary**: Always ensure that your test can run against the installed binary in `~/.local/bin/`, not just the source script.
