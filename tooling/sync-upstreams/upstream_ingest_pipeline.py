#!/usr/bin/env python3
"""
Upstream Ingest Pipeline — qwen-code fork
Propagates changes from upstream through a verification gate, then rebases
all PR branches and updates develop.

Flow:
    upstream/main
        ↓  fetch + reset
    upstream-mirror
        ↓  merge into staging branch off integration
    sync/staging-TIMESTAMP
        ↓  Gate 1: npm install + build
        ↓  Gate 2: typecheck
        ↓  Gate 3: symmetry check
    integration  [ff-only merge + LKG tag]
        ↓  rebase PR branches onto new integration
        ↓  cherry-pick develop's unique commits onto new base
    develop

Usage:
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py                # full sync
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --dry-run      # gates only
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --skip-build    # skip npm install + build
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --push          # push integration + tags
    python3 tooling/sync-upstreams/upstream_ingest_pipeline.py --rebase-only   # skip sync, just rebase branches
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, stream=sys.stdout)
logger = logging.getLogger("upstream_ingest_pipeline")

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
INTEGRATION_BRANCH = "integration"
DEVELOP_BRANCH = "develop"
MIRROR_BRANCH = "upstream-mirror"
REQUIRED_REMOTES = {"upstream", "origin"}

# Branches that are part of the fork infrastructure — never rebase or touch.
PROTECTED_BRANCHES = {
    "main",
    "develop",
    "integration",
    "upstream-mirror",
    "fork/infra",
}

# Branch prefixes that identify PR branches (upstream-candidates).
# These get rebased onto integration after sync.
PR_BRANCH_PREFIXES = ("feat/", "fix/", "chore/", "refactor/", "perf/")

# Files owned by this fork that must not be overwritten by upstream merges.
# After each merge the pipeline restores these to their integration-branch state.
PROTECTED_FILES: list[str] = [
    "tooling/sync-upstreams/upstream_ingest_pipeline.py",
    "tooling/sync-upstreams/gate_failure_tests.py",
    "tooling/symmetry-check.py",
    "pyproject.toml",
    "pnpm-workspace.yaml",
    "scripts/dev.js",
    "scripts/start.js",
    "scripts/prepare-package.js",
    "scripts/sync-computer-use-schemas.ts",
    ".husky/pre-commit",
    ".qwen/skills/fork-main-reconciliation/SKILL.md",
    ".qwen/skills/fork-sync-contributions/SKILL.md",
    ".qwen/skills/fork-workbench-analysis/SKILL.md",
    ".qwen/skills/fork-workbench-audit/SKILL.md",
    ".qwen/skills/fork-workbench-pipeline/SKILL.md",
    ".qwen/skills/fork-workbench-template/SKILL.md",
]


class Colors:
    BLUE = "\033[0;34m"
    GREEN = "\003[0;32m"
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    NC = "\033[0m"


def log_info(msg: str) -> None:
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")


def log_success(msg: str) -> None:
    print(f"{Colors.GREEN}[OK]{Colors.NC} {msg}")


def log_warn(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {msg}", file=sys.stderr)


def log_error(msg: str) -> None:
    print(f"{Colors.RED}[FAIL]{Colors.NC} {msg}", file=sys.stderr)


@dataclass
class SyncResult:
    success: bool
    stage: str
    message: str
    lkg_tag: str | None = None
    dry_run: bool = False


@dataclass
class BranchStatus:
    name: str
    base_commit: str
    unique_commits: list[str]
    status: str = "pending"  # pending, rebased, conflict, skipped, error
    error: str | None = None


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
    def __init__(self, git: _GitRunner, skip_build: bool = False, rebase_only: bool = False) -> None:
        self._git = git
        self._skip_build = skip_build
        self._rebase_only = rebase_only

    def check(self) -> bool:
        logger.info("Running pre-flight checks...")
        try:
            branch = self._git.current_branch()
            if branch != INTEGRATION_BRANCH:
                raise RuntimeError(
                    f"Must be on '{INTEGRATION_BRANCH}' branch. Current: '{branch}'"
                )

            remotes = set(self._git.output(["git", "remote"]).splitlines())
            missing = REQUIRED_REMOTES - remotes
            if missing:
                raise RuntimeError(f"Missing required remotes: {missing}")

            if not self._skip_build and not self._rebase_only:
                if not shutil.which("npm"):
                    raise RuntimeError("npm not found. Install Node.js >= 22")
                if not (self._git.root / "node_modules").exists():
                    raise RuntimeError(
                        "node_modules not found. Run: npm install"
                    )

            dirty = self._git.run(
                ["git", "diff", "--quiet", "HEAD"], check=False
            ).returncode != 0
            if dirty:
                raise RuntimeError(
                    "Integration branch has uncommitted changes — stash or commit before syncing."
                )

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
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.staging_branch = f"sync/staging-{timestamp}"
        log_info(f"Creating staging branch: {self.staging_branch}")
        self._git.run(["git", "checkout", "-b", self.staging_branch])

    def merge_mirror_to_stage(self) -> None:
        integration_ref = self._git.output(["git", "rev-parse", "HEAD"])
        log_info(f"Merging {MIRROR_BRANCH} into {self.staging_branch}...")
        result = self._git.run(
            ["git", "merge", MIRROR_BRANCH, "--no-edit"], check=False
        )
        if result.returncode == 0:
            log_success("Merge clean.")
            self._restore_protected_files(integration_ref)
            return

        conflict_files = self._git.output(
            ["git", "diff", "--name-only", "--diff-filter=U"]
        )
        self._git.run(["git", "merge", "--abort"], check=False)
        raise RuntimeError(
            f"Merge conflict — manual resolution required:\n{conflict_files}\n\n"
            "Resolve, commit, then re-run the ingest pipeline."
        )

    def _restore_protected_files(self, integration_ref: str) -> None:
        for path in PROTECTED_FILES:
            self._git.run(
                ["git", "checkout", integration_ref, "--", path], check=False
            )
            if path.endswith("/"):
                upstream_added = self._git.output(
                    [
                        "git", "diff", "--name-only", "--diff-filter=A",
                        integration_ref, "--", path,
                    ]
                )
                for added in upstream_added.splitlines():
                    self._git.run(
                        ["git", "rm", "-f", "--cached", "--", added], check=False
                    )

        staged = self._git.output(["git", "diff", "--cached", "--name-only"])
        restored = [
            f for f in staged.splitlines() if f in PROTECTED_FILES
        ]
        if restored:
            log_info(f"Restored {len(restored)} fork-owned file(s).")
            self._git.run(
                ["git", "commit", "--no-verify", "-m", "chore(sync): restore fork-owned files after upstream merge"]
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
    def __init__(self, git: _GitRunner, skip_build: bool = False) -> None:
        self._git = git
        self._skip_build = skip_build

    def verify(self) -> bool:
        if self._skip_build:
            log_warn("Gates 1/3 and 2/3 skipped (--skip-build). Running symmetry check only.")
            return self._gate_symmetry()
        return self._gate_build() and self._gate_typecheck() and self._gate_symmetry()

    def _gate_build(self) -> bool:
        logger.info("Gate 1/3: cleaning build artifacts + build...")
        subprocess.run(
            ["find", ".", "-name", "*.tsbuildinfo", "-not", "-path", "./.git/*", "-delete"],
            cwd=self._git.root,
            capture_output=True,
        )
        for pkg in ["packages/core", "packages/cli", "packages/acp-bridge",
                    "packages/channels/base", "packages/channels/telegram",
                    "packages/channels/weixin", "packages/channels/dingtalk",
                    "packages/channels/feishu", "packages/channels/qqbot",
                    "packages/channels/plugin-example"]:
            subprocess.run(
                ["rm", "-rf", f"{pkg}/dist", f"{pkg}/tsconfig.tsbuildinfo"],
                cwd=self._git.root,
                capture_output=True,
            )
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=self._git.root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            log_error(f"Build gate failed:\n{result.stderr.strip()}")
            return False
        log_success("Build gate passed.")
        return True

    def _gate_typecheck(self) -> bool:
        logger.info("Gate 2/3: TypeScript typecheck...")
        result = subprocess.run(
            ["npm", "run", "typecheck"],
            cwd=self._git.root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            log_error(f"Typecheck gate failed:\n{result.stderr.strip()}")
            return False
        log_success("Typecheck gate passed.")
        return True

    def _gate_symmetry(self) -> bool:
        symmetry_script = self._git.root / "tooling" / "symmetry-check.py"
        if not symmetry_script.exists():
            log_success("Gate 3/3: Symmetry check skipped (script not present).")
            return True
        logger.info("Gate 3/3: Symmetry check (config ↔ docs)...")
        result = subprocess.run(
            ["python3", str(symmetry_script)],
            cwd=self._git.root,
        )
        if result.returncode != 0:
            log_error("Symmetry gate failed. .qwen/config/ and docs/ are out of sync.")
            return False
        log_success("Symmetry gate passed.")
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
        log_success(f"Tagged as {tag}.")
        return tag


class BranchRebaser:
    """
    Rebases PR branches onto the new integration HEAD and re-cherry-picks
    develop's unique commits so develop stays current.
    """

    def __init__(self, git: _GitRunner) -> None:
        self._git = git
        self.integration_head: str = ""
        self.develop_base: str = ""
        self.statuses: list[BranchStatus] = []

    def get_pr_branches(self) -> list[str]:
        """Return local branch names that match PR branch prefixes."""
        all_branches = self._git.output(["git", "branch", "--format=%(refname:short)"]).splitlines()
        pr_branches = []
        for b in all_branches:
            if b in PROTECTED_BRANCHES:
                continue
            if any(b.startswith(prefix) for prefix in PR_BRANCH_PREFIXES):
                pr_branches.append(b)
        return sorted(pr_branches)

    def get_unique_commits(self, branch: str, base: str) -> list[str]:
        """Get commits on branch that are not on base."""
        if not base:
            return []
        output = self._git.output(
            ["git", "log", "--oneline", f"{base}..{branch}", "--format=%H"]
        )
        return [c for c in output.splitlines() if c]

    def find_develop_base(self) -> str:
        """Find the merge-base between develop and upstream-mirror (the fork-only base)."""
        try:
            base = self._git.output(
                ["git", "merge-base", DEVELOP_BRANCH, MIRROR_BRANCH]
            )
            return base
        except RuntimeError:
            return ""

    def rebase_branch(self, branch: str) -> BranchStatus:
        """Rebase a single PR branch onto integration HEAD."""
        status = BranchStatus(
            name=branch,
            base_commit="",
            unique_commits=[],
        )

        try:
            base = self.find_develop_base()
            status.base_commit = base
            unique = self.get_unique_commits(branch, base)
            status.unique_commits = unique

            if not unique:
                status.status = "skipped"
                log_info(f"  {branch}: no unique commits — skipping.")
                return status

            log_info(f"  {branch}: rebasing {len(unique)} commit(s) onto integration...")

            self._git.run(["git", "checkout", branch])
            result = self._git.run(
                ["git", "rebase", "--onto", self.integration_head, base, branch],
                check=False,
            )

            if result.returncode != 0:
                self._git.run(["git", "rebase", "--abort"], check=False)
                status.status = "conflict"
                status.error = result.stderr.strip()
                log_error(f"  {branch}: rebase conflict — needs manual resolution.")
                return status

            status.status = "rebased"
            log_success(f"  {branch}: rebased cleanly.")
            return status

        except Exception as e:
            status.status = "error"
            status.error = str(e)
            log_error(f"  {branch}: error — {e}")
            return status

    def update_develop(self) -> bool:
        """
        Rebuild develop: reset to integration, then cherry-pick develop's
        unique commits on top.
        """
        log_info("Updating develop branch...")

        try:
            base = self.find_develop_base()
            if not base:
                log_error("Cannot find merge-base between develop and upstream-mirror.")
                return False

            unique_commits = self.get_unique_commits(DEVELOP_BRANCH, base)
            if not unique_commits:
                log_info("No unique commits on develop — resetting to integration.")
                self._git.run(["git", "checkout", DEVELOP_BRANCH])
                self._git.run(["git", "reset", "--hard", self.integration_head])
                log_success("Develop is now in sync with integration (no unique commits).")
                return True

            self._git.run(["git", "checkout", DEVELOP_BRANCH])
            self._git.run(["git", "reset", "--hard", self.integration_head])

            for commit_hash in reversed(unique_commits):
                result = self._git.run(
                    ["git", "cherry-pick", commit_hash],
                    check=False,
                )
                if result.returncode != 0:
                    self._git.run(["git", "cherry-pick", "--abort"], check=False)
                    log_error(
                        f"Cherry-pick conflict on {commit_hash[:8]}. "
                        "Manual resolution needed."
                    )
                    return False

            log_success(f"Develop updated: {len(unique_commits)} commit(s) cherry-picked.")
            return True

        except Exception as e:
            log_error(f"Failed to update develop: {e}")
            return False

    def rebase_all(self) -> bool:
        """Rebase all PR branches and update develop."""
        self.integration_head = self._git.output(
            ["git", "rev-parse", INTEGRATION_BRANCH]
        )

        branches = self.get_pr_branches()
        if not branches:
            log_info("No PR branches found — skipping rebase.")
            return True

        log_info(f"Rebasing {len(branches)} PR branch(es) onto integration...")

        for branch in branches:
            status = self.rebase_branch(branch)
            self.statuses.append(status)

        conflicts = [s for s in self.statuses if s.status == "conflict"]
        if conflicts:
            log_error(
                f"{len(conflicts)} branch(es) have rebase conflicts. "
                "Resolve manually, then re-run with --rebase-only."
            )
            return False

        return self.update_develop()

    def report(self) -> str:
        lines = ["\nBRANCH REBASE REPORT", "=" * 50]
        for s in self.statuses:
            status_icon = {
                "rebased": "✓",
                "skipped": "○",
                "conflict": "✗",
                "error": "!",
                "pending": "?",
            }.get(s.status, "?")
            lines.append(f"  {status_icon} {s.name:<40} {s.status}")
            if s.error:
                lines.append(f"      {s.error[:80]}")
        lines.append("=" * 50)
        return "\n".join(lines)


class UpstreamIngestPipeline:
    """
    Full upstream ingestion pipeline:

        upstream/main
            ↓  (fetch + reset)
        upstream-mirror
            ↓  (merge into staging branch off integration)
        sync/staging-TIMESTAMP
            ↓  (Gate 1: npm run build)
            ↓  (Gate 2: npm run typecheck)
            ↓  (Gate 3: symmetry check)
        integration  [ff-only merge + LKG tag]
            ↓  (rebase PR branches onto integration)
            ↓  (rebuild develop from integration + unique commits)
        develop
    """

    def __init__(
        self,
        dry_run: bool = False,
        skip_build: bool = False,
        push: bool = False,
        rebase_only: bool = False,
    ) -> None:
        self._git = _GitRunner(REPO_ROOT)
        self._dry_run = dry_run
        self._skip_build = skip_build
        self._push = push
        self._rebase_only = rebase_only
        self.preflight = PreFlight(
            self._git, skip_build=skip_build, rebase_only=rebase_only
        )
        self.sync = SyncManager(self._git)
        self.gates = GateKeeper(self._git, skip_build=skip_build)
        self.promotion = PromotionEngine(self._git)
        self.rebaser = BranchRebaser(self._git)

    def run(self) -> SyncResult:
        if self._dry_run:
            log_warn("DRY RUN — gates will run against current state; no commits or tags.")

        if not self.preflight.check():
            return SyncResult(False, "PREFLIGHT", "Pre-flight checks failed.")

        try:
            if self._rebase_only:
                log_info("Rebase-only mode — skipping upstream sync.")
                if not self.rebaser.rebase_all():
                    return SyncResult(False, "REBASE", "Branch rebase failed — see report above.")
                log_info(self.rebaser.report())
                return SyncResult(True, "REBASE_COMPLETE", "All branches rebased.")

            if not self._dry_run:
                has_new = self.sync.sync_mirror()
                if not has_new:
                    log_info("No new upstream commits. Checking if rebase is needed anyway.")
                    if not self.rebaser.rebase_all():
                        return SyncResult(False, "REBASE", "Branch rebase failed — see report above.")
                    log_info(self.rebaser.report())
                    return SyncResult(True, "REBASE_COMPLETE", "No new upstream, branches rebased.", dry_run=self._dry_run)
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

            if not self.rebaser.rebase_all():
                return SyncResult(False, "REBASE", "Branch rebase failed — see report above.")
            log_info(self.rebaser.report())

            if self._push:
                log_info("Pushing integration and tags to origin...")
                self._git.run(["git", "push", "origin", INTEGRATION_BRANCH])
                self._git.run(["git", "push", "origin", "--tags"])
                log_success("Pushed.")
            else:
                log_warn(
                    "Not pushing — run with --push or push manually: "
                    "git push origin integration --follow-tags"
                )

            return SyncResult(True, "PROMOTION", "Sync complete.", lkg_tag=tag)

        except Exception as e:
            log_error(str(e))
            return SyncResult(False, "PIPELINE_ERROR", str(e))
        finally:
            if not self._dry_run:
                self.sync.cleanup_staging()
                if self._git.current_branch() != INTEGRATION_BRANCH:
                    self._git.run(
                        ["git", "checkout", INTEGRATION_BRANCH], check=False
                    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upstream Ingest Pipeline — syncs upstream, rebases PR branches, updates develop."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run gates against current state without syncing or promoting.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip npm install + build and typecheck gates. Only run symmetry check.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push integration and tags to origin after promotion.",
    )
    parser.add_argument(
        "--rebase-only",
        action="store_true",
        help="Skip upstream sync. Just rebase PR branches onto current integration and update develop.",
    )
    args = parser.parse_args()

    orch = UpstreamIngestPipeline(
        dry_run=args.dry_run,
        skip_build=args.skip_build,
        push=args.push,
        rebase_only=args.rebase_only,
    )
    result = orch.run()

    if result.success:
        if result.lkg_tag:
            log_success(f"Pipeline complete. LKG tag: {result.lkg_tag}")
        elif result.stage == "REBASE_COMPLETE":
            log_success("Rebase complete.")
        elif result.stage == "UP_TO_DATE":
            log_success("Nothing to do — already up to date.")
        sys.exit(0)
    else:
        log_error(f"Pipeline failed at [{result.stage}]: {result.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
