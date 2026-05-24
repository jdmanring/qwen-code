# Deployment Guide

This guide explains how to deploy the Mega Code stack from the Blueprint (source) to the Machine (runtime).

## 1. The Deployment Model

Mega Code uses a **Mirror-Destination Layout**. The `install.sh` script reads a layout manifest (`config/meta/layout.json`) and mirrors the Blueprint's configuration and services into the user's home directory.

### Deployment Mapping
- **The Brain (AI Config)** $\rightarrow$ `~/.qwen/`
  - Agent personas, skill definitions, and user settings.
- **The Body (Infrastructure)** $\rightarrow$ `~/.local/share/megalonyx/`
  - System services, Python virtual environment, and Qdrant data.
- **The Wrappers (Binaries)** $\rightarrow$ `~/.local/bin/`
  - Executable entrypoints for the system.

---

## 2. Installation Process

### Prerequisites
- **Python 3.10+**
- **Node.js & npm**
- **Git & Curl**
- **NVIDIA GPU** (Recommended for vLLM/PyTorch acceleration)

### Execution
Run the hardened installer from the project root:
```bash
chmod +x install.sh
./install.sh
```

### Advanced Options
- **Force Config Reset**: To overwrite existing `settings.json` and `.env` with defaults:
  ```bash
  ./install.sh --force-config
  ```

---

## 3. Post-Installation Verification

The installer automatically performs a full-stack verification. A successful installation is indicated by the `[8/9] Verifying deployment` phase passing.

### Manual Verification
If you need to verify the system manually:

1. **Check Service Status**:
   ```bash
   mega-status
   ```
2. **Run Integration Smoke Tests**:
   ```bash
   mega-run-py tests/integration_test_memory.py
   ```

---

## 4. Maintenance & Updates

To apply changes made in the Blueprint to the running Machine:
1. Modify the source code or configuration in the Blueprint.
2. Run `./install.sh`.
3. The installer will mirror the changes and restart the necessary services.

**CRITICAL**: Never modify files directly in `~/.local/share/megalonyx/` or `~/.qwen/` if you intend for those changes to be permanent. Always modify the Blueprint and redeploy.
