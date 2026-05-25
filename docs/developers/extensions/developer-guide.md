# Extension Developer Guide: Qwen Code

This guide serves as the single source of truth for developing, implementing, and managing extensions for Qwen Code. Extensions allow developers to expand the capabilities of the system—adding tools, specialized agents, and automated workflows—without modifying the core codebase.

---

## 1. Introduction

### What is an Extension?
An extension is a modular, plugin-like package that injects new functionality into Qwen Code. By decoupling specialized logic from the core orchestrator, extensions ensure that the system remains maintainable while allowing for rapid iteration of new features.

### Core Philosophy
- **Non-Invasive**: Extensions should not require changes to the core system files.
- **Self-Documenting**: Every extension provides its own context (`QWEN.md`) so that the AI understands how to use the extension's tools and skills.
- **Portable**: Using variable substitution and standardized manifests, extensions can be shared across different environments and operating systems.

---

## 2. Extension Anatomy

A standard Qwen Code extension follows a specific directory structure to ensure the `ExtensionManager` can correctly parse and load its assets.

### Directory Structure
```text
extension-name/
├── qwen-extension.json      # Core Manifest (Required)
├── QWEN.md                  # AI Context & Operational Law
├── commands/                # CLI Command Definitions
│   └── my-command.md        # Individual command logic
├── skills/                  # Custom Skill Implementations
│   └── data_processor.py    # Logic for a specific skill
├── agents/                  # Specialized Subagent Definitions
│   └── researcher.md        # Persona and instructions for a subagent
└── hooks/                   # Event-Driven Automation
    └── hooks.json           # Trigger and action mappings
```

### Component Roles
- **`qwen-extension.json`**: The entry point. Defines metadata, dependencies, and registers MCP servers, agents, and skills.
- **`QWEN.md`**: The "Brain" of the extension. It provides the AI with the necessary instructions, constraints, and axioms required to operate the extension's features.
- **`commands/`**: A collection of Markdown files. Each file is transformed into a CLI command that the user or the AI can invoke.
- **`skills/`**: Contains the actual implementation logic. Skills are atomic units of work that can be called by agents or commands.
- **`agents/`**: Definitions for specialized personas. These subagents have their own system prompts and focuses, allowing for "Divide and Conquer" task execution.
- **`hooks/`**: Defines automation. When a specific system event occurs (e.g., `file_saved`), the hook triggers a predefined action.

### Integration Levels
To manage conflict resolution and loading priority, all extension-provided assets (skills and subagents) are assigned a `level: 'extension'`. This metadata ensures that project-specific or personal configurations take precedence over extension defaults during the orchestrator's resolution phase.

---

## 3. Configuration Reference: `qwen-extension.json`

The `qwen-extension.json` file is the manifest that tells the `ExtensionManager` what the extension provides.

### Schema Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String | Unique identifier for the extension (e.g., `com.qwen.git-helper`). |
| `name` | String | Human-readable name of the extension. |
| `version` | String | Semantic versioning (e.g., `1.0.0`). |
| `description` | String | Brief explanation of what the extension does. |
| `mcpServers` | Array | List of Model Context Protocol servers to launch for tool provision. |
| `lspServers` | Array | LSP server configurations to provide language intelligence. |
| `contextFileName` | String | Specifies the file (e.g., `QWEN.md`) to be treated as AI context. |
| `agents` | Array | List of agent definitions located in the `agents/` folder. |
| `skills` | Array | List of skill implementations located in the `skills/` folder. |
| `channels` | Array | Configuration for custom communication interfaces (e.g., Telegram). |
| `settings` | Array | Definitions for environment variables and secret management. |
| `config` | Object | Custom key-value pairs used by the extension's internal logic. |

### Example Manifest
```json
{
  "id": "qwen.web-researcher",
  "name": "Web Researcher",
  "version": "1.2.0",
  "description": "Adds web search and synthesis capabilities to Qwen Code.",
  "contextFileName": "QWEN.md",
  "mcpServers": [
    {
      "name": "brave-search",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "${BRAVE_API_KEY}" }
    }
  ],
  "lspServers": [
    {
      "language": "markdown",
      "command": "markdown-lsp"
    }
  ],
  "agents": ["researcher.md"],
  "skills": ["web_scraper.py"],
  "channels": [
    {
      "type": "telegram",
      "botToken": "${TELEGRAM_BOT_TOKEN}"
    }
  ],
  "settings": [
    {
      "name": "Brave API Key",
      "description": "API key for Brave Search",
      "envVar": "BRAVE_API_KEY",
      "sensitive": true
    }
  ],
  "config": {
    "max_results": 5,
    "preferred_domain": "stackoverflow.com"
  }
}
```

