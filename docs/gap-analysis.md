# System Gap Analysis

This document maps what Megalonyx inherited from QwenLM/qwen-code, what was added, where
the two systems overlap, and what the plan is for each overlap. It is a living reference --
update it when architectural decisions are made.

---

## Systems from Qwen Code we use directly

These systems arrived via the upstream sync and are used as-is. We do not modify their source.

| System | What it does | How we use it |
|---|---|---|
| Qwen Code CLI (`packages/cli/`) | Terminal AI agent: reads files, runs shells, calls tools | Primary user interface; our agents and MCP servers register with it |
| Tool registry (`packages/core/src/tools/tool-registry.ts`) | Manages available tools per session | Our MCP servers register tools here automatically via MCP discovery |
| MCP client (`packages/core/tools/mcp/`) | Starts and communicates with MCP subprocess servers | Used to connect the CLI to `agent-memory` |
| Skills loader (`packages/core/src/tools/skill.ts`) | Loads `.qwen/skills/` SKILL.md files as callable tools | We add 21 skills to `.qwen/skills/` that are loaded automatically |
| SubAgent tool (`packages/core/src/tools/agent/agent.js`) | Spawns isolated sub-sessions | Used by the control plane to delegate isolated jobs |
| Settings system (`packages/cli/src/config/settings.ts`) | Loads and merges settings layers | We add project-level `config/settings.json` with our providers and MCP server config |
| Python SDK (`packages/sdk-python/`) | Python client library for the CLI API | Available for Python code that needs to interact with the CLI programmatically |

---

## Systems from Qwen Code we partially replace

These systems exist in upstream but we override or extend them.

| System | What it does | What we replace/extend | Why | Status |
|---|---|---|---|---|
| Memory bridge (original `packages/core/src/stdio_socket_relay.py` reference) | Stub for a memory MCP server | Replaced by `agent-memory` -- a full Python MCP server with Qdrant | The upstream stub references a path that doesn't exist; we provide a working implementation | Complete |
| Model provider list | Default set of Qwen-series and compatible models | Extended with LongCat and additional Gemini models in `config/settings.json` | We use providers not in the upstream defaults | Complete |
| `ci.yml` (upstream CI) | Runs upstream test suite | Replaced by `python-quality.yml` | Upstream CI is for their repo structure, not ours | Complete |

---

## Systems from Qwen Code we ignore

These systems exist in upstream but we don't use them. They arrive in the repo with each sync
but nothing in Megalonyx depends on them.

| System | What it does | Why we don't use it |
|---|---|---|
| Qwen OAuth provider | Authentication via Alibaba Cloud OAuth | We use direct API keys to model providers instead |
| Alibaba Cloud Coding Plan integration | Free-tier model access via Alibaba | Not relevant to our provider setup |
| Qwen-series model configs | Upstream's default model list | Overridden entirely by our `settings.json` provider configuration |
| Upstream docs (`docs/users/`, `docs/developers/`, etc.) | End-user and developer docs for qwen-code | We have our own docs; upstream docs describe the upstream product, not ours |

---

## Systems Megalonyx adds

These don't exist in qwen-code. We built them.

| System | What it does | Depends on Qwen Code? | Status |
|---|---|---|---|
| `control-plane-daemon` | Classifies intent, decomposes tasks, routes jobs to models | Yes -- reads settings.json; can spawn CLI subagents | Implemented; boot test pending |
| `agent-memory` | Persistent vector memory via Qdrant; MCP server | Yes -- registers as MCP server in CLI | Implemented; boot test pending |
| `agent-infra` | Shared logging and infrastructure utilities | No | Implemented; used by both services |
| `ExecutionProfileSelector` | Matches task to execution profile from `.qwen/agents/` | Indirect -- profiles list CLI skills | Implemented; integration test pending |
| Upstream ingest pipeline | Quality-gated sync from QwenLM/qwen-code | No | Complete, operational |
| Project standards linter | Enforces naming, config symmetry, code standards | No | Complete, runs in CI |
| Pre-commit hook | Catches lint/standards violations before commit | No | Complete, installed locally |
| 21 custom skills | Task-specific instruction sets in `.qwen/skills/` | Yes -- loaded by CLI skills system | Migrated; not yet integration-tested |
| 20 execution profiles | Model+tool configs per task type in `.qwen/agents/` | Indirect -- profiles configure CLI behavior | Migrated; not yet integration-tested |

---

## Known integration points

Places where Megalonyx code and Qwen Code code meet:

1. **Memory MCP server** -- `agent-memory` runs as an MCP subprocess. The CLI's `McpClientManager` starts it by calling `mega-memory`. Tool calls from the model (`store_memory`, `search_memory`) cross this boundary.

2. **Settings file** -- `config/settings.json` is a project-level settings file that the CLI's settings loader picks up automatically. We use it to inject our model providers, MCP server definitions, and CLI preferences.

3. **Skills** -- Files in `.qwen/skills/` are loaded by the CLI's `SkillTool`. Megalonyx skills appear as callable tools in every CLI session without any code change.

4. **Execution profiles** -- The control-plane-daemon reads `.qwen/agents/` profiles. These profiles list CLI skill names. The skill names must exist in `.qwen/skills/` for the coupling to work.

5. **SubAgent delegation** -- The control-plane-daemon can instruct the CLI to spawn a subagent via the `AgentTool`. This is the main mechanism for the daemon to run work inside a CLI session context.

---

## Planned work

Items in the table above marked as "not yet integration-tested" need boot and smoke tests.
See `todo.md` Phase 3 Step 2 for the boot test plan.

The CLI source is not modified. If a future feature requires changes to the CLI (e.g., a new
tool type, a hook point), the change should go through the upstream contribution process
(`docs/upstream/sync-policy.md`) so it benefits the upstream project and arrives cleanly via
the sync pipeline.
