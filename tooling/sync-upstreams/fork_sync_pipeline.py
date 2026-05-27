#!/usr/bin/env python3
"""
Fork Sync Pipeline

Manages bidirectional code flow between QwenLM/qwen-code and the monorepo
via the jdmanring/qwen-code fork ('upstream' remote).

The fork serves two roles:

  Inbound filter  -- New QwenLM commits land in the fork first. A human reviews
                    them here before upstream_ingest_pipeline.py absorbs them
                    into integration. This prevents QwenLM breakage from entering
                    our pipeline unexamined.

  Outbound channel -- Fixes destined for QwenLM are pushed to the fork as clean
                     branches, then opened as PRs. The fork keeps all monorepo
                     history out of the upstream diff.

Usage (run from the monorepo root):

  Show fork position vs QwenLM and vs integration:
    python3 tooling/sync-upstreams/fork_sync_pipeline.py --status

  Absorb new QwenLM commits into the fork (inbound):
    python3 tooling/sync-upstreams/fork_sync_pipeline.py --sync
    python3 tooling/sync-upstreams/fork_sync_pipeline.py --sync --dry-run

  Push a fix to the fork as an upstream PR branch (outbound):
    python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <branch>
    python3 tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <branch> --dry-run

Inbound flow (--sync):
  QwenLM/qwen-code
    | fetch to temp ref (no persistent remote added to monorepo)
    | GATE-CIFILES   -- .github/workflows/ files changed?  (advisory)
    | GATE-PROTECTED -- PROTECTED_FILES changed?            (advisory)
    | GATE-MANIFESTS -- package.json / lockfiles changed?  (advisory)
    | GATE-NEWFILES  -- new files added to the repo?       (advisory)
    | human confirmation (explicit 'y' required)
  upstream/main  (jdmanring/qwen-code)
    | next step: python3 tooling/sync-upstreams/upstream_ingest_pipeline.py

Outbound flow (--contribute <hash> <branch>):
  commit on develop
    | GATE-MEGALONYX -- diff contains 'megalonyx'?          HARD BLOCK
    | GATE-PNPM      -- diff contains 'pnpm-workspace'?     HARD BLOCK
    | GATE-JDMANRING -- diff contains 'jdmanring'?          HARD BLOCK
    | GATE-CONFIG    -- diff contains 'config/megalonyx'?   HARD BLOCK
    | GATE-CIFILES   -- diff touches PROTECTED_FILES?       HARD BLOCK
    | cherry-pick onto contribute/<branch> from upstream/main
  upstream fork  ->  PR to QwenLM/qwen-code
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

# URL of the upstream source. Never added as a persistent remote --
# fetched into a temporary ref only during --sync and --status.
QWENLM_URL = "https://github.com/QwenLM/qwen-code.git"

# Temporary ref used during --sync and --status. Cleaned up after every run.
QWENLM_TEMP_REF = "refs/sync-pipeline/qwenlm-snapshot"

# The 'upstream' remote points to jdmanring/qwen-code (the fork).
# It is both the inbound source for our pipeline and the outbound PR channel.
UPSTREAM_REMOTE = "upstream"

FORK_OWNER = "jdmanring"
QWENLM_OWNER = "QwenLM"
QWENLM_REPO = "qwen-code"
INTEGRATION_BRANCH = "integration"

# Files owned by Megalonyx that differ from upstream.
# Inbound: changes are flagged for review.
# Outbound: any appearance in the diff is a hard block.
PROTECTED_FILES: list[str] = [
    ".github/workflows/ci.yml",
    ".github/workflows/e2e.yml",
    "packages/sdk-python/pyproject.toml",
]

# Manifest patterns whose changes signal dependency updates needing evaluation.
MANIFEST_PATTERNS: list[str] = [
    "package.json",
    "pnpm-workspace.yaml",
    "pyproject.toml",
    "uv.lock",
    "pnpm-lock.yaml",
]


class Colors:
    BLUE = "\033[0;34m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    YELLOW = "\033[0;33m"
    NC = "\033[0m"


def log_info(msg: str) -> None:
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")


def log_success(msg: str) -> None:
    print(f"{Colors.GREEN}[OK]{Colors.NC} {msg}")


def log_warn(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {msg}")


def log_error(msg: str) -> None:
    print(f"{Colors.RED}[FAIL]{Colors.NC} {msg}", file=sys.stderr)


@dataclass
class GateResult:
    name: str
    passed: bool
    message: str
    lines: list[str] = field(default_factory=list)


class _GitRunner:
    """Thin subprocess wrapper scoped to the repo root."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, check=check)

    def output(self, cmd: list[str]) -> str:
        return self.run(cmd).stdout.strip()

    def current_branch(self) -> str:
        return self.output(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    def remote_exists(self, name: str) -> bool:
        return name in self.output(["git", "remote"]).splitlines()


def _check_preflight(git: _GitRunner) -> None:
    """
    Validates the environment before any git operations.
    Raises RuntimeError with a clear message if any check fails.
    """
    if not git.remote_exists(UPSTREAM_REMOTE):
        raise RuntimeError(
            f"'{UPSTREAM_REMOTE}' remote not found.\n"
            f"  Add it:  git remote add {UPSTREAM_REMOTE} "
            f"https://github.com/{FORK_OWNER}/{QWENLM_REPO}.git"
        )


# -- Advisory gates (inbound --sync) ------------------------------------------
#
# Advisory gates flag changes that need human attention before absorbing QwenLM
# commits into the fork. They do not hard-block -- the human acknowledges each
# flagged item and then confirms (or cancels) the sync.


def gate_ci_files(changed_files: list[str]) -> GateResult:
    """
    Flags changes to .github/workflows/ files.

    Our CI is patched for pnpm. Upstream CI changes may conflict with those
    patches. Verify that any CI change here does not overwrite our modifications
    before absorbing.
    """
    hits = [f for f in changed_files if f.startswith(".github/workflows/")]
    return GateResult(
        name="GATE-CIFILES",
        passed=not hits,
        message=(
            "CI workflow file(s) changed -- our CI is patched for pnpm. "
            "Verify these do not overwrite our patches."
        ),
        lines=hits,
    )


def gate_protected_files(changed_files: list[str]) -> GateResult:
    """
    Flags changes to PROTECTED_FILES specifically.

    These files are deliberately maintained differently from upstream.
    The monorepo's upstream_ingest_pipeline.py will restore them after merging,
    but the fork sync is the earlier opportunity to review the diff.
    """
    hits = [f for f in changed_files if f in PROTECTED_FILES]
    return GateResult(
        name="GATE-PROTECTED",
        passed=not hits,
        message=(
            "PROTECTED_FILES changed -- these are owned by Megalonyx and "
            "maintained differently from upstream."
        ),
        lines=hits,
    )


def gate_manifests(changed_files: list[str]) -> GateResult:
    """
    Flags changes to package manifests and lockfiles.

    Dependency bumps may conflict with our pinned versions in pnpm-workspace.yaml
    overrides. Evaluate each bump before it enters the monorepo pipeline.
    """
    hits = [
        f for f in changed_files if any(f == m or f.endswith(f"/{m}") for m in MANIFEST_PATTERNS)
    ]
    return GateResult(
        name="GATE-MANIFESTS",
        passed=not hits,
        message="Package manifest/lockfile changed -- evaluate dep bumps before absorbing.",
        lines=hits,
    )


def gate_new_files(added_files: list[str]) -> GateResult:
    """
    Flags newly added files.

    New files may introduce new dependencies, configuration conventions, or
    tooling that conflicts with the monorepo setup.
    """
    return GateResult(
        name="GATE-NEWFILES",
        passed=not added_files,
        message="New file(s) added -- review before absorbing into the pipeline.",
        lines=added_files,
    )


# -- Isolation gates (outbound --contribute) -----------------------------------
#
# Isolation gates prevent Megalonyx-specific content from leaking into upstream
# PRs. These are HARD BLOCKS -- no override. A failed isolation gate means the
# commit must be cleaned up before it can go upstream.


def _gate_isolation_pattern(diff: str, pattern: str, gate_name: str, message: str) -> GateResult:
    """
    Scans a commit diff for a pattern that must not appear in upstream PRs.

    Checks added content lines (+) and git diff file headers (diff --git) so
    that both content references and file-path references are caught.
    """
    hits = [
        line
        for line in diff.splitlines()
        if pattern.lower() in line.lower()
        and (line.startswith("+") or line.startswith("diff --git"))
    ]
    return GateResult(name=gate_name, passed=not hits, message=message, lines=hits)


def run_isolation_gates(diff: str, changed_files: list[str]) -> list[GateResult]:
    """
    Runs all five isolation gates against a commit diff.

    Returns a list of GateResult -- any failure is a hard block. No cherry-pick
    is attempted if any gate fails.

    Args:
        diff:          output of `git show --format= <hash>`
        changed_files: output of `git diff-tree --no-commit-id -r --name-only <hash>`
    """
    results = [
        _gate_isolation_pattern(
            diff,
            "megalonyx",
            "GATE-MEGALONYX",
            "Diff contains 'megalonyx' -- remove all Megalonyx-specific references.",
        ),
        _gate_isolation_pattern(
            diff,
            "pnpm-workspace",
            "GATE-PNPM",
            "Diff contains 'pnpm-workspace' -- pnpm config must not appear upstream.",
        ),
        _gate_isolation_pattern(
            diff,
            "jdmanring",
            "GATE-JDMANRING",
            "Diff contains 'jdmanring' -- fork owner references must not go upstream.",
        ),
        _gate_isolation_pattern(
            diff,
            "config/megalonyx",
            "GATE-CONFIG",
            "Diff contains 'config/megalonyx' -- private config paths must not go upstream.",
        ),
    ]
    protected_hits = [f for f in changed_files if f in PROTECTED_FILES]
    results.append(
        GateResult(
            name="GATE-CIFILES",
            passed=not protected_hits,
            message=("Diff touches PROTECTED_FILES -- our patched CI/config must not go upstream."),
            lines=protected_hits,
        )
    )
    return results


# -- Mode implementations ------------------------------------------------------


def cmd_status(git: _GitRunner) -> None:
    """
    Shows the fork's position relative to QwenLM and integration.
    Read-only -- no git state is modified.

    Fetches from QwenLM (via URL, no persistent remote) and from the fork to
    get current commit counts for both directions.
    """
    log_info("Fetching fork and QwenLM state...")
    git.run(["git", "fetch", UPSTREAM_REMOTE, "main"])
    git.run(["git", "fetch", QWENLM_URL, f"main:{QWENLM_TEMP_REF}"])

    try:
        fork_lag = git.output(
            [
                "git",
                "rev-list",
                "--count",
                f"{UPSTREAM_REMOTE}/main..{QWENLM_TEMP_REF}",
            ]
        )
        fork_ahead = git.output(
            [
                "git",
                "rev-list",
                "--count",
                f"{QWENLM_TEMP_REF}..{UPSTREAM_REMOTE}/main",
            ]
        )
        pipeline_lag = git.output(
            [
                "git",
                "rev-list",
                "--count",
                f"{INTEGRATION_BRANCH}..{UPSTREAM_REMOTE}/main",
            ]
        )

        print()
        if fork_lag == "0" and fork_ahead == "0":
            log_success("Fork is in sync with QwenLM.")
        elif fork_lag == "0":
            log_warn(
                f"Fork is {fork_ahead} commit(s) ahead of QwenLM "
                "(e.g. merged PRs not yet in QwenLM main -- this is normal)."
            )
        else:
            log_warn(f"Fork is {fork_lag} commit(s) behind QwenLM:")
            commits = git.output(
                [
                    "git",
                    "log",
                    "--oneline",
                    f"{UPSTREAM_REMOTE}/main..{QWENLM_TEMP_REF}",
                ]
            )
            for line in commits.splitlines():
                print(f"       {line}")
            print()
            print("  Absorb:  python3 tooling/sync-upstreams/fork_sync_pipeline.py --sync")

        print()
        if pipeline_lag == "0":
            log_success("Integration is up to date with the fork.")
        else:
            log_warn(f"Integration is {pipeline_lag} commit(s) behind the fork:")
            commits = git.output(
                [
                    "git",
                    "log",
                    "--oneline",
                    f"{INTEGRATION_BRANCH}..{UPSTREAM_REMOTE}/main",
                ]
            )
            for line in commits.splitlines():
                print(f"       {line}")
            print()
            print("  Absorb:  python3 tooling/sync-upstreams/upstream_ingest_pipeline.py")

        print()
        branches_raw = git.output(["git", "ls-remote", "--heads", UPSTREAM_REMOTE, "contribute/*"])
        if branches_raw:
            names = [
                line.split("refs/heads/")[-1]
                for line in branches_raw.splitlines()
                if "refs/heads/" in line
            ]
            log_info(f"Active contribute/* branches on fork ({len(names)}):")
            for b in names:
                print(f"       {b}")
        else:
            log_success("No active contribute/* branches on fork.")
        print()

    finally:
        git.run(["git", "update-ref", "-d", QWENLM_TEMP_REF], check=False)


def cmd_sync(git: _GitRunner, dry_run: bool = False, auto: bool = False) -> None:
    """
    Inbound: fetches new QwenLM commits, runs advisory gates, and on confirmation
    fast-forward pushes them to the fork (upstream remote).

    Advisory gates are informational -- they display flagged items so the human
    can make an informed decision. After reviewing, an explicit 'y' is required
    to proceed. Any answer other than 'y' cancels the sync safely.

    If --auto is provided, confirmation is skipped and sync proceeds automatically.

    After a successful sync, run upstream_ingest_pipeline.py to absorb the
    fork's new commits into integration.
    """
    if dry_run:
        log_warn("[dry-run] Advisory gates will run; nothing will be pushed.")

    log_info("Fetching QwenLM/qwen-code main...")
    git.run(["git", "fetch", QWENLM_URL, f"main:{QWENLM_TEMP_REF}"])
    git.run(["git", "fetch", UPSTREAM_REMOTE, "main"])

    try:
        qwenlm_ahead = int(
            git.output(
                [
                    "git",
                    "rev-list",
                    "--count",
                    f"{UPSTREAM_REMOTE}/main..{QWENLM_TEMP_REF}",
                ]
            )
        )
        fork_ahead = int(
            git.output(
                [
                    "git",
                    "rev-list",
                    "--count",
                    f"{QWENLM_TEMP_REF}..{UPSTREAM_REMOTE}/main",
                ]
            )
        )

        if qwenlm_ahead == 0:
            if fork_ahead > 0:
                log_warn(f"Fork is {fork_ahead} commit(s) ahead of QwenLM -- nothing to absorb.")
            else:
                log_success("Fork is already up to date with QwenLM.")
            return

        print()
        log_info(f"{qwenlm_ahead} new QwenLM commit(s) to review:")
        commits = git.output(
            [
                "git",
                "log",
                "--oneline",
                f"{UPSTREAM_REMOTE}/main..{QWENLM_TEMP_REF}",
            ]
        )
        for line in commits.splitlines():
            print(f"  {line}")
        print()

        # Compute advisory gate inputs
        changed_raw = git.output(
            [
                "git",
                "diff",
                "--name-only",
                f"{UPSTREAM_REMOTE}/main",
                QWENLM_TEMP_REF,
            ]
        )
        changed_files = changed_raw.splitlines() if changed_raw else []

        added_raw = git.output(
            [
                "git",
                "diff",
                "--name-only",
                "--diff-filter=A",
                f"{UPSTREAM_REMOTE}/main",
                QWENLM_TEMP_REF,
            ]
        )
        added_files = added_raw.splitlines() if added_raw else []

        gates = [
            gate_ci_files(changed_files),
            gate_protected_files(changed_files),
            gate_manifests(changed_files),
            gate_new_files(added_files),
        ]
        flagged = [g for g in gates if not g.passed]

        if flagged:
            for g in flagged:
                log_warn(f"{g.name}: {g.message}")
                for line in g.lines:
                    print(f"         {Colors.YELLOW}{line}{Colors.NC}")
            print()
            log_warn(f"{len(flagged)} advisory flag(s) -- review each before confirming.")
        else:
            log_success("Advisory gates: nothing flagged.")

        if dry_run:
            log_info("[dry-run] No changes pushed.")
            return

        # Verify fast-forward safety before attempting push
        is_ff = (
            git.run(
                [
                    "git",
                    "merge-base",
                    "--is-ancestor",
                    f"{UPSTREAM_REMOTE}/main",
                    QWENLM_TEMP_REF,
                ],
                check=False,
            ).returncode
            == 0
        )
        if not is_ff:
            raise RuntimeError(
                "QwenLM history has diverged from the fork -- cannot fast-forward.\n"
                "The fork has commits not in QwenLM. Manual resolution required."
            )

        print()
        if auto:
            confirm = "y"
            log_info("Auto-mode enabled: skipping confirmation.")
        else:
            prompt = f"Absorb {qwenlm_ahead} commit(s) into the fork? [y/N] "
            confirm = input(prompt).strip().lower()

        if confirm != "y":
            log_warn("Sync cancelled.")
            return

        log_info(f"Pushing to {UPSTREAM_REMOTE}/main...")
        git.run(["git", "push", UPSTREAM_REMOTE, f"{QWENLM_TEMP_REF}:main"])
        log_success("Fork updated.")
        print()
        log_info("Next step -- absorb into integration:")
        print("  python3 tooling/sync-upstreams/upstream_ingest_pipeline.py")
        print()

    finally:
        git.run(["git", "update-ref", "-d", QWENLM_TEMP_REF], check=False)


def cmd_contribute(
    git: _GitRunner,
    commit_hash: str,
    branch_name: str,
    dry_run: bool = False,
) -> None:
    """
    Outbound: validates a commit's isolation from Megalonyx, then cherry-picks
    it onto a clean branch from upstream/main and pushes it to the fork.

    Isolation gates are HARD BLOCKS with no override. Any gate failure means the
    commit contains Megalonyx-specific content that must be removed first. See
    docs/upstream/upstream-pr-guide.md for the full contribution procedure.

    The resulting branch on the fork is:  contribute/<branch-name>
    Open the PR at:
      github.com/QwenLM/qwen-code/compare/main...<fork-owner>:<branch>
    """
    if dry_run:
        log_warn("[dry-run] Isolation gates will run; no branch will be created.")

    # Resolve and validate commit
    try:
        full_hash = git.output(["git", "rev-parse", f"{commit_hash}^{{commit}}"])
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Commit '{commit_hash}' not found in this repository.") from exc

    commit_msg = git.output(["git", "log", "--format=%s", "-1", full_hash])
    changed_raw = git.output(["git", "diff-tree", "--no-commit-id", "-r", "--name-only", full_hash])
    changed_files = changed_raw.splitlines() if changed_raw else []

    print()
    log_info(f"Commit  : {full_hash[:12]} -- {commit_msg}")
    log_info(f"Files   : {len(changed_files)} changed")
    for f in changed_files:
        print(f"          {f}")
    print()

    diff = git.output(["git", "show", "--format=", full_hash])
    gates = run_isolation_gates(diff, changed_files)
    failures = [g for g in gates if not g.passed]

    if failures:
        for g in failures:
            log_error(f"{g.name}: {g.message}")
            for line in g.lines[:5]:
                print(f"         {Colors.RED}{line}{Colors.NC}")
            if len(g.lines) > 5:
                print(f"         ... and {len(g.lines) - 5} more")
        print()
        log_error("Isolation gates FAILED -- commit is not upstream-eligible. No branch created.")
        sys.exit(1)

    log_success("All isolation gates passed.")

    if dry_run:
        log_info("[dry-run] No branch created. Commit is clean for contribution.")
        return

    pr_branch = f"contribute/{branch_name}"
    original_branch = git.current_branch()

    log_info(f"Fetching {UPSTREAM_REMOTE}/main...")
    git.run(["git", "fetch", UPSTREAM_REMOTE, "main"])
    log_info(f"Creating clean branch: {pr_branch}")
    git.run(["git", "checkout", "-b", pr_branch, f"{UPSTREAM_REMOTE}/main"])

    try:
        log_info(f"Cherry-picking {full_hash[:12]}...")
        result = git.run(["git", "cherry-pick", "--no-edit", full_hash], check=False)
        if result.returncode != 0:
            print()
            log_error("Cherry-pick conflict. Resolve manually, then:")
            print("  git cherry-pick --continue")
            print(f"  git push {UPSTREAM_REMOTE} {pr_branch}")
            pr_url = (
                f"https://github.com/{QWENLM_OWNER}/{QWENLM_REPO}"
                f"/compare/main...{FORK_OWNER}:{pr_branch}"
            )
            print(f"\n  Open PR:  {pr_url}")
            sys.exit(1)

        log_info(f"Pushing {pr_branch} to {UPSTREAM_REMOTE}...")
        git.run(["git", "push", UPSTREAM_REMOTE, pr_branch])

        pr_url = (
            f"https://github.com/{QWENLM_OWNER}/{QWENLM_REPO}"
            f"/compare/main...{FORK_OWNER}:{pr_branch}"
        )
        print()
        log_success("Branch pushed to fork.")
        print()
        print(f"  Open PR:  {pr_url}")
        print()
        log_info("PR checklist (docs/upstream/upstream-pr-guide.md):")
        print("  [ ] Title: conventional commits format  (fix(scope): description)")
        print("  [ ] Description: what changed, why, how tested")
        print("  [ ] QwenLM CI passes on the branch")
        print()

    finally:
        current = git.current_branch()
        if current == pr_branch:
            git.run(["git", "checkout", original_branch], check=False)
        git.run(["git", "branch", "-D", pr_branch], check=False)


# -- CLI entry point -----------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Fork Sync Pipeline -- manages bidirectional code flow between\n"
            "QwenLM/qwen-code and the monorepo via the jdmanring/qwen-code fork.\n\n"
            "Start with --status to see what is pending, then use --sync (inbound)\n"
            "or --contribute (outbound) to act."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--status",
        action="store_true",
        help="Show fork position vs QwenLM and vs integration. Read-only.",
    )
    mode.add_argument(
        "--sync",
        action="store_true",
        help=(
            "Inbound: fetch QwenLM commits, run advisory gates, push to fork. "
            "Run upstream_ingest_pipeline.py next to absorb into integration."
        ),
    )
    mode.add_argument(
        "--contribute",
        nargs=2,
        metavar=("HASH", "BRANCH"),
        help=(
            "Outbound: run isolation gates then cherry-pick commit as "
            "contribute/<BRANCH> on the fork."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=("Evaluate gates only; do not push anything. Valid with --sync and --contribute."),
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Skip confirmation for --sync and proceed automatically.",
    )
    args = parser.parse_args()

    git = _GitRunner(REPO_ROOT)

    try:
        _check_preflight(git)

        if args.status:
            cmd_status(git)
        elif args.sync:
            cmd_sync(git, dry_run=args.dry_run, auto=args.auto)
        elif args.contribute:
            commit_hash, branch_name = args.contribute
            cmd_contribute(git, commit_hash, branch_name, dry_run=args.dry_run)

    except (RuntimeError, subprocess.CalledProcessError, OSError) as e:
        log_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
