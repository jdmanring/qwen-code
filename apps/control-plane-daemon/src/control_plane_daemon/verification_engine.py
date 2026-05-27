import json
import os
from dataclasses import dataclass
from typing import Any

from .job_state_manager import JobStateManager
from .models import JobStatus


@dataclass
class VerificationResult:
    is_success: bool
    confidence: float
    logs: str
    suggested_action: str  # "RETRY", "PIVOT", "ABORT"


class BaseContract:
    """Base class for all verification contracts."""

    min_confidence = 0.8

    def evaluate(self, output_data: Any, context: dict[str, Any]) -> VerificationResult:
        raise NotImplementedError("Contracts must implement the evaluate method.")


class VerificationEngine:
    def __init__(
        self, job_state_manager: JobStateManager, settings_path: str | None = None
    ) -> None:
        self.jsm = job_state_manager
        if settings_path is None:
            settings_path = os.path.expanduser("~/.qwen/settings.json")

        with open(settings_path) as f:
            self.settings = json.load(f)

        # Registry of active contracts
        self.contracts: dict[str, BaseContract] = {}

    def register_contract(self, job_type: str, contract: BaseContract) -> None:
        """Registers a verification contract for a specific job type."""
        self.contracts[job_type] = contract

    def verify_job(
        self,
        job_id: str,
        job_type: str,
        output_data: Any,
        context: dict[str, Any] | None = None,
    ) -> VerificationResult:
        """
        Orchestrates the verification of a job.
        """
        context = context or {}
        contract = self.contracts.get(job_type)

        if not contract:
            # Default: If no contract exists, we assume success but with low confidence
            return VerificationResult(
                is_success=True,
                confidence=0.5,
                logs="No contract defined for this job type. Defaulting to success.",
                suggested_action="NONE",
            )

        # Execute the contract's evaluation logic
        result = contract.evaluate(output_data, context)

        # Update the JobStateManager based on the result
        if result.is_success and result.confidence >= contract.min_confidence:
            self.jsm.update_job_status(job_id, JobStatus.COMPLETED, result=result.logs)
        else:
            self.jsm.update_job_status(job_id, JobStatus.FAILED, result=result.logs)

        return result


if __name__ == "__main__":
    # Simple test for the engine
    jsm = JobStateManager()
    jsm.initialize_job_set([{"job_id": "test_1", "status": JobStatus.PENDING, "dependencies": []}])

    engine = VerificationEngine(jsm)
    # Test default behavior
    res = engine.verify_job("test_1", "unknown_type", "some data")
    print(f"Default Result: {res.is_success}, Confidence: {res.confidence}")
