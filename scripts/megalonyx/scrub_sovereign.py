import os
import re

# Path to the root of the monorepo
ROOT = "/home/james/projects/megalonyx-monorepo"

# Replacement Mapping
REPLACEMENTS = [
    (r"(?i)Sovereign Stack", "Standalone Stack"),
    (r"(?i)Sovereign Infrastructure", "Standalone Infrastructure"),
    (r"(?i)Sovereign Bridge", "Standalone Bridge"),
    (r"(?i)Sovereign Foundation", "Standalone Foundation"),
    (r"(?i)Sovereign Monorepo", "Independent Monorepo"),
    (r"(?i)Sovereign Development", "Independent Development"),
    (r"(?i)Sovereign Flow", "Independent Flow"),
    (r"(?i)Sovereign Law", "Project Standard"),
    (r"(?i)Sovereign Mandate", "Project Mandate"),
    (r"(?i)Sovereign Alignment", "Project Standard Alignment"),
    (r"(?i)Sovereign Failure Mode Analysis", "Standalone Failure Mode Analysis"),
    (r"(?i)Sovereign assets", "Standalone assets"),
    (r"(?i)Sovereign", "Standalone"),
]

FILES_TO_PROCESS = [
    "docs/megalonyx/architecture/layer-manifest.md",
    "docs/megalonyx/architecture/hybrid-stack.md",
    "docs/megalonyx/architecture/dependency-graph.md",
    "docs/megalonyx/architecture/component-map.md",
    "docs/megalonyx/architecture/agent-registry.md",
    "docs/megalonyx/architecture/agent-orchestration.md",
    "docs/megalonyx/architecture/mcp-bridge/transport-spec.md",
    "docs/megalonyx/architecture/mcp-bridge/security-audit.md",
    "docs/megalonyx/architecture/interaction-plane.md",
    "docs/megalonyx/architecture/integration-blueprint.md",
    "docs/megalonyx/process/integration_roadmap.md",
]


def scrub_file(file_path: str) -> None:
    full_path = os.path.join(ROOT, file_path)
    if not os.path.exists(full_path):
        print(f"File not found: {file_path}")
        return

    with open(full_path, encoding="utf-8") as f:
        content = f.read()

    original_content = content
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Scrubbed: {file_path}")
    else:
        print(f"No changes: {file_path}")


if __name__ == "__main__":
    for file in FILES_TO_PROCESS:
        scrub_file(file)
