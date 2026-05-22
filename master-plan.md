# 🚀 Mega Code Master Plan (v0.3.0)

## 🎯 Current Focus: Sovereign Integration Pipeline
**Objective**: Transition the project from a standalone directory into a professional monorepo to enable seamless upstream inlining, modular component releases, and zero-debt scaling.
- **Problem**: Building features (like the Search Stack) on top of a non-standardized project structure creates massive technical debt and merge conflicts with upstream Qwen Code.
- **Solution**: Implement a "Sovereign Factory" using Nx, uv, and pnpm, combined with a tiered Git branching strategy.
- **Dual-Track Strategy**: For all major upstream assets, we employ a dual-track flow:
    - **Public Track (Contribution)**: Maintain a public fork for bug fixes and community contributions.
    - **Sovereign Track (Innovation)**: Integrate refined features into the private monorepo for proprietary advancement.
- **Success Criteria**:
    - `qwen_code_stack` is successfully migrated into `apps/qwen-orchestrator/`.
    - Upstream changes can be pulled into `upstream-master` and integrated into `develop` via a deterministic pipeline.
    - The MCP UDS Bridge is isolated in `packages/mcp-uds-bridge/` and can be pushed to a public repo without leaking internals.
    - All services boot and function within the new monorepo structure.


---

## 1. Vision Statement
**Mega Code** transforms LLM-based coding from a linear chat into a structured, deterministic system. By separating **Intent**, **Routing**, **Execution**, and **Interaction** into distinct planes, we eliminate "ego agent" behavior, ensure provider-agnosticism, and enforce strict privacy and safety controls.

---

## 2. The 4-Layer Architecture

| Layer | Component | Responsibility | Decision Authority |
| :--- | :--- | :--- | :--- |
| **Control Plane** | `qwen_code_stack` | Intent, Policy, Memory, Decomposition | **WHAT** needs to be done? |
| **Routing Plane** | `OmniRoute` | Provider Abstraction, Fallbacks, Secrets | **WHICH** model runs it? |
| **Execution Plane** | `Qwen Code` | Subagents, Tool Execution, File Edits | **HOW** is it physically done? |
| **Interaction Plane**| `IDE / MCP / CLI` | UI/UX, Real-time Edits, Tool Access | **HOW** is it experienced? |

### 🏗️ AI-Native Foundation: The Cognitive-Symmetry Framework (CSF)
To ensure maximum adherence and zero-latency context recovery, the entire stack is built upon the **Cognitive-Symmetry Framework**. This transforms the project from a codebase into a **self-documenting execution environment**.

- **Contextual Anchors (`.qwen-context`)**: Directory-level operational laws that override global axioms.
- **Symmetric Mirroring**: A 1:1 mapping between `config/` and `docs/` to enable structural analogy navigation.
- **Machine-Readable Contracts**: Skill outputs validated against JSON Schemas to eliminate hallucinations.
- **Meta-Audit Loops**: A 'Judge' agent auditing execution traces against `QWEN.md` axioms.

---

## 3. Operational Standards: The CPU-Worker Model
To ensure stability and prevent sub-agent timeouts, the following delegation protocol is mandatory:

- **Cognitive Split**: Synthesis, Analysis, and Planning MUST occur in the primary orchestrator. Sub-agents are used exclusively for **Atomic Execution and Data Extraction**.
- **Atomic Prompting**: NEVER delegate outcomes (e.g., "Build a guide"). ALWAYS delegate steps (e.g., "Find files containing X").
- **Rendering Standard**: All architectural diagrams and documentation must adhere to `docs/guidelines/rendering-standard.md` (No LaTeX, Unicode only).
- **Standard Reference**: Adhere strictly to `docs/guidelines/agent-protocol.md`.

---

## 4. SOTA Imports (Best Practices)
The following patterns are imported from state-of-the-art agentic frameworks:

- **Cyclic State Machines (Control Plane)**: Replace linear DAGs with $\text{Plan} \rightarrow \text{Act} \rightarrow \text{Observe} \rightarrow \text{Verify} \rightarrow \text{Correct}$ loops.
- **AST Symbol Mapping (Execution Plane)**: Use Tree-sitter for semantic navigation instead of basic grep.
- **Structured Output Constraints (Routing Plane)**: Enforce strict JSON schemas for Task Contracts using Pydantic-style validation.
- **PII Scrubbing Middleware (Interaction Plane)**: Local-first masking of sensitive data before cloud transmission.
- **WASM Sandboxing (Interaction Plane)**: Lightweight, non-persistent tool isolation.
- **Parallel Atomic Execution (Efficiency Pattern)**: Maximize work per turn by dispatching multiple tool calls in a single response. Minimize "Turn-Based Loops."
- **Specialized Agent Delegation (Microservices Pattern)**: Delegate high-entropy data extraction to specialized sub-agents to prevent context dilution in the primary orchestrator.
- **Surgical Discovery (Access Pattern)**: Prioritize `glob` and `grep_search` for scope narrowing before `read_file`.
- **Minimalist Communication (Protocol Pattern)**: Enforce strict "No Chitchat" to minimize token overhead and maximize context density.
- **PageRank-based Code Navigation (SOTA: Aider)**: Use structural centrality (PageRank) on the codebase dependency graph to identify "hub" files and suggest relevant context automatically.
- **Bi-Directional File-Based State (SOTA: Cline)**: Use a physical markdown todo list as a shared source of truth between the user and agent for real-time, high-bandwidth steering.
- **Hierarchical Community Summaries (SOTA: GraphRAG)**: Implement pre-computed community reports to enable global reasoning over large datasets without context overflow.
- **Tavily-Compatible AI-Search Wrapper (SOTA: OrioSearch)**: Use a clean `Extraction -> Reranking` pipeline to transform raw web results into high-density, LLM-ready markdown.
- **Sovereign Metasearch Aggregation (SOTA: SearXNG)**: Unify disparate search sources into a single, track-free JSON stream for maximum recall and privacy.


