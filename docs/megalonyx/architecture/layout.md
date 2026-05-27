 
# System Layout & Deployment Architecture

This document defines the structural organization of the Mega Code stack, implementing a **Mirror-Destination Layout** to ensure zero cross-contamination between development artifacts and the production runtime.

---

## 1. The Mirror-Destination Layout

The Mega Code stack is divided into two distinct environments: the **Blueprint** and the **Machine**.

### The Blueprint (`[PROJECT_ROOT]`)
The Blueprint is a static, version-controlled definition of the system. It contains the source code, configuration schemas, and deployment manifests. **No code should be executed or tested directly within the Blueprint.**

### The Machine (`~/.qwen` and `~/.local/share/megalonyx`)
The Machine is the active runtime environment. It is a mirrored projection of the Blueprint, deployed via the `install.sh` script.

| Blueprint Path (Source) | Machine Path (Destination) | Purpose |
| :--- | :--- | :--- |
| `config/agents/` | `~/.qwen/agents/` | Agent Personas & Profiles |
| `config/skills/` | `~/.qwen/skills/` | Tool Schemas & Workflow Docs |
| `config/settings.json` | `~/.qwen/settings.json` | User Preferences & Model Config |
| `config/.env` | `~/.qwen/.env` | Secrets & API Keys |
| `packages/` | `~/.local/share/megalonyx/packages/` | Core System Implementation |
| `scripts/` | `~/.local/share/megalonyx/scripts/` | Lifecycle Management Scripts |
| `bin/` | `~/.local/bin/` | Executable Wrappers |

---

## 2. The Two-Pillar Configuration Model

To optimize for AI-agentic operation and security, the system segregates configuration into two "Pillars."

### Pillar 1: The Brain (AI Configuration) $\rightarrow$ `~/.qwen/`
This pillar contains the "Cognitive" layer. It is designed to be easily readable and modifiable by the AI agents themselves.
- **Agents**: Folder-per-entity layout containing `persona.md`.
- **Skills**: Folder-per-entity layout containing `{skill}.yaml` and `SKILL.md`.
- **Settings**: The `settings.json` file defining model providers and global behavior.

### Pillar 2: The Body (Infrastructure) $\rightarrow$ `~/.local/share/megalonyx/`
This pillar contains the "Physical" layer. It is the software implementation that supports the Brain.
- **Services**: The Python implementations of the Memory System and other core daemons.
- **Runtime**: The isolated Python virtual environment (`venv`) and the Qdrant vector database.
- **Binaries**: The compiled or scripted wrappers used to launch the system.

---

## 3. The Layout Manifest

The mapping between the Blueprint and the Machine is not hardcoded in the installer. Instead, it is governed by the **Layout Manifest**: `config/meta/layout.json`.

This JSON file serves as the single source of truth for the deployment process. When the `install.sh` script runs, it reads the manifest to determine exactly which source directories and files should be mirrored to which destination paths.

### Manifest Structure
The manifest organizes mappings into sections:
- `ai_config`: Mappings for the "Brain" pillar.
- `stack_runtime`: Mappings for the "Body" pillar.
- `binaries`: Mappings for the executable wrappers.

---

## 4. Development Protocol: The "No-Direct-Execution" Rule

To prevent "Divergence Debt" (where the running system differs from the source code), the following workflow is absolute:

1. **Modify**: Edit the source code in the **Blueprint**.
2. **Deploy**: Run `./install.sh` to mirror the changes to the **Machine**.
3. **Verify**: Execute and test the system within the **Machine** (e.g., using `mega-memory-manager` or `mega-status`).
4. **Commit**: Once verified, commit the changes back to the Blueprint's Git history.

**NEVER** run `python packages/memory_daemon.py` or similar commands from within the Blueprint directory. Always use the installed wrappers in `~/.local/bin/`.
