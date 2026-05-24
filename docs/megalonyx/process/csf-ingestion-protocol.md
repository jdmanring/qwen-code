# Operational Law: CSF Ingestion Protocol

This protocol defines the mandatory procedure for transforming raw source repositories into **Cognitive Assets**. Ingestion is not complete until the repository is "AI-Navigable" and achieves structural symmetry with the Megalonyx.

## 1. Objective & Scope
**Goal**: Establish a Zero-Friction interface between the AI and an external codebase by deploying **Anchors**, **Mirrors**, and **Axiomatic Distillations**.

---

## 2. The Ingestion Pipeline (Axiomatic Phases)

### Phase 1: Physical Ingestion (The Body)
**Objective**: Establish physical presence and structural mapping.
- **Axiom [P1-A]**: `(Repo Identified $\to$ Clone to /labs/[cat]/[name] $\to$ Map Hierarchy)` $\to$ Use `glob` for full discovery.
- **Axiom [P1-B]**: `(Mapped Hierarchy $\to$ Initialize .codegraph $\to$ Index Evolution)` $\to$ Must capture Git history.
- **Verification**: Symmetry-check must resolve the root directory and primary entry points.

### Phase 2: Cognitive Mapping (The Brain)
**Objective**: Establish "Local Law" and mirror intelligence.
- **Axiom [P2-A]**: `(Index Complete $\to$ Identify Config/Docs Zones $\to$ Deploy .qwen-context Anchors)` $\to$ One anchor per cognitive zone.
- **Axiom [P2-B]**: `(Anchor Deployed $\to$ Mirror Critical Configs to /docs/ingested/ $\to$ Apply Symmetry Template)` $\to$ Template: `Identity` $\to$ `Mandates` $\to$ `Trigger Logic` $\to$ `Symmetry Link`.
- **Verification**: Execution of `../../scripts/symmetry-check.py` must return `Exit 0`.

### Phase 3: Axiomatic Distillation (The Spirit)
**Objective**: Extract the codebase's "Soul" as deterministic laws.
- **Axiom [P3-A]**: `(Mirrored Docs $\to$ Pattern Analysis via Scout/Researcher $\to$ Identify Recurring Architectures)` $\to$ Focus on data flow and state management.
- **Axiom [P3-B]**: `(Pattern Identified $\to$ Synthesize (Trigger $\to$ Action) Axiom $\to$ Ingest to Cloud Memory)` $\to$ Axioms must be atomic.
- **Verification**: Memory query must recall the new axioms when prompted with target repo context.

### Phase 4: Verification (The Gate)
**Objective**: Prove "AI-Navigability."
- **Axiom [P4-A]**: `(Integrated Repo $\to$ Assign Fresh Agent $\to$ Execute Non-Trivial Task)` $\to$ Agent must have zero prior context.
- **Axiom [P4-B]**: `(Task Execution $\to$ Monitor Queries $\to$ Ban "How/Where" Questions)` $\to$ Agent must rely exclusively on Anchors and Mirrors.
- **Verification**: Task Success $\to$ Mark as **Cognitively Integrated**. Failure $\to$ Revert to Phase 2.

---

## 3. Tooling & Automation Matrix

| Tool | Purpose | Mandate |
| :--- | :--- | :--- |
| `scripts/ingest-repo.sh` | Scaffolding | Initialize mirrored directory structure. |
| `tests/integration/test_symmetry.py` | Validation | Verify mirroring accuracy. |
| `ingest` (Tool) | Memory Commit | Persist axiomatic distillations to Qdrant. |

---

## 🔗 Symmetry Link
This protocol is the SSOT for the `ingestion-specialist` agent.
`../../config/agents/ingestion-specialist.md` $\leftrightarrow$ `csf-ingestion-protocol.md`