import os
import sys

from audit_type_hints import run_audit


def main() -> None:
    base_dir = "packages"
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} not found.")
        sys.exit(1)

    all_issues = []

    for root, dirs, files in os.walk(base_dir):
        # Filter out directories to skip
        # dirs[:] modifies the list in place, which affects os.walk
        dirs[:] = [d for d in dirs if d not in ("tests", "build", "scripts", "__pycache__")]

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                issues = run_audit(file_path)
                all_issues.extend(issues)

    if all_issues:
        print("\n".join(all_issues))
        sys.exit(1)
    else:
        print("No type hinting issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
