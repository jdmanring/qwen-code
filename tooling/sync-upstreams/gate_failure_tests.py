#!/usr/bin/env python3
"""
Gate Failure Tests

Verifies that each pipeline gate correctly blocks failures.
Run after any changes to the pipeline itself.

Usage:
    python3 tooling/sync-upstreams/gate_failure_tests.py

Note: These tests verify the pipeline code contains the correct patterns.
They do NOT run actual gates against broken code — they test the pipeline
structure is correctly wired.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()


class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.message = ""

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"  {status}  {self.name}" + (f" — {self.message}" if self.message else "")


def test_merge_conflict_detection() -> TestResult:
    result = TestResult("Merge Conflict Detection")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ('"merge", "--abort"', "Pipeline should abort merge on conflict"),
        ("--diff-filter=U", "Pipeline should detect conflicted files"),
        ("RuntimeError", "Pipeline should raise on unresolvable conflicts"),
        ("Merge conflict", "Pipeline should report merge conflicts"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def test_protected_files_restored() -> TestResult:
    result = TestResult("Protected Files Restoration")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ("PROTECTED_FILES", "Pipeline should define protected files list"),
        ("_restore_protected_files", "Pipeline should have restore function"),
        ("checkout", "Pipeline should checkout protected files"),
        ("integration_ref", "Pipeline should use integration ref for restoration"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def test_staging_isolation() -> TestResult:
    result = TestResult("Staging Branch Isolation")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ("sync/staging-", "Pipeline should create staging branches"),
        ("ff-only", "Pipeline should ff-only merge into integration"),
        ("cleanup_staging", "Pipeline should clean up staging branches"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def test_lkg_tagging() -> TestResult:
    result = TestResult("LKG Tag Creation")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ("LKG-", "Pipeline should create LKG tags"),
        ('"tag", "-a"', "Pipeline should create annotated tags"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def test_preflight_checks() -> TestResult:
    result = TestResult("Pre-flight Checks")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ("PreFlight", "Pipeline should have pre-flight checks"),
        ("integration", "Pipeline should verify integration branch"),
        ("REQUIRED_REMOTES", "Pipeline should verify required remotes"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def test_three_gates() -> TestResult:
    result = TestResult("Three-Gate Pipeline")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ("_gate_build", "Pipeline should have build gate"),
        ("_gate_lint", "Pipeline should have lint gate"),
        ("_gate_tests", "Pipeline should have test gate"),
        ("Gate 1/3", "Pipeline should label build gate"),
        ("Gate 2/3", "Pipeline should label lint gate"),
        ("Gate 3/3", "Pipeline should label test gate"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def test_gate_commands() -> TestResult:
    result = TestResult("Gate Commands (Node.js)")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ("pnpm install", "Build gate should use pnpm"),
        ("eslint", "Lint gate should use eslint"),
        ("vitest", "Test gate should use vitest"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def test_finally_cleanup() -> TestResult:
    result = TestResult("Finally Block Cleanup")
    pipeline_file = REPO_ROOT / "tooling" / "sync-upstreams" / "upstream_ingest_pipeline.py"
    content = pipeline_file.read_text()

    checks = [
        ("finally:", "Pipeline should have finally block"),
        ("cleanup_staging", "Finally block should call cleanup"),
    ]

    missing = [desc for pattern, desc in checks if pattern not in content]
    if missing:
        result.message = f"Missing: {', '.join(missing)}"
    else:
        result.passed = True

    return result


def main() -> None:
    print("=" * 56)
    print("  PIPELINE GATE FAILURE TEST REPORT")
    print("=" * 56)
    print()

    results = []

    print("Structural Tests:")
    results.append(test_merge_conflict_detection())
    results.append(test_protected_files_restored())
    results.append(test_staging_isolation())
    results.append(test_lkg_tagging())
    results.append(test_preflight_checks())
    results.append(test_three_gates())
    results.append(test_gate_commands())
    results.append(test_finally_cleanup())

    for r in results:
        print(r)

    print()

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"Results: {passed}/{total} passed")

    if passed == total:
        print("[PASS] All gate failure tests passed.")
        sys.exit(0)
    else:
        print("[FAIL] Some tests failed. Review the pipeline code.")
        sys.exit(1)


if __name__ == "__main__":
    main()
