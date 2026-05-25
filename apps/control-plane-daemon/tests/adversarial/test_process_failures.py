import asyncio
import os
import shutil
import signal
import subprocess
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from control_plane_daemon.control_plane import ControlPlane


class ProcessAdversarialBase:
    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix="megalonyx-proc-")
        self.settings_path = os.path.join(self.test_dir, "settings.json")
        self.socket_path = os.path.join(self.test_dir, "test_daemon.sock")
        self.setup_environment()

    def setup_environment(self):
        settings = {
            "fastModel": "gemini-2.5-flash-lite",
            "modelProviders": {
                "google": [{"id": "gemini-2.5-flash-lite", "baseUrl": "...", "envKey": "..."}]
            },
        }
        with open(self.settings_path, "w") as f:
            import json

            json.dump(settings, f)

    def cleanup(self):
        shutil.rmtree(self.test_dir)

    def get_control_plane(self) -> ControlPlane:
        return ControlPlane(settings_path=self.settings_path)


@pytest.mark.asyncio
async def test_proc_01_daemon_sigkill():
    """
    Scenario PROC-01: Daemon SIGKILL (Hard crash)
    Expected: Orchestrator detects service death via socket failure.
    """
    proc = ProcessAdversarialBase()
    try:
        # 1. Start a dummy daemon that just listens on a socket
        # We use a simple python script to simulate the daemon
        daemon_script = f"""
import asyncio
import os

async def main():
    socket_path = '{proc.socket_path}'
    if os.path.exists(socket_path):
        os.remove(socket_path)

    server = await asyncio.start_unix_server(lambda r, w: w.close(), path=socket_path)
    async with server:
        await asyncio.Future() # Run forever

if __name__ == "__main__":
    asyncio.run(main())
"""
        with open(os.path.join(proc.test_dir, "dummy_daemon.py"), "w") as f:
            f.write(daemon_script)

        daemon_proc = subprocess.Popen(["python3", os.path.join(proc.test_dir, "dummy_daemon.py")])

        # Give it a moment to start
        await asyncio.sleep(0.5)
        assert os.path.exists(proc.socket_path), "Daemon should have created the socket"

        # 2. Simulate Hard Crash (SIGKILL)
        daemon_proc.send_signal(signal.SIGKILL)
        daemon_proc.wait()

        # 3. Verify Orchestrator behavior
        cp = proc.get_control_plane()

        # Mock a job that requires the daemon
        job = {
            "job_id": "test_job",
            "description": "Call daemon",
            "assigned_skill": "memory",
            "job_type": "discovery",
            "verification_criteria": "Success",
        }

        with (
            patch.object(cp.jsm, "get_next_job", side_effect=[job, None]),
            patch.object(cp.jsm, "update_job_status"),
            patch.object(cp.ve, "verify_job") as mock_verify,
        ):
            mock_verify.return_value = MagicMock(
                is_success=False, suggested_action="RETRY", logs="Socket error"
            )

            # This should now trigger the BrokenPipeError/ConnectionRefusedError logic we added to ControlPlane
            # since the daemon is dead and the socket is either gone or unresponsive.
            try:
                # We use a real tool executor call if possible, or mock it to raise the error
                with patch(
                    "control_plane_daemon.tool_executor.run_job_execution",
                    side_effect=ConnectionRefusedError("Connection refused"),
                ):
                    cp.execute(
                        prompt="Test daemon crash",
                        model_id="gemini-2.5-flash-lite",
                        settings={},
                        search_tool=MagicMock(),
                        root_context=MagicMock(),
                    )
                print("✅ PROC-01: Daemon SIGKILL handled gracefully.")
            except ConnectionRefusedError:
                pytest.fail("ControlPlane should handle ConnectionRefusedError internally")

    finally:
        proc.cleanup()


@pytest.mark.asyncio
async def test_proc_02_daemon_sigterm():
    """
    Scenario PROC-02: Daemon SIGTERM (Graceful)
    Expected: Daemon closes socket and cleans up.
    """
    proc = ProcessAdversarialBase()
    try:
        # 1. Start a daemon that handles SIGTERM
        daemon_script = f"""
import asyncio
import os
import signal
import sys

async def main():
    socket_path = '{proc.socket_path}'
    if os.path.exists(socket_path):
        os.remove(socket_path)

    def handle_exit(sig, frame):
        if os.path.exists(socket_path):
            os.remove(socket_path)
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_exit)

    server = await asyncio.start_unix_server(lambda r, w: w.close(), path=socket_path)
    async with server:
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
"""
        with open(os.path.join(proc.test_dir, "dummy_daemon.py"), "w") as f:
            f.write(daemon_script)

        daemon_proc = subprocess.Popen(["python3", os.path.join(proc.test_dir, "dummy_daemon.py")])
        await asyncio.sleep(0.5)
        assert os.path.exists(proc.socket_path)

        # 2. Graceful Shutdown
        daemon_proc.send_signal(signal.SIGTERM)
        daemon_proc.wait()

        # 3. Verify Cleanup
        assert not os.path.exists(proc.socket_path), "Socket should have been removed on SIGTERM"
        print("✅ PROC-02: Daemon SIGTERM cleanup verified.")

    finally:
        proc.cleanup()


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
