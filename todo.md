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
- [x] Configure `.ruff.toml` with Debt Suppression rules.
- [x] Verify environment hermeticity (uv/pnpm).

### Lair 2: The Orchestrator (Tooling) — COMPLETE
- [x] Implement `IntegrationOrchestrator` in Python (`tooling/sync-upstreams/orchestrator.py`).
- [x] Build `PreFlight` -> `Sync` -> `Verify` -> `Promote` flow.
- [x] Implement LKG (Last Known Good) snapshotting via annotated git tags.
- [x] `--dry-run` mode: run all gates against current state without sync or promotion.
- [x] Ruff binary resolution: `uv run ruff` > `RUFF_BIN` > PATH (eliminates false-green problem).
- [x] Boot gate uses `uv lock --check` (real test, not file-existence check).
- [x] Gate order: Boot → Lint → Symmetry (boot runs before `uv run ruff` can recreate a missing lockfile).
- [x] Windows installer scripts restored to `integration`; `.bat` purge removed from pipeline.
- [x] `contribute-upstream.sh`: cherry-pick a fix onto a clean upstream branch and push to public fork for PR.
- [x] All three gates verified green via `--dry-run`.

### Lair 3: Adversarial Certification (QA) — COMPLETE
- [x] Chaos Test: Simulate merge conflicts -> Verified `integration` stability.
- [x] Chaos Test: Simulate symmetry gate failure -> Verified promotion block.
- [x] Chaos Test: Simulate boot failure -> Verified promotion block.
- [x] **SYSTEM CERTIFIED: Adversarial-Proof** (all three chaos tests pass).

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