### Secret Management
Extensions can define a `settings` array in the manifest to manage environment variables and secrets. Each entry in the `settings` array should include:
- `name`: A human-readable label for the setting.
- `description`: A brief explanation of what the setting is used for.
- `envVar`: The name of the environment variable to be set.
- `sensitive`: (Optional) A boolean. If set to `true`, the value is stored securely in the system keychain. If `false` or omitted, the value is stored in a plain-text `.env` file associated with the extension.

This mechanism allows extension authors to define required credentials without forcing users to manually edit shell profiles.

---

## 4. Development Workflow

### Step 1: Scaffolding
Create the directory structure as outlined in the **Extension Anatomy** section. Start by creating the folder and the mandatory `qwen-extension.json`.

### Step 2: Defining Logic
1. **Tools**: If your extension needs external tools, configure them in the `mcpServers` section of the manifest.
2. **Skills**: Write Python or JS files in `skills/` to handle complex data processing.
3. **Commands**: Create `.md` files in `commands/` to define how users trigger your logic.

### Step 3: Providing AI Context
Write the `QWEN.md` file. This is critical. If the AI doesn't know *why* or *when* to use your extension, the tools will remain dormant. Define:
- **Axioms**: Rules the AI must follow when using this extension.
- **Trigger Conditions**: "When the user asks for X, use the Y tool from this extension."

### Step 4: Installation & Enablement
Extensions can be installed from multiple sources:
- **Local**: Place the folder in the extensions directory.
- **Git/GitHub**: Provide the repository URL.
- **NPM**: Install via package manager.

To activate the extension, add its `id` to the `extension-enablement.json` file:
```json
{
  "enabled_extensions": [
    "qwen.web-researcher"
  ]
}
```

---

## 5. Advanced Topics

### Event-Driven Automation (Hooks)
Hooks allow extensions to react to system events. The `hooks/hooks.json` file maps events to actions.
- **Example**: A hook can be configured to run a "Code Linting" skill every time a file is modified in the workspace.

### Variable Substitution
To ensure extensions work across different machines, Qwen Code supports dynamic variables in the manifest and configuration:
- `${workspacePath}`: Resolves to the absolute path of the current project root.
- `${extensionPath}`: Resolves to the absolute path of the extension's root directory.
- `${CLAUDE_PLUGIN_ROOT}`: Resolves to the base directory where plugins/extensions are stored.
- `${env.VAR_NAME}`: Resolves to a system environment variable.

#### Internal File Transformations
During the loading phase, the `ExtensionManager` automatically performs several transformations on `.md` and `.sh` files to ensure compatibility and functionality:
- **Syntax Conversion**: Markdown code blocks starting with ` ```! ` are converted into the system's internal `!{...}` execution syntax.
- **Path Migration**: References to `.claude` directories are automatically updated to `.qwen`.
- **Transcript Adaptation**: In shell scripts, transcript parsing logic (e.g., filters for `.message.content`) is updated to match the Qwen Code internal format.

### Enablement and Overrides
While extensions are typically enabled globally via `extension-enablement.json`, the system supports **Path-Based Overrides**. This allows you to enable or disable specific extensions based on the current working directory.

For example, you can configure an extension to be active only when working within a specific project directory, preventing unnecessary tool loading in unrelated workspaces.

### Cross-Platform Interoperability
Qwen Code is designed to be an aggregator. It supports the conversion of extensions from other ecosystems:
- **Claude Plugins $\to$ Qwen Extensions**: Maps `plugin.json` to `qwen-extension.json` and converts tool definitions to MCP servers.
- **Gemini Extensions $\to$ Qwen Extensions**: Maps tool-calling schemas to the Qwen skill/agent framework.

To maintain compatibility, Qwen Code continuously updates its internal converters to track changes in the Claude and Gemini plugin specifications. If you are porting an extension, it is recommended to use the standard `qwen-extension.json` format to ensure native performance.

### Verification Checklist for Developers
- [ ] Does `qwen-extension.json` exist and have a unique `id`?
- [ ] Does `QWEN.md` explicitly tell the AI how to use the new tools?
- [ ] Are all paths using variable substitution instead of hardcoded absolute paths?
- [ ] Is the extension listed in `extension-enablement.json`?
