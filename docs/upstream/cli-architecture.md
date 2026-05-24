# Qwen Code CLI Architecture

This document describes how the Qwen Code CLI works at the code level. It is written for
Megalonyx maintainers who need to understand what they inherited and where to look when
something in the CLI needs to be understood or modified.

The CLI is a Node.js/TypeScript application. The original README is preserved at
`docs/upstream/qwen-code-readme.md`.

---

## Entry points

| File | Purpose |
|---|---|
| `packages/cli/index.ts` | Executable entry point (shebang). Records a startup timestamp, then calls `main()`. |
| `packages/cli/src/gemini.tsx` | Exports `main()`. Parses arguments, loads settings, initializes the app, and renders the UI. |

The npm package declares `"qwen": "dist/index.js"` as its bin, so the installed command is `qwen`.

---

## Startup sequence

1. `index.ts` records a startup checkpoint (for profiling) and calls `main()`
2. `parseArguments()` in `packages/cli/src/config/config.ts:498` processes argv with Yargs
3. Settings are loaded from user (`~/.qwen/settings.json`), project (`config/settings.json`), and extension layers
4. Subcommand routing: if a known subcommand is matched, it runs and exits; otherwise the interactive session starts
5. The React/Ink UI renders the terminal interface

---

## Subcommands

Registered at `packages/cli/src/config/config.ts:997–1008`:

| Command | What it does |
|---|---|
| `qwen mcp` | Manage MCP server connections |
| `qwen auth` | Configure authentication (API keys, provider selection) |
| `qwen extensions` | Manage extensions |
| `qwen hooks` | Manage lifecycle hooks |
| `qwen channel` | Channel operations |
| `qwen review` | PR review mode |
| `qwen serve` | Run as a server process |

Without a subcommand, `qwen` starts an interactive session. The `-i` flag forces interactive mode even when stdin is piped.

---

## Tool registry

File: `packages/core/src/tools/tool-registry.ts`

The `ToolRegistry` class manages all tools available in a session:

- **Lazy registration** (`registerFactory(name, factory)` at line 274): the tool object is not created until first use. Concurrent calls share one promise to avoid double-initialization.
- **Eager registration** (`registerTool(tool)` at line 223): registers a pre-built tool object directly.
- **Disabled-tools check** (line 215): every registration checks the disabled-tools set before proceeding.
- **MCP collision handling**: when an MCP server advertises a tool with the same name as a built-in, the MCP tool is renamed with a `mcp__servername__` prefix.

Subagent sessions get isolated registries via `Config.createToolRegistryForSubagent()`, which prevents tool state from leaking between agents.

---

## Skills

File: `packages/core/src/tools/skill.ts`

Skills are reusable instruction sets stored in `SKILL.md` files. The `SkillTool` loads them from four levels in priority order:

1. Project level: `.qwen/skills/` in the current working directory
2. User level: `~/.qwen/skills/`
3. Extension level: from installed extensions
4. Bundled: skills shipped with the package

Each skill has a `SKILL.md` manifest with a name, description, and instructions. Skills appear as tools the model can invoke by name.

Activation path: `packages/core/src/skills/skill-activation.ts`

---

## SubAgent tool

File: `packages/core/src/tools/agent/agent.js`

The `AgentTool` lets the model spawn a sub-session that runs with its own context, tools, and instructions. It uses `AsyncLocalStorage` to detect and prevent nested subagent calls, which would cause runaway recursion.

---

## MCP client

File: `packages/core/src/tools/mcp/` (MCP client infrastructure)

The `McpClientManager` maintains connections to MCP servers defined in `settings.mcpServers`. It:
- Starts each MCP server as a subprocess or connects to a running one
- Enforces a budget cap with hysteresis (warns at 75% usage, re-arms at 37.5%)
- Exposes each server's tools into the tool registry under the `mcp__servername__toolname` namespace

---

## Interactive session vs. one-shot

- **Interactive**: the React/Ink UI renders a chat loop; the user types, the model responds, tools execute, repeat.
- **One-shot**: `qwen "do this"` — runs the prompt, executes any tool calls, prints the result, exits.

The routing decision is at `packages/cli/src/config/config.ts:1050`.

---

## What Megalonyx adds on top

Megalonyx does not modify the CLI's TypeScript source. Instead it:

1. Replaces `settings.mcpServers.memory` with the `agent-memory` MCP server (`mega-memory` bin script)
2. Adds execution profiles in `.qwen/agents/` that the `ExecutionProfileSelector` reads to configure model and tool selection per task type
3. Adds skills in `.qwen/skills/` that appear as callable tools inside the CLI

The CLI itself is left untouched so upstream syncs apply cleanly.
