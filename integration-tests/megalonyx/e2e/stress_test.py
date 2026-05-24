#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# ======================================
# CONFIGURATION
# ======================================
STACK_ROOT = Path.home() / ".local/share/megalonyx"
TMP_DIR = STACK_ROOT / "tmp"
# Derive manager path relative to this test file
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANAGER_PATH = PROJECT_ROOT / "scripts" / "mega-memory-manager.py"
MANAGER = [sys.executable, str(MANAGER_PATH)]


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess:
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def main() -> None:
    print("Starting Infrastructure Stability Stress Test...")

    # Ensure stack is stopped before starting cycles
    print("Initializing: Stopping stack...")
    run_cmd(MANAGER + ["stop"])

    for i in range(1, 11):
        print(f"\n--- Cycle {i}/10 ---")

        # 1. Restart the stack
        print("Action: Restarting stack...")
        res = run_cmd(MANAGER + ["restart"])
        if res.returncode != 0:
            print(f"CRITICAL: Restart failed in cycle {i}!")
            print(f"STDOUT: {res.stdout}")
            print(f"STDERR: {res.stderr}")
            sys.exit(1)

        # 2. Verify health
        print("Action: Verifying health...")
        status_res = run_cmd(MANAGER + ["status"])
        if status_res.returncode != 0:
            print(f"CRITICAL: Health check failed in cycle {i}!")
            print(f"STDOUT: {status_res.stdout}")
            print(f"STDERR: {status_res.stderr}")
            sys.exit(1)

        print(f"Cycle {i}/10: PASSED")

    # 3. Stop the stack
    print("\n--- Finalization ---")
    print("Action: Stopping stack...")
    run_cmd(MANAGER + ["stop"])

    # 4. Verify no stale files
    print("Action: Verifying no stale files in tmp...")
    if not TMP_DIR.exists():
        print("TMP_DIR does not exist, which is fine.")
    else:
        stale_files = list(TMP_DIR.glob("*.pid")) + list(TMP_DIR.glob("*.sock"))
        if stale_files:
            print(f"CRITICAL: Stress test failed! Stale files found: {stale_files}")
            sys.exit(1)

    print("\n========================================")
    print("Infrastructure Stability Stress Test: PASSED")
    print("========================================")


if __name__ == "__main__":
    main()
