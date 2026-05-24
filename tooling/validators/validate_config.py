import os
import sys


def verify_machine_config() -> None:
    """
    Verifies that the required runtime configuration files are present.
    """
    print("Verifying machine configuration...")

    required_files = {
        "settings": os.path.expanduser("~/.qwen/settings.json"),
        "env": os.path.expanduser("~/.local/share/megalonyx/.env"),
    }

    # QWEN.md lives at the repo root, not deployed to ~/.qwen/
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    required_files["instructional_memory"] = os.path.join(repo_root, "QWEN.md")

    missing = []
    for name, path in required_files.items():
        if not os.path.exists(path):
            print(f"MISSING: {name} at {path}")
            missing.append(path)
        else:
            print(f"FOUND: {name}")

    if missing:
        print("\nERROR: Configuration is incomplete.")
        print("Run 'scripts/megalonyx/install-megalonyx-stack.sh' to deploy default configs.")
        sys.exit(1)

    print("\nMachine configuration is valid.")


if __name__ == "__main__":
    verify_machine_config()
