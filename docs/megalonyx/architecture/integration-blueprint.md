# 🏛️ Sovereign Integration Blueprint: The Unified Engineering Engine (v2.0 - Enterprise Grade)

## 1. Executive Summary
The objective is to transition from a wrapper-based architecture to a **Sovereign Monorepo**. This involves merging the core capabilities of Qwen Code with specialized features from Aider, Cline, OpenHands, OpenCode, OmniRoute, Claw Code, and T3.

To eliminate technical debt and ensure scalability for hundreds of contributors, the project adopts a **"Cellular" architecture**. Each integrated project is treated as an isolated cell with its own dependency graph, wrapped in a standardized **Sovereign Bridge**.

---

## 2. The Architectural Map (Monorepo Structure)

The repository uses **Nx** as a polyglot meta-manager to handle the dependency graph and computation caching.

**Root Path:** `/home/james/Projects/qwen_code_stack/`

```text
/home/james/Projects/qwen_code_stack/
├── .qwen/                       # Global AI context and operational laws
├── docs/                        # System-wide technical documentation
├── tooling/                     # Automation Suite (Foolproof Scripts)
│   ├── build/                   # Unified build scripts
│   └── scripts/                 # sync-upstreams.sh, integrate-package.sh, verify-bridges.sh
├── packages/
│   ├── core/                    # [FORK] Qwen Code Orchestrator (The Brain)
│   │   ├── src/
│   │   │   ├── agent/           # Main agentic loops and state machines
│   │   │   ├── planner/         # High-level task decomposition
│   │   │   └── supervisor/      # Quality control and verification logic
│   │   └── tests/
│   ├── bridge/                  # THE INTEGRATION LAYER (Contracts & Adapters)
│   │   ├── src/
│   │   │   ├── contracts/       # Interface definitions (Execution, Routing, Memory)
│   │   │   └── adapters/        # Concrete adapters (e.g., aider_adapter.ts)
│   │   └── tests/
│   ├── routing/                 # [INTEGRATION] OmniRoute (The Switchboard)
│   │   ├── src/
│   │   │   ├── dispatcher/      # Intent-based routing logic
│   │   │   └── registry/        # Map of available tool capabilities
│   │   └── tests/
│   ├── execution/               # [INTEGRATION] The "Hands" (Action Providers)
│   │   ├── aider/               # Precise diffing and file editing logic
│   │   ├── openhands/           # Sandbox execution and runtime environments
│   │   └── claw/                # Autonomous system-level execution loops
│   ├── interaction/             # [INTEGRATION] The "Face" (User Interfaces)
│   │   ├── t3/                  # Advanced TUI/UX components (See docs/architecture/interaction-plane.md)
│   │   ├── opencode/            # IDE integration and plugins (See docs/architecture/interaction-plane.md)
│   │   └── cline/               # MCP (Model Context Protocol) implementation
│   └── memory/                  # [INTEGRATION] State & Context Management
│       ├── src/
│       │   ├── vector_db/       # Long-term semantic storage
│       │   ├── graph_db/        # Repository structural mapping
│       │   └── session/         # Short-term conversation state
│       └── tests/
├── shared/                      # Common types, utilities, and JSON schemas
│   ├── types/                   # Unified inter-package communication schemas
│   └── utils/                   # Shared logging, file I/O, and network helpers
├── COMPLIANCE.json              # Licensing and Upstream Audit Registry
└── README.md
```

---

## 3. The Integration Engine (The Bridge Layer)

To prevent the `core` from becoming dependent on the internal logic of any single tool, all communication must occur through the **Bridge Layer**.

### A. Dependency Isolation (The Wall)
To prevent "Dependency Hell" (conflicting library versions), we use strict isolation:
- **Python Packages**: Managed via **`uv` workspaces**. Each package in `/packages` has its own `pyproject.toml` and `uv.lock`.
- **TypeScript Packages**: Managed via **`pnpm` workspaces**. 
- **The Bridge**: Uses the **Adapter Pattern**. `core` calls a generic interface; the adapter translates that call into the specific requirements of the target package.

### B. Execution Plane Contract (`IExecutionProvider`)
Standardizes how the system modifies code or runs commands.

**Request Interface:**
- `taskId`: Unique identifier for the operation.
- `operation`: `EDIT` | `RUN` | `CREATE` | `DELETE`.
- `payload`: Includes target files, shell commands, or diff blocks.
- `options`: Timeout settings, `sandbox_id` for isolation, and `dry_run` flag.

**Response Interface:**
- `status`: `SUCCESS` | `FAILURE` | `PARTIAL`.
- `result`: Contains `stdout`, `stderr`, `exit_code`, and a list of `applied_diffs`.
- `snapshot_id`: The Git commit hash resulting from the operation.

