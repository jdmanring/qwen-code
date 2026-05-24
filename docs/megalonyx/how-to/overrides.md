# Override Mechanisms

Mega Code provides several ways to customize system behavior without modifying the core Blueprint.

## 1. Primary Configuration Overrides

The system uses a two-tier configuration model to separate defaults from user-specific overrides.

### `settings.json` (User Preferences)
Located at `~/.qwen/settings.json`, this is the primary source of truth for:
- Model provider selection and API endpoints.
- Memory routing policies.
- Tool approval modes.

### `.env` (Secrets & Keys)
Located at `~/.qwen/.env`, this file stores sensitive information:
- API Keys (Gemini, OpenAI, etc.).
- Database credentials.
- Private environment flags.

---

## 2. Behavioral Overrides

### `QWEN.md` (The Law)
The `QWEN.md` file in the project root acts as a live override for the primary agent's system prompt.
- **Merging**: This file is merged into the agent's persona at startup.
- **Usage**: Use this to add project-specific rules, coding standards, or temporary behavioral constraints.

---

## 3. Deployment Overrides

### The Layout Manifest
If you need to change where the system is installed on your machine, modify `config/meta/layout.json`. The `install.sh` script will respect these mappings during the next deployment.

---

## 4. Summary Table

| Override Target | File | Location | Effect |
| :--- | :--- | :--- | :--- |
| **System Settings** | `settings.json` | `~/.qwen/` | Changes model, memory, and tool config. |
| **Secrets** | `.env` | `~/.qwen/` | Updates API keys and sensitive tokens. |
| **Agent Behavior** | `QWEN.md` | Project Root | Overrides the core system prompt. |
| **Install Paths** | `layout.json` | `config/meta/` | Changes where the "Body" is deployed. |

**Important**: Avoid modifying files in `~/.local/share/megalonyx/` directly. These files are overwritten during every `install.sh` run. Always use the Blueprint or the `~/.qwen/` config files.
