# Upstream PR Guide: Contributing to QwenLM/qwen-code

This guide covers everything required to prepare and submit a professional pull request
to the upstream QwenLM/qwen-code project. Read it completely before opening any PR.

See `docs/upstream/upstream-pr-checklist.md` for the gate-by-gate checklist to run
before each submission.

---

## The Core Constraint: Isolation

Every upstream PR must contain **only code that would exist in QwenLM's repo independently
of Megalonyx**. No Megalonyx config, no Megalonyx-specific paths, no references to our
private tooling, no pnpm-specific changes (they use npm).

The upstream maintainers review everything that goes into their project. A single leaked
internal detail -- a private URL, an internal package name, a reference to our stack --
creates confusion, erodes trust, and may cause the PR to be closed. Isolation is not
optional.

---

## What Qualifies as an Upstream Contribution

A fix or upgrade belongs upstream when **all three** of these are true:

1. The problem exists in `QwenLM/qwen-code` independently -- it would reproduce in a fresh
   clone of their repo without any Megalonyx additions.
2. The fix touches only code that lives in their repository: `packages/core/`, `packages/cli/`,
   `packages/sdk-python/`, `packages/acp-bridge/`, or `packages/channels/`.
3. The fix does not require any Megalonyx infrastructure to test or verify.

When in doubt: clone `QwenLM/qwen-code` fresh, apply only the fix, run their test suite.
If it passes, the fix is upstream-eligible.

## What Does Not Belong Upstream

| Category | Examples | Why |
|---|---|---|
| Megalonyx stack config | `config/megalonyx/`, `scripts/megalonyx/` | Private to this repo |
| pnpm workspace changes | `pnpm-workspace.yaml`, `pnpm-lock.yaml` | They use npm |
| Our CI workflows | `.github/workflows/integration-test.yml` | Written for our infra |
| Tooling | `tooling/sync-upstreams/`, `tooling/symmetry_check.py` | Our private pipeline |
| Version overrides | `pnpm-workspace.yaml` overrides section | pnpm-specific |
| Any reference to Megalonyx | Internal names, URLs, paths | Not upstream-relevant |

---

## One-Time Setup: The Mirror Remote

The public fork (`jdmanring/qwen-code`) is the outbound channel for upstream contributions.
Upstream code never flows through it -- it flows inbound via the `upstream` remote. The fork
is exclusively for submitting PRs.

Add it once:

```bash
# upstream remote is already configured -- verify:
git remote -v  # should show: upstream -> git@github.com:jdmanring/qwen-code.git
git fetch upstream
```

If it shows HTTPS instead of SSH, fix it:

```bash
git remote set-url upstream git@github.com:jdmanring/qwen-code.git
```

Verify the remotes are correctly configured:

```bash
git remote -v
# upstream  git@github.com:jdmanring/qwen-code.git  (inbound filter + outbound PR channel)
# origin    git@github.com:jdmanring/megalonyx-monorepo.git  (our private repo)
```

---

## Preparing a PR: The Full Procedure

### Step 1 -- Identify the commit

Find the commit on `develop` that contains only the fix you want to contribute.
If the fix was bundled with other changes, it cannot be cherry-picked cleanly -- you must
either split it first or apply the fix manually on a clean branch.

```bash
git log --oneline develop | grep <keyword>
git show <commit-hash> --stat   # verify what files it touches
```

### Step 2 -- Create a clean branch from upstream/main

```bash
git fetch upstream
git checkout -b upstream-contrib/<branch-name> upstream/main
```

This branch starts from QwenLM's current `main`. It has zero Megalonyx history.

Naming convention: `upstream-contrib/<type>/<short-description>`
Examples:
- `upstream-contrib/fix/openai-union-type`
- `upstream-contrib/chore/diff-v9-upgrade`
- `upstream-contrib/fix/eslint-node-modules`

### Step 3 -- Apply the change

**Option A -- Cherry-pick (preferred when the commit is clean):**

```bash
git cherry-pick <commit-hash>
```

If cherry-pick conflicts: resolve conflicts, keeping only the upstream-relevant parts.
Do not let conflict resolution introduce any Megalonyx code.

**Option B -- Manual apply (when the commit mixed concerns):**

Apply only the relevant lines manually. Commit with the same message.

### Step 4 -- Verify isolation (mandatory)

