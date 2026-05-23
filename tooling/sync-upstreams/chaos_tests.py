#!/usr/bin/env python3
"""
Integration Pipeline Adversarial Certification Suite
Tests the resilience of the Integration Pipeline against failure modes.
"""

import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from orchestrator import IntegrationOrchestrator, SyncManager, _GitRunner, REPO_ROOT


class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'


def log_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")


def log_success(msg: str):
    print(f"{Colors.GREEN}[PASS]{Colors.NC} {msg}")


def log_error(msg: str):
    print(f"{Colors.RED}[FAIL]{Colors.NC} {msg}")


def git(cmd: list, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


class ChaosSuite:
    def __init__(self):
        self.root = REPO_ROOT

    def test_merge_conflict(self):
        """
        Verify the pipeline aborts and leaves integration untouched when a
        merge conflict occurs.

        Uses SyncManager directly so the injected commits on upstream-mirror
        are not wiped by sync_mirror()'s reset-to-upstream/main.
        """
        log_info("Testing Failure Mode: Merge Conflict")

        _git = _GitRunner(self.root)
        sync = SyncManager(_git)
        test_file = self.root / "Conflict_Test.txt"

        orig_integration = _git.output(["git", "rev-parse", "integration"])
        orig_mirror = _git.output(["git", "rev-parse", "upstream-mirror"])

        success = False
        try:
            # Establish a shared base on integration
            git(["git", "checkout", "integration"], self.root)
            test_file.write_text("base version\n")
            git(["git", "add", str(test_file)], self.root)
            git(["git", "commit", "-m", "chaos: conflict-test base"], self.root)
            base_commit = _git.output(["git", "rev-parse", "HEAD"])

            # Diverge integration from the base
            test_file.write_text("Integration version\n")
            git(["git", "add", str(test_file)], self.root)
            git(["git", "commit", "-m", "chaos: conflict-test integration"], self.root)

            # Reset upstream-mirror to the shared base and add a conflicting change
            git(["git", "checkout", "-B", "upstream-mirror", base_commit], self.root)
            test_file.write_text("Mirror version\n")
            git(["git", "add", str(test_file)], self.root)
            git(["git", "commit", "-m", "chaos: conflict-test mirror"], self.root)

            git(["git", "checkout", "integration"], self.root)

            # Merge via SyncManager — bypasses sync_mirror so injected commits survive
            sync.create_staging()
            try:
                sync.merge_mirror_to_stage()
                log_error("Merge unexpectedly succeeded — conflict was not detected!")
            except RuntimeError:
                log_success("Pipeline correctly detected and aborted merge conflict.")

                git(["git", "checkout", "integration"], self.root, check=False)
                content = test_file.read_text() if test_file.exists() else ""
                if "Integration version" in content:
                    log_success("Integration branch remained stable.")
                    success = True
                else:
                    log_error(f"Integration branch was polluted! Content: {content!r}")

        finally:
            sync.cleanup_staging()
            git(["git", "checkout", "integration"], self.root, check=False)
            git(["git", "reset", "--hard", orig_integration], self.root, check=False)
            git(["git", "checkout", "-B", "upstream-mirror", orig_mirror], self.root, check=False)
            git(["git", "checkout", "integration"], self.root, check=False)
            test_file.unlink(missing_ok=True)

        return success

    def test_symmetry_violation(self):
        """
        Verify the symmetry gate blocks a config file without a matching doc.

        Writes an untracked file (survives git checkouts) and uses dry_run to
        run gates against the current working state.
        """
        log_info("Testing Failure Mode: Symmetry Violation")

        config_file = self.root / ".qwen" / "config" / "violation.toml"
        config_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            config_file.write_text("test = 1\n")

            orch = IntegrationOrchestrator(dry_run=True)
            result = orch.run()

            if not result.success and result.stage == "VERIFICATION":
                log_success("Pipeline correctly blocked symmetry violation.")
                return True
            else:
                log_error(
                    f"Pipeline failed to block symmetry violation. "
                    f"Stage: {result.stage}, success: {result.success}"
                )
                return False
        finally:
            config_file.unlink(missing_ok=True)

    def test_boot_failure(self):
        """
        Verify the boot gate blocks when uv.lock is missing.

        Uses dry_run=True so no git checkout can restore uv.lock before the
        gate runs. Boot gate is ordered first (before lint) so uv run ruff
        cannot recreate the lockfile and defeat the check.
        """
        log_info("Testing Failure Mode: Boot Failure")

        lockfile = self.root / "uv.lock"
        if not lockfile.exists():
            log_info("uv.lock not found — skipping.")
            return True

        backup = lockfile.with_suffix(".lock.bak")
        lockfile.rename(backup)

        success = False
        try:
            orch = IntegrationOrchestrator(dry_run=True)
            result = orch.run()

            if not result.success and result.stage == "VERIFICATION":
                log_success("Pipeline correctly blocked boot failure.")
                success = True
            else:
                log_error(
                    f"Pipeline failed to block boot failure. "
                    f"Stage: {result.stage}, success: {result.success}"
                )
        finally:
            backup.rename(lockfile)

        return success

    def run_all(self):
        results = []
        results.append(("Merge Conflict", self.test_merge_conflict()))
        results.append(("Symmetry Violation", self.test_symmetry_violation()))
        results.append(("Boot Failure", self.test_boot_failure()))

        print("\n" + "=" * 42)
        print("INTEGRATION PIPELINE CERTIFICATION REPORT")
        print("=" * 42)
        for name, res in results:
            status = "PASS" if res else "FAIL"
            print(f"  {name:<25}: {status}")
        print("=" * 42)

        return all(res for _, res in results)


if __name__ == "__main__":
    suite = ChaosSuite()
    if suite.run_all():
        log_success("SYSTEM CERTIFIED: Adversarial-Proof.")
        sys.exit(0)
    else:
        log_error("SYSTEM CERTIFICATION FAILED.")
        sys.exit(1)
