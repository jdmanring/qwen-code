# AI Context — Qwen Code

> **The Map.** This document provides the mental model and codebase map for the Qwen Code project.

This fork is a contribution workbench. Every fix, feature, and document defaults to upstream-candidate unless it specifically manages the fork/upstream relationship.

---

## Project Overview

Qwen Code is an AI-powered coding assistant. It is architected as a split between a user-facing CLI and a core orchestration engine.

---

## Code Layout

**Core Packages (`packages/`)**
- `packages/cli`: The frontend. Handles user input (slash commands, @-files), TUI rendering (using Ink), and session management.
- `packages/core`: The backend. Orchestrates LLM API calls, manages prompt construction, and executes tools.
- `packages/core/src/tools/`: The tool library. Individual modules for file system access, shell execution, web fetching, and MCP integration.
- `packages/sdk-typescript`, `sdk-python`, `sdk-java`: SDKs for external integration with the Qwen Code daemon.
- `packages/vscode-ide-companion`: The VS Code extension for IDE-integrated assistance.
- `packages/webui`: A standalone React-based web interface.

**Project Root**
- `docs/`: Technical documentation. `docs/design/` contains the a detailed archive of technical specs.
- `scripts/`: Build and utility scripts.
- `integration-tests/`: End-to-end tests validating the CLI $\rightarrow$ Core $\rightarrow$ LLM flow.
- `Makefile`: The primary orchestration tool for building, testing, and linting.
- `package.json`: Defines the workspace, dependencies, and critical scripts (e.g., `npm run preflight`).

---

## Interaction Flow

```
User (CLI/IDE) → packages/cli → packages/core → LLM API
  → Response streamed back → packages/cli renders to TUI/UI
```

When a tool is required:
`packages/core` $\rightarrow$ `packages/core/src/tools/[tool]` $\rightarrow$ System Execution $\rightarrow$ Result back to Core $\rightarrow$ LLM

---

## Configuration & Data

- **Configuration Layers**: Command-line args $\rightarrow$ Env vars $\rightarrow$ `.qwen/settings.json` $\rightarrow$ `~/.qwen/settings.json`.
- **Sandboxing**: Critical security feature. Controlled via `QWEN_SANDBOX=true` and configured in `package.json` (sandboxImageUri).

---

## Fork Pipeline — Mental Model

The fork uses a structured pipeline to ensure clean upstream contributions:

```
upstream/main → upstream-mirror → origin/ingest → origin/develop → origin/main
                                   ↑
                             contribution branches
```

**Sync upstream changes:**
`upstream/main` → `upstream-mirror` (fast-forward) → `origin/ingest` (reset) → `origin/develop` (merge)

**Create new upstream-candidate work:**
Branch from `origin/ingest` → commit → merge to `origin/develop`.

**Rebase a staging branch:**
Reset to `origin/ingest` and cherry-pick the unique contribution commit(s).

**Release:**
Merge `origin/develop` → `origin/main` (downstream release endpoint).