---

## 5. Systemic Roadmap

### Phase 0: Vision Alignment & Implementation
**Goal**: Codify the "Single Source of Truth" principle and align all project manifests.
**Technical Milestones**:
- [ ] **Codify Principle**: Update `QWEN.md`, `README.md`, and `master-plan.md` to establish `todo.md` as the authoritative roadmap.
- [ ] **Operational Shift**: Transition all task management to be driven by `todo.md`.

### Phase 1: Foundation & Infrastructure Hardening (HARDENING)
**Technical Milestones**:
- [x] Implement the **Mirror-Destination Layout** (AI Configuration vs System Infrastructure).
- [x] Codify deployment mapping in `config/meta/layout.json` (The Layout Manifest).
- [x] Refactor `install.sh` to be manifest-driven with robust stale-socket cleanup.
- [x] Implement mandatory post-install health checks (service startup, connectivity)
- [x] Implement the **Two-Pillar Model** (Brain vs Body segregation).
- [x] Implement **Production Transport Validation** (Socket vs Stdio) in the installer.
- [ ] Synchronize all manifests (`todo.md`, `master-plan.md`, `QWEN.md`) and documentation.

**Definition of Done**: Blueprint and Machine are synchronized, and `install.sh` provides a verified, reproducible deployment. Adversarial verification of infrastructure stability is complete.

---

### Phase 2: The Control Plane (Orchestration)
*Implementing the intelligence layer that transforms linear chat into a deterministic engineering process.*

**Goal**: A functional orchestrator capable of intent routing, task decomposition, and deterministic execution.
**Technical Milestones**:
- [ ] **Intent Router**: Implement a system to map user requests to high-level architectural intents.
- [ ] **Task Decomposer**: Implement a logic layer to break intents into atomic, verifiable todo lists (using the `feat-dev` pipeline).
- [ ] **Deterministic Runner**: Implement the execution loop (Act $\rightarrow$ Observe $\rightarrow$ Verify $\rightarrow$ Correct) with strict Verification Contracts.
- [ ] **Surgical History Management**: Implement `stripOrphanedUserEntriesFromHistory()` to eliminate "Ghost Turns" during retries.
- [ ] **Subagent Isolation**: Implement Prototype-based context delegation to ensure strict state isolation between implementers and verifiers.
- [ ] **Job State Machine**: Implement persistent tracking of job lifecycles.

**Definition of Done**: The system can autonomously decompose a complex request into a verifiable plan and execute it to completion with proven correctness.

---

### Phase 3: Advanced RAG & Semantic Intelligence
*Moving from basic retrieval to deep structural understanding.*

**Goal**: A high-fidelity semantic memory system that understands code architecture, not just text.
**Technical Milestones**:
- [ ] **Dreaming Pipeline**: Implement background consolidation, deduplication, and pruning of semantic memory.
- [ ] **Race-to-Deadline Recall**: Implement a strict 2.5s deadline for memory retrieval to eliminate perceived latency.
- [ ] **GraphRAG Integration**: Move from flat vector search to structural knowledge graph mapping.
- [ ] **Self-Correcting Retrieval (CRAG)**: Implement agentic feedback loops for retrieval verification.
- [ ] **Multi-Tier Memory Routing**: Optimize the Local $\rightarrow$ Cloud routing logic based on context entropy.

**Definition of Done**: The system provides high-precision architectural context with minimal noise and zero latency impact.

---

### Phase 4: Agentic Ecosystem & Scalability
*Expanding the stack into a specialized, multi-agent swarm.*

**Goal**: A scalable ecosystem of specialized agents operating under a unified control plane.
**Technical Milestones**:
- [ ] **Agent Discovery Protocol**: Automate the onboarding of new agents via the `config/agents/` layout.
- [ ] **Skill Orchestration**: Implement high-level workflow macros that chain multiple skills.
- [ ] **Autonomous Optimization**: Implement a "System Optimizer" agent to refine personas based on failure logs.

