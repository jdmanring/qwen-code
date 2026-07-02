# Repository Health Audit

**Standard Activity:** Quarterly senior developer review
**Frequency:** Every 3 months or after major structural changes
**Last performed:** 2026-07-02
**Next due:** 2026-10-02

---

## Purpose

This document records the findings of a comprehensive senior developer and professional maintainer review of the qwen-code fork. It serves as:

1. A historical record of project health over time
2. A tracking mechanism for identified issues
3. A standard operating procedure for maintaining contribution-ready forks

---

## Audit Procedure

### Scope

Every audit MUST cover these areas:

1. **Project Structure & Architecture** — package boundaries, workspace config, build system
2. **Codebase Quality & Conventions** — TypeScript strictness, linting, formatting, naming
3. **Dependency Management** — upgrade policy, vulnerabilities, workarounds, patches
4. **Testing Strategy** — unit, integration, E2E, coverage, pre-existing failures
5. **CI/CD Pipeline & Tooling** — workflows, gates, automation, monitoring
6. **Contribution Workflow & Processes** — branch naming, commit conventions, update pipeline
7. **Documentation** — completeness, accuracy, broken links, gaps

### Output

Each audit produces:

1. A review document in `.qwen/reviews/` with findings and recommendations
2. Critical issues are fixed immediately or tracked in `.qwen/issues/`
3. Staged contribution branches are updated if the audit affects them
4. This document is updated with the audit date and key findings

---

## Audit History

### 2026-07-02 — Post-Update Pipeline Audit

**Trigger:** Completion of the v0.19.5 update pipeline
**Reviewer:** Senior Developer Perspective
**Full report:** `.qwen/reviews/senior-developer-review-20260702.md`

#### Findings Summary

| Area | Rating | Notes |
|------|--------|-------|
| Architecture | Strong | Clean monorepo, good package separation |
| Code Quality | Strong | Strict TS, ESLint, Prettier all enforced |
| Dependencies | Fair | `--legacy-peer-deps` workaround, 40 vulnerabilities |
| Testing | Strong | Unit, integration, E2E, terminal-bench |
| CI/CD | Good | 27 workflows, merge queue, no bundle/coverage gates |
| Workflow | Fair | Atomic branches are excellent, update pipeline is fragile |
| Documentation | Fair | Comprehensive but has broken links and gaps |

#### Critical Issues Identified

| # | Issue | Status | Action |
|---|-------|--------|--------|
| 1 | `eslint-plugin-storybook` missing from `package.json` | Fixed | Removed from root config (moved to webui) |
| 2 | 1 critical npm vulnerability | Open | Needs investigation |
| 3 | `read-package-up` missing from `package.json` | Fixed | Added during update pipeline |
| 4 | `--legacy-peer-deps` for ESLint 10 | Fixed | Removed unused React plugins |
| 5 | `--legacy-peer-deps` for vitest version conflict | Documented | Legitimate mismatch, documented in CONTRIBUTING.md |

#### Recommendations

**Immediate:**
- Add `eslint-plugin-storybook` to `package.json` or remove the import
- Investigate critical npm vulnerability
- Document the `ink+7.0.3.patch`

**Short-term:**
- Create a scripted update pipeline
- Add CODEOWNERS file
- Add test coverage thresholds
- Fix `docs/architecture.md` broken link

**Long-term:**
- Migrate away from `patch-package`
- Add ADRs for key architecture decisions
- Implement bundle size monitoring
- Create a dependency upgrade policy

---

## Deep Dive: Critical Issues

### 1. `--legacy-peer-deps` Workaround

#### What It Is

npm 7+ introduced strict peer dependency resolution. When package A declares a peer dependency on `eslint@"^9"` and package B installs `eslint@10`, npm 7+ fails with `ERESOLVE unable to resolve dependency tree`.

`--legacy-peer-deps` tells npm to fall back to npm 6 behavior, which ignores peer dependency conflicts and installs anyway.

#### Why We Were Using It (ESLint 10 — FIXED)

The original cause was `eslint-plugin-react@7.37.5`. Its `package.json` declares:

```json
{
  "peerDependencies": {
    "eslint": "^2 || ^3 || ^4 || ^5 || ^6 || ^7.2.0 || ^8 || ^9.7.0"
  }
}
```

This range does NOT include ESLint 10. When we upgraded to ESLint 10, npm refused to install.

**FIX:** We removed `eslint-plugin-react` and `eslint-plugin-react-hooks` entirely. Investigation revealed that all React linting rules were disabled (`'react/prop-types': 'off'`, `'react/react-in-jsx-scope': 'off'`). The plugins were loaded but not actually used. Removing them eliminated the peer dependency conflict.

#### Why We Still Need It (vitest — LEGITIMATE)

The remaining conflict is between `packages/webui` and the rest of the monorepo:

- `packages/webui` requires `vitest@^4.1.9` for `@storybook/addon-vitest` compatibility
- `packages/core` and `packages/cli` use `vitest@^3.1.1`

This is a genuine version mismatch. The `@storybook/addon-vitest@10.4.6` package requires `@vitest/browser@4.1.9` which requires `vitest@4.1.9`. The root `package.json` has `vitest@^3.2.4` which resolves to a 3.x version.

**This is a legitimate use of `--legacy-peer-deps`** that requires upstream resolution from the Storybook team or a decision to upgrade all packages to vitest 4.x.

