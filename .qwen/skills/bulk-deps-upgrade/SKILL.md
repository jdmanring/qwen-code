---
name: bulk-deps-upgrade
description: Create staged contribution branches for every outdated dependency and apply version bumps to develop.
source: auto-skill
extracted_at: '2026-06-13T21:30:00.000Z'
---

# Bulk Dependency Upgrade

When the user wants to bring all dependencies up to date with a reference repo (like megalonyx-monorepo), create one contribution branch per outdated dependency, plus matching GitHub issues on the fork. Then apply the version bumps to develop.

## Prerequisites

- `FORK_WORKBENCH_TEMPLATE.md` workflow understood
- `gh` CLI configured; default repo may be upstream — **always use `--repo <fork>`** for issue creation
- Reference repo (e.g., `/home/james/Projects/megalonyx-monorepo`) available locally

## Input

The user says something like "upgrade all deps to match megalonyx-monorepo" or "create 22 staged contributions for dependency upgrades".

## Steps

### 1. Compute the outdated deps list

Run a Node.js script that reads all `package.json` files from both the fork and the reference repo, compares versions, and outputs a deduplicated list:

```javascript
const fs = require('fs');
function readPkg(p) {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    return null;
  }
}
function allDeps(pkg) {
  return { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
}
```

Compare each package (root, core, cli, webui) against the reference. Skip deps already in staged branches. Output a sorted list of `{ dep, our, target, pkgs }`.

### 2. Create GitHub issues on the fork (NOT upstream)

**CRITICAL: Always use `--repo <fork-owner>/<fork-name>` with `gh issue create`.** The default `gh` repo may be the upstream source. Creating issues upstream is FORBIDDEN.

```bash
gh issue create --repo jdmanring/qwen-code \
  --title "chore(deps): upgrade <dep> <current> → <target>" \
  --body "Upgrade <dep> from <current> to <target> in <packages>.\n\nReference: megalonyx-monorepo uses <target>."
```

Collect all issue numbers.

### 3. Create one contribution branch per dep

For each outdated dependency:

```bash
git checkout -b chore/upgrade-<dep-name> upstream-mirror
```

Apply the version bump using `sed` on each affected `package.json`:

```bash
sed -i 's/"<dep>": "<current>"/"<dep>": "<target>"/' packages/<pkg>/package.json
```

Verify the diff contains ONLY the intended `package.json` changes:

```bash
git diff upstream-mirror..HEAD --name-only
```

Commit with `--no-verify` (since `.husky/pre-commit` fix is on `fork/infra`, not yet on `upstream-mirror`):

```bash
git add <affected-package-jsons>
git commit --no-verify -m "chore(deps): upgrade <dep> <current> → <target>

Upgrade <dep> to latest across affected packages.

Co-Authored-By: Claude <<EMAIL>>"
```

### 4. Push branches and create PR drafts

```bash
git push origin chore/upgrade-<dep-name>
```

Create PR draft in `docs/fork/upstream/pr-drafts/chore-upgrade-<dep-name>.md`.

### 5. Apply version bumps to develop

**IMPORTANT**: Do NOT cherry-pick contribution branch commits onto develop. Cherry-picking fails when develop has diverged from upstream-mirror (e.g., old merged branches, code changes). Instead, apply version bumps directly to develop's package.json files using `sed`.

#### 5a. Reset develop to upstream-mirror

```bash
git checkout develop
git reset --hard upstream-mirror
```

This gives a clean base that matches the contribution branches.

#### 5b. Apply all version bumps via sed

For each outdated dependency, run the same `sed` commands used in the contribution branches:

```bash
# Core package.json
sed -i 's/"<dep>": "<current>"/"<dep>": "<target>"/' packages/core/package.json

# CLI package.json
sed -i 's/"<dep>": "<current>"/"<dep>": "<target>"/' packages/cli/package.json

# Root package.json
sed -i 's/"<dep>": "<current>"/"<dep>": "<target>"/' package.json

# WebUI package.json
sed -i 's/"<dep>": "<current>"/"<dep>": "<target>"/' packages/webui/package.json
```

#### 5c. Commit all bumps as a single commit

```bash
git add package.json packages/cli/package.json packages/core/package.json packages/webui/package.json
git commit --no-verify -m "chore(deps): upgrade 38 dependencies to latest versions

Upgrade all outdated dependencies across all packages to match
megalonyx-monorepo reference versions.

Co-Authored-By: Claude <<EMAIL>>"
```

