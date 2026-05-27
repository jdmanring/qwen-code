#  Standalone Failure Mode Analysis (SFMA)

This document serves as the institutional memory of technical failures encountered during the transition to the Standalone Integration Pipeline. Its purpose is to prevent the recurrence of "sloppiness-driven" regressions.

##  High-Severity Failure Modes

### 1. The LaTeX Leak (Rendering Violation)
- **Symptom**: Porting operational laws (`QWEN.md`) from the blueprint to the monorepo while retaining LaTeX symbols (e.g., `$\to$`).
- **Root Cause**: Assumption that existing files were already compliant.
- **Corrective Action**: **S-SCRUB Mandate**. Every file ported from an external source MUST undergo a regex-based rendering scrub for LaTeX before being committed to the Standalone root.

### 2. The TOML Corruption (Shell Misuse)
- **Symptom**: `pyproject.toml` files created with literal `\n` characters instead of actual newlines.
- **Root Cause**: Using `echo` in a shell command to create multiline files without proper escaping or heredocs.
- **Corrective Action**: **No-OneLiner Law**. Bulk file creation or modification MUST be performed via:
    - A dedicated Python script.
    - A proper Bash heredoc (`cat <<EOF`).
    - The `write_file` tool for single files.

### 3. The File-System Pollution (Broad-Find Disaster)
- **Symptom**: Thousands of redundant `pyproject.toml` files created in every subdirectory of `packages/`, including `node_modules` and `dist/`.
- **Root Cause**: Using `find . -exec` without strict path exclusions (`-not -path "*/node_modules/*"`).
- **Corrective Action**: **Sieve-First Protocol**. Any filesystem operation affecting multiple directories MUST:
    - Explicitly exclude `node_modules`, `.git`, and `dist`.
    - Be verified with a `dry-run` (listing files) before execution.

##  Updated Operational Guardrails
- [ ] **Dry-Run Requirement**: All `find` or `sed` operations affecting $>10$ files must be preceded by a `ls` or `grep` to verify the target list.
- [ ] **Standalone-Sieve**: Use a dedicated exclusion list for all codebase-wide audits.
- [ ] **Linter-First**: No "Standalone" claim is valid until `ruff check .` and `npm run check` return zero errors.
