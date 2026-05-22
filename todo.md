# 📌 Project TODO

## ✅ COMPLETED: Strategic Pivot & Alignment
- [x] **Pivot to Sovereign Integration Pipeline**
    - [x] Identify technical debt risk of premature feature implementation
    - [x] Define "Sovereign Integration Pipeline" as the primary priority
    - [x] Establish Cognitive Triggering logic for "Sovereign" naming
- [x] **Architectural Alignment**
    - [x] Define Monorepo structure (Nx, uv, pnpm)
    - [x] Establish tiered branching strategy (`upstream-master` $\to$ `integration` $\to$ `develop` $\to$ `main`)
    - [x] Align on "Sovereign" vs "Mega Code" naming boundaries
- [x] **Manifest Synchronization**
    - [x] Update `master-plan.md` to v0.3.0
    - [x] Granularize `todo.md` with 5-stage execution program

## 🔴 CRITICAL: Sovereign Integration Pipeline (THE FACTORY)
- [x] **Stage 1: Repository Foundation (Dual-Track Setup)**
    - [x] Create GitHub Fork of `qwen-code`
    - [x] Create `megacode-sovereign-stack` monorepo repository on GitHub
    - [x] Clone `megacode-sovereign-stack` locally
    - [x] Configure remotes:
        - [x] Add `origin` (monorepo)
        - [x] Add `upstream` (official qwen-code)
        - [x] Add `mirror` (user fork)
    - [x] Establish tiered branching strategy:
        - [x] Create `upstream-main` branch (pull from `upstream/main`)
        - [x] Create `integration` branch from `upstream-main`
        - [x] Create `develop` branch from `integration`
        - [x] Create `main` branch from `develop`
    - [x] Document the branch flow in `docs/meta/git-strategy.md`
- [x] **Stage 2: Monorepo Scaffolding (Sovereign-Grade)**
    - [x] Initialize Nx workspace
    - [x] Configure `pnpm-workspace.yaml` for TS/Node packages
    - [x] Initialize `uv` workspace for Python environment
    - [x] Establish global dependency locking (Root `package.json` / `pyproject.toml`)
    - [x] Setup Monorepo-aware `.gitignore`
    - [x] Build the `tooling/sync-upstreams/` automation suite
    - [x] Harden `nx.json` with targetDefaults and caching
- [ ] **Stage 2.5: The Sovereign Scrub (Base Realignment)**
    - [ ] **2.5.1: Technical Policy Enforcement**
        - [ ] Execute project-wide `ruff check --fix` and `ruff format`
        - [ ] Resolve remaining `ANN` (Type Hint) and `E501` (Line Length) errors in core packages
    - [ ] **2.5.2: Documentation Rendering Scrub**
        - [ ] Search and replace all LaTeX symbols ($\to$, etc.) with ASCII/Unicode across all `.md` files
        - [ ] Verify zero LaTeX presence in `docs/` and `config/`
    - [ ] **2.5.3: Cognitive Naming Realignment**
        - [ ] Audit all inherited files for `kebab-case` compliance in `docs/` and `config/`
        - [ ] Rename non-compliant files to meet Sovereign standards
    - [ ] **2.5.4: Final Base Verification**
        - [ ] Run full `ruff check .` and `npm run check`
        - [ ] Verify zero errors in the inherited base
- [ ] **Stage 3: The Great Migration**
    - [ ] Create `apps/qwen-orchestrator/` directory
    - [ ] Migrate all existing `qwen_code_stack` logic $\to$ `apps/qwen-orchestrator/`
    - [ ] Analyze codebase for shared logic extraction
    - [ ] Extract to `packages/mcp-uds-bridge/`
    - [ ] Extract to `packages/shared-utils/` (CSF-Symmetry, Logging)
    - [ ] Update all internal imports in `apps/qwen-orchestrator` to reference `packages/`
    - [ ] Update `stack-manager.py` to use monorepo-relative paths
    - [ ] Perform first "Monorepo Boot" test
    - [ ] Resolve path resolution errors until `stack-manager status` is green
