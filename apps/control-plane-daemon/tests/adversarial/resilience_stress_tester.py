import json
import logging
import os
import random
import signal
import subprocess
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Fault:
    name: str
    action: Callable
    description: str


class ResilienceStressTester:
    """
    The ResilienceStressTester injects randomized faults into the Control Plane environment
    to verify the resilience of the S-CORRECT recovery loop.
    """

    def __init__(self, socket_path: str, settings_path: str, daemon_pid_file: str = None):
        self.socket_path = socket_path
        self.settings_path = settings_path
        self.daemon_pid_file = daemon_pid_file
        self.logger = logging.getLogger("ResilienceStressTester")

        # Define the fault library based on the Adversarial Matrix
        self.faults: list[Fault] = [
            Fault("SIGKILL_DAEMON", self._kill_daemon, "Hard crash of the background daemon"),
            Fault("DROP_SOCKET", self._drop_socket, "Sudden deletion of the UDS socket"),
            Fault(
                "CORRUPT_CONFIG",
                self._corrupt_config,
                "Injection of invalid data into settings.json",
            ),
            Fault(
                "PERMISSION_DENIAL",
                self._deny_permissions,
                "Removing read/write access to critical files",
            ),
        ]

    def _kill_daemon(self):
        """Simulates a hard crash by sending SIGKILL to the daemon process."""
        if self.daemon_pid_file and os.path.exists(self.daemon_pid_file):
            with open(self.daemon_pid_file) as f:
                try:
                    pid = int(f.read().strip())
                    os.kill(pid, signal.SIGKILL)
                    self.logger.warning(f"ResilienceStressTester: Sent SIGKILL to PID {pid}")
                except (ValueError, ProcessLookupError):
                    pass
        else:
            # Fallback: try to find it via pgrep if pid_file is missing
            try:
                pid = (
                    subprocess.check_output(["pgrep", "-f", "control_plane_daemon"])
                    .decode()
                    .split()[0]
                )
                os.kill(int(pid), signal.SIGKILL)
                self.logger.warning(f"ResilienceStressTester: Sent SIGKILL to discovered PID {pid}")
            except subprocess.CalledProcessError:
                self.logger.error("ResilienceStressTester: Could not find daemon process to kill")

    def _drop_socket(self):
        """Simulates transport failure by deleting the socket file."""
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
            self.logger.warning(f"ResilienceStressTester: Dropped socket at {self.socket_path}")
        else:
            self.logger.error("ResilienceStressTester: Socket already missing")

    def _corrupt_config(self):
        """Simulates state failure by corrupting the settings.json file."""
        try:
            with open(self.settings_path) as f:
                data = json.load(f)

            # Corrupt a random key
            keys = list(data.keys())
            if keys:
                target = random.choice(keys)
                data[target] = "CORRUPTED_BY_STRESS_TESTER"
                with open(self.settings_path, "w") as f:
                    json.dump(data, f)
                self.logger.warning(f"ResilienceStressTester: Corrupted config key '{target}'")
        except Exception as e:
            self.logger.error(f"ResilienceStressTester: Failed to corrupt config: {e}")

    def _deny_permissions(self):
        """Simulates permission errors by changing file modes."""
        try:
            os.chmod(self.settings_path, 0o000)
            self.logger.warning(
                f"ResilienceStressTester: Denied all permissions to {self.settings_path}"
            )
        except Exception as e:
            self.logger.error(f"ResilienceStressTester: Failed to deny permissions: {e}")

    def restore_environment(self):
        """Restores the environment to a known good state."""
        self.logger.info("ResilienceStressTester: Restoring environment...")
        # Restore permissions
        if os.path.exists(self.settings_path):
            os.chmod(self.settings_path, 0o644)

        # Note: Socket restoration and Daemon restart are handled by the
        # ControlPlane's own recovery or the test harness.

    def inject_random_fault(self):
        """Selects and executes a random fault from the library."""
        fault = random.choice(self.faults)
        self.logger.info(
            f"ResilienceStressTester: Injecting fault [{fault.name}] - {fault.description}"
        )
        fault.action()
        return fault.name


if __name__ == "__main__":
    # Simple smoke test
    logging.basicConfig(level=logging.INFO)
    tester = ResilienceStressTester("/tmp/test.sock", "/tmp/settings.json")
    tester.inject_random_fault()
