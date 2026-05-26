# 🗺️ Component Map: The Golden Features

This document maps the core architectural pillars of the Runtime Stack to their primary implementation files. This map serves as the reference for the migration to the monorepo structure.

## 🛡️ Permission Classifier
**Purpose**: The central authority for evaluating if a tool call is safe to execute based on the current approval mode.
- **Primary Implementation**: `packages/core/src/permissions/`
- **Key Files**:
    - `permission-manager.ts`: The main evaluator for tool permissions.
    - `denialTracking.ts`: Logic for managing consecutive blocks and failure states.
    - `dangerousRules.ts`: Hardcoded rules for high-risk operations.

## ⚙️ Tool Dispatcher (`CoreToolScheduler`)
**Purpose**: Manages the execution lifecycle of tool calls, coordinating between the LLM's request and the actual execution.
- **Primary Implementation**: `packages/core/src/core/coreToolScheduler.ts`
- **Key Files**:
    - `coreToolScheduler.ts`: The primary scheduler and dispatcher.
    - `coreToolScheduler.test.ts`: The verification suite for dispatch logic.

## 🧠 Memory Bridge (`MemoryManager`)
**Purpose**: Coordinates the "Managed Auto-Memory" system, bridging session history and persistent project memory.
- **Primary Implementation**: `packages/core/src/memory/`
- **Key Files**:
    - `manager.ts`: The central coordinator for memory operations.
    - `store.ts`: Interface for the underlying vector database (Qdrant).
    - `extract.ts`: Logic for pulling facts from turns into memory.
    - `dream.ts`: Logic for periodic memory consolidation and refinement.

---

## 🔗 Relationship Summary
The **Tool Dispatcher** acts as the primary orchestrator. When a tool is requested:
1. It queries the **Permission Classifier** to verify safety.
2. It interacts with the **Memory Bridge** to inject relevant context.
3. It executes the tool and feeds the result back to the **Memory Bridge** for potential extraction.
