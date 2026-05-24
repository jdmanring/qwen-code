import json
import os

# Add the system directory to path so we can import the components
import sys
from typing import Any
from unittest.mock import patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/system")))

from contracts import MutationContract
from intent_classifier import IntentClassifier
from job_state_manager import JobStateManager
from policy_engine import PolicyEngine
from task_decomposer import TaskDecomposer
from verification_engine import BaseContract, VerificationEngine, VerificationResult

# --- Mocks and Helpers ---


def create_mock_settings() -> str:
    """Creates a temporary settings file for testing."""
    settings = {"fastModel": "mock-model", "env": {"API_KEY": "mock-key"}}
    path = "/tmp/qwen_test_settings.json"
    with open(path, "w") as f:
        json.dump(settings, f)
    return path


def execute_tool(tool_name: str, policy: dict[str, Any]) -> str:
    """Simulates the tool execution logic with policy enforcement."""
    if tool_name not in policy["allowed_tools"]:
        return "Policy Violation"
    return "Success"


# --- Test Suite ---


class TestControlPlane:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.settings_path = create_mock_settings()
        self.classifier = IntentClassifier(settings_path=self.settings_path)
        self.policy_engine = PolicyEngine(settings_path=self.settings_path)
        self.decomposer = TaskDecomposer(settings_path=self.settings_path)
        self.jsm = JobStateManager(settings_path=self.settings_path)
        self.verify_engine = VerificationEngine(self.jsm, settings_path=self.settings_path)

    def test_policy_enforcement(self) -> None:
        """
        Test Case 1: Policy Enforcement
        Input: A prompt that triggers 'Exploratory Analysis' (Read-Only).
        Action: Attempt to call the 'edit' tool.
        Expected: The execute_tool function must return a 'Policy Violation' error.
        """
        # Mock classification result
        with patch.object(
            IntentClassifier,
            "classify",
            return_value={
                "intent": "Exploratory Analysis",
                "reasoning": "User wants to understand the code.",
                "risk_profile": "Low",
                "suggested_tool_chain": ["read_file", "grep_search"],
            },
        ):
            prompt = "Explain how the memory system works."
            classification = self.classifier.classify(prompt)
            intent = classification["intent"]

            policy = self.policy_engine.get_permissions(intent)
            result = execute_tool("edit", policy)

            assert result == "Policy Violation", (
                f"Tool 'edit' should be blocked for intent {intent}"
            )

    def test_end_to_end_happy_path(self) -> None:
        """
        Test Case 2: End-to-End Happy Path
        Input: A 'Surgical Correction' prompt.
        Action: Execute the full job sequence.
        Expected: Jobs transition from pending -> in_progress -> completed.
        """
        # 1. Intent Classification
        with patch.object(
            IntentClassifier,
            "classify",
            return_value={
                "intent": "Surgical Correction",
                "reasoning": "User wants to fix a specific bug.",
                "risk_profile": "Low-Med",
                "suggested_tool_chain": ["read_file", "edit"],
            },
        ):
            prompt = "Fix the typo in README.md"
            classification = self.classifier.classify(prompt)
            intent = classification["intent"]

        # 2. Policy Check
        policy = self.policy_engine.get_permissions(intent)
        assert policy["can_write"] is True

        # 3. Task Decomposition
        job_contract = {"intent": intent, "risk_profile": "Low-Med"}
        jobs = self.decomposer.decompose(job_contract)

        # 4. State Management Initialization
        self.jsm.initialize_job_set(jobs)

        # 5. Job Execution Loop
        # We mock a simple contract that always succeeds for this test
        class SuccessContract(BaseContract):
            def evaluate(self, output_data: Any, context: dict[str, Any]) -> VerificationResult:
                return VerificationResult(True, 1.0, "Success!", "NONE")

        self.verify_engine.register_contract("isolation", SuccessContract())
        self.verify_engine.register_contract("mutation", SuccessContract())
        self.verify_engine.register_contract("verification", SuccessContract())

        while not self.jsm.is_task_complete():
            job = self.jsm.get_next_job()
            assert job is not None

            # Transition to in_progress
            self.jsm.update_job_status(job["job_id"], "in_progress")

            # Simulate work and verify
            self.verify_engine.verify_job(
                job["job_id"],
                job["job_type"],
                "Mock output data",
                {"project_root": "/tmp"},
            )

            # Verify transition to completed
            updated_job = self.jsm.update_job_status(
                job["job_id"], "completed"
            )  # This is redundant as verify_job does it, but let's be explicit
            assert updated_job["status"] == "completed"

        assert self.jsm.is_task_complete() is True

    def test_verification_gate(self) -> None:
        """
        Test Case 3: Verification Gate
        Input: A mutation job that produces a result that fails the MutationContract.
        Action: Run verify_job.
        Expected: The job status must be set to FAILED and the VerificationResult must contain the failure logs.
        """
        # Setup a job
        job_id = "mutation_job_1"
        self.jsm.initialize_job_set([{"job_id": job_id, "status": "pending", "dependencies": []}])

        # Mock MutationContract to fail
        class FailingMutationContract(MutationContract):
            def evaluate(self, output_data: Any, context: dict[str, Any]) -> VerificationResult:
                return VerificationResult(
                    is_success=False,
                    confidence=0.0,
                    logs="Pytest failed: test_core_logic failed",
                    suggested_action="RETRY",
                )

        self.verify_engine.register_contract("mutation", FailingMutationContract())

        # Verify job
        result = self.verify_engine.verify_job(
            job_id, "mutation", "Some buggy code", {"project_root": "/tmp"}
        )

        # Check result
        assert result.is_success is False
        assert "Pytest failed" in result.logs

        # Check state manager
        job_set = self.jsm.sm.get("active_job_set")
        assert job_set["jobs"][job_id]["status"] == "failed"
        assert "Pytest failed" in job_set["jobs"][job_id]["result"]

    def test_decomposition_accuracy(self) -> None:
        """
        Test Case 4: Decomposition Accuracy
        Input: A 'Feature Synthesis' prompt.
        Expected: The TaskDecomposer must produce a sequence of at least 3 jobs.
        """
        job_contract = {"intent": "Feature Synthesis", "risk_profile": "Med"}
        jobs = self.decomposer.decompose(job_contract)

        assert len(jobs) >= 3

        # Verify sequence: Planning -> Implementation -> Verification
        job_types = [j["job_type"] for j in jobs]
        assert "planning" in job_types
        assert "mutation" in job_types
        assert "verification" in job_types