### C. Routing Plane Contract (`IRoutingProvider`)
Standardizes how the system selects the best tool for a given task.

**Request Interface:**
- `intent`: Natural language or categorized task intent.
- `complexity`: `LOW` | `MED` | `HIGH`.
- `requirements`: Boolean flags for `requires_sandbox`, `requires_precision`, and `requires_mcp`.

**Response Interface:**
- `target_package`: The specific package to use (e.g., `execution/aider`).
- `confidence`: Probability score (0.0 to 1.0).
- `routing_reason`: Technical justification for the selection.

### D. Memory Plane Contract (`IMemoryProvider`)
Standardizes how the system retrieves architectural context.

**Request Interface:**
- `scope`: `FILE` | `MODULE` | `REPO` | `GLOBAL`.
- `target`: Path or query string.
- `depth`: Recursion depth for dependency mapping.

**Response Interface:**
- `map_data`: AST or Graph representation of the requested scope.
- `summaries`: File-level semantic summaries.
- `tokens_estimated`: Estimated token count for the retrieved context.

---

## 4. Capability Mapping

| Feature | Source Project | Target Package | Responsibility |
| :--- | :--- | :--- | :--- |
| **Precision Diffing** | Aider | `packages/execution/aider` | Surgical file modifications. |
| **Runtime Sandboxing** | OpenHands | `packages/execution/openhands` | Isolated code execution. |
| **Intent Dispatch** | OmniRoute | `packages/routing` | Tool selection and provider routing. |
| **Advanced TUI/UX** | T3 | `packages/interaction/t3` | Primary developer interface. |
| **MCP Support** | Cline | `packages/interaction/cline` | Standardized tool connectivity. |
| **Autonomous Loops** | Claw Code | `packages/execution/claw` | System-level agentic cycles. |
| **IDE Plugins** | OpenCode | `packages/interaction/opencode` | VSCode/JetBrains integration. |
| **Repo-Mapping** | Aider/Qwen | `packages/memory` | Structural codebase mapping. |
| **Orchestration** | Qwen Code | `packages/core` | Supervisor and state management. |

---

## 5. Quality Assurance & Compliance

### A. CI/CD Quality Gates
We use **Nx Change-Detection** to ensure only affected components are tested, keeping the pipeline fast.

**Promotion Criteria:**
- **Feat $\to$ Develop**: 100% pass on package unit tests + Bridge Interface tests + Peer Review.
- **Develop $\to$ Main**: Full regression suite pass + No "Technical Debt" tags + Upstream sync verification.

### B. Licensing Compliance
All merged projects must be registered in `COMPLIANCE.json`. A `check-compliance.sh` script is run as a hard-block in the CI pipeline to prevent forbidden licenses (e.g., proprietary closed-source) from entering the codebase.

### C. Clean-Room Bug Reporting
To ensure upstream authors accept bug reports, we use the **Clean-Room Protocol**:
1. **Isolate**: Clone the upstream repo in a fresh `/tmp` directory.
2. **Mirror**: Checkout the exact commit used in our monorepo.
3. **Reproduce**: Create a minimal reproduction script (`repro.py`) using only upstream dependencies.
4. **Report**: Submit the reproduction script to the original author.

---

## 6. Detailed Execution Roadmap

### Phase 1: Infrastructure Foundation
- Fork Qwen Code as the root repository.
- Initialize **Nx**, **uv**, and **pnpm** workspaces.
- Configure all `upstream-` remotes.

### Phase 2: The Bridge Implementation
- Define the TypeScript/Python interfaces in `packages/bridge/src/contracts/`.
- Implement the first set of adapters for OmniRoute (Routing) and Aider (Execution).
- Verify the `core` can call an Aider-based edit via the Bridge.

### Phase 3: Package Ingestion
- **OmniRoute**: Full merger into `packages/routing`.
- **Aider/OpenHands**: Migration of core logic into `packages/execution`.
- **T3/OpenCode**: Integration of UI components into `packages/interaction`.
- **Claw Code**: Integration of autonomous loops into `packages/execution/claw`.

### Phase 4: Standardization & Polish
- **Rebranding**: Global alignment of identity and naming.
- **CEAP Pass**: Refactor all integrated code to meet token efficiency and "Institutional Tone" standards.
- **Doc Migration**: Convert all external docs into the symmetric documentation standard.

### Phase 5: Full-Stack Verification
- Execute the `MQA-Snapshot-Suite` stress tests.
- Validate the `install.sh` deployment for the entire integrated stack.
- Final symmetry audit of `config/` vs `docs/`.
