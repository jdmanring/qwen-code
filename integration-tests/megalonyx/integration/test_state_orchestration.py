import os
import sys

import pytest
from state_manager import StateManager

# Use a temporary state file for testing to avoid corrupting actual project state
TEST_STATE_FILE = "/tmp/qwen_test_state.json"


from collections.abc import Generator  # noqa: E402


@pytest.fixture
def state_manager() -> Generator[StateManager, None, None]:
    # Setup: Create a fresh StateManager with a test file
    sm = StateManager(state_file=TEST_STATE_FILE)
    sm.state = sm._get_default_state()
    sm.save()
    yield sm
    # Teardown: Remove the test file
    if os.path.exists(TEST_STATE_FILE):
        os.remove(TEST_STATE_FILE)


@pytest.fixture
def orchestrator(state_manager: StateManager) -> 'SkillOrchestrator':
    # This fixture is currently broken because SkillOrchestrator was removed.
    pytest.skip("SkillOrchestrator removed in refactor")
    # Use the same state manager as the fixture to ensure consistency
    orch = SkillOrchestrator()
    orch.state_manager = state_manager
    return orch


def test_state_persistence(state_manager: StateManager) -> None:
    """Verify that state is correctly saved and loaded from disk."""
    state_manager.set("active_phase", "VERIFICATION")
    state_manager.set("last_agent", "developer")

    # Create a new manager instance to see if it loads the saved state
    new_sm = StateManager(state_file=TEST_STATE_FILE)
    assert new_sm.get("active_phase") == "VERIFICATION"
    assert new_sm.get("last_agent") == "developer"


def test_phase_boost(
    state_manager: StateManager, orchestrator: 'SkillOrchestrator'
) -> None:
    """Verify that the active_phase correctly boosts relevant agents."""
    pytest.skip("SkillOrchestrator removed in refactor")
    # Set phase to VERIFICATION
    state_manager.set("active_phase", "VERIFICATION")
    # Inject the test state manager into the orchestrator
    orchestrator.state_manager = state_manager

    # Prompt is neutral, but phase is VERIFICATION
    # Reviewer and QA Lead should be top priority
    active = orchestrator.get_active_skills(prompt_text="Check this")

    # The first agent should be one of the verification specialists
    top_agent = active[0]["name"]
    assert top_agent in ["reviewer", "qa_lead"], (
        f"Expected verification agent, got {top_agent}"
    )


def test_confidence_escalation(
    state_manager: StateManager, orchestrator: 'SkillOrchestrator'
) -> None:
    """Verify that low confidence in a report triggers the Reviewer."""
    pytest.skip("SkillOrchestrator removed in refactor")
    # Mock a low-confidence report
    report = "The implementation is done. CONFIDENCE: 0.4"
    analysis = orchestrator.analyze_report(report)

    # Ensure the analysis flags it for review
    assert analysis["needs_review"] is True

    # Check if the orchestrator prioritizes the reviewer based on this context
    active = orchestrator.get_active_skills(
        prompt_text="Continue", report_context=analysis
    )
    assert active[0]["name"] == "reviewer", (
        "Low confidence should force a Reviewer audit"
    )


def test_handoff_routing(
    state_manager: StateManager, orchestrator: 'SkillOrchestrator'
) -> None:
    """Verify that 'NEXT STEP' suggestions correctly route to the suggested agent."""
    pytest.skip("SkillOrchestrator removed in refactor")
    # Mock a report suggesting the Developer
    report = "I have mapped the files. NEXT STEP: Suggest Developer to implement."
    analysis = orchestrator.analyze_report(report)

    # Check if the orchestrator boosts the developer
    active = orchestrator.get_active_skills(
        prompt_text="Proceed", report_context=analysis
    )
    assert active[0]["name"] == "developer", (
        "Handoff suggestion should prioritize the Developer"
    )


def test_iteration_tracking(state_manager: StateManager) -> None:
    """Verify that iteration counts are tracked and reset correctly."""
    state_manager.increment_iteration()
    state_manager.increment_iteration()
    assert state_manager.get("iteration_count") == 2

    state_manager.reset_iteration()
    assert state_manager.get("iteration_count") == 0


def test_state_aware_scoring_priority(
    state_manager: StateManager, orchestrator: 'SkillOrchestrator'
) -> None:
    """Verify that Phase Match > Keyword Match in the scoring hierarchy."""
    pytest.skip("SkillOrchestrator removed in refactor")
    # Set phase to IMPLEMENTATION
    state_manager.set("active_phase", "IMPLEMENTATION")
    orchestrator.state_manager = state_manager

    # Prompt contains 'architecture' (Architect keyword)
    # but phase is IMPLEMENTATION (Developer boost)
    prompt = "I have a question about the architecture while implementing"
    active = orchestrator.get_active_skills(prompt_text=prompt)

    # Developer should be boosted by phase, potentially beating the Architect's keyword
    # (Depending on exact weights: Phase=1.5, Keyword=1.0)
    assert active[0]["name"] == "developer", (
        "Phase match should outweigh simple keyword match"
    )


def test_loop_guard_escalation(
    state_manager: StateManager, orchestrator: 'SkillOrchestrator'
) -> None:
    """Verify that exceeding MAX_ITERATIONS triggers the OPTIMIZATION phase."""
    pytest.skip("SkillOrchestrator removed in refactor")
    # Simulate 8 iterations in the current phase
    for _ in range(8):
        state_manager.increment_iteration()

    # In a real scenario, the skill_bridge.py handles the transition.
    # We simulate the bridge's loop guard logic here.
    MAX_ITERATIONS = 8
    if state_manager.get("iteration_count", 0) >= MAX_ITERATIONS:
        state_manager.set("active_phase", "OPTIMIZATION")
        state_manager.reset_iteration()

    assert state_manager.get("active_phase") == "OPTIMIZATION"
    assert state_manager.get("iteration_count") == 0

    # Debug: print loaded skills
    print(f"Loaded skills: {list(orchestrator.skills.keys())}")

    # Verify that the orchestrator now prioritizes the System Optimizer
    active = orchestrator.get_active_skills(prompt_text="Fix this loop")
    assert len(active) > 0, "No agents were triggered in OPTIMIZATION phase"
    assert active[0]["name"] == "system_optimizer", (
        f"Loop escalation should prioritize System Optimizer, got {active[0]['name']}"
    )