**Preferred: use the automated pipeline.** The isolation gates run automatically when you
use `--contribute` mode, so for single-commit cherry-picks you can skip manual grep checks:

```bash
# Runs all isolation gates, then creates the branch and pushes if gates pass
python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <branch-name>

# Gates only -- no branch created (safe to run first)
python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <branch-name> --dry-run
```

The pipeline runs five gates and hard-blocks if any fail:
- `GATE-MEGALONYX` -- diff contains 'megalonyx'
- `GATE-PNPM` -- diff contains 'pnpm-workspace'
- `GATE-JDMANRING` -- diff contains 'jdmanring'
- `GATE-CONFIG` -- diff contains 'config/megalonyx'
- `GATE-CIFILES` -- diff touches any file in `PROTECTED_FILES`

**For multi-commit or manual PRs**, run the checks by hand:

```bash
git diff upstream/main HEAD -- .
# Read every line -- does it make sense in a fresh QwenLM clone?

# Should each return nothing:
git diff upstream/main HEAD | grep -i megalonyx
git diff upstream/main HEAD | grep -i 'pnpm-workspace'
git diff upstream/main HEAD | grep -i 'jdmanring'
git diff upstream/main HEAD | grep -i 'config/megalonyx'
```

If any check returns output, the branch is not clean. Fix it before proceeding.

### Step 5 -- Verify the change works in their environment

QwenLM uses **npm**, not pnpm. Their tests run with `npm ci` + `npm run test:ci`.

For code changes (not just dep bumps), verify locally:

```bash
# From the branch root, simulate their environment
npm ci
npm run build
npm test
```

For dependency bumps only, verify the package resolves:

```bash
npm install <package>@<version> --dry-run
```

### Step 6 -- Push to the fork

```bash
git push upstream upstream-contrib/<branch-name>
```

### Step 7 -- Open the PR

Open the PR against `QwenLM/qwen-code main` from your fork branch.

```bash
gh pr create \
  --repo QwenLM/qwen-code \
  --base main \
  --head jdmanring:upstream-contrib/<branch-name> \
  --title "<title>" \
  --body "$(cat <<'EOF'
<body>
EOF
)"
```

---

## PR Title Format

Follow conventional commits. QwenLM uses this format throughout their repo.

```
<type>(<scope>): <short description>
```

Types:
- `fix` -- corrects a bug
- `chore(deps)` -- dependency version bump with no behavior change
- `refactor` -- restructuring with no behavior change
- `feat` -- new capability (rare for our contribution type)

Scope is the package or subsystem: `core`, `cli`, `lint`, `deps`, `openai`, `acp`.

Examples from our planned PRs:
```
fix(lint): extend node_modules ignore pattern to cover package-level dirs
fix(openai): narrow toolCall union type before accessing .function property
chore(deps): upgrade diff ^7.0.0 -> ^9.0.0; fix renamed types
chore(deps): upgrade undici ^6.22.0 -> ^8.3.0
chore(deps): upgrade @agentclientprotocol/sdk 0.14->0.22; fix renamed APIs
fix(core): bypass simple-git unsafe-operations block on core.hooksPath config
```

Keep the title under 72 characters. Do not end with a period.

---

## PR Description Format

Every upstream PR description must include all of these sections.

### What changed

One short paragraph. What does this PR do? Do not explain why here.

### Why

One short paragraph. What problem does this fix? If it is a dependency upgrade, state
the specific motivation: security advisory, required API, breaking change in a transitive dep.
Link to the upstream package changelog if relevant.

### What code changed (for dependency upgrades with code fixes)

A table or list of every source file modified and the specific change made. Maintainers
need to understand what the code changes are before they can approve a dep bump.

Example:
```
Required code changes for diff v9:
- `packages/core/src/tools/diffOptions.ts`: `Hunk` -> `StructuredPatchHunk`, `ParsedDiff` -> `StructuredPatch`
- `packages/core/src/services/fileHistoryService.ts`: same `Hunk` rename
- `packages/core/src/utils/gitDiff.ts`: same `Hunk` rename
```

### Testing

State explicitly what was tested and how:
- Which test suite covers the changed code
- Whether existing tests were sufficient or new tests were needed
- Test command used and result

Example:
```
`npm run test:ci` passes. The diff package changes are covered by existing tests in
`packages/core/src/tools/` and `packages/core/src/utils/`. No new tests required --
the type renames are compile-time only.
```

