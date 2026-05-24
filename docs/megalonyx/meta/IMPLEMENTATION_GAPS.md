# 🚩 Implementation Gaps Ledger

This document serves as a technical audit of the "Implementation Gap" between the project's documented claims (`README.md`, `ROADMAP.md`) and the actual functional reality of the codebase. 

**Status**: Active Audit
**Last Updated**: 2026-05-21

---

## 📉 The Core Failure: The Persistence Gap
The system suffers from a systemic lack of **Persistence**. While "Services" (the brains) are implemented, the "Connectors" (the hands) that commit changes to the Blueprint or Machine are missing. The system operates in an "Ephemeral State" where high-value generation happens in memory but is never materialized.

---

## 🔍 Granular Gap Analysis

### 1. Agent Generation System (`AgentGeneratorService`)
- **Claim**: "Synthesizes system prompts via LLM."
- **Reality**: **Ghost Feature.**
- **The Gap**: 
    - The `create_agent` tool in `skill_bridge.py` calls the service and receives a valid JSON configuration (`name`, `description`, `systemPrompt`).
    - **Break**: The tool returns this JSON to the LLM as a string. It **does not write** the configuration to `config/agents/{name}/persona.md`.
    - **Result**: The "generated agent" only exists for the duration of that specific tool response. It cannot be called in the next turn because it was never saved to the project structure.
- **Criticality**: 🔴 High

### 2. Cognitive-Symmetry Framework (`symmetry-check.py`)
- **Claim**: "Symmetry between config/ and docs/ => Verified by Symmetry Linter."
- **Reality**: **Orphan Tool.**
- **The Gap**: 
    - The `symmetry-check.py` script is technically sound and works.
    - **Break**: There is no trigger in the `ControlPlane` or `skill_bridge` that mandates this check. The LLM is not instructed to run it after modifying `config/`.
    - **Result**: Symmetry is a manual opt-in rather than a systemic guarantee.
- **Criticality**: 🟡 Medium

### 3. Tiered Semantic Memory (Qdrant/MemoryDaemon)
- **Claim**: "Persistent, tiered semantic memory."
- **Reality**: **Fragile Pipeline.**
- **The Gap**: 
    - The `memory_daemon` and `MemoryAuthority` logic is implemented.
    - **Break**: 
        1. **Health Blindness**: The orchestrator assumes the memory daemon is running. If it crashes, the tools simply return errors without a recovery trigger.
        2. **Incentive Gap**: The core system prompts do not mandate the use of `memory_ingest` or `memory_search` for architectural truths, leading the agent to rely on its own (limited) context window instead of the tiered memory.
    - **Result**: The memory system is a "sidecar" that is rarely utilized by the primary agent.
- **Criticality**: 🔴 High

### 4. Reproducible Infrastructure (Blueprint $\to$ Machine)
- **Claim**: "Mirroring: `install.sh` materializes the Blueprint into the Machine."
- **Reality**: **One-Way Street.**
- **The Gap**: 
    - `install.sh` works for initial deployment.
    - **Break**: There is no `sync` or `deploy` command to push updates from the Blueprint (the git repo) to the Machine (`~/.local/share/megalonyx`) without re-running the full installation.
    - **Result**: Changes made to the Blueprint in this session are not reflected in the actual runtime environment of the stack.
- **Criticality**: 🟡 Medium

---

## 🛠️ Summary of Missing Circuitry

| Component | Brain (Exists) | Hand (Missing) | Result |
| :--- | :--- | :--- | :--- |
| **Agent Gen** | `AgentGeneratorService` | `FileSystemWriter` | Ephemeral Agents |
| **Symmetry** | `symmetry-check.py` | `Orchestrator Trigger` | Manual Verification |
| **Memory** | `MemoryAuthority` | `Context Mandate` | Under-utilization |
| **Infra** | `install.sh` | `Sync/Patch Engine` | Stale Runtime |
