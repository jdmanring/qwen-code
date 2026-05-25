#!/usr/bin/env python3
"""
Boot verification smoke test.

Verifies that all three workspace packages import, instantiate, and
produce correct output without requiring external services for the
import/instantiation steps. The memory round-trip step requires a
running Qdrant instance and is skipped automatically when unavailable.

Exit codes:
  0 — all required steps passed
  1 — at least one required step failed

Usage:
  uv run python3 tooling/smoke-tests/boot_verification.py
  uv run python3 tooling/smoke-tests/boot_verification.py --skip-memory
"""

import argparse
import sys
import time
from collections.abc import Callable
from pathlib import Path

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
SKIP = "\033[33mSKIP\033[0m"

failures: list[str] = []


def check(label: str, fn: Callable[[], None], required: bool = True) -> bool:
    try:
        fn()
        print(f"  {PASS}  {label}")
        return True
    except Exception as e:  # noqa: CODE-03 — test harness must catch any failure
        status = FAIL if required else SKIP
        print(f"  {status}  {label}")
        print(f"        {type(e).__name__}: {e}")
        if required:
            failures.append(label)
        return False


# ---------------------------------------------------------------------------
# Step 1: package imports
# ---------------------------------------------------------------------------

print("\n── Step 1: package imports ─────────────────────────────────────────")


def _import_agent_infra() -> None:
    import agent_infra  # noqa: F401
    from agent_infra.system_logger import SystemLogger  # noqa: F401


def _import_agent_memory() -> None:
    import agent_memory  # noqa: F401
    from agent_memory.memory_daemon import MemoryDaemon  # noqa: F401
    from agent_memory.memory_search import ensure_collections_exist  # noqa: F401


def _import_control_plane_daemon() -> None:
    import control_plane_daemon  # noqa: F401
    from control_plane_daemon.control_plane import ControlPlane  # noqa: F401
    from control_plane_daemon.execution_profile_selector import (
        ExecutionProfileSelector,  # noqa: F401
    )


check("agent_infra imports", _import_agent_infra)
check("agent_memory imports", _import_agent_memory)
check("control_plane_daemon imports", _import_control_plane_daemon)

# ---------------------------------------------------------------------------
# Step 2: ControlPlane instantiation
# ---------------------------------------------------------------------------

print("\n── Step 2: ControlPlane instantiation ──────────────────────────────")

cp = None


def _instantiate_control_plane() -> None:
    global cp
    from control_plane_daemon.control_plane import ControlPlane

    cp = ControlPlane()


def _check_cp_classifier() -> None:
    assert cp is not None
    from control_plane_daemon.intent_classifier import IntentClassifier

    assert isinstance(cp.classifier, IntentClassifier)


def _check_cp_decomposer() -> None:
    assert cp is not None
    from control_plane_daemon.task_decomposer import TaskDecomposer

    assert isinstance(cp.decomposer, TaskDecomposer)


def _check_cp_jsm() -> None:
    assert cp is not None
    from control_plane_daemon.job_state_manager import JobStateManager

    assert isinstance(cp.jsm, JobStateManager)


def _check_cp_command_manager() -> None:
    assert cp is not None
    from control_plane_daemon.command_manager import CommandManager

    assert isinstance(cp.command_manager, CommandManager)


def _check_cp_profile_selector() -> None:
    assert cp is not None
    from control_plane_daemon.execution_profile_selector import ExecutionProfileSelector

    assert isinstance(cp.execution_profile_selector, ExecutionProfileSelector)
    assert len(cp.execution_profile_selector.profiles) > 0, "no execution profiles loaded"


_settings_path = Path.home() / ".qwen" / "settings.json"

if not _settings_path.exists():
    print(f"  {SKIP}  ControlPlane() instantiates (no settings.json at {_settings_path})")
    print(f"  {SKIP}    └─ IntentClassifier")
    print(f"  {SKIP}    └─ TaskDecomposer")
    print(f"  {SKIP}    └─ JobStateManager")
    print(f"  {SKIP}    └─ CommandManager")
    print(f"  {SKIP}    └─ ExecutionProfileSelector (profiles loaded)")
