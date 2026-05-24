import os
import shutil
import sys
import tempfile
from collections.abc import Generator

import pytest

# --- PATH HACK FOR LEGACY IMPORTS ---
# This must happen BEFORE any other imports to allow modules with
# non-standard relative imports to be loaded correctly.

for pkg in ["packages/core/src", "packages/memory"]:
    pkg_path = PROJECT_ROOT / pkg
    if pkg_path.exists() and str(pkg_path) not in sys.path:
        sys.path.insert(0, str(pkg_path))
# -------------------------------------

from control_plane_daemon.mcp_manager import MCPManager  # noqa: E402

# --- CONFIGURATION ---
# We use a temporary directory for all integration tests to avoid
# polluting the actual Blueprint or the Machine's ~/.local share.
TEST_SANDBOX_ROOT = os.path.join(tempfile.gettempdir(), "qwen_integration_sandbox")


@pytest.fixture(scope="session", autouse=True)
def setup_sandbox() -> Generator[str, None, None]:
    """
    Creates a clean sandbox environment for the entire test session.
    """
    if os.path.exists(TEST_SANDBOX_ROOT):
        shutil.rmtree(TEST_SANDBOX_ROOT)
    os.makedirs(TEST_SANDBOX_ROOT)

    # Setup basic structure inside sandbox
    os.makedirs(os.path.join(TEST_SANDBOX_ROOT, "config"))
    os.makedirs(os.path.join(TEST_SANDBOX_ROOT, "packages"))
    os.makedirs(os.path.join(TEST_SANDBOX_ROOT, "logs"), exist_ok=True)

    yield TEST_SANDBOX_ROOT

    # Cleanup after session
    shutil.rmtree(TEST_SANDBOX_ROOT)


@pytest.fixture
async def memory_server(setup_sandbox):
    """
    Launches a local MemoryDaemon instance for the duration of a test.
    Returns the MCP command needed to connect to it.
    """
    # In a real integration test, we would launch the daemon as a subprocess.
    # For these tests, we can instantiate the MemoryCore directly if it's
    # compatible, or use the subprocess approach for maximum fidelity.

    # Using subprocess for maximum fidelity (Mirroring the Lab's approach)
    import subprocess

    # Force the daemon to use the sandbox for its storage/logs
    env = os.environ.copy()
    env["STACK_ROOT"] = TEST_SANDBOX_ROOT

    # We use the actual installed python from the project's venv
    # (Assuming the user is running tests from the project root)
    python_bin = os.path.abspath("./.venv/bin/python3")
    daemon_script = os.path.abspath("./packages/memory/memory_daemon.py")

    process = subprocess.Popen(
        [python_bin, daemon_script],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Wait for socket to be created
    _socket_path = "/tmp/qwen_memory_test.sock"  # Use a test-specific socket
    # Note: We'd need to modify memory_daemon.py to accept a socket path via env
    # For now, we assume it uses the default or we override it.

    # To keep it simple for the first set of tests, we'll return the command
    # and let the MCPManager handle the connection.
    cmd = [python_bin, daemon_script]

    yield cmd

    process.terminate()
    process.wait()


@pytest.fixture
async def mcp_client():
    """
    Provides a configured MCPManager instance.
    """
    return MCPManager()


@pytest.fixture
def sandbox_project(setup_sandbox: str) -> str:
    """
    Provides the path to the temporary sandbox project.
    """
    return TEST_SANDBOX_ROOT
