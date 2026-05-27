import os
import sys

# Add project root to path for imports
project_root = os.path.expanduser("~/.local/share/megalonyx")
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "packages/core/src"))

from control_plane import ControlPlane  # noqa: E402
from task_registry import TaskRegistry  # noqa: E402


def test_no_roadmap_jitter() -> None:
    # Setup using Machine paths
    settings_file = os.path.join(project_root, "config/settings.json")
    # We use a temporary todo file for the test to avoid messing with the real one
    todo_file = os.path.join(project_root, "TEST_TODO.md")

    with open(todo_file, "w") as f:
        f.write("# Test Roadmap\n\n- [ ] Strategic Goal 1")

    # Instantiate ControlPlane
    cp = ControlPlane(settings_path=settings_file)
    # Force the registry to use our test file
    cp.task_registry = TaskRegistry(todo_file)

    print(f"Initial TODO.md content ({todo_file}):")
    with open(todo_file) as f:
        print(f.read())

    # Process an intent that would cause decomposition
    prompt = "Implement a new authentication system"
    cp.process_intent(prompt)

    print("\nTODO.md content after process_intent:")
    with open(todo_file) as f:
        content = f.read()
        print(content)

    if "Strategic Goal 1" in content and len(content.split("\n")) <= 3:
        print(
            "\n SUCCESS: No roadmap jitter detected. Only the strategic goal remains."
        )
    else:
        print(
            "\n FAILURE: Roadmap jitter detected. Atomic jobs were written to TODO.md."
        )
        exit(1)

    # Clean up
    if os.path.exists(todo_file):
        os.remove(todo_file)


if __name__ == "__main__":
    test_no_roadmap_jitter()
