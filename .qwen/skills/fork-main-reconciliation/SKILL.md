---
name: fork-main-reconciliation
description: Reconcile a divergent fork release branch by promoting an integration branch containing all staged contributions.
source: auto-skill
extracted_at: '2026-06-13T05:15:00.000Z'
---

When a fork's release branch (`main`) has diverged significantly from the `upstream/main` and contains a mix of upstream updates and fork-specific contributions, use this promotion-based reconciliation workflow instead of individual cherry-picking.

### Procedure

1. **Audit Divergence**
   - Identify how far `main` is behind `upstream/main` (`git log origin/main..upstream/main --oneline | wc -l`).
   - Verify that the integration branch (`develop`) is up-to-date with the latest upstream source.

2. **Promote via Integration Branch**
   - Instead of cherry-picking commits directly onto `main`, merge all staged contribution branches into `develop` first.
   - This ensures that all inter-contribution conflicts are resolved in the integration environment before the release.
   - **Handling Dependency Conflicts**: When merging multiple branches that update `package.json` (e.g., version bumps), use `git merge -X theirs <branch>` to automatically favor the incoming branch's version for trivial conflicts.

3. **Reset Release Branch**
   - Checkout the release branch: `git checkout main`.
   - Reset it to the now-complete integration branch: `git reset --hard develop`.
   - Force-push the clean release to the remote: `git push origin main --force`.

4. **Remote State Cleanup**
   - Delete stale remnant branches (e.g., `origin/upstream-main`).
   - Prune orphaned remote contribution branches that are no longer tracked in the project's PR status records.

5. **Local Branch Realignment**
   - Rebase all active local contribution branches onto the `upstream-mirror` to ensure they are based on the latest upstream source, not the stale `develop` or `main`.
   - Delete temporary workbench branches.
