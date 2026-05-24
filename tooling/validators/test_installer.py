import os
import shutil
import subprocess
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def fake_home() -> Generator[Path, None, None]:
    """Temporary directory on disk acting as a fake HOME for install testing."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    tmp_home = repo_root / "tooling" / "validators" / "tmp_install_home"

    if tmp_home.exists():
        shutil.rmtree(tmp_home)
    tmp_home.mkdir(parents=True)

    yield tmp_home

    if tmp_home.exists():
        shutil.rmtree(tmp_home)


def test_installation_process(fake_home: Path) -> None:
    """
    Verifies that install-megalonyx-stack.sh sets up the stack correctly.
    """
    env = os.environ.copy()
    env["HOME"] = str(fake_home)

    repo_root = Path(__file__).resolve().parent.parent.parent
    install_script = repo_root / "scripts" / "megalonyx" / "install-megalonyx-stack.sh"

    os.chmod(install_script, 0o755)

    print(f"Running installation in fake home: {fake_home}")
    result = subprocess.run([str(install_script)], env=env, capture_output=True, text=True)

    assert result.returncode == 0, (
        f"Installation failed with exit code {result.returncode}\n"
        f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )

    stack_root = fake_home / ".local/share/megalonyx"
    bin_dir = fake_home / ".local/bin"

    assert stack_root.exists(), "STACK_ROOT was not created"
    assert (stack_root / "config").is_dir(), "config directory missing in STACK_ROOT"
    assert (stack_root / "data").is_dir(), "data directory missing in STACK_ROOT"

    # Verify bin wrappers are present and executable
    for bin_name in ["mega-memory", "mega-status", "mega-tasks", "mega-db"]:
        bin_path = bin_dir / bin_name
        assert bin_path.exists() or bin_path.is_symlink(), f"{bin_name} missing in BIN_DIR"
        assert os.access(bin_path, os.X_OK), f"{bin_name} is not executable"

    # Verify Python workspace is importable
    import_check = subprocess.run(
        [
            "uv",
            "run",
            "--project",
            str(repo_root),
            "python",
            "-c",
            "import agent_memory; import control_plane_daemon; import agent_infra; print('OK')",
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert import_check.returncode == 0, (
        f"Python workspace import check failed: {import_check.stderr}"
    )
    assert "OK" in import_check.stdout

    assert (stack_root / "config/qdrant_config.yaml").exists(), "qdrant_config.yaml not deployed"

    print("Installation verification successful!")


if __name__ == "__main__":
    pytest.main([__file__])
