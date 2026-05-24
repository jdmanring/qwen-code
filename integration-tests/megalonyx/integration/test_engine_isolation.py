import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../packages/core/src"))
)

from context import ExecutionContext
from control_plane import ControlPlane


@pytest.fixture
def temp_settings(tmp_path):
    settings_file = tmp_path / "settings.json"
    settings_file.write_text(json.dumps({"model": {"name": "mock-model"}}))
    return str(settings_file)


@pytest.fixture
def temp_agent_dir(tmp_path):
    """Creates a temporary directory with a test agent persona."""
    agent_dir = tmp_path / "agents"
    agent_dir.mkdir()
    agent_file = agent_dir / "test-agent.md"
    agent_file.write_text("""---
name: test-agent
description: A test agent.
model: inherit
tools:
  - read_file
---

# Test Agent

<agent_persona>
  <identity>
    You are a test agent.
  </identity>
</agent_persona>
""")
    return agent_dir


@pytest.fixture
def control_plane(temp_settings, temp_agent_dir):
    """Initializes ControlPlane with mocked paths."""
    with patch("command_manager.CommandManager") as mock_cmd_manager_class:
        mock_cmd_manager = mock_cmd_manager_class.return_value
        mock_cmd_manager.get_command.return_value = {
            "name": "test-cmd",
            "description": "Test command",
            "workflow": "## Step 1: Task\nSpawn the test-agent agent",
        }

        # We need to patch os.path.expanduser and os.path.exists in the control_plane module
        with patch("control_plane.os.path.expanduser") as mock_expanduser:
            mock_expanduser.side_effect = lambda p: (
                str(temp_agent_dir / os.path.basename(p)) if "agents" in p else p
            )

            with patch("control_plane.os.path.exists") as mock_exists:
                # Ensure comparison works by converting p to string
                mock_exists.side_effect = lambda p: (
                    str(temp_agent_dir / os.path.basename(p)).endswith(".md")
                    or str(p) == str(temp_settings)
                )

                cp = ControlPlane(settings_path=temp_settings)
                yield cp, mock_cmd_manager


class TestEngineIsolation:
    def test_subagent_isolation_context(self, control_plane):
        cp, _ = control_plane
        agent_id = "test-agent"
        task_prompt = "Hello"
        model_id = "mock-model"
        settings = {"model": {"name": "mock-model"}}
        rag_tool = MagicMock()
        root_context = ExecutionContext()
        root_context.file_cache.set("/some/file.txt", "content")

        with patch("skill_bridge.run_job_execution") as mock_run_job:
            mock_run_job.return_value = "Done"
            cp._spawn_agent(
                agent_id, task_prompt, model_id, settings, rag_tool, root_context
            )

            args, kwargs = mock_run_job.call_args
            passed_context = kwargs.get("context") or args[8]
            assert passed_context.file_cache.get("/some/file.txt") is None

    def test_subagent_isolation_history(self, control_plane):
        cp, _ = control_plane
        agent_id = "test-agent"
        task_prompt = "Task for agent"
        model_id = "mock-model"
        settings = {"model": {"name": "mock-model"}}
        rag_tool = MagicMock()
        root_context = ExecutionContext()

        with patch("skill_bridge.run_job_execution") as mock_run_job:
            mock_run_job.return_value = "Done"
            cp._spawn_agent(
                agent_id, task_prompt, model_id, settings, rag_tool, root_context
            )

            args, kwargs = mock_run_job.call_args
            passed_history = kwargs.get("history") or args[10]
            assert len(passed_history) == 1
            assert passed_history[0]["content"] == task_prompt
