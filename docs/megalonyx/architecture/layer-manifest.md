# 🏛️ Layer Manifest: The Sovereign Zoning Law

This document defines the architectural boundaries and "zoning laws" for the Megacode monorepo. All code migration and new development must adhere to these constraints to ensure modularity and prevent circular dependencies.

## 🗺️ Monorepo Structure

The monorepo is divided into two primary pillars: **Apps** and **Packages**.

### 1. The App Layer (`apps/`)
**Purpose**: Delivery, Orchestration, and User Interface.
- **Role**: This layer is the "entry point" for the system. It handles user sessions, high-level workflow orchestration, and the final presentation of results.
- **Allowed Contents**: 
    - Application-specific configuration.
    - User interface logic (CLI, Web, etc.).
    - High-level orchestrators (e.g., `qwen-orchestrator`).
- **Dependency Rule**: 
    - ✅ May depend on any `package/`.
    - ❌ May NOT be depended upon by any `package/`.

---

### 2. The Package Layer (`packages/`)
The package layer is further divided into functional tiers to enforce a strict hierarchical flow.

#### A. Core Packages (`packages/core`)
**Purpose**: Pure Domain Logic and Brains.
- **Role**: The absolute foundation of the system. It contains the "intelligence" that is agnostic of how it is delivered.
- **Allowed Contents**: 
    - Permission evaluation systems.
    - Tool scheduling and dispatch logic.
    - Memory management and RAG logic.
    - Shared types and constants.
- **Dependency Rule**: 
    - ❌ Zero dependencies on other internal packages.
    - ❌ Zero dependencies on `apps/`.

#### B. Infrastructure Packages (`packages/infra`)
**Purpose**: System Adapters and Hardware Integration.
- **Role**: Bridges the gap between the Core logic and the actual system environment.
- **Allowed Contents**: 
    - Database adapters (e.g., Qdrant client).
    - Filesystem wrappers.
    - External API clients.
    - OS-level utilities.
- **Dependency Rule**: 
    - ✅ May depend on `packages/core` (primarily for types).
    - ❌ May NOT depend on `apps/`.

#### C. SDK Packages (`packages/sdk-*`)
**Purpose**: Programmatic Bridges and Language Wrappers.
- **Role**: Provides a clean API for external systems or other languages to interact with the Sovereign stack.
- **Allowed Contents**: 
    - Language-specific wrappers (TypeScript, Python, Java).
    - API definitions.
    - Client-side validation.
- **Dependency Rule**: 
    - ✅ May depend on `packages/core` and `packages/infra`.
    - ❌ May NOT depend on `apps/`.

---

## 🔄 Dependency Flow Summary

The allowed flow of dependencies is strictly one-way:

**`apps/`** -> **`packages/sdk-*`** -> **`packages/infra`** -> **`packages/core`**

Any violation of this flow (e.g., a `core` package importing from an `app`) is a critical architectural failure and must be corrected immediately.
