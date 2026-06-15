# PR Draft: feat/vitest-vite-upgrade → upstream/main

**Branch:** `feat/vitest-vite-upgrade`
**Issue:** #6
**Status:** Needs Verification

---

## Title

`feat: migrate Vitest 3 → 4 and Vite 5 → 6 to reduce CI critical path`

## Description

Comprehensive upgrade of the testing and build stack. By migrating to Vitest 4 and Vite 6, we directly support the P2 priority goal of reducing the PR critical path (#5027) and optimizing build performance (#3226) through improved compilation speeds and execution efficiency.

## Testing

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Build artifacts verified
- [ ] Performance Benchmark: Run `.qwen/scripts/benchmark-ci.sh` to verify reduction in build time compared to `upstream-mirror`.