- [ ] **Stage 4: The Upstream Inlining Pipeline**
    - [ ] Implement `tooling/sync-upstreams/raw-inline.sh` (`upstream` $\to$ `upstream-master`)
    - [ ] Implement `tooling/sync-upstreams/integrate.sh` (`upstream-master` $\to$ `integration` $\to$ `develop`)
    - [ ] Create `docs/meta/conflict-resolution-protocol.md` (How to handle upstream breaks)
    - [ ] Implement `tooling/sync-upstreams/verify-boot.sh` (Auto-check `stack-manager` after sync)
    - [ ] Create "Sovereign Sync" wrapper script to chain the entire flow
    - [ ] Execute full loop test: Pull upstream $\to$ Merge integration $\to$ Verify boot
- [ ] **Stage 5: Component Release Workflow**
    - [ ] Install `git-filter-repo` for clean history extraction
    - [ ] Create test extraction script for `packages/mcp-uds-bridge`
    - [ ] Create separate public GitHub repo for `qwen-mcp-uds-bridge`
    - [ ] Implement `tooling/release/extract-component.sh`
    - [ ] Configure GitHub Action for `develop` $\to$ public component repo sync
    - [ ] Verify public repo contains only component code (zero monorepo leakage)
- [ ] **Stage 6: Public Contribution Management**
    - [ ] Establish protocol for "Sovereign-to-Upstream" bug reporting
    - [ ] Implement `tooling/contribution/create-pr.sh` (Automated PR creation from `develop` to `public-fork`)
    - [ ] Track community feedback on public releases to inform internal roadmap
- [ ] **Stage 7: CI/CD Automation (The Guardrails)**
    - [ ] Configure GitHub Actions for the Monorepo
    - [ ] Implement "Upstream Watchdog" (Automated detection of upstream updates)
    - [ ] Implement "Symmetry Linter" (Block merges if `config/` $\leftrightarrow$ `docs/` alignment fails)
    - [ ] Implement "Boot Validator" (Automated `stack-manager start` check on PRs)
    - [ ] Establish a "Safe-to-Merge" certification process for `develop` $\to$ `main`

## 🔴 CRITICAL: Cognitive Realignment & Cold Start
- [x] **Cognitive Naming Standard**
    - [x] Establish `docs/meta/COGNITIVE_NAMING_STANDARDS.md`
    - [x] Normalize Root Documentation to kebab-case
    - [x] Transform Validators to actionable verb-first naming
    - [x] Eliminate duplicate core entry points
    - [x] Purge "Magic-Strings" and ambiguous terminology
- [x] **Cold Start Readiness**
    - [x] Synchronize `config/QWEN.md` $\to$ `docs/meta/QWEN.md`
    - [x] Document systemic failures in `docs/meta/IMPLEMENTATION_GAPS.md`
    - [x] Establish `docs/meta/REALIGNMENT_PLAN.md` as the recovery blueprint
- [ ] **Systemic Realignment (The "Fix")**
    - [ ] Implement Agent Materialization (Persistence Layer)
    - [ ] Integrate Symmetry Check into the `S-VERIFY` loop
    - [ ] Enforce Memory Mandates in system prompts
    - [ ] Implement Blueprint $\to$ Machine Synchronization utility

## 🔴 CRITICAL: AI-Native Hardening (Cognitive-Symmetry Framework)
- [ ] **Phase 1: Contextual Anchors**

    - [ ] Implement `.qwen-context` standard across all major directories
    - [ ] Update `QWEN.md` to mandate reading anchors upon directory entry
    - [ ] Verify "Local Law" override behavior via self-audit
- [ ] **Phase 2: Structural Symmetry**
    - [ ] Perform 1:1 audit of `config/` vs `docs/`
    - [x] Implement `symmetry-check` linter script
    - [ ] Resolve all orphaned configuration files
- [ ] **Phase 3: Deterministic Contracts**
    - [ ] Migrate `SKILL.md` output contracts to JSON Schema
    - [ ] Implement `schema-validator` tool for agent outputs
    - [ ] Integrate validation into the `S-VERIFY` loop
- [ ] **Phase 4: Meta-Audit Implementation**
    - [ ] Define "Judge Agent" persona and axiom-mapping logic
    - [ ] Implement execution trace auditing
    - [ ] Integrate "Axiom Violation" alerts into the session tracker

