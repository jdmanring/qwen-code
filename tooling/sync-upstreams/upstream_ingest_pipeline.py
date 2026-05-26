#!/usr/bin/env python3
"""
Upstream Ingest Pipeline
Propagates changes from upstream-mirror to integration through a hardened
verification pipeline: Sync → Gate(Boot/Lint/Symmetry) → Promote.

Usage:
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py           # full sync
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run # gates only
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, stream=sys.stdout)
logger = logging.getLogger("upstream_ingest_pipeline")

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
INTEGRATION_BRANCH = "integration"
MIRROR_BRANCH = "upstream-mirror"
REQUIRED_REMOTES = {"upstream", "origin"}

# Files owned by Megalonyx that must not be overwritten by upstream merges.
# After each merge, the pipeline restores these files to their integration-branch
# state so that a non-conflicting upstream change cannot silently replace our patches.
# Add any file here that we deliberately maintain differently from upstream.
PROTECTED_FILES: list[str] = [
    ".github/workflows/ci.yml",
    ".github/workflows/e2e.yml",
    "packages/sdk-python/pyproject.toml",
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
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {msg}", file=sys.stderr)


def log_error(msg: str) -> None:
    print(f"{Colors.RED}[FAIL]{Colors.NC} {msg}", file=sys.stderr)


def _resolve_ruff() -> list[str]:
    """
    Resolves the ruff command so every caller uses the same binary.

    Priority:
      1. `uv run ruff`  — uses the project-pinned version via uv (preferred)
      2. RUFF_BIN env var — explicit override for CI environments
      3. PATH ruff       — last resort

    This eliminates the "works on my machine" false-green problem where
    different ruff versions disagree on what constitutes a lint error.
    """
    if shutil.which("uv"):
        return ["uv", "run", "ruff"]
    env_ruff = os.environ.get("RUFF_BIN")
    if env_ruff:
        if not Path(env_ruff).exists():
            raise RuntimeError(f"RUFF_BIN={env_ruff!r} does not exist.")
        return [env_ruff]
    system_ruff = shutil.which("ruff")
    if system_ruff:
        return [system_ruff]
    raise RuntimeError(
        "ruff not found. Install uv (https://docs.astral.sh/uv/) or set RUFF_BIN=/path/to/ruff"
    )


@dataclass
class SyncResult:
    success: bool
    stage: str
    message: str
    lkg_tag: str | None = None
    dry_run: bool = False


class _GitRunner:
    """Thin wrapper around git subprocess calls scoped to a fixed root."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, check=check)

    def output(self, cmd: list[str]) -> str:
        return self.run(cmd).stdout.strip()

    def current_branch(self) -> str:
        return self.output(["git", "rev-parse", "--abbrev-ref", "HEAD"])


class PreFlight:
    """Validates the environment before any destructive operation begins."""

    def __init__(self, git: _GitRunner) -> None:
        self._git = git

    def check(self) -> bool:
        logger.info("Running pre-flight checks...")
        try:
            branch = self._git.current_branch()
            if branch != INTEGRATION_BRANCH:
                raise RuntimeError(f"Must be on '{INTEGRATION_BRANCH}' branch. Current: '{branch}'")

            remotes = set(self._git.output(["git", "remote"]).splitlines())
            missing = REQUIRED_REMOTES - remotes
            if missing:
                raise RuntimeError(f"Missing required remotes: {missing}")

            symmetry_check = self._git.root / "tooling" / "symmetry_check.py"
            if not symmetry_check.exists():
                raise RuntimeError(f"Missing {symmetry_check.relative_to(self._git.root)}")

            _resolve_ruff()

            if not shutil.which("uv"):
                raise RuntimeError("uv not found. Install from https://docs.astral.sh/uv/")

            # Only block on changes to tracked files — untracked files can't pollute a merge.
            dirty = self._git.run(["git", "diff", "--quiet", "HEAD"], check=False).returncode != 0
            if dirty:
                raise RuntimeError(
                    "Integration branch has uncommitted changes — stash or commit before syncing."
                )

            log_success("Pre-flight passed.")
            return True
        except (RuntimeError, subprocess.CalledProcessError, OSError) as e:
            log_error(f"Pre-flight failed: {e}")
            return False