#### Impact on Staged Contributions

None. The `--legacy-peer-deps` workaround does not affect the content of staged contributions. It only affects the install process.

---

### 2. Update Pipeline Fragility

#### Why It Was Considered Fragile

The update pipeline is the process of:
1. Fast-forwarding `upstream-mirror` to match `upstream/main`
2. Rebasing `develop` onto the updated `upstream-mirror`
3. Rebasing all contribution branches onto the updated `upstream-mirror`

It was fragile because:

**Manual conflict resolution at scale.** The 2026-07-02 rebase touched 73 branches. Each branch can have conflicts in any file. Resolving conflicts manually for 73 branches is:
- Slow (hours of work)
- Error-prone (the `--strategy-option=ours` mistake proved this)
- Unverifiable (no automated check that the resolution was correct)

**The `--strategy-option=ours` mistake.** During the first attempt, I used `git rebase --strategy-option=ours` which silently takes upstream's version for every conflict. This:
- Exits 0 even when real semantic conflicts exist
- Silently discards changes from the branch being rebased
- Cannot be detected without manually reviewing every rebased branch

**No automated verification.** After rebasing, there's no script that:
- Checks each branch still compiles
- Checks each branch's tests still pass
- Checks the branch's diff against upstream is still clean
- Checks no commits were dropped

**The eslint fix commit was dropped.** During the rebase of `develop`, the commit that replaced `eslint-plugin-import` with `eslint-plugin-import-x` was silently lost. This was only caught because the pre-commit hook failed. Without that, the broken state would have been pushed.

**No rollback mechanism.** If a rebase goes wrong, there's no automated way to restore the original branch tips. I had to use `git reflog` to find the original positions, which is manual and error-prone.

#### The Fix: Scripted Pipeline

Created `scripts/update-pipeline.sh` to automate the process:

- **Auto-discovers** contribution branches (`chore/*`, `fix/*`, `feat/*`, etc.)
- **Saves original branch tips** for rollback before starting
- **Rebases each branch individually** onto upstream-mirror
- **Detects conflicts and reports them** — does NOT auto-resolve
- **Aborts and restores** branches with conflicts to their original state
- **Generates a markdown report** of results
- **Supports `--dry-run`** mode for previewing

The script is general-purpose and works with any branch. No per-branch customization is needed. It explicitly prohibits `--strategy-option=ours` or `--strategy-option=theirs` in its documentation.

#### Remaining Risks

- The script does not verify that rebased branches still compile or pass tests. This could be added in a future iteration.
- The script does not push to remote. This is intentional — the user should review the results before pushing.
- Complex semantic conflicts (e.g., API changes in upstream that affect branch code) still require manual resolution.

---

### 3. Broken Links & Documentation Gaps

#### Broken Links

| Link | Location | Target | Status |
|------|----------|--------|--------|
| `docs/architecture.md` | `CONTRIBUTING.md` | Architecture documentation | Fixed — replaced with actual `docs/design/`, `docs/developers/`, `docs/users/` paths |
| `docs/developers/development/integration-tests.md` | `CONTRIBUTING.md` | Integration test docs | Verify existence |

The `docs/architecture.md` link was referenced in `CONTRIBUTING.md` as "For more detailed architecture, see `docs/architecture.md`." This file did not exist. Fixed by replacing the link with references to the actual documentation directories.

#### Documentation Gaps

**SECURITY.md has content.** The file includes a security policy with a link to the Aliyun security portal for reporting vulnerabilities.

**ADRs created.** Architecture Decision Records are now documented in `docs/design/adr/README.md`:
- ADR-001: Fork-Specific Infrastructure Separation
- ADR-002: Atomic Contribution Branches
- ADR-003: Cherry-Pick to Develop, Never Merge
- ADR-004: ESLint 10 Migration Strategy
- ADR-005: Package Desktop Exclusion
- ADR-006: Patch Package for Ink Exports

**`ink+7.0.3.patch` documented.** Added a comment at the top of the patch file explaining:
- What bug it fixes (missing exports in Ink's package.json)
- Why it can't be upstreamed (needs upstream fix)
- When it can be removed (when upstream Ink fixes the exports)

**`--legacy-peer-deps` documented in workflow.** `CONTRIBUTING.md` now explains:
- Why `--legacy-peer-deps` is needed (vitest version conflict)
- Which packages are affected (webui vs core/cli)
- That this is a known limitation requiring upstream resolution

#### Remaining Gaps

**No dependency upgrade policy.** There's no documented policy for when to upgrade dependencies or how to handle security patches.

**No bundle size monitoring.** The `check:serve-fast-path-bundle` script exists but isn't in CI.

**No test coverage thresholds.** Coverage can silently degrade.

---

## Standard Activity Checklist

Use this checklist for future audits:

- [ ] Review project structure and architecture
- [ ] Check codebase quality and conventions
- [ ] Audit dependencies (vulnerabilities, workarounds, patches)
- [ ] Review testing strategy and coverage
- [ ] Review CI/CD pipeline and automation
- [ ] Review contribution workflow and update pipeline
- [ ] Check documentation for completeness and accuracy
- [ ] Fix critical issues immediately
- [ ] Track high/medium/low issues in `.qwen/issues/`
- [ ] Update staged contributions if audit affects them
- [ ] Record findings in `.qwen/reviews/`
- [ ] Update this document with audit date and summary