## 🔴 CRITICAL: Final Purge (Code Debt Audit)
- [ ] **[CODE-01] Resolve WARNING level type-hint gaps in Python source.**
- [ ] **[CODE-02] Refactor INFO level complexity issues (nesting depth/function length).**

## 🔴 CRITICAL: Operational Hardening
- [x] **Axiomatization of Operational Law**
    - [x] Extract rules from `docs/guidelines/`
    - [x] Convert to Trigger $\to$ Action axioms
- [x] **Systemic Integration**
    - [x] Rewrite `config/QWEN.md` using Axiomatic framework
    - [x] Apply lossless compression for token efficiency
    - [x] Implement mandatory Pre-Flight Check mandate
- [x] **Plan Alignment**
    - [x] Merge hardening tasks into `master-plan.md`
    - [x] Synchronize `todo.md`
- [ ] **Self-Audit Verification**
    - [ ] Execute a trivial task following the new `QWEN.md`
    - [ ] Verify 100% adherence to AIP and Plan Mode protocols
    - [ ] Document any remaining frictions in the operational flow

## 🔴 CRITICAL: Infrastructure Stability
- [x] **Phase 1: Path Agnosticism & Environment Hardening**


    - [x] Audit `scripts/stack-manager.py` for all hardcoded paths
    - [x] Replace `/home/james` with `os.path.expanduser("~")` for `STACK_ROOT` and `LOG_FILE`
    - [x] Ensure all internal path constructions are relative to environment roots
    - [x] Verify path resolution with `stack-manager status`
- [x] **Phase 2: Resilient Orchestration**
    - [x] Refactor `cmd_start` to decouple service management (non-fatal starts)
    - [x] Implement a `ServiceResult` system to track and report failure summaries
    - [x] Enhance `cmd_stop` to ensure exhaustive cleanup of all PIDs and sockets
    - [x] Implement a `--strict` flag for fatal start behavior
    - [x] Verify resilience via simulated service failures
- [x] **Phase 3: Connectivity & Stability Verification**
    - [x] Implement `connectivity-check` command in `stack-manager`
    - [x] Verify `127.0.0.1` vs `localhost` reachability for all services
    - [x] Create and run a "Stress Test" script (10x restart cycles)
    - [x] Verify zero stale sockets/PIDs after stress testing
- [ ] **Final Adversarial Verification**
    - [ ] Static audit for absolute paths
    - [ ] Code review of `stack-manager.py`
    - [ ] Functional baseline check on live system
    - [ ] Sandbox adversarial tests (Resilience, Strictness, Cleanup)

## 🔵 Testing Pyramid Rebuild
- [x] Audit existing tests
- [x] Define testing strategy
- [x] Implement `mcp_bridge` integration tests
- [x] Implement `mcp_daemon` integration tests
- [x] Implement E2E and Deployment tests
- [x] Phase 2: Comprehensive Documentation
- [ ] **Professional Test Suite Consolidation**
    - [ ] **Phase 1: Audit & Categorization**
        - [ ] Map all `tests/**/*.py` files to Pyramid levels
        - [ ] Identify redundant/obsolete files in `tests/debug/` and `tests/`
    - [ ] **Phase 2: Migration & Organization**
        - [ ] Move unit tests to `tests/unit/`
        - [ ] Move integration tests to `tests/integration/`
        - [ ] Move fidelity/sandbox tests to `tests/fidelity/`
        - [ ] Move E2E/Chaos tests to `tests/e2e/`
        - [ ] Relocate floating tests in `tests/` to appropriate subdirectories
    - [ ] **Phase 3: Pruning & Cleanup**
        - [ ] Delete obsolete debug scripts and reproduction files
        - [ ] Remove temporary/scratch files
        - [ ] Standardize all tests to `test_*.py` naming convention
    - [ ] **Phase 4: Verification**
        - [ ] Run full test suite with `pytest` to verify no regressions
        - [ ] Verify `pytest` discovery works with the new structure

## 🟡 Pending Infrastructure
- [ ] Verify all binaries in `~/.local/bin` are correctly linked
- [ ] Audit `install.sh` for any remaining timeouts or dependency gaps

## 🔴 CRITICAL: Sovereign Library (Lab Ingestion)
- [x] **Phase 1: The Great Audit (Dark Data Discovery)**
    - [x] Perform exhaustive technical audit of `labs/unsorted`
    - [x] Extract core identity, purpose, and "Golden Features"
    - [x] Assign Utility Scores (1-10) for all assets
    - [x] Populate `labs/CATALOG.json` master index
