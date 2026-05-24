🏛️ 
# ⚖️ The Symmetry Law

This document defines the structural mandate of the `qwen_code_stack`: the requirement for a 1:1 mirroring between the system's configuration (The Machine) and its documentation (The Blueprint).

## 1. The Mandate
For every operational configuration file, script, or parameter defined in the `config/` directory, there must exist a corresponding documentation file in the `docs/` directory.

**Symmetry Equation**: `config/{path}/{file}.{ext}` $\leftrightarrow$ `docs/{path}/{file}.md`

## 2. Purpose of Symmetry
Symmetry is not a bureaucratic requirement; it is a cognitive optimization for AI agents.
- **Zero-Friction Retrieval**: Agents can find the "Why" (docs) immediately after finding the "What" (config).
- **Verification**: The `symmetry-check.py` script provides a binary pass/fail for the system's documentation health.
- **Sovereign Alignment**: Ensures that no "hidden" configurations exist that aren't governed by the Sovereign Law in `QWEN.md`.

## 3. Enforcement Mechanism
The system utilizes a structural linter to enforce this law:
- **Tool**: `scripts/symmetry-check.py`
- **Action**: The script recursively scans `config/` and verifies the existence of the mirrored `.md` file in `docs/`.
- **Requirement**: A failing symmetry check is considered a "Documentation Debt" and must be resolved before any major version release.

## 4. Symmetry Link
This law is enforced by the following implementation:
`scripts/symmetry-check.py` $\leftrightarrow$ `symmetry.md`
