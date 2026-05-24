import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/core/src"))
)

from pathlib import Path

from context import ExecutionContext
from control_plane import ControlPlane

# --- Mocks and Helpers ---


@pytest.fixture
def temp_settings(tmp_path: Path) -> str:
    settings_file = tmp_path / "settings.json"
    settings_file.write_text(json.dumps({"model": {"name": "mock-model"}}))
    return str(settings_file)


@pytest.fixture
def control_plane(temp_settings: str) -> tuple[ControlPlane, MagicMock]:
    # We need to patch the command manager to avoid it looking in ~/.qwen/commands
    # It's imported inside __init__, so we patch the module where it's defined
    with patch("command_manager.CommandManager") as mock_cmd_manager_class:
        mock_cmd_manager = mock_cmd_manager_class.return_value

        # Setup a dummy command
        mock_cmd_manager.get_command.return_value = {
            "name": "bugfix",
            "description": "Fix a bug",
            "workflow": "## Step 1: Reproduce\nSpawn the test-engineer agent\n\n## Step 2: Verify\nSpawn the reviewer agent",
        }

        cp = ControlPlane(settings_path=temp_settings)
        yield cp, mock_cmd_manager


# --- Test Suite ---


class TestCommandRouting:
    def test_process_intent_slash_command(
        self, control_plane: tuple[ControlPlane, MagicMock]
    ) -> None:
        """
        Test Case: Slash Command Routing
        Input: A prompt starting with '/bugfix'
        Expected: The intent is 'command:bugfix' and the command_workflow is returned.
        """
        cp, mock_cmd_manager = control_plane
        prompt = "/bugfix some issue"

        # We need to mock the job set initialization as it's called during command processing
        with patch.object(
            cp.jsm, "initialize_job_set", return_value={"job_set_id": "test_job_set"}
        ) as mock_init_jobs:
            result = cp.process_intent(prompt)

            assert result["intent"] == "command:bugfix"
            assert "command_workflow" in result
            assert result["command_workflow"]["name"] == "bugfix"
            assert "Fix a bug" in result["command_workflow"]["description"]

            # Verify that a workflow job was created
            mock_init_jobs.assert_called_once()
            jobs = mock_init_jobs.call_args[0][0]
            assert len(jobs) == 1
            assert jobs[0]["job_type"] == "workflow"
            assert jobs[0]["job_id"] == "workflow_root"

    def test_execute_workflow_parsing(
        self, control_plane: tuple[ControlPlane, MagicMock]
    ) -> None:
        """
        Test Case: Workflow Parsing
        Action: Call execute_workflow with a command that contains agent spawning.
        Expected: The workflow is parsed into steps, and agents are spawned.
        """
        cp, mock_cmd_manager = control_plane
        cmd_id = "bugfix"
        prompt = "Fix the bug in math.py"
        model_id = "mock-model"
        settings = {"model": {"name": "mock-model"}}
        rag_tool = MagicMock()
        root_context = ExecutionContext()

        # Mock _spawn_agent to avoid real agent loading
        with patch.object(
            cp, "_spawn_agent", return_value="Agent Report: Done"
        ) as mock_spawn:
            # Mock run_job_execution for the non-agent steps
            with patch(
                "control_plane_daemon.tool_executor.run_job_execution",
                return_value="Orchestrator Result",
            ) as _mock_run:
                result = cp.execute_workflow(
                    cmd_id, prompt, model_id, settings, rag_tool, root_context
                )

                # Verify agents were spawned
                assert mock_spawn.call_count == 2
                mock_spawn.assert_any_call(
                    "test-engineer",
                    f"WORKFLOW STEP 1: Reproduce\nSpawn the test-engineer agent\n\nINPUT CONTEXT: {prompt}",
                    model_id,
                    settings,
                    rag_tool,
                    root_context,
                )
                mock_spawn.assert_any_call(
                    "reviewer",
                    f"WORKFLOW STEP 2: Verify\nSpawn the reviewer agent\n\nINPUT CONTEXT: {prompt}\n\nStep 1 Result: Agent Report: Done",
                    model_id,
                    settings,
                    rag_tool,
                    root_context,
                )

                # Verify orchestrator was called for non-agent steps (if any)
                # In this case, both steps are agent spawns, so mock_run shouldn't be called for steps
                # but it might be called if there were other steps.

                # Check if the final log contains the results
                assert "## Step 1 (Agent: test-engineer)" in result
                assert "Agent Report: Done" in result
                assert "## Step 2 (Agent: reviewer)" in result
                assert "Agent Report: Done" in result
