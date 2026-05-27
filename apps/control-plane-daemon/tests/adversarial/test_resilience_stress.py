import asyncio
import json
import os
import shutil
import subprocess
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from adversarial.resilience_stress_tester import ResilienceStressTester
from control_plane_daemon.control_plane import ControlPlane


class ResilienceTestBase:
    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix="megalonyx-resilience-")
        self.settings_path = os.path.join(self.test_dir, "settings.json")
        self.socket_path = os.path.join(self.test_dir, "daemon.sock")
        self.pid_file = os.path.join(self.test_dir, "daemon.pid")
        self.setup_environment()

    def setup_environment(self):
        settings = {
            "fastModel": "gemini-2.5-flash-lite",
            "modelProviders": {
                "google": [{"id": "gemini-2.5-flash-lite", "baseUrl": "...", "envKey": "..."}]
            },
        }
        with open(self.settings_path, "w") as f:
            json.dump(settings, f)

    def start_dummy_daemon(self):
        daemon_script = f"""
import asyncio
import os

async def main():
    socket_path = '{self.socket_path}'
    if os.path.exists(socket_path):
        os.remove(socket_path)

    server = await asyncio.start_unix_server(lambda r, w: w.close(), path=socket_path)
    # Write PID to file for ResilienceStressTester
    with open('{self.pid_file}', 'w') as f:
        f.write(str(os.getpid()))

    async with server:
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
"""
        script_path = os.path.join(self.test_dir, "daemon.py")
        with open(script_path, "w") as f:
            f.write(daemon_script)

        proc = subprocess.Popen(["python3", script_path])
        return proc

    def cleanup(self):
        shutil.rmtree(self.test_dir)


@pytest.mark.asyncio
async def test_resilience_loop():
    """
    Scenario RES-01: Random Fault Injection during Execution
    Expected: ControlPlane handles the fault via S-CORRECT and completes the job.
    """
    base = ResilienceTestBase()
    daemon_proc = base.start_dummy_daemon()
    try:
        # Give daemon time to start
        await asyncio.sleep(0.5)

        tester = ResilienceStressTester(
            socket_path=base.socket_path,
            settings_path=base.settings_path,
            daemon_pid_file=base.pid_file,
        )

        cp = ControlPlane(settings_path=base.settings_path)

        # Mock a complex job set
        job = {
            "job_id": "resilience_job",
            "description": "Resilient Task",
            "assigned_skill": "memory",
            "job_type": "discovery",
            "verification_criteria": "Success",
        }

        # Patch the tool executor globally for this test
        mock_exec = patch("control_plane_daemon.tool_executor.run_job_execution").start()
        mock_get_job = patch.object(cp.jsm, "get_next_job").start()
        _mock_update_status = patch.object(cp.jsm, "update_job_status").start()
        mock_verify = patch.object(cp.ve, "verify_job").start()
        mock_is_complete = patch.object(cp, "is_complete").start()

        try:
            # Return the job until it's completed
            mock_get_job.side_effect = [job, job, None]
            mock_is_complete.side_effect = [False, False, True]

            # First call fails (transport), second succeeds
            mock_exec.side_effect = [
                ConnectionRefusedError("Stress Tester struck!"),
                "Successfully recovered and completed task.",
            ]

            # First verification succeeds (since first iteration skipped it)
            mock_verify.side_effect = [
                MagicMock(is_success=True, suggested_action="NONE", logs="Recovered")
            ]

            # Run execution in a thread to avoid blocking the event loop
            loop = asyncio.get_event_loop()

            # We start the execution
            exec_task = loop.run_in_executor(
                None,
                lambda: cp.execute(
                    prompt="Resilience Test",
                    model_id="gemini-2.5-flash-lite",
                    settings={},
                    search_tool=MagicMock(),
                    root_context=MagicMock(),
                ),
            )

            # Inject fault while it's running
            await asyncio.sleep(0.1)
            fault_name = tester.inject_random_fault()
            print(f"ResilienceStressTester injected: {fault_name}")

            result = await exec_task

            assert "completed" in result.lower() or "Successfully recovered" in result
            print(" RES-01: System recovered from random fault.")
        finally:
            patch.stopall()

    finally:
        daemon_proc.kill()
        base.cleanup()


if __name__ == "__main__":
    pytest.main([__file__])
