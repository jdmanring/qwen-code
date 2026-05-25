import asyncio

import pytest

from .base_e2e import E2EBase


@pytest.mark.asyncio
async def test_golden_path_bugfix():
    """
    Scenario: User requests a targeted bugfix.
    Verification: Intent is correctly identified, jobs are executed, and result is aggregated.
    """
    e2e = E2EBase()
    try:
        prompt = "Fix the bug in utils.py where calculate_sum fails for negative numbers."
        mock_intent = {
            "intent": "Targeted Bugfix",
            "reasoning": "User is reporting a specific bug in a specific file.",
            "risk_profile": "Low",
            "suggested_tool_chain": ["read_file", "edit"],
        }
        # Mock results for the 3 typical jobs in a bugfix flow
        mock_results = [
            "Identified bug at line 12: missing abs() call.",
            "Applied fix: replaced x with abs(x).",
            "Verified fix with pytest: 5 tests passed.",
        ]

        result, cp = await e2e.run_scenario(prompt, mock_intent, mock_results)

        assert "Applied fix" in result
        assert "Verified fix" in result
        assert cp.is_complete()
    finally:
        e2e.cleanup()


@pytest.mark.asyncio
async def test_golden_path_feature():
    """
    Scenario: User requests a new feature implementation.
    Verification: Intent is 'Feature Implementation', complex job set is handled.
    """
    e2e = E2EBase()
    try:
        prompt = "Add a new export_to_csv function to the data_manager.py."
        mock_intent = {
            "intent": "Feature Implementation",
            "reasoning": "User wants to add new functionality.",
            "risk_profile": "Med",
            "suggested_tool_chain": ["todo_write", "edit"],
        }
        # Mock results for a feature flow (7 jobs in template)
        mock_results = [
            "Investigated requirements.",
            "Designed CSV schema.",
            "Created test suite.",
            "Proved baseline fails.",
            "Implemented export_to_csv function.",
            "Verified implementation via tests.",
            "Performed final quality audit.",
        ]

        result, cp = await e2e.run_scenario(prompt, mock_intent, mock_results)

        assert "Implemented export_to_csv" in result
        assert "Verified implementation" in result
        assert cp.is_complete()
    finally:
        e2e.cleanup()


@pytest.mark.asyncio
async def test_golden_path_refactor():
    """
    Scenario: User requests an architectural refactor.
    Verification: Intent is 'Architectural Refactor', stability is verified.
    """
    e2e = E2EBase()
    try:
        prompt = "Refactor the auth module to use a Strategy pattern for different providers."
        mock_intent = {
            "intent": "Architectural Refactor",
            "reasoning": "User wants to improve the architectural structure.",
            "risk_profile": "High",
            "suggested_tool_chain": ["grep_search", "edit", "review"],
        }
        # Mock results for refactor flow (3 jobs in template)
        mock_results = [
            "Mapped existing auth providers.",
            "Migrated providers to Strategy pattern.",
            "Verified no behavioral changes via regression tests.",
        ]

        result, cp = await e2e.run_scenario(prompt, mock_intent, mock_results)

        assert "Migrated providers" in result
        assert "regression tests" in result
        assert cp.is_complete()
    finally:
        e2e.cleanup()


if __name__ == "__main__":
    # Allow running via 'python test_golden_paths.py'
    asyncio.run(pytest.main([__file__]))
