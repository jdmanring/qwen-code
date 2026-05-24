# Megalonyx — System Overview

## Purpose

This system extends Qwen Code into a persistent AI memory and retrieval system. It implements a **Three-Layer Memory Hierarchy** to separate behavioral rules from technical knowledge:

1. **Instructional Memory**: Rules and constraints defined in `QWEN.md`.
2. **Semantic Memory**: Facts and history stored in Dual Qdrant vector databases.
3. **Ephemeral Memory**: The immediate session context window.

This architecture enables:
- Fast local semantic memory
- High-quality cloud semantic memory
- Tool-based retrieval inside Qwen Code

For a detailed explanation of how the agent cognitively interacts with this system, see [Memory Intelligence: From Tools to Cognition](memory-intelligence.md) and the [Memory Taxonomy](memory-taxonomy.md).

---

## Core Capabilities

The Qwen Code stack provides a comprehensive set of agentic coding features:

- **Autonomous Workflows**: Advanced coding agent loops and planning cycles.
- **Intelligent Tooling**: Native tool calling and MCP integration for extended capabilities.
- **Deep Repo Understanding**: Comprehensive codebase analysis and semantic search.
- **Direct Execution**: Terminal execution and autonomous file modifications.
- **Iterative Development**: Multi-file modification and automated debugging loops.
- **Context Management**: Sophisticated context handling and persistent memory.
- **Local-First Design**: Fully local execution with self-host compatibility.

---

## Architecture


Qwen Code CLI
↓
MCP Servers
↓
Embedding Router (single source of truth)
↓
┌──────────────────────────┐
│ LOCAL RAG │
│ MiniLM (384 dims) │
│ Qdrant local │
└──────────────────────────┘
┌──────────────────────────┐
│ CLOUD RAG │
│ Gemini Embedding 2 │
│ Qdrant cloud │
└──────────────────────────┘


---

## Core Components

### 1. Qwen Code CLI
Main agent runtime.

### 2. MCP Layer
Connects tools:
- filesystem
- github
- memory
- qdrant-local
- qdrant-cloud

### 3. Embedding Router
Single file controlling embedding logic:

embedding-router.py


### 4. Vector Databases
- Local Qdrant (fast, offline)
- Cloud Qdrant (high quality, remote)

