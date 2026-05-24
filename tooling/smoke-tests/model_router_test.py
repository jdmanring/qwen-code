#!/usr/bin/env python3
"""
Model router integration test.

Tests the full profile selection pipeline without making a live LLM call.
Directly passes each of the 6 classified intent types into ExecutionProfileSelector
and asserts the top-ranked profile is the canonical one for that intent.

This verifies the scoring logic in execution_profile_selector.py routes correctly
for all intents when the LLM classifier produces its expected output.

Exit codes:
  0 — all assertions passed
  1 — at least one assertion failed

Usage:
  uv run python3 tooling/smoke-tests/model_router_test.py
"""

import sys
from collections.abc import Callable

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"

failures: list[str] = []


def check(label: str, fn: Callable[[], None]) -> bool:
    try:
        fn()
        print(f"  {PASS}  {label}")
        return True
    except AssertionError as e:
        print(f"  {FAIL}  {label}")
        print(f"        AssertionError: {e}")
        failures.append(label)
        return False
    except Exception as e:  # noqa: CODE-03 — test harness must catch any failure
        print(f"  {FAIL}  {label}")
        print(f"        {type(e).__name__}: {e}")
        failures.append(label)
        return False


# ---------------------------------------------------------------------------
# Step 1: Import
# ---------------------------------------------------------------------------

print("\n── Step 1: import ──────────────────────────────────────────────────")


def _import() -> None:
    from control_plane_daemon.execution_profile_selector import (
        ExecutionProfileSelector,  # noqa: F401
    )


check("ExecutionProfileSelector imports", _import)


# ---------------------------------------------------------------------------
# Step 2: Intent → profile routing (no LLM call)
# ---------------------------------------------------------------------------

print("\n── Step 2: intent → profile routing ───────────────────────────────")

# Each tuple: (intent, prompt, expected_top_profile_or_set)
# expected is either a str (exact match) or a set[str] (any of these is acceptable)
ROUTING_CASES: list[tuple[str, str, str | set[str]]] = [
    (
        "Feature Synthesis",
        "implement the new user authentication flow",
        "developer",
    ),
    (
        "Surgical Correction",
        "fix the off-by-one error in the pagination logic",
        {"developer", "troubleshooter"},
    ),
    (
        "Structural Evolution",
        "refactor the data pipeline to reduce coupling between modules",
        "architect",
    ),
    (
        "Adversarial Review",
        "review for security vulnerabilities and injection risks",
        {"code-reviewer", "security-auditor", "reviewer"},
    ),
    (
        "Exploratory Analysis",
        "find all places where the config is loaded and trace the data flow",
        {"scout", "Explore", "researcher"},
    ),
    (
        "Knowledge Sync",
        "update the README to reflect the current API surface",
        {"doc-expert", "documentation-writer"},
    ),
]


def _make_routing_check(intent: str, prompt: str, expected: str | set[str]) -> Callable[[], None]:
    def _check() -> None:
        from control_plane_daemon.execution_profile_selector import ExecutionProfileSelector

        sel = ExecutionProfileSelector()
        active = sel.get_active_profiles(prompt_text=prompt, intent=intent)
        assert active, f"No profiles returned for intent '{intent}'"

        top = active[0]["name"]
        if isinstance(expected, str):
            assert top == expected, (
                f"intent='{intent}': expected top profile '{expected}', got '{top}'\n"
                f"        Full ranking: {[p['name'] for p in active[:5]]}"
            )
        else:
            assert top in expected, (
                f"intent='{intent}': expected top profile in {expected}, got '{top}'\n"
                f"        Full ranking: {[p['name'] for p in active[:5]]}"
            )

    return _check


for intent, prompt, expected in ROUTING_CASES:
    label = f"{intent} → {expected if isinstance(expected, str) else '/'.join(sorted(expected))}"
    check(label, _make_routing_check(intent, prompt, expected))


# ---------------------------------------------------------------------------
# Step 3: Fallback — unknown intent still returns profiles
# ---------------------------------------------------------------------------

print("\n── Step 3: fallback behaviour ──────────────────────────────────────")


def _unknown_intent_returns_profiles() -> None:
    from control_plane_daemon.execution_profile_selector import ExecutionProfileSelector

    sel = ExecutionProfileSelector()
    active = sel.get_active_profiles(
        prompt_text="do something with the code",
        intent="Unknown Intent Type",
    )
    assert active, "No profiles returned for unknown intent — selector must always return something"


def _empty_prompt_returns_profiles() -> None:
    from control_plane_daemon.execution_profile_selector import ExecutionProfileSelector

    sel = ExecutionProfileSelector()
    active = sel.get_active_profiles(prompt_text="", intent="Feature Synthesis")
    assert active, "No profiles returned for empty prompt with valid intent"
    assert active[0]["name"] == "developer", (
        f"Feature Synthesis with empty prompt: expected 'developer', got '{active[0]['name']}'"
    )


check("unknown intent still returns profiles", _unknown_intent_returns_profiles)
check("empty prompt + valid intent → correct profile", _empty_prompt_returns_profiles)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n────────────────────────────────────────────────────────────────────")
if failures:
    print(f"  FAILED — {len(failures)} assertion(s) did not pass:")
    for f in failures:
        print(f"    • {f}")
    sys.exit(1)
else:
    print("  All assertions passed.")
    sys.exit(0)
