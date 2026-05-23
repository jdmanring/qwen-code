# 📌 Project TODO (Engineering Mode)

## 🛠️ STAGE 1: GROUND TRUTH AUDIT (Completed)
*Goal: Eliminate all assumptions. Establish a verified baseline of the system.*

- [x] **Audit Git State**: Verify all branches (`upstream-mirror`, `integration`, `develop`, `main`) and remotes (`upstream`, `mirror`, `origin`).
- [x] **Audit Tooling State**: Verify presence and logic of `raw-inline.sh`, `integrate.sh`, `verification-gate.sh`, and `symmetry-check.py`.
- [x] **Audit Blueprint State**: Verify `.qwen/config/` and `docs/` mapping.
- [x] **Audit Environment State**: Verify `uv` and `pnpm` workspace configurations.

## 📐 STAGE 2: SOVEREIGN EXECUTION PLAN (Completed)
*Goal: Create a deterministic, verified roadmap for implementation.*

- [x] **Define Environment Hermeticity**: Establish pre-flight checks for every tool.
- [x] **Design Ingestion Pipeline**: Map the flow from Upstream $\to$ Mirror $\to$ Integration $\to$ Develop.
- [x] **Define Sovereignization Process**: Codify the transformation steps (Isolation $\to$ Standardization $\to$ Modularization $\to$ Verification).
- [x] **Define Final Certification**: Establish the "Green" criteria for project completion.

## 🚀 STAGE 3: IMPLEMENTATION (Execution)

### Lair 1: Foundation Restoration (Current)
- [ ] Restore `main` and `develop` branches from `origin`.
- [ ] Configure `.ruff.toml` with Debt Suppression rules.
- [ ] Verify environment hermeticity (uv/pnpm).

### Lair 2: The Orchestrator (Tooling)
- [ ] Implement `SovereignSyncOrchestrator` in Python.
- [ ] Build `PreFlight` $\to$ `Sync` $\to$ `Verify` $\to$ `Promote` flow.
- [ ] Implement LKG (Last Known Good) snapshotting.
- [ ] Verify orchestrator with "Dry Run" mode.

### Lair 3: Adversarial Certification (QA)
- [ ] Chaos Test: Simulate merge conflicts $\to$ Verify `integration` stability.
- [ ] Chaos Test: Simulate gate failures $\to$ Verify promotion block.
- [ ] Chaos Test: Simulate boot failure $\to$ Verify promotion block.
- [ ] Final Certification: Successful end-to-end sync with LKG tag.

### Phase 2: The Great Migration (Sovereignization)
- [ ] **Targeted Ingestion**: Move `qwen_code_stack` logic into `integration` branch.
- [ ] **Sovereignization**: Apply Ruff, Mypy, and CSF standards.
- [ ] **Shared Extraction**: Extract logic to `packages/`.
- [ ] **Promote to Develop**: Merge after gate pass.
- [ ] **Monorepo Boot**: Perform first successful boot test.

---

## 📦 LEGACY ARCHIVE
*Previous attempts are archived here for reference. No further work will be done on these paths unless integrated into the new plan.*

- [x] Initial File Migration (Moved to apps/qwen-orchestrator)
- [x] Initial Branching Strategy (Documented)
- [x] Initial Config Relocation (Moved to .qwen/config)
