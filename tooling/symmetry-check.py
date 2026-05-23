#!/usr/bin/env python3
import sys
from pathlib import Path

def check_symmetry(config_dir: Path, docs_dir: Path):
    """
    Verify 1:1 symmetry between configuration files and documentation.
    Every file in .qwen/config/ must have a corresponding .md file in docs/.
    """
    print(f"Checking symmetry between {config_dir} and {docs_dir}...")
    
    if not config_dir.exists():
        print(f"Error: Config directory {config_dir} does not exist.")
        return False

    config_files = sorted([f for f in config_dir.rglob('*') if f.is_file()])
    missing_docs = []
    
    for config_file in config_files:
        # Get path relative to config_dir
        rel_path = config_file.relative_to(config_dir)
        
        # Construct expected doc path: replace .qwen/config/ with docs/ and add .md
        # Example: .qwen/config/meta/versions.lock -> docs/meta/versions.lock.md
        doc_path = docs_dir / rel_path.with_suffix(rel_path.suffix + '.md')
        
        if not doc_path.exists():
            missing_docs.append((config_file, doc_path))

    if missing_docs:
        print("\nSymmetry Violation: The following config files are missing documentation mirrors:")
        for config, doc in missing_docs:
            print(f"  - {config.relative_to(Path.cwd())}  -->  {doc.relative_to(Path.cwd())}")
        return False

    print("\nSymmetry Check Passed: All configurations are mirrored in documentation.")
    return True

if __name__ == "__main__":
    # Use absolute paths based on the monorepo root
    root = Path(__file__).parent.parent
    config_path = root / ".qwen" / "config"
    docs_path = root / "docs"
    
    if not check_symmetry(config_path, docs_path):
        sys.exit(1)
    sys.exit(0)
