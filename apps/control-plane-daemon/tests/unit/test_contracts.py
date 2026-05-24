import os

import pytest
from control_plane_daemon.verification_contracts import DynamicVerificationContract


def test_dynamic_contract_success() -> None:
    """Verify that a command returning exit 0 is marked as PASSED."""
    contract = DynamicVerificationContract()

    # Use 'ls' as a simple command that should succeed
    context = {"project_root": os.getcwd(), "verification_criteria": "ls ."}

    # We pass None as output_data because the contract uses the context command
    result = contract.evaluate(None, context)

    assert result.is_success is True
    assert result.confidence == 1.0
    assert "Verification PASSED" in result.logs


def test_dynamic_contract_failure() -> None:
    """Verify that a command returning non-zero is marked as FAILED."""
    contract = DynamicVerificationContract()

    # Use a command that should fail
    context = {
        "project_root": os.getcwd(),
        "verification_criteria": "ls /non_existent_directory_12345",
    }

    result = contract.evaluate(None, context)

    assert result.is_success is False
    assert result.confidence == 0.0
    assert "Verification FAILED" in result.logs


def test_dynamic_contract_missing_criteria() -> None:
    """Verify handling of missing verification criteria."""
    contract = DynamicVerificationContract()

    context = {"project_root": os.getcwd()}
    result = contract.evaluate(None, context)

    assert result.is_success is False
    assert "No verification criteria provided" in result.logs


if __name__ == "__main__":
    pytest.main([__file__])
