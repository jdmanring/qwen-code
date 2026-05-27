#!/usr/bin/env python3
"""
LKG Rollback Utility

Rolls back the 'integration' branch to a Last Known Good (LKG) state.
LKG tags are created by the upstream_ingest_pipeline.py after a successful
sync and verification.

Usage:
  python3 tooling/sync-upstreams/rollback_to_lkg.py
  python3 tooling/sync-upstreams/rollback_to_lkg.py --tag LKG-20260523-0426
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
INTEGRATION_BRANCH = "integration"


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


class GitRunner:
    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, check=check)

    def output(self, cmd: list[str]) -> str:
        return self.run(cmd).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Roll back integration branch to an LKG tag.")
    parser.add_argument("--tag", help="Specific LKG tag to roll back to. Defaults to most recent.")
    args = parser.parse_args()

    git = GitRunner(REPO_ROOT)

    # 1. Determine target tag
    target_tag = args.tag
    if not target_tag:
        log_info("Searching for most recent LKG tag...")
        try:
            target_tag = git.output(["git", "tag", "-l", "LKG-*", "--sort=-version:refname"])
            if not target_tag:
                log_error("No LKG tags found in the repository.")
                sys.exit(1)
            target_tag = target_tag.splitlines()[0]
        except subprocess.CalledProcessError as e:
            log_error(f"Failed to list tags: {e}")
            sys.exit(1)

    log_info(f"Target LKG tag: {Colors.YELLOW}{target_tag}{Colors.NC}")

    # 2. Confirm with user
    print()
    log_warn(
        "CRITICAL: This operation is destructive. It will hard-reset 'integration' and force-push."
    )
    confirm = input(f"Are you sure you want to roll back to {target_tag}? [y/N] ").strip().lower()
    if confirm != "y":
        log_info("Rollback cancelled.")
        return

    try:
        # 3. Checkout integration
        log_info(f"Checking out {INTEGRATION_BRANCH}...")
        git.run(["git", "checkout", INTEGRATION_BRANCH])

        # 4. Hard reset to tag
        log_info(f"Resetting hard to {target_tag}...")
        git.run(["git", "reset", "--hard", target_tag])

        # 5. Force push with lease
        log_info(f"Pushing to origin {INTEGRATION_BRANCH} via --force-with-lease...")
        git.run(["git", "push", "--force-with-lease", "origin", INTEGRATION_BRANCH])

        log_success(f"Successfully rolled back {INTEGRATION_BRANCH} to {target_tag}.")

    except subprocess.CalledProcessError as e:
        log_error(f"Rollback failed: {e.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    main()
