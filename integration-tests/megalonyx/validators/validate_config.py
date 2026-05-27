import os
import sys


def verify_machine_config() -> None:
    """
    Verifies that the operational Machine directory contains all required
    configuration files.
    """
    print(" Verifying Machine Configuration...")

    required_files = {
        "settings": os.path.expanduser("~/.qwen/settings.json"),
        "env": os.path.expanduser("~/.qwen/.env"),
        "instructional_memory": os.path.expanduser("~/.qwen/QWEN.md"),
    }

    missing = []
    for name, path in required_files.items():
        if not os.path.exists(path):
            print(f" MISSING: {name} at {path}")
            missing.append(path)
        else:
            print(f" FOUND: {name}")

    if missing:
        print("\\nERROR: Machine configuration is incomplete.")
        print("Please run 'install.sh' to deploy default configurations.")
        sys.exit(1)

    print("\\n Machine configuration is valid.")


if __name__ == "__main__":
    verify_machine_config()
