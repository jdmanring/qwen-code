---
name: fork-rebuild-contributions
description: Rebuild contaminated contribution branches from upstream-mirror when branches have diverged or been polluted with fork-specific changes.
source: auto-skill
extracted_at: '2026-06-13T19:36:52.720Z'
---

# Fork Rebuild Contributions

This skill handles the recovery path when contribution branches have become too contaminated to rebase. Unlike `fork-sync-contributions` (which rebases existing branches), this skill **destroys and recreates** contribution branches from `upstream-mirror`.

## When to Use

Use this skill when:

- Contribution branches were based on `develop` instead of `upstream-mirror`
- Branches contain fork-specific files (docs/fork/, tooling/, .github/) that shouldn't be in upstream PRs
- Branches have more than 5-10 commits (scope creep / merge contamination)
- `git diff upstream-mirror..branch` shows 50+ files changed
- Previous merge into `develop` polluted the branch with fork history

## Pre-Rebuild Checklist

Before destroying anything, verify:

1. **`develop` is safe**: `git status` on develop shows clean working tree
2. **Remote branches exist**: `git ls-remote --heads origin | grep chore/` — you'll force-push over these
3. **You know what each contribution needs**: Review `.qwen/design/` docs or the branch-rebuild-plan for the file inventory per branch

## Rebuild Procedure

### Step 1: Preserve develop

```bash
git checkout develop
git status  # must be clean
```

If develop has uncommitted changes, stash them first: `git stash --include-untracked`

### Step 2: For Each Contribution Branch

#### 2a. Delete the contaminated local branch

```bash
git branch -D chore/<name>
```

#### 2b. Create fresh branch from upstream-mirror

```bash
git checkout -b chore/<name> upstream-mirror
```

#### 2c. Apply changes surgically

There are three strategies, in order of preference:

**Strategy A: sed version bumps (for dependency upgrades)**

Use `sed -i` to change version strings in package.json files. This avoids checking out files from develop (which brings in unrelated changes).

```bash
sed -i 's/"old-pkg": "1.0.0"/"old-pkg": "^2.0.0"/' packages/core/package.json
```

Verify only the intended lines changed:

```bash
git diff -- packages/core/package.json | grep "^[-+]" | grep -v "^---\|^+++"
```

**Strategy B: Checkout specific files from develop (for code changes)**

When the contribution requires actual code changes (not just version bumps), checkout individual files from develop:

```bash
git checkout develop -- packages/core/src/core/openaiContentGenerator/converter.ts
```

Then verify the diff is clean:

```bash
git diff --cached --name-only
```

**Strategy C: Cherry-pick a known-good commit (when available)**

If a clean commit exists on develop that matches exactly what the branch needs:

```bash
git cherry-pick <commit-hash> --no-commit
```

Resolve any conflicts by checking out the upstream-mirror version for unrelated files:

```bash
git checkout --theirs packages/some/package.json  # keep upstream version
git checkout --ours packages/core/src/foo.ts     # keep our change
```

#### 2d. Fix tooling that blocks commits

Common blockers:

- **Husky hooks using `npm`**: If `npm` is not installed, `.husky/pre-commit` will fail. Fix by using the full node path:
  ```bash
  sed -i 's|^npm run pre-commit|export PATH="/home/james/.local/lib/qwen-code/node/bin:$PATH" \&\& /home/james/.local/lib/qwen-code/node/bin/node scripts/pre-commit.js|' .husky/pre-commit
  ```
  **Better approach**: Put the `.husky/pre-commit` fix on a `fork/infra` branch (based on `develop`) and merge it to `develop` first. Then contribution branches inherit the fix and can commit normally without `--no-verify`.
- **ESLint `import/no-internal-modules`**: If checking out files from develop that use internal cross-module imports, add **file-specific** overrides in `eslint.config.js`:
  ```js
  // SubAgentTracker uses internal cross-module imports (./emitters/)
  {
    files: ['packages/cli/src/acp-integration/session/SubAgentTracker.ts'],
    rules: { 'import/no-internal-modules': 'off' },
  },
  ```
  **Important**: The `allow` option in `import/no-internal-modules` does NOT work for relative paths (e.g., `./emitters/ToolCallEmitter.js`). It only matches package-style imports. Use file-specific overrides instead.

