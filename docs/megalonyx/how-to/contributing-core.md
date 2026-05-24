# Contributing to Mega Code Core

This guide outlines the professional workflow for modifying the core orchestration logic and infrastructure of the Mega Code stack.

## 1. The Architecture

Mega Code is a hybrid system combining a **Node.js Orchestrator** (the brain) and **Python-based Services** (the body).

- **Orchestrator**: Implements the ReAct loops, intent routing, and tool management.
- **Services**: Implements the Semantic Memory system, transport layers, and background daemons.

---

## 2. The "Surgical" Modification Loop

To prevent "Divergence Debt" (where the running system differs from the source code), all core modifications must follow the **Surgical Workflow**.

### Step 1: Experiment in the Lab
1. Use a dedicated **Lab** environment (a clone of the official source) for experimentation.
2. Implement and test your changes in the Lab.
3. Verify the changes using the integration test suite.

### Step 2: Extract the Patch
Once the change is stable:
1. Generate a git patch of the changes:
   ```bash
   git diff main > /path/to/blueprint/patches/feature-name.patch
   ```

### Step 3: Commit to the Blueprint
1. Add the `.patch` file to the `/patches` directory in the Blueprint.
2. Commit the patch to Git:
   ```bash
   git add patches/feature-name.patch
   git commit -m "Core: Implement [feature name] via patch"
   ```

### Step 4: Deploy to the Machine
1. Run the installer from the Blueprint:
   ```bash
   ./install.sh
   ```
2. The installer will rebuild the runtime and apply all patches in the `/patches` folder.

---

## 3. Quality Control & Standards

### Coding Standards
- **Python Services**: Adhere to PEP 8. Use type hints for all function signatures.
- **Node Orchestrator**: Use strict TypeScript where applicable.
- **JSONL Logging**: All core services MUST use the `SystemLogger` for structured event logging.

### Testing Requirements
Any change to the core must be accompanied by a verification test:
1. **Integration Test**: Add a test case to `tests/integration_test_memory.py` or create a new test file in `tests/`.
2. **Smoke Test**: Ensure the change does not break the `install.sh` verification phase.

---

## 4. The "No-Direct-Execution" Rule

**CRITICAL**: The Blueprint is a static definition. **NEVER** execute or test core services directly from the Blueprint directory.

**Wrong**: `python packages/memory_daemon.py`
**Right**: `./install.sh` $\rightarrow$ `mega-memory-manager` (via `~/.local/bin/`)

This ensures that the system you are testing is exactly what will be deployed to other environments.
