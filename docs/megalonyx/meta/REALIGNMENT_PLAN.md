# 🗺️ Realignment Roadmap: From Posturing to Functional

This document defines the engineering path to bridge the implementation gaps identified in [IMPLEMENTATION_GAPS.md](/docs/meta/IMPLEMENTATION_GAPS.md). The goal is to move from a collection of independent services to a unified, persistent, and self-verifying system.

---

## 🎯 Objective
**Eliminate the Persistence Gap.** Ensure that every "generation" or "discovery" made by the system is materialized into the Source Repository or Runtime Environment, and that every "standard" is programmatically enforced.

---

## 🛠️ Technical Resolution Path

### 1. Agent Materialization (The "Hand" for Agent Gen)
**Problem**: Generated agents are ephemeral.
**Solution**: Implement a Persistence Layer for `AgentGeneratorService`.
- **Action**: Modify the `create_agent` tool in `packages/core/src/skill_bridge.py`.
- **Logic**:
    1. Call `AgentGeneratorService.generate()`.
    2. Create the directory `config/agents/{name}/`.
    3. Write the `systemPrompt` to `config/agents/{name}/persona.md`.
    4. Write the `description` to `config/agents/{name}/metadata.json`.
- **Success Criteria**: After calling `create_agent`, a new folder and persona file exist in the filesystem, and the agent is immediately available for delegation.

### 2. Mirroring Enforcement (The "Mirroring Loop")
**Problem**: Mirroring check is a manual orphan.
**Solution**: Integrate `symmetry-check.py` into the `S-VERIFY` pipeline.
- **Action**:
    1. Create a new tool `verify_symmetry` that wraps `scripts/symmetry-check.py`.
    2. Update the `S-VERIFY` rule in `config/QWEN.md` to mandate: `Change in config/ => run verify_symmetry => Fail => Correct`.
- **Success Criteria**: Any edit to a configuration file is automatically followed by a mirroring check; the agent cannot mark the task as "completed" until the check passes.

### 3. Memory Deep-Integration (The "Memory Requirement")
**Problem**: Tiered memory is a sidecar, not a core.
**Solution**: Shift from "Available Tool" to "Operational Requirement."
- **Action**:
    1. **Prompt Engineering**: Update the global system prompts to mandate `memory_search` for any query involving "architecture," "policy," or "standard."
    2. **Health Monitoring**: Integrate a `memory_daemon` heartbeat check into the `ControlPlane` startup. If the daemon is offline, the system should attempt a restart via `mega-memory-manager` before proceeding.
- **Success Criteria**: The agent proactively uses memory tools to resolve architectural ambiguities without being explicitly told to do so.

### 4. Source $\to$ Runtime Synchronization
**Problem**: Runtime is stale after Source changes.
**Solution**: Implement a `sync-blueprint` utility.
- **Action**:
    1. Create a script `scripts/sync-blueprint.py` that uses `rsync` to mirror the `config/` and `docs/` directories from the Git root to `~/.local/share/megalonyx/`.
    2. Add `sync-blueprint` as a command in `mega-memory-manager`.
- **Success Criteria**: Running `mega-memory-manager sync` updates the runtime environment to match the current Git state without requiring a full `install.sh` run.

---

## 📅 Execution Priority

| Priority | Task | Target File(s) | Impact |
| :--- | :--- | :--- | :--- |
| **P0** | Agent Persistence | `packages/core/src/skill_bridge.py` | 🔴 Critical (Core Functionality) |
| **P1** | Mirroring Integration | `config/QWEN.md`, `skill_bridge.py` | 🟡 High (System Integrity) |
| **P2** | Memory Mandates | `config/agents/*/persona.md` | 🟡 High (Memory Efficiency) |
| **P3** | Infra Sync | `scripts/sync-blueprint.py` | 🟢 Medium (Developer UX) |

---

## ✅ Verification Matrix (Proof of Life)
A feature is only "Implemented" when it passes this test:
- **Agent Gen**: `User Request` $\to$ `create_agent` $\to$ `ls config/agents/` $\to$ `Verify File Exists`.
- **Mirroring**: `Edit config/settings.json` $\to$ `run symmetry-check` $\to$ `Expect Fail` $\to$ `Edit docs/settings.md` $\to$ `run symmetry-check` $\to$ `Expect Pass`.
- **Memory**: `Ingest "Project X uses React"` $\to$ `Clear Context` $\to$ `Ask "What does Project X use?"` $\to$ `Verify memory_search call`.
