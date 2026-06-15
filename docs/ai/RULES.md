# AI Rules — Qwen Code

> **The Law.** This document contains hard constraints, the Git pipeline, and non-negotiable policies.

---

## Core Mandates

**Read the source before writing code.** Find the relevant file, read it, report what
you find. Do not generate code against an assumption about what the code looks like.

**No sudo.** If an operation requires elevated privileges, write the command for
the user to run — do not execute it yourself.

**Issue before PR.** Upstream explicitly requires an issue to exist before any PR
is filed. This applies to agent-generated work as well.

**One thing per PR.** No mixing unrelated fixes, formatting changes, or refactors into
a single PR. Each PR must be reviewable in isolation.

**Verify the fix in the running app.** Tests are not sufficient. Before any PR is
considered ready, the fix must be confirmed end-to-end in the actual application.

**Verification Protocol:**

1. **Logs**: Tail the daemon logs or check the browser console for tracebacks.
2. **Tests**: Run the relevant test suite (e.g., `pnpm test` in the package directory or `make test`).
3. **UI**: Perform the specific user action in the CLI or IDE that triggered the bug.

**Visual changes require screenshots.** Any PR touching CSS, HTML, or UI components
must include a screenshot or clip.

**Use existing constants and helpers.** Never hardcode paths, ports, or URLs that
the project already exposes.

---

## Workbench Rules (jdmanring/qwen-code only)

These rules apply only when working in this fork.

**This fork is a contribution workbench.** Its purpose is to develop and stage upstream
pull requests. Every fix, feature, and document defaults to upstream-candidate. Fork-only
is the narrow exception: the sync pipeline, fork CI, and fork management docs.

- **Never push to the `upstream` remote.**
- **Never commit to `upstream-mirror`.**
- **Never cherry-pick upstream → `develop` directly.** Use the ingest pipeline.
- **Branch origin matters.** Upstream-candidate branches must start from `upstream-mirror`.
  Fork-only branches start from `develop`.

---

## Lifecycle Ownership & Definition of Done

You are an engineer, not a script. A task is not "done" when the code is written; it is done when the entire delivery chain is complete.

**The Definition of Done:**

1. **Implementation**: Code is written, linted (via `pnpm run lint`), and committed to the correct branch.
2. **Verification**: The fix is verified via the Verification Protocol.
3. **Tracking**: All project tracking is synced:
   - Update `docs/fork/issue-tracker.md`.
   - Update the corresponding PR draft in `docs/fork/upstream/pr-drafts/`.
   - Update `docs/fork/upstream/pr-status.md`.
4. **Reporting**: Report the final state and explicitly confirm that all tracking is updated.
