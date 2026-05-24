import json
import sys
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project root to sys.path to import local modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent

from control_plane_daemon.control_plane import ControlPlane  # noqa: E402
from control_plane_daemon.execution_context import ExecutionContext  # noqa: E402

# --- Mocks and Helpers ---


@pytest.fixture
def temp_agent_dir(tmp_path: Path) -> Path:
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
def control_plane(
    temp_agent_dir: Path, tmp_path: Path
) -> Generator[tuple[ControlPlane, Path], None, None]:
    """Initializes ControlPlane with mocked paths."""
    # We will patch os.path.expanduser in the control_plane module
    # Using yield to keep the patch active during the test
    with patch("control_plane_daemon.control_plane.os.path.expanduser") as mock_expanduser:
        mock_expanduser.side_effect = lambda p: (
            str(temp_agent_dir / p.split("/")[-1]) if "agents" in p else p
        )

        # We also need to mock the settings_path for ControlPlane
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({"model": {"name": "mock-model"}}))

        cp = ControlPlane(settings_path=str(settings_file))
        yield cp, temp_agent_dir


# --- Test Suite ---


class TestAgentSpawning:
    def test_spawn_agent_success(self, control_plane: tuple[ControlPlane, Path]) -> None:
        """
        Test Case: Successful Agent Spawning
        Action: Call _spawn_agent for a valid agent.
        Expected: The agent's persona is loaded and run_job_execution is called.
        """
        cp, agent_dir = control_plane
        agent_id = "test-agent"
        task_prompt = "Hello, test agent!"
        model_id = "mock-model"
        settings = {"model": {"name": "mock-model"}}
        rag_tool = MagicMock()
        root_context = ExecutionContext()

        # We need to patch run_job_execution in skill_bridge
        # Note: ControlPlane imports it inside the method
        with patch("control_plane_daemon.tool_executor.run_job_execution") as mock_run_job:
            mock_run_job.return_value = "Agent response: Hello!"

            response = cp._spawn_agent(
                agent_id=agent_id,
                task_prompt=task_prompt,
                model_id=model_id,
                settings=settings,
                rag_tool=rag_tool,
                root_context=root_context,
            )

            assert response == "Agent response: Hello!"
            mock_run_job.assert_called_once()

            # Verify the agent_config passed to run_job_execution
            args, kwargs = mock_run_job.call_args
            agent_config = args[2]
            assert agent_config["name"] == agent_id
            assert "You are a test agent" in agent_config["system_prompt"]

    def test_spawn_agent_not_found(self, control_plane: tuple[ControlPlane, Path]) -> None:
        """
        Test Case: Agent Not Found
        Action: Call _spawn_agent for a non-existent agent.
        Expected: Return an error message.
        """
        cp, _ = control_plane
        agent_id = "non-existent-agent"

        response = cp._spawn_agent(
            agent_id=agent_id,
            task_prompt="Hello",
            model_id="mock-model",
            settings={},
            rag_tool=MagicMock(),
            root_context=ExecutionContext(),
        )

        assert "Error: Agent non-existent-agent not found." in response


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
