#!/bin/bash

# ==============================================================================
# CSF-INGEST-REPO: Automated Scaffolding for Cognitive-Symmetry Ingestion
# ==============================================================================
# Purpose: Automates the physical setup of an ingested repository and its 
#          corresponding mirrored documentation in the Blueprint.
# ==============================================================================

set -e

# --- Configuration ---
PROJECT_ROOT="/home/james/Projects/qwen_code_stack"
LABS_DIR="$PROJECT_ROOT/labs"
DOCS_INGEST_DIR="$PROJECT_ROOT/docs/ingested"

# --- Helper: Usage ---
usage() {
    echo "Usage: $0 -r <repo_url> -n <repo_name> -c <category>"
    echo ""
    echo "Options:"
    echo "  -r    URL of the repository to ingest"
    echo "  -n    Name of the repository (used for folder names)"
    echo "  -c    Category (targets | inspiration | ecosystem)"
    echo "  -h    Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 -r https://github.com/example/repo -n example-repo -c targets"
    exit 1
}

# --- Argument Parsing ---
while getopts "r:n:c:h" opt; do
    case "$opt" in
        r) REPO_URL=$OPTARG ;;
        n) REPO_NAME=$OPTARG ;;
        c) CATEGORY=$OPTARG ;;
        h) usage ;;
        *) usage ;;
    esac
done

if [[ -z "$REPO_URL" || -z "$REPO_NAME" || -z "$CATEGORY" ]]; then
    usage
fi

# --- Validation ---
if [[ ! "$CATEGORY" =~ ^(targets|inspiration|ecosystem)$ ]]; then
    echo "Error: Invalid category. Must be one of: targets, inspiration, ecosystem"
    exit 1
fi

# --- Execution ---

echo "🚀 Starting CSF-Ingestion for: $REPO_NAME"

# 1. Create Lab Directory
TARGET_LAB_PATH="$LABS_DIR/$CATEGORY/$REPO_NAME"
echo "📂 Cloning into: $TARGET_LAB_PATH"
mkdir -p "$LABS_DIR/$CATEGORY"
if [ -d "$TARGET_LAB_PATH" ]; then
    echo "⚠️  Directory already exists. Skipping clone."
else
    git clone "$REPO_URL" "$TARGET_LAB_PATH"
fi

# 2. Create Mirrored Documentation Scaffolding
echo "📚 Creating mirrored documentation structure in $DOCS_INGEST_DIR/$REPO_NAME"
MIRROR_PATH="$DOCS_INGEST_DIR/$REPO_NAME"
mkdir -p "$MIRROR_PATH"

# Create basic structural mirrors (Symmetry placeholders)
# These will be filled by the ingestion-specialist agent
mkdir -p "$MIRROR_PATH/agents"
mkdir -p "$MIRROR_PATH/skills"
mkdir -p "$MIRROR_PATH/architecture"
mkdir -p "$MIRROR_PATH/reference"

# Create the root index for the ingested repo
cat <<EOF > "$MIRROR_PATH/INDEX.md"
# 📦 Ingested Asset: $REPO_NAME
Source: $REPO_URL
Category: $CATEGORY
Symmetry Status: PENDING

## 🗺️ Cognitive Map
- [Agents](./agents/)
- [Skills](./skills/)
- [Architecture](./architecture/)
- [Reference](./reference/)

## 📜 Integration Status
- [ ] Phase 1: Physical Ingestion (COMPLETE)
- [ ] Phase 2: Cognitive Mapping (PENDING)
- [ ] Phase 3: Axiomatic Distillation (PENDING)
- [ ] Phase 4: Verification (PENDING)
EOF

echo "✅ Scaffolding complete."
echo "Next Step: Invoke 'ingestion-specialist' to perform Cognitive Mapping."
