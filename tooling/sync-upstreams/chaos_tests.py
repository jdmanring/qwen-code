#!/usr/bin/env python3
"""
Integration Pipeline Adversarial Certification Suite
Tests the resilience of the Integration Pipeline against failure modes.
"""

import subprocess
import sys
from pathlib import Path
from typing import List

# Fix for hyphenated directory name in import
sys.path.append(str(Path(__file__).parent))
from orchestrator import IntegrationOrchestrator

class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def log_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def log_success(msg: str):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

def log_error(msg: str):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def run_cmd(cmd: List[str], cwd: Path):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

class ChaosSuite:
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent.resolve()
        self.orch = IntegrationOrchestrator()

    def test_merge_conflict(self):
        log_info("Testing Failure Mode: Merge Conflict")
        
        # 1. Setup conflict: Modify a file in both mirror and integration
        test_file = self.root / "Conflict_Test.txt"
        
        # On integration
        run_cmd(["git", "checkout", "integration"], self.root)
        test_file.write_text("Integration version\n")
        run_cmd(["git", "add", str(test_file)], self.root)
        run_cmd(["git", "commit", "-m", "conflict: base"], self.root)
        
        # On mirror
        run_cmd(["git", "checkout", "upstream-mirror"], self.root)
        test_file.write_text("Mirror version\n")
        run_cmd(["git", "add", str(test_file)], self.root)
        run_cmd(["git", "commit", "-m", "conflict: mirror"], self.root)
        
        # Return to integration
        run_cmd(["git", "checkout", "integration"], self.root)
        
        # 2. Execute Sync
        result = self.orch.run()
        
        # 3. Verify: Pipeline should fail, and integration should NOT have the mirror's change
        if not result.success and "ORCHESTRATION" in result.stage:
            log_success("Pipeline correctly failed on merge conflict.")
            
            # Verify integration is still at the original state
            content = test_file.read_text()
            if "Integration version" in content:
                log_success("Integration branch remained stable.")
            else:
                log_error("Integration branch was polluted!")
                return False
        else:
            log_error(f"Pipeline unexpectedly { 'succeeded' if result.success else 'failed' }")
            return False
        
        # Cleanup
        run_cmd(["git", "checkout", "integration"], self.root)
        run_cmd(["git", "rm", str(test_file)], self.root)
        run_cmd(["git", "commit", "-m", "chore: cleanup conflict test"], self.root)
        return True

    def test_symmetry_violation(self):
        log_info("Testing Failure Mode: Symmetry Violation")
        
        # 1. Setup violation: Add config without doc
        config_file = self.root / ".qwen" / "config" / "violation.toml"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("test = 1")
        
        # Put it in the mirror
        run_cmd(["git", "checkout", "upstream-mirror"], self.root)
        config_file.write_text("test = 1")
        run_cmd(["git", "add", str(config_file)], self.root)
        run_cmd(["git", "commit", "-m", "violation: mirror config"], self.root)
        
        run_cmd(["git", "checkout", "integration"], self.root)
        
        # 2. Execute Sync
        result = self.orch.run()
        
        # 3. Verify: Gate should block promotion
        if not result.success and result.stage == "VERIFICATION":
            log_success("Pipeline correctly blocked symmetry violation.")
        else:
            log_error(f"Pipeline failed to block symmetry violation. Result: {result.stage}")
            return False
            
        # Cleanup: remove from upstream-mirror (committed) and working directory
        run_cmd(["git", "checkout", "upstream-mirror"], self.root)
        run_cmd(["git", "rm", "-f", str(config_file)], self.root)
        run_cmd(["git", "commit", "-m", "chore: cleanup symmetry test"], self.root)
        run_cmd(["git", "checkout", "integration"], self.root)
        config_file.unlink(missing_ok=True)
        return True

    def test_boot_failure(self):
        log_info("Testing Failure Mode: Boot Failure")

        lockfile = self.root / "uv.lock"
        if not lockfile.exists():
            log_info("uv.lock not found — skipping boot failure test.")
            return True

        # 1. Setup failure: rename uv.lock so `uv lock --check` fails.
        #    This simulates upstream adding a dependency without regenerating
        #    the lockfile — a real scenario the gate is designed to catch.
        backup = lockfile.with_suffix(".lock.bak")
        lockfile.rename(backup)

        # Ensure mirror is ahead so the orchestrator has something to sync
        run_cmd(["git", "checkout", "upstream-mirror"], self.root)
        run_cmd(["git", "commit", "--allow-empty", "-m", "trigger: boot failure test"], self.root)
        run_cmd(["git", "checkout", "integration"], self.root)

        # 2. Execute sync
        result = self.orch.run()

        # 3. Verify: boot gate must block promotion
        if not result.success and result.stage == "VERIFICATION":
            log_success("Pipeline correctly blocked boot failure.")
            success = True
        else:
            log_error(
                f"Pipeline failed to block boot failure. "
                f"Stage: {result.stage}, success: {result.success}"
            )
            success = False

        # Always restore — leave repo in working state regardless of outcome
        backup.rename(lockfile)
        return success

    def run_all(self):
        results = []
        results.append(("Merge Conflict", self.test_merge_conflict()))
        results.append(("Symmetry Violation", self.test_symmetry_violation()))
        results.append(("Boot Failure", self.test_boot_failure()))
        
        print("\n" + "="*30)
        print("INTEGRATION PIPELINE CERTIFICATION REPORT")
        print("="*30)
        for name, res in results:
            status = "PASS" if res else "FAIL"
            print(f"{name: <25} : {status}")
        print("="*30)
        
        return all(res for name, res in results)

if __name__ == "__main__":
    suite = ChaosSuite()
    if suite.run_all():
        log_success("SYSTEM CERTIFIED: Adversarial-Proof.")
        sys.exit(0)
    else:
        log_error("SYSTEM CERTIFICATION FAILED.")
        sys.exit(1)
