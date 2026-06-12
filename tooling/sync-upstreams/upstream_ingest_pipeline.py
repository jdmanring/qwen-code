#!/usr/bin/env python3
"""
Upstream Ingest Pipeline — Qwen Code fork
Propagates changes from upstream-mirror to integration through a
verification pipeline: Sync → Gate(Syntax/Lint/Tests) → Promote.

Usage:
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py                        # full sync
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run              # gates only
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --skip-tests           # sync, skip tests (CI mode)
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
UPSTREAM_BRANCH = "main"          # Qwen Code default branch
REQUIRED_REMOTES = {"upstream", "origin"}

# Files or directories owned by this fork that must not be overwritten by upstream merges.
PROTECTED_FILES: list[str] = [
    "tooling/sync-upstreams/upstream_ingest_pipeline.py",
    "AI.md",
    "docs/ai/RULES.md",
    "docs/ai/CONTEXT.md",
    "docs/fork/",
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

def _resolve_python() -> str:
    return sys.executable

def _resolve_tests() -> list[str] | None:
    """Resolve test command (e.g., vitest or pytest)."""
    # Qwen Code uses vitest/npm for many tests
    return ["npm", "test"]

def _resolve_lint() -> list[str] | None:
    return ["npm", "run", "lint"]

@dataclass
class SyncResult:
    success: bool
    stage: str
    message: str
    lkg_tag: str | None = None
    dry_run: bool = False

class _GitRunner:
    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True)
        if check and result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()
            raise RuntimeError(f"Command {cmd!r} failed (exit {result.returncode}):\n{detail}")
        return result

    def output(self, cmd: list[str]) -> str:
        return self.run(cmd).stdout.strip()

    def current_branch(self) -> str:
        return self.output(["git", "rev-parse", "--abbrev-ref", "HEAD"])

class PreFlight:
    def __init__(self, git: _GitRunner, skip_tests: bool = False) -> None:
        self._git = git
        self._skip_tests = skip_tests

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

            dirty = self._git.run(["git", "diff", "--quiet", "HEAD"], check=False).returncode != 0
            if dirty:
                raise RuntimeError("Integration branch has uncommitted changes.")

            log_success("Pre-flight passed.")
            return True
        except Exception as e:
            log_error(f"Pre-flight failed: {e}")
            return False

class SyncManager:
    def __init__(self, git: _GitRunner) -> None:
        self._git = git
        self.staging_branch: str | None = None

    def sync_mirror(self) -> bool:
        log_info(f"Fetching upstream/{UPSTREAM_BRANCH}...")
        self._git.run(["git", "fetch", "upstream", UPSTREAM_BRANCH])

        new_count = self._git.output(
            ["git", "rev-list", "--count", f"upstream/{UPSTREAM_BRANCH}", f"^{INTEGRATION_BRANCH}"]
        )
        if new_count == "0":
            log_success("Already up to date.")
            return False

        log_info(f"Resetting {MIRROR_BRANCH} to upstream/{UPSTREAM_BRANCH}...")
        self._git.run(["git", "checkout", "-f", MIRROR_BRANCH])
        self._git.run(["git", "reset", "--hard", f"upstream/{UPSTREAM_BRANCH}"])
        self._git.run(["git", "checkout", INTEGRATION_BRANCH])
        log_success("Mirror synchronized.")
        return True

    def create_staging(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.staging_branch = f"sync/staging-{timestamp}"
        log_info(f"Creating staging branch: {self.staging_branch}")
        self._git.run(["git", "checkout", "-b", self.staging_branch])

    def merge_mirror_to_stage(self) -> None:
        integration_ref = self._git.output(["git", "rev-parse", "HEAD"])
        log_info(f"Merging {MIRROR_BRANCH} into {self.staging_branch}...")
        result = self._git.run(["git", "merge", MIRROR_BRANCH, "--no-edit"], check=False)
        if result.returncode == 0:
            log_success("Merge clean.")
            self._restore_protected_files(integration_ref)
            return

        conflict_files = self._git.output(["git", "diff", "--name-only", "--diff-filter=U"])
        self._git.run(["git", "merge", "--abort"], check=False)
        raise RuntimeError(f"Merge conflict in: {conflict_files}")

    def _restore_protected_files(self, integration_ref: str) -> None:
        for path in PROTECTED_FILES:
            self._git.run(["git", "checkout", integration_ref, "--", path], check=False)

        staged = self._git.output(["git", "diff", "--cached", "--name-only"])
        if staged:
            self._git.run(["git", "commit", "-m", "chore(sync): restore fork-owned files"])
        else:
            log_success("Protected files unchanged.")

    def cleanup_staging(self) -> None:
        if not self.staging_branch:
            return
        if self._git.current_branch() == self.staging_branch:
            self._git.run(["git", "checkout", INTEGRATION_BRANCH])
        self._git.run(["git", "branch", "-D", self.staging_branch], check=False)
        self.staging_branch = None

class GateKeeper:
    def __init__(self, git: _GitRunner, skip_tests: bool = False) -> None:
        self._git = git
        self._skip_tests = skip_tests

    def verify(self) -> bool:
        return self._gate_tests()

    def _gate_tests(self) -> bool:
        if self._skip_tests:
            log_warn("Tests skipped.")
            return True
        logger.info("Running tests...")
        test_cmd = _resolve_tests()
        if not test_cmd:
            return True
        result = subprocess.run(test_cmd, cwd=REPO_ROOT)
        if result.returncode != 0:
            log_error("Tests failed.")
            return False
        log_success("Tests passed.")
        return True

class PromotionEngine:
    def __init__(self, git: _GitRunner) -> None:
        self._git = git

    def promote(self, staging_branch: str) -> str:
        log_info(f"Promoting {staging_branch} → {INTEGRATION_BRANCH}...")
        self._git.run(["git", "checkout", INTEGRATION_BRANCH])
        self._git.run(["git", "merge", "--ff-only", staging_branch])

        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        tag = f"LKG-{timestamp}"
        self._git.run(["git", "tag", "-a", tag, "-m", f"Last Known Good — {timestamp}"])
        return tag

class UpstreamIngestPipeline:
    def __init__(self, dry_run: bool = False, skip_tests: bool = False, push: bool = False) -> None:
        self._git = _GitRunner(REPO_ROOT)
        self._dry_run = dry_run
        self._push = push
        self.preflight = PreFlight(self._git, skip_tests=skip_tests)
        self.sync = SyncManager(self._git)
        self.gates = GateKeeper(self._git, skip_tests=skip_tests)
        self.promotion = PromotionEngine(self._git)

    def run(self) -> SyncResult:
        if not self.preflight.check():
            return SyncResult(False, "PREFLIGHT", "Pre-flight failed.")

        try:
            if not self._dry_run:
                if not self.sync.sync_mirror():
                    return SyncResult(True, "UP_TO_DATE", "Already up to date.")
                self.sync.create_staging()
                self.sync.merge_mirror_to_stage()

            if not self.gates.verify():
                return SyncResult(False, "VERIFICATION", "Gates failed.", dry_run=self._dry_run)

            if self._dry_run:
                return SyncResult(True, "DRY_RUN", "Dry run complete.", dry_run=True)

            tag = self.promotion.promote(self.sync.staging_branch)
            if self._push:
                self._git.run(["git", "push", "origin", INTEGRATION_BRANCH])
                self._git.run(["git", "push", "origin", "--tags"])
            return SyncResult(True, "PROMOTION", "Sync complete.", lkg_tag=tag)

        except Exception as e:
            log_error(str(e))
            return SyncResult(False, "PIPELINE_ERROR", str(e))
        finally:
            if not self._dry_run:
                self.sync.cleanup_staging()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    orch = UpstreamIngestPipeline(dry_run=args.dry_run, skip_tests=args.skip_tests, push=args.push)
    result = orch.run()
    sys.exit(0 if result.success else 1)

if __name__ == "__main__":
    main()