- [x] **Phase 2: The Sorting & Migration**
    - [x] Map projects to categories (agent-frameworks, memory-systems, etc.)
    - [x] Migrate folders from `unsorted` $\to$ `labs/<category>/`
    - [x] Synchronize `labs/CATALOG.json` with new paths
- [x] **Phase 3: Cognitive Ingestion (Mirroring)**
    - [x] Create `labs/docs/` directory structure matching `labs/` categories
    - [x] Identify high-utility projects (Score $\ge 7$) from `CATALOG.json`
    - [x] Draft technical mirrors in `labs/docs/<category>/<project>.md`
        - [x] Ingest SearXNG (Infrastructure Spec)
        - [x] Ingest OrioSearch (API & Reranking Spec)
        - [x] Ingest Aider (Repomap Spec)
        - [x] Ingest Cline (Plan/Act Workflow Spec)
        - [x] Ingest GraphRAG (Structural Memory Spec)
    - [x] Extract "Golden Features" and integrate into `master-plan.md`
- [ ] **Phase 4: Library Maintenance**
    - [ ] Implement `labs/INVENTORY.md` for human-readable tracking
    - [ ] Establish formal protocol for new lab ingestion

## 🔴 CRITICAL: Frontier Search Stack Implementation
- [ ] **Phase 1: Sovereign Foundation (Infrastructure)**
    - [ ] Create `docker-compose.yml` for SearXNG and OrioSearch
    - [ ] Deploy SearXNG and configure hardened `settings.yml` (Anti-bot, Engine filtering)
    - [ ] Deploy OrioSearch (Tavily-compatible layer)
    - [ ] Initialize Qdrant Search Cache collection (Schema definition)
    - [ ] Verify end-to-end connectivity: `Query` $\to$ `SearXNG` $\to$ `OrioSearch` $\to$ `JSON`
- [ ] **Phase 2: Orchestration Layer (Search-Router MCP)**
    - [ ] Scaffold `search-router` MCP server project
    - [ ] Implement `frontier_search` tool (The primary entry point)
    - [ ] Implement `domain_search` tool (Targeted registry search)
    - [ ] Build Query Decomposition Engine (1 $\to$ N sub-queries)
    - [ ] Integrate `approvalMode` logic (Matching `[A-PERM]` matrix in `QWEN.md`)
- [ ] **Phase 3: Extraction Pipeline (High-Fidelity Context)**
    - [ ] Integrate `trafilatura` for boilerplate removal
    - [ ] Integrate `readability-lxml` as fallback extractor
    - [ ] Implement Hybrid Reranker (Semantic + BM25)
    - [ ] Build the `Extract $\to$ Cache $\to$ Rerank` data flow
- [ ] **Phase 4: Domain Specialization (Deep-Dive Tools)**
    - [ ] Implement GitHub Code Search tool
    - [ ] Implement PyPI / npm / crates.io search tools
    - [ ] Implement arXiv academic search tool
    - [ ] Integrate Reddit + StackOverflow specialized scrapers
- [ ] **Phase 5: Verification & Optimization**
    - [ ] Run "Retrieval Benchmarks" (Stock vs. Frontier)
    - [ ] Optimize multi-query pipeline latency
    - [ ] Audit extraction confidence scoring

## 🔴 CRITICAL: Operational Hardening (Cognitive Alignment)
- [ ] **Permission Matrix Enforcement**
    - [ ] Update `IntentClassifier` to calculate Risk Scores for tool calls
    - [ ] Implement `ApprovalEngine` that maps `Mode` + `RiskScore` $\to$ `Action` (Auto/Ask/Block)
    - [ ] Integrate `Mode` indicators into the Orchestrator's system prompt
- [ ] **Symmetry Check Integration**
    - [ ] Implement `symmetry-check.py` to verify `config/` $\leftrightarrow$ `docs/` alignment
    - [ ] Add symmetry check to the `stack-manager` health check suite

## 🟢 Long-Term Goals
- [ ] Phase 2: Control Plane Implementation
- [ ] Phase 3: Advanced RAG & Semantic Intelligence
