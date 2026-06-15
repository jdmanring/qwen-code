# PR Draft: feat/migrate-to-pnpm → upstream/main

**Branch:** `feat/migrate-to-pnpm`
**Issue:** #TBD
**Status:** Drafting Proposal

---

## Title

`feat(deps): migrate project from npm to pnpm to optimize CI critical path`

## Description

This PR proposes migrating the project's package manager from `npm` to `pnpm`.

### Strategic Alignment

This migration directly addresses the P2 priority of reducing the PR critical path (#5027). By moving to `pnpm`, we can significantly cut down installation times in CI and resolve the dependency loading issues mentioned in #3225.

### Why pnpm?

As the project grows in complexity and the number of packages in the workspace increases, the limitations of `npm` become more apparent. `pnpm` offers several critical advantages:

1. **Installation Speed**: `pnpm` uses a content-addressable store, significantly reducing installation times by avoiding redundant downloads and copies.
2. **Strict Dependency Tree**: Unlike `npm`, `pnpm` does not flatten the `node_modules` directory. This prevents "phantom dependencies", leading to more predictable and stable builds.
3. **Disk Efficiency**: By symlinking from a single global store, `pnpm` drastically reduces disk usage across multiple local clones of the repository.
4. **Better Monorepo Support**: `pnpm`'s workspace implementation is more robust and performant for large-scale monorepos.

### Migration Plan

1. Remove `package-lock.json`.
2. Generate `pnpm-lock.yaml` via `pnpm install`.
3. Update `CONTRIBUTING.md` and `README.md` to reflect the change in package manager.
4. Verify that all CI pipelines, tests, and build artifacts remain identical to the `npm` baseline.

## Verification Protocol

- [ ] `pnpm install` completes without errors.
- [ ] `npm run build` (via pnpm) produces identical artifacts.
- [ ] All unit and integration tests pass.
- [ ] CI pipeline is updated and green.
