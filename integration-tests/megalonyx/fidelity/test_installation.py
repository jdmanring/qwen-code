import os
import shutil
import subprocess
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def fake_home() -> Generator[Path, None, None]:
    """Provides a temporary directory on the actual disk to act as a fake HOME.
    We use a directory inside the project root to avoid /tmp space limits.
    """
    # Create a directory in the project root for the fake home
    project_root = Path(__file__).resolve().parent.parent.parent
    tmp_home = project_root / "tests" / "tmp_install_home"

    if tmp_home.exists():
        shutil.rmtree(tmp_home)
    tmp_home.mkdir(parents=True)

    yield tmp_home

    # Cleanup after test
    if tmp_home.exists():
        shutil.rmtree(tmp_home)


def test_installation_process(fake_home: Path) -> None:
    """
    Verifies that install.sh correctly sets up the stack in a clean environment.
    """
    # 1. Setup Environment
    env = os.environ.copy()
    env["HOME"] = str(fake_home)

    # Get absolute path to the project root (where install.sh lives)
    project_root = Path(__file__).resolve().parent.parent.parent
    install_script = project_root / "install.sh"

    # Ensure install.sh is executable
    os.chmod(install_script, 0o755)

    # 2. Execute Installation
    print(f"Running installation in fake home: {fake_home}")
    result = subprocess.run(
        [str(install_script)], env=env, capture_output=True, text=True
    )

    # 3. Verify Installation Success
    assert result.returncode == 0, (
        f"Installation failed with exit code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )

    # 4. Verify Directory Structure
    stack_root = fake_home / ".local/share/megalonyx"
    bin_dir = fake_home / ".local/bin"

    assert stack_root.exists(), "STACK_ROOT was not created"
    assert (stack_root / "scripts").is_dir(), "scripts directory missing in STACK_ROOT"
    assert (stack_root / "config").is_dir(), "config directory missing in STACK_ROOT"
    assert (stack_root / "packages").is_dir(), (
        "packages directory missing in STACK_ROOT"
    )

    # 5. Verify Binaries/Wrappers
    assert (bin_dir / "mega-run-py").exists(), "mega-run-py wrapper missing in BIN_DIR"
    assert (bin_dir / "mega-memory-manager").exists(), (
        "mega-memory-manager wrapper missing in BIN_DIR"
    )
    assert (bin_dir / "mega-status").exists(), "mega-status wrapper missing in BIN_DIR"

    # Check execution permissions
    for bin_name in ["mega-run-py", "mega-memory-manager", "mega-status"]:
        assert os.access(bin_dir / bin_name, os.X_OK), (
            f"Binary {bin_name} is not executable"
        )

    # 6. Verify Python Virtual Environment
    venv_python = stack_root / "py/venv/bin/python3"
    assert venv_python.exists(), "Python virtual environment not found in STACK_ROOT"

    # Test the venv by checking a dependency
    dep_check = subprocess.run(
        [str(venv_python), "-c", "import qdrant_client; print('OK')"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert dep_check.returncode == 0, (
        f"Virtual environment dependency check failed: {dep_check.stderr}"
    )
    assert "OK" in dep_check.stdout

    # 7. Verify Configuration Deployment
    assert (stack_root / "config/qdrant_config.yaml").exists(), (
        "qdrant_config.yaml not deployed"
    )

    print("Installation verification successful!")


if __name__ == "__main__":
    pytest.main([__file__])
