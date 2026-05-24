🏛️ 
# System Layout Configuration

## Component Identity
The `layout.json` file is the master mapping for the Megalonyx's deployment. It defines how files in the `config/` and `packages/` directories are mirrored or deployed to the user's home directory for runtime execution.

## Technical Specification
The layout is divided into three primary deployment zones:

### 1. AI Configuration (`ai_config`)
- **Destination**: `~/.qwen`
- **Mappings**: Maps critical agent and system configs (agents, skills, settings, `.env`, and `QWEN.md`) from the repository to the hidden home directory.

### 2. Stack Runtime (`stack_runtime`)
- **Destination**: `~/.local/share/megalonyx`
- **Mappings**: Deploys operational assets including `packages`, `scripts`, `docs`, and `validators`.

### 3. Binaries (`binaries`)
- **Destination**: `~/.local/bin`
- **Mappings**: Maps executable scripts (e.g., `mega-status`, `mega-memory`) to the system path for direct CLI access.

## Interdependencies
- **Installation Script**: The `install.sh` script uses this layout to perform the initial setup and subsequent updates.
- **Runtime Environment**: The system expects these files to exist at the specified destinations to function correctly.

## Symmetry Link
[Original Config: `config/meta/layout.json`](../../config/meta/layout.json)
