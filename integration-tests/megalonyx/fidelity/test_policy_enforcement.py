import pytest
from control_plane_daemon.policy_engine import PolicyEngine


def test_test_engineer_no_fix_constraint() -> None:
    """
    Verify that the test-engineer agent is strictly forbidden from using write tools.
    """
    engine = PolicyEngine()

    # Test for the 'test-engineer' agent
    policy = engine.get_permissions(
        intent="Surgical Correction", agent_name="test-engineer"
    )

    # Check that write tools are NOT in the allowed list
    forbidden_tools = ["write_file", "edit"]
    for tool in forbidden_tools:
        assert tool not in policy["allowed_tools"], (
            f"test-engineer should NOT be allowed to use {tool}"
        )

    # Verify that verification tools ARE allowed
    assert "run-pytest" in policy["allowed_tools"]
    assert "run-mypy" in policy["allowed_tools"]


def test_developer_can_write() -> None:
    """Verify that the developer agent CAN use write tools."""
    engine = PolicyEngine()

    policy = engine.get_permissions(
        intent="Surgical Correction", agent_name="logic-implementer"
    )

    assert "write_file" in policy["allowed_tools"]
    assert "edit" in policy["allowed_tools"]


def test_intent_based_write_restriction() -> None:
    """Verify that 'Exploratory Analysis' intent denies write access regardless of agent."""
    engine = PolicyEngine()

    policy = engine.get_permissions(
        intent="Exploratory Analysis", agent_name="logic-implementer"
    )

    assert policy["can_write"] is False


if __name__ == "__main__":
    pytest.main([__file__])
