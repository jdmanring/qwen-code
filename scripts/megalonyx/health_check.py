import json
import os
import socket
import sys


def check_memory_socket() -> tuple[bool, str]:
    socket_path = os.path.expanduser("~/.local/share/megalonyx/tmp/qwen_memory.sock")
    if not os.path.exists(socket_path):
        return False, f"Socket file not found at {socket_path}"

    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            s.connect(socket_path)
        return True, "Socket is active and accepting connections"
    except (OSError, ConnectionRefusedError) as e:
        return False, f"Socket connection failed: {e}"


def check_settings_json() -> tuple[bool, str]:
    settings_path = os.path.expanduser("~/.qwen/settings.json")
    if not os.path.exists(settings_path):
        return False, f"Settings file not found at {settings_path}"

    try:
        with open(settings_path) as f:
            json.load(f)
        return True, "Settings JSON is valid"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON syntax: {e}"
    except OSError as e:
        return False, f"Error reading settings file: {e}"


def main() -> None:
    results = []

    # Check Memory Socket
    socket_ok, socket_msg = check_memory_socket()
    results.append(
        {
            "component": "Memory Socket",
            "status": "PASS" if socket_ok else "FAIL",
            "details": socket_msg,
        }
    )

    # Check Settings JSON
    json_ok, json_msg = check_settings_json()
    results.append(
        {
            "component": "Settings JSON",
            "status": "PASS" if json_ok else "FAIL",
            "details": json_msg,
        }
    )

    # Output according to Skill Contract
    for res in results:
        print(f"COMPONENT: {res['component']}")
        print(f"STATUS: {res['status']}")
        print(f"DETAILS: {res['details']}")
        print("-" * 20)

    # Exit code based on overall health
    if any(res["status"] == "FAIL" for res in results):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
