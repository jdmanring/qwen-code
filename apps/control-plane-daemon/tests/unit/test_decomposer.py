import pytest
from control_plane_daemon.task_decomposer import TaskDecomposer


def test_feat_dev_pipeline_generation() -> None:
    """
    Verify that 'Feature Synthesis' intent triggers the surgical feat-dev pipeline.
    """
    decomposer = TaskDecomposer()

    contract = {
        "intent": "Feature Synthesis",
        "original_prompt": "Add a new dark mode toggle to the settings page",
    }

    jobs = decomposer.decompose(contract)

    # Check for the mandatory feat-dev steps
    descriptions = [j["description"].lower() for j in jobs]

    # We check for the core sequence defined in the templates/prompt
    assert any("investigate" in d for d in descriptions), "Missing Investigation step"
    assert any("design" in d for d in descriptions), "Missing Design step"
    assert any("test suite" in d or "test plan" in d for d in descriptions), (
        "Missing Test Plan step"
    )
    assert any("baseline fails" in d or "dry-run" in d for d in descriptions), (
        "Missing Dry-Run step"
    )
    assert any("implement" in d for d in descriptions), "Missing Implementation step"
    assert any("verify" in d for d in descriptions), "Missing Verification step"
    assert any("review" in d for d in descriptions), "Missing Review step"


def test_decomposer_fallback() -> None:
    """Verify that unknown intents fallback to a basic analysis/mutation/verification loop."""
    decomposer = TaskDecomposer()

    contract = {"intent": "Unknown Intent", "original_prompt": "Do something weird"}

    jobs = decomposer.decompose(contract)
    assert len(jobs) == 3
    assert jobs[0]["assigned_skill"] == "general-purpose"


if __name__ == "__main__":
    pytest.main([__file__])
