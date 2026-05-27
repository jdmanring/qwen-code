# Operational Standard: Config-Doc Sync Ingestion Protocol

This protocol defines the mandatory procedure for transforming raw source repositories into **Integrated Assets**. Ingestion is not complete until the repository is "AI-Navigable" and achieves structural mirroring with the project.

## 1. Objective & Scope
**Goal**: Establish a Zero-Friction interface between the AI and an external codebase by deploying **Anchors**, **Mirrors**, and **Functional Distillations**.

---

## 2. The Ingestion Pipeline (Rule-Based Phases)

### Phase 1: Physical Ingestion
**Objective**: Establish physical presence and structural mapping.
- **Rule [P1-A]**: `(Repo Identified $\to$ Clone to /labs/[cat]/[name] $\to$ Map Hierarchy)` $\to$ Use `glob` for full discovery.
- **Rule [P1-B]**: `(Mapped Hierarchy $\to$ Initialize .codegraph $\to$ Index Evolution)` $\to$ Must capture Git history.
- **Verification**: Mirroring-check must resolve the root directory and primary entry points.

### Phase 2: Structural Mapping
**Objective**: Establish "Local Rules" and mirror intelligence.
- **Rule [P2-A]**: `(Index Complete $\to$ Identify Config/Docs Zones $\to$ Deploy .qwen-context Anchors)` $\to$ One anchor per structural zone.
- **Rule [P2-B]**: `(Anchor Deployed $\to$ Mirror Critical Configs to /docs/ingested/ $\to$ Apply Mirroring Template)` $\to$ Template: `Identity` $\to$ `Mandates` $\to$ `Trigger Logic` $\to$ `Mirror Link`.
- **Verification**: Execution of `../../scripts/symmetry-check.py` must return `Exit 0`.

### Phase 3: Functional Distillation
**Objective**: Extract the codebase's core logic as deterministic rules.
- **Rule [P3-A]**: `(Mirrored Docs $\to$ Pattern Analysis via Scout/Researcher $\to$ Identify Recurring Architectures)` $\to$ Focus on data flow and state management.
- **Rule [P3-B]**: `(Pattern Identified $\to$ Synthesize (Trigger $\to$ Action) Rule $\to$ Ingest to Cloud Memory)` $\to$ Rules must be atomic.
- **Verification**: Memory query must recall the new rules when prompted with target repo context.

### Phase 4: Verification
**Objective**: Prove "AI-Navigability."
- **Rule [P4-A]**: `(Integrated Repo $\to$ Assign Fresh Agent $\to$ Execute Non-Trivial Task)` $\to$ Agent must have zero prior context.
- **Rule [P4-B]**: `(Task Execution $\to$ Monitor Queries $\to$ Ban "How/Where" Questions)` $\to$ Agent must rely exclusively on Anchors and Mirrors.
- **Verification**: Task Success $\to$ Mark as **Fully Integrated**. Failure $\to$ Revert to Phase 2.

---

## 3. Tooling & Automation Matrix

| Tool | Purpose | Requirement |
| :--- | :--- | :--- |
| `scripts/ingest-repo.sh` | Scaffolding | Initialize mirrored directory structure. |
| `tests/integration/test_symmetry.py` | Validation | Verify mirroring accuracy. |
| `ingest` (Tool) | Memory Commit | Persist functional distillations to Qdrant. |

---

##  Mirror Link
This protocol is the SSOT for the `ingestion-specialist` agent.
`../../config/agents/ingestion-specialist.md` $\leftrightarrow$ `csf-ingestion-protocol.md`