**Why a single commit**: The version bumps are all related (dependency maintenance) and should be one logical change on develop. This also makes it easy to revert if needed.

#### 5d. Re-apply doc commits

If develop had documentation commits that were lost in the reset, re-apply them:

```bash
git cherry-pick <doc-commit-hash>
```

### 6. Update tracking docs

- `docs/fork/upstream/pr-status.md` — add each new contribution
- `docs/fork/issue-tracker.md` — add issue-to-branch mapping

### 7. Final verification

Run the health checks from `FORK_WORKBENCH_TEMPLATE.md` on each branch:

```bash
git merge-base chore/upgrade-<dep> upstream-mirror  # should equal upstream-mirror HEAD
git rev-list --count upstream-mirror..chore/upgrade-<dep>  # should be 1
git diff upstream-mirror..chore/upgrade-<dep> --name-only  # only package.json files
git diff upstream-mirror..chore/upgrade-<dep> --check  # no conflict markers
```

Verify develop has all bumps:

```bash
git diff upstream-mirror..develop --stat  # should show all package.json changes
```

## Post-Upgrade Verification & Contribution Restoration

After applying all bumps to `develop`, you must verify that they didn't introduce regressions. If regressions are found, use a "Gold State" workflow to ensure granular PRs remain clean and reviewable.

### 1. Establish "Gold State" on develop

Apply all necessary source code fixes to `develop` until the project is fully compliant (`npm run typecheck` passes) and stable (integration tests pass). This becomes your "Gold State".

### 2. Map Fixes to Granular Branches

Analyze the fixes applied to `develop` and map each change to the corresponding `chore/upgrade-<dep>` branch.

- **Library-specific fixes**: Port to the matching `chore/upgrade-<dep>` branch.
- **General type/logic fixes**: Port to the most relevant branch (e.g., `chore/upgrade-types`).
- **Infrastructure fixes**: Port to a separate `chore/upgrade-infra` branch (e.g., build shims, config changes).

### 3. Distribute Fixes

For each granular branch:

```bash
git checkout chore/upgrade-<dep>
git checkout develop -- <relevant-files>
git commit --no-verify -m "fix(deps): resolve regressions for <dep> upgrade"
```

### 4. Verify Granular Branches

Run `typecheck` on each branch to ensure it is self-contained and compliant before submitting the PR.

## Key Rules

- **NEVER** `gh issue create` without `--repo <fork>` — upstream issue creation is forbidden
- **NEVER** merge contribution branches to `develop` — apply bumps directly via sed
- **ALWAYS** base contribution branches on `upstream-mirror`, not `develop`
- Use `--no-verify` for commits on contribution branches (the `.husky/pre-commit` fix lives on `fork/infra`)
- One branch per dependency — do NOT batch multiple deps into one branch
- Each branch gets exactly one commit
- **NEVER mention private repos** (megalonyx-monorepo, etc.) in issue bodies or PR descriptions — say "reference repo" instead
- **NEVER compare source code against a reference repo** — the reference is for version numbers only; code changes must be found by running typecheck/build on the fork itself
- **ALWAYS verify after bumps** — run `node_modules/.bin/tsc --noEmit` and compare error count against baseline to catch breakage

## Common Pitfalls

| Pitfall                                                  | How to avoid                                                                 |
| -------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Cherry-pick fails due to develop divergence              | Apply version bumps directly via `sed` instead of cherry-picking             |
| `git reset --hard upstream-mirror` loses develop commits | Re-apply doc commits after reset                                             |
| `gh` targets upstream by default                         | Always use `--repo jdmanring/qwen-code`. Run `gh repo view` first.           |
| Accidentally mentioning private repos in public content  | Say "reference repo" instead of naming megalonyx-monorepo                    |
| Stash conflicts from `.qwen/skills/` files               | `git stash drop` and `git checkout develop` to clean up                      |
| Assuming version bumps need no code changes              | Run typecheck before AND after bumps; compare error counts                   |
| Using reference repo source code as a crutch             | Only use reference for version numbers; verify breakage by building the fork |
| Consolidating all fixes into one commit on develop       | Use the "Gold State" workflow to distribute fixes back to granular branches  |