class SyncManager:
    """Handles the git operations that move upstream changes into a staging branch."""

    def __init__(self, git: _GitRunner) -> None:
        self._git = git
        self.staging_branch: str | None = None

    def sync_mirror(self) -> bool:
        """
        Fetches upstream/main, checks for new commits, then resets upstream-mirror
        and returns to integration.

        Returns False if integration already contains all upstream commits (nothing to do).
        """
        log_info("Fetching upstream/main...")
        self._git.run(["git", "fetch", "upstream", "main"])

        new_count = self._git.output(
            ["git", "rev-list", "--count", "upstream/main", f"^{INTEGRATION_BRANCH}"]
        )
        if new_count == "0":
            log_success("Already up to date — nothing to sync.")
            return False

        log_info(f"{new_count} new upstream commit(s) to integrate.")
        log_info(f"Resetting {MIRROR_BRANCH} to upstream/main...")
        self._git.run(["git", "checkout", "-f", MIRROR_BRANCH])
        self._git.run(["git", "reset", "--hard", "upstream/main"])

        self._git.run(["git", "checkout", INTEGRATION_BRANCH])
        log_success("Mirror synchronized.")
        return True

    def create_staging(self) -> None:
        """Creates a short-lived staging branch from integration HEAD."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.staging_branch = f"sync/staging-{timestamp}"
        log_info(f"Creating staging branch: {self.staging_branch}")
        self._git.run(["git", "checkout", "-b", self.staging_branch])

    # Files that are always resolved by keeping ours. package-lock.json is
    # upstream's npm lockfile; this repo uses pnpm-lock.yaml instead.
    _AUTO_RESOLVE_OURS: frozenset[str] = frozenset({"package-lock.json"})

    def merge_mirror_to_stage(self) -> None:
        """
        Merges upstream-mirror into the staging branch.
        Files in _AUTO_RESOLVE_OURS are auto-resolved (keep ours); any other
        conflict aborts and requires manual resolution. After a clean merge,
        restores PROTECTED_FILES so non-conflicting upstream changes cannot
        silently overwrite our patches.
        """
        integration_ref = self._git.output(["git", "rev-parse", "HEAD"])

        log_info(f"Merging {MIRROR_BRANCH} into {self.staging_branch}...")
        result = self._git.run(["git", "merge", MIRROR_BRANCH, "--no-edit"], check=False)
        if result.returncode == 0:
            log_success("Merge clean.")
            self._restore_protected_files(integration_ref)
            return

        conflict_files = self._git.output(["git", "diff", "--name-only", "--diff-filter=U"])
        conflict_set = {f.strip() for f in conflict_files.splitlines() if f.strip()}
        unresolvable = conflict_set - self._AUTO_RESOLVE_OURS

        if unresolvable:
            self._git.run(["git", "merge", "--abort"], check=False)
            files = "\n".join(sorted(unresolvable))
            raise RuntimeError(
                f"Merge conflict — manual resolution required:\n{files}\n\n"
                "Resolve, commit, then re-run the ingest pipeline."
            )

        for f in conflict_set & self._AUTO_RESOLVE_OURS:
            log_info(f"Auto-resolving {f} (keeping ours)")
            self._git.run(["git", "checkout", "--ours", f], check=True)
            self._git.run(["git", "add", f], check=True)

        self._git.run(
            ["git", "-c", "core.editor=true", "merge", "--continue"],
            check=True,
        )
        resolved = ", ".join(sorted(conflict_set & self._AUTO_RESOLVE_OURS))
        log_success(f"Merge clean (auto-resolved: {resolved}).")

    def _restore_protected_files(self, integration_ref: str) -> None:
        """
        Restores Megalonyx-owned files to their integration-branch version after merge.

        Prevents upstream changes to PROTECTED_FILES from silently overwriting
        our patched versions even when the merge produces no conflict. Without this,
        a non-conflicting upstream edit to (e.g.) ci.yml would replace our pnpm
        patches on every sync.
        """
        for path in PROTECTED_FILES:
            self._git.run(["git", "checkout", integration_ref, "--", path], check=False)

        staged = self._git.output(["git", "diff", "--cached", "--name-only"])
        restored = [f for f in staged.splitlines() if f in PROTECTED_FILES]
        if restored:
            log_info(f"Restored {len(restored)} protected file(s): {restored}")
            self._git.run(
                [
                    "git",
                    "commit",
                    "-m",
                    "chore(sync): restore Megalonyx-owned files after upstream merge",
                ]
            )
        else:
            log_success("Protected files unchanged by upstream — no restoration needed.")

    def cleanup_staging(self) -> None:
        if not self.staging_branch:
            return
        if self._git.current_branch() == self.staging_branch:
            self._git.run(["git", "checkout", INTEGRATION_BRANCH])
        self._git.run(["git", "branch", "-D", self.staging_branch], check=False)
        self.staging_branch = None


class GateKeeper:
    """Runs the three verification gates. All three must pass for promotion."""

    def __init__(self, git: _GitRunner) -> None:
        self._git = git
        self._ruff = _resolve_ruff()

    def verify(self) -> bool:
        # Boot runs first: fail before `uv run ruff` can recreate a missing lockfile.
        return self._gate_boot() and self._gate_lint() and self._gate_symmetry()

    def _gate_boot(self) -> bool:
        """
        Runs first — verifies the Python workspace is bootable before any `uv run`
        command can silently recreate a stale or missing lockfile.
        """
        logger.info("Gate 1/3: Boot test (uv lock --check)...")
        result = subprocess.run(
            ["uv", "lock", "--check"],
            cwd=self._git.root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            log_error(
                f"Boot gate failed — lockfile out of sync:\n"
                f"{result.stderr.strip()}\n"
                "Fix with: uv lock"
            )
            return False
        log_success("Boot gate passed.")
        return True

    def _gate_lint(self) -> bool:
        logger.info("Gate 2/3: Ruff lint...")
        cmd = self._ruff + ["check", "."]
        result = subprocess.run(cmd, cwd=self._git.root)
        if result.returncode != 0:
            fix_cmd = " ".join(self._ruff + ["check", "--fix", "."])
            log_error(f"Lint gate failed. Auto-fix attempt: {fix_cmd}")
            return False
        log_success("Lint gate passed.")
        return True

    def _gate_symmetry(self) -> bool:
        logger.info("Gate 3/3: Symmetry check (config ↔ docs)...")
        result = subprocess.run(
            ["python3", "tooling/symmetry_check.py"],
            cwd=self._git.root,
        )
        if result.returncode != 0:
            log_error("Symmetry gate failed. config/ and docs/ are out of sync.")
            return False
        log_success("Symmetry gate passed.")
        return True


class PromotionEngine:
    """Fast-forward merges the verified staging branch into integration and tags it."""

    def __init__(self, git: _GitRunner) -> None:
        self._git = git

    def promote(self, staging_branch: str) -> str:
        log_info(f"Promoting {staging_branch} → {INTEGRATION_BRANCH}...")
        self._git.run(["git", "checkout", INTEGRATION_BRANCH])
        self._git.run(["git", "merge", "--ff-only", staging_branch])

        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        tag = f"LKG-{timestamp}"
        self._git.run(["git", "tag", "-a", tag, "-m", f"Last Known Good — {timestamp}"])
        log_success(f"Tagged as {tag}.")
        return tag


class UpstreamIngestPipeline:
    """
    Coordinates the full upstream ingestion pipeline:

        upstream/main
            ↓  (fetch + reset)
        upstream-mirror
            ↓  (merge into staging branch off integration)
        sync/staging-TIMESTAMP
            ↓  (Gate 1: uv lock --check)
            ↓  (Gate 2: ruff lint)
            ↓  (Gate 3: symmetry check)
        integration  [ff-only merge + LKG tag]
    """

    def __init__(self, dry_run: bool = False) -> None:
        self._git = _GitRunner(REPO_ROOT)
        self._dry_run = dry_run
        self.preflight = PreFlight(self._git)
        self.sync = SyncManager(self._git)
        self.gates = GateKeeper(self._git)
        self.promotion = PromotionEngine(self._git)

    def run(self) -> SyncResult:
        if self._dry_run:
            log_warn("DRY RUN — gates will run against current state; no commits or tags.")

        if not self.preflight.check():
            return SyncResult(False, "PREFLIGHT", "Pre-flight checks failed.")

        try:
            if not self._dry_run:
                has_new = self.sync.sync_mirror()
                if not has_new:
                    return SyncResult(True, "UP_TO_DATE", "Already up to date.")
                self.sync.create_staging()
                self.sync.merge_mirror_to_stage()
            else:
                log_info("[dry-run] Skipping sync and staging.")

            if not self.gates.verify():
                return SyncResult(
                    False,
                    "VERIFICATION",
                    "One or more verification gates failed.",
                    dry_run=self._dry_run,
                )

            if self._dry_run:
                log_success("[dry-run] All gates passed. Nothing promoted.")
                return SyncResult(True, "DRY_RUN", "Dry run complete.", dry_run=True)

            if not self.sync.staging_branch:
                raise RuntimeError("staging_branch is None after create_staging — this is a bug")
            tag = self.promotion.promote(self.sync.staging_branch)
            return SyncResult(True, "PROMOTION", "Sync complete.", lkg_tag=tag)

        except (RuntimeError, subprocess.CalledProcessError, OSError) as e:
            log_error(str(e))
            return SyncResult(False, "PIPELINE_ERROR", str(e))
        finally:
            if not self._dry_run:
                self.sync.cleanup_staging()
                # Ensure we always land on integration regardless of where a failure left us.
                if self._git.current_branch() != INTEGRATION_BRANCH:
                    self._git.run(["git", "checkout", INTEGRATION_BRANCH], check=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Upstream Ingest Pipeline — ingests upstream-mirror into integration "
            "through a three-gate verification pipeline."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run all gates against the current working state without syncing or promoting.",
    )
    args = parser.parse_args()

    orch = UpstreamIngestPipeline(dry_run=args.dry_run)
    result = orch.run()

    if result.success:
        if result.lkg_tag:
            log_success(f"Pipeline complete. LKG tag: {result.lkg_tag}")
        elif result.stage == "UP_TO_DATE":
            log_success("Nothing to do — integration is already current.")
        sys.exit(0)
    else:
        log_error(f"Pipeline failed at [{result.stage}]: {result.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
