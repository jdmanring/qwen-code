#!/usr/bin/env python3
"""
Fork Sync Pipeline Tests

Verifies that advisory and isolation gate functions correctly flag violations.
Run: python3 tooling/sync-upstreams/fork_sync_pipeline_tests.py
"""

import sys

from fork_sync_pipeline import (
    PROTECTED_FILES,
    gate_ci_files,
    gate_manifests,
    gate_new_files,
    gate_protected_files,
    run_isolation_gates,
)

PASS = "\033[0;32m[PASS]\033[0m"
FAIL = "\033[0;31m[FAIL]\033[0m"


def run_test(name, fn):
    try:
        fn()
        print(f"{PASS} {name}")
        return True
    except AssertionError as e:
        print(f"{FAIL} {name}: {e}")
        return False


# ── Advisory gate tests ───────────────────────────────────────────────────────


def test_ci_gate_flags_workflow_change():
    """GATE-CIFILES flags changes to .github/workflows/ files."""
    changed = [".github/workflows/ci.yml", "packages/cli/src/index.ts"]
    result = gate_ci_files(changed)
    assert not result.passed, "Should flag CI workflow changes"
    assert ".github/workflows/ci.yml" in result.lines


def test_ci_gate_passes_non_ci_files():
    """GATE-CIFILES passes when no CI workflow files are changed."""
    changed = ["packages/core/src/utils.ts", "README.md"]
    result = gate_ci_files(changed)
    assert result.passed, "Should not flag non-CI files"
    assert result.lines == []


def test_protected_gate_flags_pyproject():
    """GATE-PROTECTED flags changes to any file in PROTECTED_FILES."""
    changed = ["packages/sdk-python/pyproject.toml", "packages/cli/src/index.ts"]
    result = gate_protected_files(changed)
    assert not result.passed, "Should flag protected file changes"
    assert "packages/sdk-python/pyproject.toml" in result.lines


def test_manifests_gate_flags_package_json():
    """GATE-MANIFESTS flags changes to package.json files."""
    changed = ["packages/core/package.json", "packages/cli/src/runner.ts"]
    result = gate_manifests(changed)
    assert not result.passed, "Should flag package.json changes"
    assert "packages/core/package.json" in result.lines


def test_new_files_gate_flags_additions():
    """GATE-NEWFILES flags a list of newly added files."""
    added = ["packages/core/src/newFeature.ts", "docs/new-guide.md"]
    result = gate_new_files(added)
    assert not result.passed, "Should flag newly added files"
    assert len(result.lines) == 2


def test_new_files_gate_passes_empty_list():
    """GATE-NEWFILES passes when no files were added."""
    result = gate_new_files([])
    assert result.passed, "Should pass with no new files"


# ── Isolation gate tests ──────────────────────────────────────────────────────


def test_isolation_blocks_megalonyx_reference():
    """GATE-MEGALONYX hard-blocks a diff that contains 'megalonyx'."""
    diff = (
        "diff --git a/packages/cli/src/config.ts b/packages/cli/src/config.ts\n"
        "+++ b/packages/cli/src/config.ts\n"
        "+// Load megalonyx config from path\n"
    )
    results = run_isolation_gates(diff, [])
    gate = next(g for g in results if g.name == "GATE-MEGALONYX")
    assert not gate.passed, "GATE-MEGALONYX should fail on 'megalonyx' in diff"
    assert len(gate.lines) >= 1


def test_isolation_blocks_pnpm_workspace_reference():
    """GATE-PNPM hard-blocks a diff containing 'pnpm-workspace'."""
    diff = (
        "diff --git a/package.json b/package.json\n"
        "+++ b/package.json\n"
        '+  "config": "pnpm-workspace.yaml"\n'
    )
    results = run_isolation_gates(diff, [])
    gate = next(g for g in results if g.name == "GATE-PNPM")
    assert not gate.passed, "GATE-PNPM should fail on 'pnpm-workspace' in diff"


def test_isolation_blocks_protected_file_in_changed_list():
    """GATE-CIFILES (outbound) hard-blocks when a PROTECTED_FILE is in changed_files."""
    diff = ""
    changed = [PROTECTED_FILES[0], "packages/core/src/utils.ts"]
    results = run_isolation_gates(diff, changed)
    gate = next(g for g in results if g.name == "GATE-CIFILES")
    assert not gate.passed, "GATE-CIFILES should fail when a PROTECTED_FILE is touched"
    assert PROTECTED_FILES[0] in gate.lines


def test_isolation_passes_clean_diff():
    """All isolation gates pass for a diff with no Megalonyx references."""
    diff = (
        "diff --git a/packages/cli/src/runner.ts b/packages/cli/src/runner.ts\n"
        "+++ b/packages/cli/src/runner.ts\n"
        "+function run(cmd: string): void {\n"
        "+  exec(cmd);\n"
        "+}\n"
    )
    results = run_isolation_gates(diff, [])
    failures = [g for g in results if not g.passed]
    assert not failures, f"Expected all gates to pass, got failures: {[g.name for g in failures]}"


TESTS = [
    ("advisory: CI gate flags .github/workflows/ change", test_ci_gate_flags_workflow_change),
    ("advisory: CI gate passes non-CI files", test_ci_gate_passes_non_ci_files),
    ("advisory: protected files gate flags pyproject.toml", test_protected_gate_flags_pyproject),
    ("advisory: manifests gate flags package.json", test_manifests_gate_flags_package_json),
    ("advisory: new files gate flags additions", test_new_files_gate_flags_additions),
    ("advisory: new files gate passes empty list", test_new_files_gate_passes_empty_list),
    ("isolation: GATE-MEGALONYX blocks megalonyx ref", test_isolation_blocks_megalonyx_reference),
    (
        "isolation: GATE-PNPM blocks pnpm-workspace ref",
        test_isolation_blocks_pnpm_workspace_reference,
    ),
    (
        "isolation: GATE-CIFILES blocks protected file",
        test_isolation_blocks_protected_file_in_changed_list,
    ),
    ("isolation: all gates pass for clean diff", test_isolation_passes_clean_diff),
]


def main():
    print()
    print("Fork Sync Pipeline — Gate Tests")
    print("─" * 55)
    results = [run_test(name, fn) for name, fn in TESTS]
    print("─" * 55)
    passed = sum(results)
    total = len(results)
    if passed == total:
        print(f"\033[0;32mAll {total} tests passed.\033[0m\n")
        sys.exit(0)
    else:
        print(f"\033[0;31m{total - passed} of {total} tests FAILED.\033[0m\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
