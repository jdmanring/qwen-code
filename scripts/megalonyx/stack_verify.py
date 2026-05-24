#!/usr/bin/env python3
"""
stack_verify: runs symmetry check and project standards linter to verify repo health.
"""

import pathlib
import subprocess
import sys


def run_tool(command: str, name: str) -> bool:
    print(f"Running {name}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{name} failed:\n{result.stdout}\n{result.stderr}")
        return False
    print(f"{name} passed.")
    return True


def main() -> None:
    _root = pathlib.Path(".").resolve()

    symmetry_passed = run_tool("python3 scripts/symmetry_check.py", "Symmetry Check")

    standards_passed = run_tool(
        "python3 scripts/project_standards_linter.py --strict .",
        "Project Standards Linter",
    )

    if not symmetry_passed or not standards_passed:
        print("\nRepo health check: FAILED")
        sys.exit(1)

    print("\nRepo health check: PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
