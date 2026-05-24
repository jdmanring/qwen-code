#!/usr/bin/env bash
# Installs git hooks from tooling/git-hooks/ into .git/hooks/.
# Run once after cloning the repo.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_SRC="${REPO_ROOT}/tooling/git-hooks"
HOOKS_DEST="${REPO_ROOT}/.git/hooks"

for hook in "${HOOKS_SRC}"/*; do
    name="$(basename "${hook}")"
    dest="${HOOKS_DEST}/${name}"
    cp "${hook}" "${dest}"
    chmod +x "${dest}"
    echo "installed: .git/hooks/${name}"
done

echo "done."
