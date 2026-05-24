# Qwen Code Agent Framework

This document describes the Skills and SubAgent system that Qwen Code provides — what it is,
how it works mechanically, and how Megalonyx uses it.

---

## What "agent" means here

In qwen-code, "agent" has two meanings:

1. **The main session** — the interactive loop where the model reads context, calls tools, and responds. This is just "the CLI running."

2. **A SubAgent** — a nested session spawned by the model to handle a specific subtask in isolation. The parent session delegates work to a subagent, waits for the result, and continues.

Skills are a layer below both: they are instruction sets that tell the model *how* to do something, not a separate process.

---

## Skills

### What they are

A skill is a Markdown file (`SKILL.md`) containing a name, a short description, and a block of instructions. When loaded, the skill appears as a callable tool in the model's tool list. The model invokes a skill by name when it judges the skill is relevant to the current task.

### Where they live

Skills are loaded from four locations (higher priority first):

| Level | Path |
|---|---|
| Project | `.qwen/skills/<skill-name>/SKILL.md` in the current working directory |
| User | `~/.qwen/skills/<skill-name>/SKILL.md` |
| Extension | Provided by installed extensions |
| Bundled | Shipped with the qwen-code package |

Megalonyx adds 21 skills to `.qwen/skills/`. These cover things like commit, cron, developer workflows, LSP integration, and MCP operations.

### How they execute

When the model calls a skill tool, the CLI injects the skill's instruction text into the model's context as a system message and then continues the conversation. The skill does not run as a subprocess — it is purely a prompt augmentation that shapes the model's next action.

File: `packages/core/src/tools/skill.ts`

---

## SubAgents

### What they are

A SubAgent is a full nested session: it has its own system prompt, its own tool registry, and its own conversation history. The parent model creates one by calling the `AgentTool` with a task description. The subagent runs to completion, returns a result string, and the parent continues with that result.

### Fork prevention

Subagents cannot spawn further subagents. The `AgentTool` uses `AsyncLocalStorage` to detect when it is already running inside a subagent context and rejects the call. This prevents unbounded recursion.

### Configuration

Subagent tool registries are created via `Config.createToolRegistryForSubagent()`. This gives each subagent an isolated set of tools — state from the parent's tool instances does not leak in.

File: `packages/core/src/tools/agent/agent.js`

---

## Execution profiles (Megalonyx extension)

Execution profiles are a Megalonyx concept layered on top of the Skills system. They live in `.qwen/agents/` as `YAML+Markdown` files. Each profile specifies:

- Which model to use for this type of task
- Which skills to activate
- What the system prompt should emphasize
- When to apply this profile (file patterns, task keywords)

The `ExecutionProfileSelector` in `apps/control-plane-daemon` reads these profiles and selects the right one when the control plane receives a task. The selected profile then influences which model the `ModelRouter` assigns and which skills are pre-loaded into the session.

See `docs/megalonyx/execution-profiles.md` for details.

---

## How Megalonyx uses this framework

| Framework feature | How Megalonyx uses it |
|---|---|
| Skills | 21 custom skills in `.qwen/skills/` add Megalonyx-specific capabilities to every session |
| SubAgents | The control-plane-daemon can instruct the CLI to spawn subagents for isolated subtasks |
| Tool registry | The memory MCP server registers as an MCP tool; agents can read/write memory via tool calls |
| Settings layer | `config/settings.json` (project-level) overrides model providers and MCP server definitions |
