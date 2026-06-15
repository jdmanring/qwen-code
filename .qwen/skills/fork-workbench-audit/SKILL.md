---
name: fork-workbench-audit
description: Audit staged contributions in a fork workbench to ensure they are PR-ready for upstream.
source: auto-skill
extracted_at: '2026-06-12T20:17:01.651Z'
---

---

name: fork-workbench-audit
description: Audit staged contributions in a fork workbench to ensure they are PR-ready for upstream.
source: auto-skill
extracted_at: '2026-06-12T20:17:01.651Z'

---

# Fork Workbench Audit

This skill is used to review contributions staged in a fork workbench to ensure they meet the strict requirements for upstream acceptance and maintain a clean pipeline.

## Audit Procedure

### 1. Tracking & Visibility Audit

- **Issue Mapping**: Verify that every active feature or chore branch has a corresponding issue in the fork's issue tracker.
- **PR Drafts**: Ensure a PR draft exists for every contribution.
- **Synchronization**: Confirm that issue numbers in the tracker, PR drafts, and git branches are consistent.

### 2. Strategic Alignment Audit

- **Upstream Mapping**: Search upstream issues and roadmaps (e.g., `ROADMAP.md`, GitHub Issues) for pain points that the contribution addresses.
- **Value Framing**: Rewrite PR titles and descriptions to lead with the _value_ to the upstream maintainer rather than the technical action (e.g., "Reduce CI critical path" instead of "Upgrade Vite").
- **Reference Integration**: Explicitly reference upstream issue numbers in the PR description and fork issue tracker to show the contribution is a solution to a known need.
- **Priority Alignment**: Tie contributions to specific priority labels (e.g., P1, P2) found in the upstream backlog.

### 3. Naming & Intent Audit

- **Standardization**: Remove internal "phase" codes or temporary ticket IDs from branch names and PR titles.
- **Descriptive Naming**: Ensure names clearly describe the _effect_ of the change (e.g., `feat/typescript-6-upgrade` instead of `contribute/phase-m`).
- **Scope Check**: Verify that the PR title accurately reflects the contents of the branch.

### 4. Isolation & Scope Audit

- **Scope Creep Detection**: Check for "noisy" PRs. A dependency upgrade should not include unrelated cleanup, deletions of tests, or modifications to CI workflows unless strictly required for the upgrade to work.
- **Isolation of Destructive Changes**: If a branch contains both a feature/upgrade and general cleanup:
  1. Create a separate `chore/cleanup-...` branch.
  2. Move the cleanup commits/changes to that branch.
  3. Revert the cleanup changes in the original feature branch to keep it "pure".

### 5. Tooling & Environment Audit

- **Version Verification**: Check that CI tool versions (e.g., `actionlint`, `eslint`) are current. Flag any accidental downgrades.
- **Lockfile Contamination**: In a mixed-manager environment (e.g., transitioning from `npm` to `pnpm`):
  - Ensure `upstream-candidate` branches strictly use the upstream's package manager.
  - Verify that no "foreign" lockfiles (e.g., `pnpm-lock.yaml` in an `npm` project) have leaked into candidate branches.

### 6. Verification Audit

- **Protocol Check**: Confirm that the "Verification Protocol" (Logs $\rightarrow$ Tests $\rightarrow$ UI) has been executed.
- **Evidence**: Check that the PR draft's testing checkboxes are actually checked and not just listed.

## Success Criteria

A contribution is "PR-Ready" when:

- [ ] It is linked to a valid issue.
- [ ] It is strategically aligned with an upstream goal or issue.
- [ ] It has a descriptive, standardized name.
- [ ] It contains only the changes necessary for the stated goal (no scope creep).
- [ ] It uses the correct upstream package manager.
- [ ] It has been verified end-to-end.
