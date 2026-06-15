# PR Draft: feat/typescript-6-upgrade → upstream/main

**Branch:** `feat/typescript-6-upgrade`
**Issue:** #11
**Status:** Needs Verification

---

## Title

`feat: upgrade TypeScript 5.3.3 → 6.0.3 to optimize type-checking and CI speed`

## Description

Upgrades the project-wide TypeScript version to 6.0.3. This update directly supports the P2 goals of reducing CI critical path (#5027) and optimizing heavy optional dependency loading (#3225) by leveraging TypeScript 6's improved compilation speed and enhanced type safety.

## Testing

- [ ] Full project type-check passed
- [ ] Build artifacts verified
- [ ] Performance Benchmark: Run `.qwen/scripts/benchmark-ci.sh` to verify reduction in type-check time compared to `upstream-mirror`.
