import os
import re


def check_prints(directory: str) -> None:
    print_pattern = re.compile(r"print\(")
    stderr_pattern = re.compile(r"file\s*=\s*sys\.stderr")

    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path) as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if print_pattern.search(line):
                            # Check if stderr is in the same line
                            if not stderr_pattern.search(line):
                                # It might be a multi-line print. Let's check the next few lines.
                                found_stderr = False
                                for j in range(i + 1, min(i + 5, len(lines))):
                                    if stderr_pattern.search(lines[j]):
                                        found_stderr = True
                                        break
                                if not found_stderr:
                                    print(f"{path}:{i + 1}: {line.strip()}")


if __name__ == "__main__":
    check_prints("services")
