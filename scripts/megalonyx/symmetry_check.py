import pathlib
import sys

# Colors for report
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def check_symmetry(root_dir: str) -> int:
    config_dir = pathlib.Path(root_dir) / "config"
    docs_dir = pathlib.Path(root_dir) / "docs"

    if not config_dir.exists() or not docs_dir.exists():
        print(f"{RED}Error: config/ or docs/ directory not found in {root_dir}{RESET}")
        sys.exit(1)

    gaps_found = False
    critical_gaps_found = False

    # 1. Folder and File Symmetry (Config -> Docs)
    # We use rglob("*") to get all files and directories recursively
    config_items = sorted(config_dir.rglob("*"))

    for item in config_items:
        relative_path = item.relative_to(config_dir)

        if item.is_dir():
            # Folder Symmetry
            mirror_folder = docs_dir / relative_path
            if not mirror_folder.exists():
                print(
                    f"{RED}[FOLDER GAP]{RESET} {relative_path} exists in config/ but not in docs/"
                )
                gaps_found = True
                critical_gaps_found = True

        elif item.is_file():
            # Skip .lock and .template files
            if item.suffix == ".lock" or item.suffix == ".template":
                continue

            # File Symmetry: config/path/file.ext -> docs/path/file.md
            mirror_file = docs_dir / relative_path.with_suffix(".md")
            if not mirror_file.exists():
                mirror_rel = mirror_file.relative_to(docs_dir)
                print(
                    f"{RED}[MISSING DOC]{RESET} {relative_path} has no corresponding"
                    f" mirror at {mirror_rel}"
                )
                gaps_found = True
                critical_gaps_found = True

    # 2. Reverse Symmetry (Docs -> Config)
    # Only check for files in docs/ that are within directories that also exist in config/
    docs_items = sorted(docs_dir.rglob("*"))

    for item in docs_items:
        if item.is_file() and item.suffix == ".md":
            relative_path = item.relative_to(docs_dir)
            parent_rel_path = relative_path.parent

            # Check if the parent folder exists in config/
            if (config_dir / parent_rel_path).exists():
                # Check if any file with the same base name exists in config/
                # (ignoring .lock/.template)
                # We look for any file that has the same stem in that directory
                config_parent = config_dir / parent_rel_path
                found_counterpart = False

                for config_file in config_parent.iterdir():
                    if config_file.is_file() and config_file.stem == item.stem:
                        if config_file.suffix not in [".lock", ".template"]:
                            found_counterpart = True
                            break

                if not found_counterpart:
                    print(
                        f"{YELLOW}[ORPHAN DOC]{RESET} {relative_path} in docs/"
                        " has no counterpart in config/"
                    )
                    gaps_found = True

    if not gaps_found:
        print(
            f"{GREEN}Cognitive-Symmetry Verified: config/ and docs/ are perfectly aligned.{RESET}"
        )
    else:
        print(f"\n{RED}Symmetry check failed. Gaps found.{RESET}")

    return 0 if not critical_gaps_found else 1


if __name__ == "__main__":
    # Use the current working directory as root or allow passing it as an argument
    root = sys.argv[1] if len(sys.argv) > 1 else pathlib.Path.cwd()
    sys.exit(check_symmetry(root))
