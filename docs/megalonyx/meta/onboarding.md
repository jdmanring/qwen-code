🏛️ 
# Onboarding Guide: Zero-to-One

Welcome to the **Megalonyx**. This guide is designed to take a developer from a fresh `git clone` to a fully operational, high-fidelity agentic environment.

The Megalonyx utilizes a **Blueprint vs. Machine** architecture. You will develop and modify the **Blueprint** (`qwen_code_stack/`) and deploy those changes to the **Machine** (`~/.local/share/megalonyx/` and `~/.qwen/`) using the provided installation scripts.

---

## 1. Prerequisites

Before beginning the installation, ensure your system meets the following requirements:

### Software Requirements
- **Python 3.10+**: The core runtime for the memory system and vLLM.
- **Git**: For repository management and patching.
- **Curl**: Used by the installer to fetch Qdrant and model weights.
- **Bash**: The installation scripts are written for Bash.
- **rsync**: (Highly Recommended) Used for efficient deployment from Blueprint to Machine.

### Hardware & System Dependencies
- **NVIDIA GPU**: Required for `vLLM` and `PyTorch` acceleration. Ensure you have the appropriate NVIDIA drivers installed.
- **CUDA Toolkit**: The system targets `cu130` (CUDA 13.0) for PyTorch.
- **Linux OS**: The current stack is optimized for Linux (Ubuntu/Debian preferred).

---

## 2. Quick Start Sequence

Follow these steps in order to initialize your environment.

### Step 1: Clone the Blueprint
```bash
git clone https://github.com/[your-org]/qwen_code_stack.git
cd qwen_code_stack
```

### Step 2: Initialize Environment Secrets
The system requires API keys for LLM providers and embedding services.
```bash
mkdir -p ~/.qwen
cp .env.example ~/.qwen/.env
```
**Action Required**: Open `~/.qwen/.env` in your editor and fill in your `OPENAI_API_KEY`, `GEMINI_API_KEY`, and any other required tokens.

### Step 3: Execute the Hardened Installer
Run the installation script from the project root. This script handles virtual environment creation, dependency resolution (including strict Torch versioning), and Qdrant deployment.
```bash
./install.sh
```

### Step 4: Verify System Health
Once the installer finishes, use the generated wrapper to check the status of the core services.
```bash
mega-status
```
*You should see `[OK]` for Qdrant and the Memory Daemon.*

---

## 3. Environment Configuration

The system's behavior is governed by two primary configuration files located in the "Brain" directory (`~/.qwen/`).

### `~/.qwen/.env` (The Secret Store)
This file contains sensitive API keys and environment-specific URLs. 
- **QDRANT_LOCAL_URL**: Points to your local vector database (default: `http://localhost:6333`).
- **LLM Keys**: Contains keys for OpenAI, Gemini, and GitHub Models.

### `~/.qwen/settings.json` (The Model Registry)
This file defines which models are used for specific tasks and how the MCP (Model Context Protocol) servers are configured.
- **Changing LLM Providers**: To switch your primary model, modify the `model` field within the relevant provider section of `settings.json`.
- **MCP Server Paths**: The installer automatically converts relative paths in `settings.json` to absolute paths relative to the Machine root to ensure the UI can spawn servers regardless of the current working directory.

---

## 4. The 'First-Boot' Checklist

To ensure your installation is truly "operational," complete the following verification suite:

1. **Service Connectivity**: Run `mega-status`. All core services must be active.
2. **Dependency Integrity**: Verify the Python environment can load critical libraries:
   ```bash
   mega-run-py -c "import torch; import qdrant_client; print('Dependencies OK')"
   ```
3. **Integration Smoke Test**: Run the memory integration test to verify the end-to-end flow from the Blueprint to the Machine:
   ```bash
   mega-run-py tests/integration_test_memory.py
   ```
4. **Manual Ingest**: Attempt to ingest a small piece of documentation into the memory system via the `mega-memory-manager` or a custom script to verify write permissions in `~/.local/share/megalonyx/data/qdrant`.

---

## 5. Troubleshooting Common Failures

### PyTorch / CUDA Version Mismatch
**Symptom**: `ImportError` or `RuntimeError: CUDA error` when running `mega-run-py`.
**Solution**: The installer mandates a specific Torch version (`2.12.0+cu130`). If you have a conflicting global installation, ensure you are using the `mega-run-py` wrapper, which uses the isolated virtual environment. If it still fails, run:
```bash
./install.sh --force-venv
```

### Qdrant Connection Refused
**Symptom**: `mega-status` reports Qdrant as `[OFF]` or `ConnectionRefusedError`.
**Solution**: 
1. Check if Qdrant is running: `ps aux | grep qdrant`.
2. Start the stack: `mega-memory-manager start`.
3. Verify the URL in `~/.qwen/.env` matches the port in `~/.local/share/megalonyx/config/qdrant_config.yaml`.

### Virtual Environment Corruption
**Symptom**: Random `ModuleNotFoundError` despite a successful installation.
**Solution**: Force a synchronization of dependencies:
```bash
./install.sh --sync-deps
```

---

## 6. Developer's First Task

To get comfortable with the workflow, your first task is to implement a "Hello World" Skill.

### The Objective
Create a simple MCP-compatible skill that returns the current system uptime.

### The Workflow: `S-DISCOVER` $\to$ `S-VERIFY` $\to$ `S-CORRECT`

1. **`S-DISCOVER`**:
   - Explore `config/skills/` to see how existing skills are structured.
   - Identify the necessary schema for a new skill in `config/meta/layout.json`.
2. **Implementation**:
   - Create the skill definition in the Blueprint (`config/skills/uptime/`).
   - Deploy the change by running `./install.sh`.
3. **`S-VERIFY`**:
   - Use the `mega-memory-manager` or the AI agent to call the new `uptime` tool.
   - Check the logs in `~/.local/share/megalonyx/logs/` for any execution errors.
4. **`S-CORRECT`**:
   - If the tool fails or returns incorrect data, modify the source in the Blueprint, re-run `./install.sh`, and verify again.

**Remember**: Never modify the files in `~/.local/share/megalonyx/` directly. Always modify the Blueprint and deploy.
