# Documentation Index

This is a flat index of every significant documentation file in the repo. An AI reading
this file should be able to predict the contents of any listed document without opening it.

---

## Project overview

| File | What it covers |
|---|---|
| `README.md` | What this repo is, what's in it, how to get started, key files |
| `todo.md` | Current work tracking — what's done and what's next |
| `CLAUDE.md` | AI agent guide — how to operate in this repo without asking questions |
| `QWEN.md` | Qwen Code agent guide — loaded by Qwen Code at session start |

---

## Megalonyx system docs

| File | What it covers |
|---|---|
| `docs/megalonyx/architecture.md` | How the three Python services fit together; data flow; startup order |
| `docs/megalonyx/control-plane-daemon.md` | Intent classification, task decomposition, job routing, module reference |
| `docs/megalonyx/agent-memory.md` | Vector memory service: ingest, search, Qdrant config, WAL recovery |
| `docs/megalonyx/agent-infra.md` | Shared library: SystemLogger, CronManager, GitWorktreeManager |
| `docs/megalonyx/execution-profiles.md` | How execution profiles work; `.qwen/agents/` format; selection logic |
| `docs/megalonyx/settings.md` | Qwen Code runtime settings reference (config/settings.json) |
| `docs/megalonyx/.env.md` | Megalonyx environment variables reference (config/megalonyx/.env.example) |
| `docs/settings.example.md` | Full settings.example.json walkthrough: sections, keys, what uses them |
| `docs/megalonyx/environment-variables.md` | Environment variable reference |

---

## Inherited Qwen Code system docs

| File | What it covers |
|---|---|
| `docs/upstream/cli-architecture.md` | CLI entry points, startup sequence, tool registry, subcommands |
| `docs/upstream/agent-framework.md` | Skills and SubAgent system: how they work, how Megalonyx uses them |
| `docs/upstream/mcp-servers.md` | All bundled MCP servers: what they do, how to configure, how to add one |
| `docs/upstream/provider-system.md` | Model provider configuration: structure, loading, Megalonyx additions |
| `docs/upstream/sync-policy.md` | What we take from upstream, quality gates, contributing fixes back |
| `docs/upstream/qwen-code-readme.md` | Preserved original Qwen Code README |

---

## Gap analysis and architecture decisions

| File | What it covers |
|---|---|
| `docs/gap-analysis.md` | Inherited vs. added systems; integration points; planned work |
| `docs/architecture/component-map.md` | Component dependency diagram |
| `docs/architecture/layer-manifest.md` | Architectural layer definitions |

---

## Engineering standards and operations

| File | What it covers |
|---|---|
| `docs/meta/engineering-standards.md` | Naming requirements, code quality rules — the binding standard |
| `docs/meta/git-strategy.md` | Branch architecture, pipeline flow, upstream contribution workflow |
| `docs/meta/pipeline-runbook.md` | What to do when a pipeline gate fails |
| `docs/meta/failure-mode-analysis.md` | Known failure modes and their mitigations |
| `docs/meta/maintainer-guide.md` | Guide for repo maintainers |

---

## Megalonyx reference docs (migrated from qwen_code_stack)

| Directory | What it covers |
|---|---|
| `docs/megalonyx/meta/` | Project history, implementation gaps, naming standards, system docs |
| `docs/megalonyx/architecture/` | Agent system design, routing, tool isolation, RAG architecture |
| `docs/megalonyx/guidelines/` | Standards for naming, execution, prompting |
| `docs/megalonyx/agents/` | Per-agent documentation for each of the 20 execution profiles |
| `docs/megalonyx/reference/` | Technical reference catalog |
| `docs/megalonyx/models/` | Model provider configuration details |
| `docs/megalonyx/providers/` | Per-provider documentation (Groq, OpenRouter, Gemini, etc.) |
| `docs/megalonyx/explanation/` | Deep-dive explanations of memory, strategy, sync protocol |
| `docs/megalonyx/how-to/` | Procedural guides for common workflows |
| `docs/megalonyx/skills/` | Skill documentation |
| `docs/megalonyx/services/` | Service configuration documentation |
| `docs/megalonyx/schemas/` | Schema definitions |

---

## Inherited Qwen Code user docs (upstream)

These describe the CLI for end users and contributors. Written by the upstream project.

| Directory | What it covers |
|---|---|
| `docs/users/` | End-user guides: configuration, IDE integration, common workflows |
| `docs/developers/` | Extension development, API integration |

---

## Configuration reference

| File | What it covers |
|---|---|
| `.ruff.toml` | Ruff lint configuration: enabled rules, per-file ignores, line length |
| `pyproject.toml` | Python workspace definition, mypy config, package membership |
| `config/settings.example.json` | Full Qwen Code settings template (see `docs/settings.example.md`) |
| `config/megalonyx/.env.example` | Megalonyx environment template (see `docs/megalonyx/.env.md`) |
