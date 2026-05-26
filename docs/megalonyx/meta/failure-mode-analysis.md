# ⚠️ System Failure Analysis (SFMA)

This document mirrors the SFMA in the Independent Monorepo. It documents critical failures encountered during the realignment of the blueprint to prevent the same mistakes during future iterations.

## 🛑 High-Severity Failure Modes

### 1. The LaTeX Leak (Rendering Violation)
- **Symptom**: Porting operational laws (`QWEN.md`) while retaining LaTeX symbols.
- **Root Cause**: Failure to scrub ported content.
- **Corrective Action**: All ported content must be scrubbed for LaTeX symbols before integration.

### 2. The TOML Corruption (Shell Misuse)
- **Symptom**: Configuration files corrupted by literal newline characters (`\n`).
- **Root Cause**: Using `echo` for multiline file creation.
- **Corrective Action**: Use dedicated scripts or heredocs for multiline content.

### 3. The File-System Pollution (Broad-Find Disaster)
- **Symptom**: Mass creation of redundant files in `node_modules` and `dist`.
- **Root Cause**: Lack of path exclusions in `find` commands.
- **Corrective Action**: Always exclude `node_modules` and `dist` from global filesystem operations.

## 🛠️ Updated Operational Guardrails
- **Dry-Run Requirement**: Verify target file lists before executing bulk changes.
- **Linter-First**: Zero-error baseline is the only acceptable state for "Runtime" assets.
