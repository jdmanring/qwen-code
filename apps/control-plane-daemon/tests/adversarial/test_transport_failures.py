import os
import shutil
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from control_plane_daemon.control_plane import ControlPlane


class TransportAdversarialBase:
    def __init__(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="megalonyx-trans-")
        self.settings_path = os.path.join(self.test_dir, "settings.json")
        self.socket_path = os.path.join(self.test_dir, "test_memory.sock")
        self.setup_environment()

    def setup_environment(self) -> None:
        settings = {
            "fastModel": "gemini-2.5-flash-lite",
            "modelProviders": {
                "google": [{"id": "gemini-2.5-flash-lite", "baseUrl": "...", "envKey": "..."}]
            },
        }
        with open(self.settings_path, "w") as f:
            import json

            json.dump(settings, f)

    def cleanup(self) -> None:
        shutil.rmtree(self.test_dir)

    def get_control_plane(self) -> ControlPlane:
        return ControlPlane(settings_path=self.settings_path)


@pytest.mark.asyncio
async def test_trans_01_socket_deleted_mid_session():
    """
    Scenario TRANS-01: UDS Socket deleted mid-session
    Expected: System detects BrokenPipeError or ConnectionResetError.
    """
    trans = TransportAdversarialBase()
    try:
        cp = trans.get_control_plane()

        # Mock the tool executor to simulate a socket call that fails
        with patch("control_plane_daemon.tool_executor.run_job_execution") as mock_executor:
            # Simulate a BrokenPipeError when calling a memory tool
            mock_executor.side_effect = BrokenPipeError("Broken pipe")

            # We use a simple prompt that would trigger a tool call
            # In a real scenario, we'd use process_intent + execute
            # For this unit-fidelity test, we'll call execute directly with a mocked job

            # Setup a mock job
            job = {
                "job_id": "test_job",
                "description": "Call memory",
                "assigned_skill": "memory",
                "job_type": "discovery",
                "verification_criteria": "Success",
            }

            # We need to mock the JobStateManager to provide the job
            with (
                patch.object(cp.jsm, "get_next_job", side_effect=[job, None]),
                patch.object(cp.jsm, "update_job_status"),
                patch.object(cp.jsm, "initialize_job_set"),
            ):
                with patch.object(cp.ve, "verify_job") as mock_verify:
                    mock_verify.return_value = MagicMock(
                        is_success=False, suggested_action="RETRY", logs="Socket error"
                    )

                    # This should trigger the BrokenPipeError via mock_executor
                    # and the ControlPlane should handle it (likely by logging and retrying/failing)
                    # Since we mocked run_job_execution to raise, we check if the loop continues or fails gracefully
                    try:
                        cp.execute(
                            prompt="Test socket failure",
                            model_id="gemini-2.5-flash-lite",
                            settings={},
                            search_tool=MagicMock(),
                            root_context=MagicMock(),
                        )
                    except BrokenPipeError:
                        pytest.fail("ControlPlane should handle BrokenPipeError internally")

            print(" TRANS-01: Socket deletion handled gracefully.")
    finally:
        trans.cleanup()


@pytest.mark.asyncio
async def test_trans_03_permission_denied():
    """
    Scenario TRANS-03: Permission denied on socket
    Expected: Bridge reports PermissionError clearly.
    """
    trans = TransportAdversarialBase()
    try:
        # Create a socket file and remove read/write permissions
        with open(trans.socket_path, "w") as f:
            f.write("dummy")
        os.chmod(trans.socket_path, 0o000)

        # We test the MCPManager directly since it handles the connection
        from control_plane_daemon.mcp_manager import MCPManager

        mgr = MCPManager()

        # Register a server using the forbidden socket
        mgr.register_server("forbidden", socket_path=trans.socket_path)

        # Attempt to get the session (which triggers the connection)
        with pytest.raises((PermissionError, OSError)):
            # Using the internal method since there's no public 'connect'
            await mgr._get_session("forbidden")

        print(" TRANS-03: Permission denied reported correctly.")
    finally:
        # Restore permissions to allow cleanup
        os.chmod(trans.socket_path, 0o666)
        trans.cleanup()


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
