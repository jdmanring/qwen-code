import glob
import os
import re

# Path to the root of the monorepo
ROOT = "/home/james/projects/megalonyx-monorepo"

# Replacement Mapping - Prioritize longer phrases first
REPLACEMENTS = [
    (r"(?i)Sovereign Failure Mode Analysis", "System Failure Analysis"),
    (r"(?i)Sovereign Monorepo", "Independent Monorepo"),
    (r"(?i)Sovereign Development", "Independent Development"),
    (r"(?i)Sovereign Flow", "Independent Flow"),
    (r"(?i)Sovereign Law", "Project Standard"),
    (r"(?i)Sovereign Mandate", "Project Mandate"),
    (r"(?i)Sovereign Alignment", "Project Standard Alignment"),
    (r"(?i)Sovereign Stack", "Runtime Stack"),
    (r"(?i)Sovereign Infrastructure", "Runtime Infrastructure"),
    (r"(?i)Sovereign Bridge", "UDS Bridge"),
    (r"(?i)Sovereign Foundation", "Base Infrastructure"),
    (r"(?i)Sovereign assets", "Runtime assets"),
    (r"(?i)Sovereign", "Standalone"),  # Fallback for remaining occurrences
]


def scrub_file(file_path: str) -> bool:
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        for pattern, replacement in REPLACEMENTS:
            content = re.sub(pattern, replacement, content)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
    except OSError as e:
        print(f"Error processing {file_path}: {e}")
    return False


def main() -> None:
    # Files to process: .md files in docs, .sh files in scripts, .py files in packages/apps
    patterns = [
        "docs/**/*.md",
        "scripts/**/*.sh",
        "packages/**/*.py",
        "apps/**/*.py",
    ]

    files_changed = 0
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(ROOT, pattern), recursive=True):
            if scrub_file(file_path):
                files_changed += 1

    print(f"Successfully scrubbed {files_changed} files.")


if __name__ == "__main__":
    main()
