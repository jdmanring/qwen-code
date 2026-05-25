# Config-Doc Mirroring Standard

This document defines the structural requirement of the Qwen Code project: the 1:1 mirroring between the system's configuration and its documentation.

## 1. The Requirement
For every operational configuration file, script, or parameter defined in the `config/` directory, there must exist a corresponding documentation file in the `docs/` directory.

**Mirroring Equation**: `config/{path}/{file}.{ext}` $\leftrightarrow$ `docs/{path}/{file}.md`

## 2. Purpose of Mirroring
Mirroring is a technical requirement to ensure the system remains maintainable and transparent for both humans and AI agents.
- **Zero-Friction Retrieval**: Agents can find the purpose and schema (docs) immediately after finding the configuration value (config).
- **Verification**: The `symmetry-check.py` script provides a binary pass/fail for the system's documentation health.
- **Project Alignment**: Ensures that no "hidden" configurations exist that aren't governed by the core operational rules in `QWEN.md`.

## 3. Enforcement Mechanism
The system utilizes a structural linter to enforce this standard:
- **Tool**: `scripts/symmetry-check.py`
- **Action**: The script recursively scans `config/` and verifies the existence of the mirrored `.md` file in `docs/`.
- **Requirement**: A failing symmetry check is considered "Documentation Debt" and must be resolved before any major version release.

## 4. Mirror Link
This standard is enforced by the following implementation:
`scripts/symmetry-check.py` $\leftrightarrow$ `symmetry.md`
