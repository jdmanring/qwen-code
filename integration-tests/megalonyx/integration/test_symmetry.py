import os
import subprocess
from pathlib import Path
import pytest


@pytest.mark.integration
def test_cognitive_symmetry() -> None:
    """
    Verifies the Cognitive Symmetry of the project by running the symmetry-check script.
    The test fails if the script returns a non-zero exit code, indicating a mismatch
    between config/ and docs/.
    """
    project_root = str(Path(__file__).resolve().parent.parent.parent.parent)
    script_path = os.path.join(project_root, "tooling/symmetry_check.py")

    # Run the symmetry check script
    # We pass the project root as an argument to the script
    result = subprocess.run(
        ["python3", script_path, project_root], capture_output=True, text=True
    )

    # Assert that the script exited successfully
    # If it failed, include the stdout and stderr in the error message
    assert result.returncode == 0, (
        f"Cognitive Symmetry check failed!\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )
