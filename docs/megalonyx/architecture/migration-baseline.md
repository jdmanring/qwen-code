# 🏁 Migration Baseline: Source State Audit

This document records the "As-Is" state of the inherited source code within the `packages/` directory of the monorepo. This baseline is used to ensure that the migration to the `apps/` and `packages/` structure does not introduce regressions.

## 📊 Current State Summary

### 1. Code Quality Baseline
- **Ruff Audit**: The codebase has been scrubbed of 219 critical errors (ANN/E501).
- **Type Safety**: Core types are defined in `packages/core/src/types/`, but some "any" types remain in the SDK bridges.
- **Formatting**: All files have been normalized to the project's linting standards.

### 2. Implementation Status
| Component | State | Note |
| :--- | :--- | :--- |
| **Permission Classifier** | Stable | Fully implemented in `packages/core/src/permissions/`. |
| **Tool Dispatcher** | Stable | Core logic resides in `coreToolScheduler.ts`. |
| **Memory Bridge** | Functional | Bridge to Qdrant is operational; "Dreaming" logic is partial. |
| **CLI Orchestrator** | Functional | Currently lives in `packages/cli`; targeted for `apps/qwen-orchestrator`. |
| **SDKs** | Stubs | Python and Java SDKs are currently lightweight wrappers. |

### 3. Known Fragilities
- **Path Resolution**: Several hardcoded paths exist in the `infra` layer that must be generalized during migration.
- **Dependency Leakage**: Minor leakage of CLI-specific types into the SDK types (to be decoupled).
- **Test Coverage**: The `core` logic is well-tested, but the `infra` adapters lack comprehensive integration tests.

## 🛠️ Verification Checklist for Migration
Every component moved during Stage 3 must be verified against this baseline:
- [ ] Does the component still perform its primary function?
- [ ] Have any new circular dependencies been introduced?
- [ ] Does the component adhere to the `layer-manifest.md` zoning rules?
- [ ] Is the logic still compatible with the current `memory-service-manager`?