### Compatibility note (for breaking changes)

If the upstream code changes behavior in any way -- even subtly -- document it here.
If it is purely a refactor or type-level change with no runtime behavior change, say so.

---

## QwenLM's CI Pipeline

Their CI runs automatically on every PR. It must be green before a PR will be merged.

| Check | Tool | What it tests |
|---|---|---|
| ESLint | `scripts/lint.js` | TypeScript/JavaScript style, imports, unused vars |
| actionlint | actionlint | GitHub Actions YAML correctness |
| shellcheck | shellcheck | Shell script correctness |
| yamllint | yamllint | YAML formatting |
| prettier | prettier | Code formatting |
| i18n check | custom | Translation key consistency |
| Unit tests | vitest (Node 22) | All test files on macOS, Ubuntu, Windows |
| CodeQL | GitHub CodeQL | Static security analysis |

**If CI fails on your PR:**
1. Read the failure log -- do not guess
2. Fix the issue on your local branch
3. `git push upstream upstream-contrib/<branch-name>` -- CI re-runs automatically
4. Do not close and re-open the PR; update the branch in place

Their ESLint config runs `eslint-plugin-import` and `@typescript-eslint`. Their vitest
version is `^3.1.1`. Their TypeScript version is `^5.3.3`. Match these constraints
when verifying locally, not our versions.

---

## Handling Reviewer Feedback

QwenLM maintainers review community PRs. Response time varies -- simple bug fixes may
merge in days; dependency bumps may take weeks.

When reviewers request changes:

1. **Read the comment carefully before responding.** Understand what they are asking
   before making any changes.
2. **Apply the change on the existing branch**, not a new PR. Push to the same branch --
   GitHub shows the diff and keeps review context intact.
3. **Reply to each review comment** after pushing. Confirm what you did or explain
   why you chose a different approach. Do not leave review comments unaddressed.
4. **Re-request review** after all comments are resolved. Use the GitHub UI -- the
   reviewer is not notified automatically when you push.

If a PR is rejected:
- Accept the decision without arguing.
- If the rejection contains useful feedback, incorporate it and re-submit as a new PR
  after a reasonable interval (at minimum one week).
- Update the plan doc to reflect the PR status.

---

## Our Planned Upstream PRs

Submit in this order. Simpler PRs first builds a credibility track record.

| PR | Title | Dependencies |
|---|---|---|
| PR-1 | `fix(lint): extend node_modules ignore + yargs import` | None |
| PR-2 | `fix(openai): narrow toolCall union type` | None |
| PR-3 | `chore(deps): upgrade diff 7->9; fix renamed types` | None |
| PR-4 | `chore(deps): upgrade undici ^6.22.0 -> ^8.3.0` | None |
| PR-5 | `chore(deps): upgrade glob ^10.5.0 -> ^13.0.0` | None |
| PR-6 | `chore(deps): upgrade html-to-text, https-proxy-agent, marked` | None |
| PR-7 | `chore(deps): upgrade openai 5.11.0 -> ^6.39.0` | PR-2 merged |
| PR-8 | `chore(deps): upgrade yargs ^17.7.2 -> ^18.0.0` | PR-1 merged |
| PR-9 | `chore(deps): upgrade @agentclientprotocol/sdk 0.14->0.22; fix renamed APIs` | None |
| PR-10 | `chore(deps): upgrade @anthropic-ai/sdk ^0.36.1 -> ^0.98.0` | None |
| PR-11 | `@google/genai` -- **do not open**. PR #4485 is already open. Comment on it instead. | -- |
| PR-12 | `chore(deps): upgrade iconv-lite, comment-json, chokidar` | None |
| PR-13 | `fix(core): migrate archiver v8 API in github.test.ts` | None |
| PR-14 | `fix(core): bypass simple-git unsafe-operations block on core.hooksPath` | None |

Track PR status in the master plan file.

---

## Reference

| Document | Purpose |
|---|---|
| `docs/upstream/upstream-pr-checklist.md` | Gate-by-gate checklist -- run before every submission |
| `docs/upstream/sync-policy.md` | What we take from upstream and what we skip |
| `docs/meta/git-strategy.md` | Branch architecture and pipeline flow |
| `tooling/sync-upstreams/contribute-upstream.sh` | Script for single-commit cherry-pick submissions |