**Definition of Done**: A fully autonomous, self-optimizing swarm of agents capable of managing the entire software lifecycle.

---

## 7. Sovereign Search Stack (The Frontier Retrieval Engine)
**Objective**: Transition from "single-query snippets" to a multi-layered, professional retrieval pipeline that ensures high-signal context for the reasoning engine.

### 🏗️ The Frontier Architecture
The system implements a **Sovereign Retrieval Pipeline** to eliminate "single-shot failure" and "hallucinated package" issues:
- **Intelligence Layer**: Multi-query decomposition (1 $\to$ N expansion) to maximize recall.
- **Retrieval Layer**: Self-hosted **SearXNG** $\to$ **OrioSearch** aggregation, supplemented by direct Domain APIs (GitHub, PyPI, npm, arXiv).
- **Processing Pipeline**: Clean Markdown extraction via `trafilatura` and `readability-lxml`, followed by **Hybrid Reranking** (Semantic + BM25).
- **Memory Layer**: **Qdrant** caching of extracted markdown and successful search results to eliminate redundant web calls.

### 🛠️ Technical Milestones
- [ ] **Sovereign Foundation**: Deploy self-hosted SearXNG and OrioSearch; initialize Qdrant search cache.
- [ ] **Search Router MCP**: Implement the `search-router` server with query decomposition and routing logic.
- [ ] **Extraction Pipeline**: Build the `Extract $\to$ Cache $\to$ Rerank` flow for high-fidelity context.
- [ ] **Domain Specialization**: Integrate dedicated search tools for GitHub, PyPI, npm, and arXiv.
- [ ] **Frontier Verification**: Benchmark retrieval recall against stock search for obscure technical queries.

### Phase 0: Discovery & Mapping (The Audit)
**Goal**: Establish the ground truth by auditing both the current codebase and local research.
- [ ] **[Audit]** Map all internal data hand-offs (Intent $\rightarrow$ Job $\rightarrow$ Tool $\rightarrow$ Memory).
- [ ] **[Audit]** Scan `~/Projects/labs` for reusable modules/patterns.
- [ ] **[Research]** Identify top 3 external components for integration.
- [ ] **[Research]** Conduct Feasibility Study on all candidates (Local & External).
- [ ] **[Docs]** Update `master-plan.md` and create `docs/integration_roadmap.md`.

### Phase 1: Sovereign Infrastructure Hardening
**Goal**: Establish the "Foolproof" monorepo foundation to eliminate technical debt before scaling.
- [ ] **[Setup]** Initialize Monorepo with **Nx**, **uv (Python)**, and **pnpm (TS)** workspaces.
- [ ] **[Git]** Configure all `upstream-` remotes and the tiered branching strategy.
- [ ] **[Tooling]** Implement the `/tooling` automation suite (`sync-upstreams`, `integrate-package`, `verify-bridges`).
- [ ] **[Legal]** Implement `COMPLIANCE.json` and the automated license checker.
- [ ] **[Protocol]** Document the "Clean-Room" upstream bug reporting workflow.

### Phase 2: The Control Plane (Orchestration)
**Goal**: Build the "Brain" that can decompose, dispatch, and monitor tasks.
- [ ] **[Connect]** Link `IntentClassifier` $\rightarrow$ `TaskDecomposer` $\rightarrow$ `JobStateManager`.
- [ ] **[Implement]** The `Act $\rightarrow$ Observe $\rightarrow$ Verify $\rightarrow$ Correct` loop.
- [ ] **[Enforce]** `PolicyEngine` integration for all dispatched jobs.

### Phase 3: The Intelligence Layer (Memory & RAG)
**Goal**: Build the "Long-Term Memory" that evolves with the project.
- [ ] **[Connect]** Integrate `rag_context` $\leftrightarrow$ `Qdrant` synchronization.
- [ ] **[Implement]** The `Knowledge Eviction` protocol (Active $\rightarrow$ Archive).
- [ ] **[Implement]** The `Dreaming Pipeline` (Background memory consolidation).

### Phase 4: The Execution Swarm (Subagents & Skills)
**Goal**: Build the "Body" that can autonomously expand and execute.
- [ ] **[Connect]** Integrate `AgentGenerator` into the `SkillOrchestrator` workflow.
- [ ] **[Refactor]** Unify `SkillBridge` as the single, secure tool interface for all agents.
- [ ] **[Enforce]** `PolicyEngine` interception for all subagent tool calls.

### Phase 5: Full-Stack Verification (The MQA-Snapshot-Suite)
**Goal**: Prove the system works under real-world stress.
- [ ] **[Test]** Build the `tests/integration/` suite (Lifecycle testing).
- [ ] **[Test]** Run the `MQA-Snapshot-Suite` (High-entropy stress tests).
- [ ] **[Finalize]** Synchronize all manifests and finalize technical documentation.
