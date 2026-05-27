# Contribution Verification Checklist

This document defines the "Hardened Verification" protocol for any code intended to be contributed back to the upstream `qwen-code` fork. Given that we operate as a solo entity without external guidance, we adhere to a zero-tolerance policy for regressions and noise in our PRs.

##  The Hardened Verification Protocol

Every contribution branch must pass through this sequence before it is considered "PR-Ready".

### 1. Isolated Update & Clean Room
- [ ] **Dedicated Branch**: The change exists on a clean `contribute/phase-XXX` branch based on `upstream/main`.
- [ ] **Environment Purge**: `node_modules` and `dist` directories have been deleted.
- [ ] **Strict Install**: `pnpm install --frozen-lockfile` succeeded without modifying the lockfile.
- [ ] **Full Build**: `pnpm build` completed without errors or warnings.

### 2. The "Hell" Test Suite
- [ ] **Unit Tests**: `pnpm exec vitest run` passed 100% of tests.
- [ ] **Type Audit**: `pnpm run typecheck` reports zero errors.
- [ ] **Lint Audit**: `pnpm run check` reports zero errors and zero warnings.
- [ ] **Runtime Smoke Test**: 
    - [ ] CLI boots successfully (`node dist/cli.js --version`).
    - [ ] Core tools (File system, Shell, MCP) executed without runtime exceptions.

### 3. Fork-Parity & Leak Check
- [ ] **Diff Audit**: `git diff upstream/main` shows *only* the intended changes.
- [ ] **Leak Check**: No monorepo-specific configurations, paths, or internal `packages/` references have leaked into the fork branch.
- [ ] **Lockfile Integrity**: `pnpm-lock.yaml` is absent from the contribution branch (per project policy).

### 4. Final Regression Analysis
- [ ] **Build Artifacts**: The size of the `dist/` bundle is within expected parameters compared to the previous version.
- [ ] **Performance**: No observable degradation in CLI startup time or tool execution speed.

---

##  Stop-Ship Criteria
If any of the following occur, the PR is blocked:
1. Any test failure, regardless of how "trivial" it seems.
2. Any new TypeScript `any` casts introduced in the diff.
3. Any linting warning that can be resolved.
4. Any evidence of monorepo-relative paths in the contributed code.
