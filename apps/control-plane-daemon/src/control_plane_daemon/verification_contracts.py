import os
import subprocess
from typing import Any

from .verification_engine import BaseContract, VerificationResult


class DynamicVerificationContract(BaseContract):
    """
    Executes a specific command as the verification criteria.
    The criteria should be a shell command (e.g., 'pytest tests/test_auth.py').
    """

    def evaluate(self, output_data: Any, context: dict[str, Any]) -> VerificationResult:
        # The verification criteria is passed via the job's context or as the output_data
        # In our system, we'll expect the criteria to be in the context
        criteria = context.get("verification_criteria")
        if not criteria:
            return VerificationResult(
                is_success=False,
                confidence=0.0,
                logs="No verification criteria provided in context.",
                suggested_action="RETRY",
            )

        project_root = context.get("project_root", os.getcwd())

        try:
            # Execute the specified command
            result = subprocess.run(
                criteria,
                shell=True,
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=60,
            )

            logs = f"Command: {criteria}\\nStdout:\\n{result.stdout}\\nStderr:\\n{result.stderr}"

            if result.returncode == 0:
                return VerificationResult(
                    is_success=True,
                    confidence=1.0,
                    logs=f"Verification PASSED: {logs}",
                    suggested_action="NONE",
                )
            else:
                return VerificationResult(
                    is_success=False,
                    confidence=0.0,
                    logs=f"Verification FAILED (Exit {result.returncode}): {logs}",
                    suggested_action="RETRY",
                )
        except subprocess.TimeoutExpired:
            return VerificationResult(False, 0.0, "Verification timed out after 60s.", "RETRY")
        except (OSError, ValueError) as e:
            return VerificationResult(
                False, 0.0, f"Verification execution error: {str(e)}", "PIVOT"
            )


class MutationContract(BaseContract):
    """Verification for code changes (Mutation jobs)."""

    min_confidence = 1.0  # Code must be 100% correct

    def evaluate(self, output_data: Any, context: dict[str, Any]) -> VerificationResult:
        project_root = context.get("project_root", os.getcwd())

        # 1. Run Pytest
        pytest_result = subprocess.run(
            ["pytest", "tests/"], cwd=project_root, capture_output=True, text=True
        )

        # 2. Run Mypy (Type Checking)
        mypy_result = subprocess.run(
            ["mypy", "."], cwd=project_root, capture_output=True, text=True
        )

        logs = (
            f"Pytest Output:\\n{pytest_result.stdout}\\n{pytest_result.stderr}\\n\\n"
            f"Mypy Output:\\n{mypy_result.stdout}\\n{mypy_result.stderr}"
        )

        if pytest_result.returncode == 0 and mypy_result.returncode == 0:
            return VerificationResult(
                is_success=True,
                confidence=1.0,
                logs="All tests and type checks passed.",
                suggested_action="NONE",
            )

        # Failure analysis
        action = "RETRY"
        if "SyntaxError" in logs:
            action = "PIVOT"  # Syntax errors usually require a different approach

        return VerificationResult(
            is_success=False, confidence=0.0, logs=logs, suggested_action=action
        )


class DiscoveryContract(BaseContract):
    """Verification for symbol/file discovery jobs."""

    min_confidence = 0.8

    def evaluate(self, output_data: Any, context: dict[str, Any]) -> VerificationResult:
        requested_symbols = context.get("requested_symbols", [])
        found_symbols = output_data if isinstance(output_data, list) else []

        if not requested_symbols:
            return VerificationResult(True, 1.0, "No symbols requested.", "NONE")

        found_count = len(set(requested_symbols) & set(found_symbols))
        coverage = found_count / len(requested_symbols)

        if coverage >= self.min_confidence:
            return VerificationResult(
                True,
                coverage,
                f"Found {found_count}/{len(requested_symbols)} symbols.",
                "NONE",
            )

        return VerificationResult(
            is_success=False,
            confidence=coverage,
            logs=f"Insufficient coverage: {found_count}/{len(requested_symbols)}",
            suggested_action="EXPAND_SCOPE",
        )


class SynthesisContract(BaseContract):
    """Verification for plan/doc synthesis jobs using a Reviewer LLM."""

    min_confidence = 0.7

    def evaluate(self, output_data: Any, context: dict[str, Any]) -> VerificationResult:
        # In a real implementation, this would call a separate LLM 'Reviewer'
        # For the prototype, we check for structural markers
        if not output_data or len(output_data) < 50:
            return VerificationResult(
                False, 0.0, "Output too short to be a valid synthesis.", "RETRY"
            )

        # Check for required sections (e.g., 'Plan', 'Verification')
        required = ["Plan", "Verification", "Outcome"]
        found = [r for r in required if r.lower() in output_data.lower()]
        coverage = len(found) / len(required)

        if coverage >= self.min_confidence:
            return VerificationResult(
                True, coverage, "Synthesis contains required sections.", "NONE"
            )

        return VerificationResult(
            False,
            coverage,
            f"Missing sections: {set(required) - set(found)}",
            "REFINEMENT",
        )