else:
    check("ControlPlane() instantiates", _instantiate_control_plane)
    check("  └─ IntentClassifier", _check_cp_classifier)
    check("  └─ TaskDecomposer", _check_cp_decomposer)
    check("  └─ JobStateManager", _check_cp_jsm)
    check("  └─ CommandManager", _check_cp_command_manager)
    check("  └─ ExecutionProfileSelector (profiles loaded)", _check_cp_profile_selector)

# ---------------------------------------------------------------------------
# Step 3: ExecutionProfileSelector standalone
# ---------------------------------------------------------------------------

print("\n── Step 3: ExecutionProfileSelector ───────────────────────────────")


def _profiles_loaded() -> None:
    from control_plane_daemon.execution_profile_selector import ExecutionProfileSelector

    sel = ExecutionProfileSelector()
    assert len(sel.profiles) >= 10, f"expected ≥10 profiles, got {len(sel.profiles)}"


def _profile_selection_feature_synthesis() -> None:
    from control_plane_daemon.execution_profile_selector import ExecutionProfileSelector

    sel = ExecutionProfileSelector()
    active = sel.get_active_profiles(
        prompt_text="implement the new login feature",
        intent="Feature Synthesis",
    )
    assert active, "no profiles returned"
    assert active[0]["name"] == "developer", f"expected 'developer', got '{active[0]['name']}'"


def _profile_selection_adversarial_review() -> None:
    from control_plane_daemon.execution_profile_selector import ExecutionProfileSelector

    sel = ExecutionProfileSelector()
    active = sel.get_active_profiles(
        prompt_text="review for security vulnerabilities",
        intent="Adversarial Review",
    )
    assert active, "no profiles returned"
    assert active[0]["name"] in ("code-reviewer", "security-auditor", "reviewer"), (
        f"unexpected top profile: '{active[0]['name']}'"
    )


check("profiles loaded (≥10)", _profiles_loaded)
check("Feature Synthesis → developer", _profile_selection_feature_synthesis)
check("Adversarial Review → reviewer/auditor", _profile_selection_adversarial_review)

# ---------------------------------------------------------------------------
# Step 4: MemoryDaemon + Qdrant round-trip (skipped if Qdrant unreachable)
# ---------------------------------------------------------------------------

print("\n── Step 4: MemoryDaemon + Qdrant round-trip ────────────────────────")

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--skip-memory", action="store_true")
args, _ = parser.parse_known_args()

daemon = None
qdrant_available = False


def _qdrant_reachable() -> None:
    global qdrant_available
    from agent_memory.memory_search import ensure_collections_exist

    ensure_collections_exist()
    qdrant_available = True


def _memory_daemon_start() -> None:
    global daemon
    from agent_memory.memory_daemon import MemoryDaemon

    daemon = MemoryDaemon()
    daemon.start()


def _memory_ingest_recall() -> None:
    assert daemon is not None
    result = daemon.ingest("smoke test: boot verification ingest round-trip", tier="local")
    assert result.get("status") == "queued", f"unexpected ingest status: {result}"
    time.sleep(5)
    hits = daemon.recall("boot verification ingest", tier="local")
    assert len(hits) > 0, "recall returned no results after ingest"
    assert hits[0].get("score", 0) > 0.4, f"top hit score too low: {hits[0].get('score')}"


if args.skip_memory:
    print(f"  {SKIP}  Qdrant reachable (--skip-memory flag set)")
    print(f"  {SKIP}  MemoryDaemon.start()")
    print(f"  {SKIP}  ingest → recall round-trip")
else:
    qdrant_ok = check("Qdrant reachable", _qdrant_reachable, required=False)
    if qdrant_ok:
        check("MemoryDaemon.start()", _memory_daemon_start)
        check("ingest → recall round-trip (score > 0.4)", _memory_ingest_recall)
    else:
        print(f"  {SKIP}  MemoryDaemon.start() (Qdrant unavailable)")
        print(f"  {SKIP}  ingest → recall round-trip (Qdrant unavailable)")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n────────────────────────────────────────────────────────────────────")
if failures:
    print(f"  FAILED — {len(failures)} required step(s) did not pass:")
    for f in failures:
        print(f"    • {f}")
    sys.exit(1)
else:
    print("  All required steps passed.")
    sys.exit(0)
