# Test Coverage: Current State, Why It Matters, and How to Fix It

## What coverage thresholds are and where they came from

`packages/cli` and `packages/core` each have a vitest coverage config that enforces
minimum percentages for statements, branches, functions, and lines. These were set once
to match the actual coverage at the time they were written — not as aspirational targets.
They are a floor, not a ceiling.

Current thresholds:

| Package | Statements | Branches | Functions | Lines |
| :--- | :--- | :--- | :--- | :--- |
| `packages/cli` | 73% | 76% | 76% | 73% |
| `packages/core` | 75% | 78% | 77% | 75% |

## Current actual state (as of 2026-05-26)

Both packages are **below threshold**. Running `pnpm exec vitest run --coverage` fails:

```
packages/cli:
  Coverage for lines (69.67%) does not meet global threshold (73%)
  Coverage for functions (68.81%) does not meet global threshold (76%)
  Coverage for statements (68.88%) does not meet global threshold (73%)
  Coverage for branches (61.29%) does not meet global threshold (76%)

packages/core:
  Coverage for functions (74.29%) does not meet global threshold (77%)
  Coverage for statements (74.95%) does not meet global threshold (75%)
  Coverage for branches (67.84%) does not meet global threshold (78%)
```

284 tests are currently failing in `packages/cli` across 23 test files.

## Why coverage dropped below threshold

The drop was not caused by deleting tests or deliberately lowering thresholds. It was caused
by **upstream sync absorbing new features that came with new tests, where those tests now
fail against the current codebase state**.

The sync pipeline (`upstream_ingest_pipeline.py`) absorbed commits from `jdmanring/qwen-code`
that added new behavior (StopHookLoop events, HookSystemMessage events, slash completion
changes, ACP session rewriting, channel commands, etc.). Each upstream commit brought its own
tests. Those tests are now in the codebase but failing — likely because the tests reference
APIs or behavior that changed in transit, or the test environment differs.

Failing test files (all in `packages/cli/src/`):
- `acp-integration/acpAgent.test.ts`
- `acp-integration/acpAgent.worktree.test.ts`
- `acp-integration/session/rewrite/MessageRewriteMiddleware.test.ts`
- `commands/channel/start.test.ts`
- `commands/extensions/install.test.ts` / `utils.test.ts`
- `commands/mcp/list.test.ts` / `reconnect.test.ts` / `remove.test.ts`
- `config/config.test.ts`
- `core/auth.test.ts` / `initializer.test.ts`
- `nonInteractive/session.test.ts`
- `services/FileCommandLoader.test.ts`
- `ui/hooks/useGeminiStream.test.tsx`
- `ui/hooks/useSlashCompletion.test.ts`
- `ui/hooks/slashCommandProcessor.test.ts`
- `ui/hooks/useAutoAcceptIndicator.test.ts`
- `ui/utils/clipboardUtils.test.ts`
- `ui/commands/insightCommand.test.ts`
- `utils/errors.test.ts` / `warningHandler.test.ts`
- `validateNonInterActiveAuth.test.ts`

## Does being below threshold affect program stability?

**No.** The threshold is a CI gate — it blocks merging code that would lower coverage further.
It has no effect on how the program runs. The binary built from this codebase behaves the same
whether coverage is 60% or 100%.

However, low coverage **is a signal**: untested code paths may contain bugs that only appear
under specific conditions. The failing tests in this case are not catching new bugs — they are
tests that were written for features and then broke. That is a maintenance debt, not a runtime
stability issue.

The real risk is: if coverage stays low and no one fixes the failing tests, new regressions
in those areas will not be caught.

## The target

90% across all four metrics (statements, branches, functions, lines) in both packages is a
reasonable long-term target. 100% is theoretically possible but not the practical goal —
some code paths (error recovery, platform-specific branches, dead code inherited from
upstream) are legitimately difficult to cover without over-engineering test setup.

The immediate goal is: **get all 284 failing tests passing again**, which will restore
coverage above threshold and re-enable the CI gate.

---

# Coverage Improvement Guide

## Step 0 — Verify the current state

```bash
cd packages/cli && pnpm exec vitest run --coverage 2>&1 | grep -E "FAIL|ERROR.*threshold"
cd packages/core && pnpm exec vitest run --coverage 2>&1 | grep -E "FAIL|ERROR.*threshold"
```

## Step 1 — Fix the failing tests (highest leverage)

Each failing test is a collapsed ceiling. Fixing it restores coverage without writing new
tests. Work through the failing files one at a time:

```bash
cd packages/cli && pnpm exec vitest run src/ui/hooks/useGeminiStream.test.tsx --reporter=verbose
```

For each failure, the pattern is:
1. Read the error — it usually says what API changed or what is undefined
2. Find the source file the test is testing
3. Check whether the source changed (git log, git diff) or the test is wrong
4. Fix whichever one is wrong

**Do not delete failing tests to make the suite pass.** That destroys the gate. Fix the
test to match current behavior, or fix the source if the test is correctly describing
intended behavior.

## Step 2 — Identify uncovered code

After all tests pass, check which lines are uncovered:

```bash
cd packages/cli && pnpm exec vitest run --coverage --reporter=verbose 2>&1 | grep "0 |"
```

Or open the HTML report:
```bash
cd packages/cli && pnpm exec vitest run --coverage
open coverage/index.html
```

Focus on files with the lowest coverage — those represent the biggest coverage gains per
test written.

## Step 3 — Write targeted tests for uncovered paths

Priority order:
1. **Error handling branches** — `catch` blocks and failure paths are often 0% covered
   and are the most likely to contain bugs
2. **Edge cases in core logic** — conditions, null checks, boundary values
3. **Integration paths** — code that is exercised but only via deep call stacks

Keep tests small and specific. One test per branch is better than one large test that
covers many things — it makes failures easier to diagnose.

## Step 4 — Raise thresholds incrementally

Once actual coverage exceeds current thresholds, raise the thresholds in the vitest
configs to match the new actual value. This ratchets the floor up and prevents future
regressions from silently lowering coverage.

Never raise a threshold above actual coverage — the suite will fail immediately.

```typescript
// packages/cli/vitest.config.ts
thresholds: {
  statements: 78,  // raise once actual >= 78
  branches: 80,
  functions: 80,
  lines: 78,
},
```

Commit each threshold raise separately with a message like:
`test(coverage): raise CLI thresholds to 78/80/80/78 — actual coverage now 79/82/81/79`

## Step 5 — Protect coverage going forward

The CI gate (`python-quality.yml`) does not run the vitest coverage check — it runs Python
tooling only. Coverage enforcement is local only (pre-commit hook or manual run). If you
want coverage regressions caught before merge, add this to the GitHub Actions workflow
for TypeScript packages:

```yaml
- name: Test with coverage
  run: pnpm exec vitest run --coverage
  working-directory: packages/cli
```

## Summary of the path to 90%

| Step | Action | Effect |
| :--- | :--- | :--- |
| 1 | Fix 284 failing tests in `packages/cli` | Restores coverage above current threshold |
| 2 | Fix failing tests in `packages/core` | Same |
| 3 | Identify and cover uncovered error paths | +5–10% per package |
| 4 | Raise thresholds to match new actual | Locks in gains |
| 5 | Add coverage to CI workflow | Prevents future regressions |