#### 2e. Verify the diff

```bash
# Must show only files for this contribution
git diff upstream-mirror..HEAD --name-only

# Must show reasonable change count (not 20K+ lines)
git diff upstream-mirror..HEAD --stat

# Must have no fork-specific files
git diff upstream-mirror..HEAD --name-only | grep -E "^docs/fork|^tooling|^.github" && echo "FAIL: fork files in diff"
```

#### 2f. Stage and commit

```bash
git add <files>
git commit -m "chore(<scope>): <description>

<one-line explanation of what and why>

Co-Authored-By: Claude <<EMAIL>>"
```

**When to use `--no-verify`**: If the `.husky/pre-commit` fix is on `fork/infra` (not yet merged to develop) and you're committing on a contribution branch, `--no-verify` is acceptable for the initial commit. The template explicitly documents this escape hatch. However, prefer merging `fork/infra` to develop first so hooks pass normally.

#### 2g. Push to origin

```bash
git push origin chore/<name> --force-with-lease
```

### Step 3: Repeat for Each Contribution

Rebuild one branch at a time. Verify each before moving to the next.

### Step 4: Return to develop

```bash
git checkout develop
git status  # should be clean, up to date with origin/develop
```

## Key Rules

1. **Branch from `upstream-mirror`, never `develop`** — this is the whole point of the rebuild
2. **Surgical file application** — only include files for this specific contribution
3. **sed > checkout** — prefer `sed -i` for version bumps over `git checkout develop --` (which brings in unrelated changes)
4. **Fork-only infra goes on `fork/*` branches** — `.husky/pre-commit` fixes, CI changes, and other fork-only changes go on a `fork/infra` branch based on `develop`, not on contribution branches. This keeps contribution diffs clean of fork-specific content.
5. **Verify before push** — always run `git diff upstream-mirror..HEAD --name-only` before force-pushing
6. **Never merge contribution branches to develop** — they stay as PR staging branches
7. **`--no-verify` is a last resort** — acceptable for initial commits when `fork/infra` hasn't been merged yet, but prefer fixing the root cause

## Common Pitfalls

| Pitfall                                                                   | How to avoid                                                                                                                                                  |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cherry-pick brings in unrelated changes                                   | Use `git cherry-pick --no-commit`, then `git reset HEAD` and re-stage only the files you need                                                                 |
| package.json has diverging versions for other deps                        | Use `sed -i` to change only the target package, not `git checkout develop -- package.json`                                                                    |
| ESLint `import/no-internal-modules` blocks commit                         | Add file-specific override in `eslint.config.js`, not a blanket package-wide disable                                                                          |
| `import/no-internal-modules` `allow` list doesn't work for relative paths | The `allow` option only matches package-style imports (e.g., `yargs/**`), NOT relative paths (e.g., `./emitters/Foo.js`). Use file-specific overrides instead |
| Husky hook uses `npm` which isn't installed                               | Put the fix on `fork/infra` branch (based on `develop`), not on contribution branches                                                                         |
| Accidentally staging build artifacts                                      | Check `git diff --name-only` for `.d.ts`, `.js.map`, `dist/` files                                                                                            |
| Fork-specific files in contribution diffs                                 | Never include `.husky/`, `docs/fork/`, `tooling/`, `.github/` in contribution branches — use `fork/*` branches instead                                        |

## Verification Command

For each rebuilt branch, run this to confirm it's clean:

```bash
echo "=== Branch: chore/<name> ==="
echo "Files changed:"
git diff upstream-mirror..HEAD --name-only
echo ""
echo "Change size:"
git diff upstream-mirror..HEAD --stat
echo ""
echo "Fork-specific files (should be empty):"
git diff upstream-mirror..HEAD --name-only | grep -E "^docs/fork|^tooling|^.github|^.qwen" || echo "(none)"
echo ""
echo "Merge base with upstream-mirror:"
git merge-base HEAD upstream-mirror
echo "Upstream-mirror HEAD:"
git rev-parse upstream-mirror
echo "(should be the same)"
```
