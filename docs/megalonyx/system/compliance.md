#  Compliance & Quality Standards

This document describes the linting, formatting, and compliance systems currently enforced in the Runtime Stack.

##  Formatting & Linting

The project uses a strict set of tools to ensure code consistency across the monorepo.

### 1. TypeScript/JavaScript
- **ESLint**: Enforces code quality and prevents common bugs.
- **Prettier**: Ensures consistent formatting (indentation, quotes, semicolons).
- **Check**: Run via `npm run lint`.

### 2. Python
- **Ruff**: Used for both linting and formatting. It replaces Flake8 and Black for high-performance compliance.
- **Check**: Run via `ruff check .`.

---

## Engineering Standards

All code entering the monorepo must adhere to `docs/meta/engineering-standards.md`. Key requirements include:
- **Type Safety**: Mandatory type hints for Python and `noImplicitAny` for TypeScript.
- **Determinism**: No magic strings; all paths must be resolved relative to the workspace root.
- **Symmetry**: Configuration changes must be mirrored in the documentation.

##  Anchoring Requirement
Every directory containing logic MUST include a `.mega-context` file. This file provides the "Local Law" for the directory, including:
- The purpose of the directory.
- Local constraints.
- Dependencies on other modules.
- Primary entry points for new developers.

---

##  Compliance Workflow
1. **Local Check**: Developer runs `ruff check` or `eslint`.
2. **Pre-Commit**: (Optional) Git hooks prevent commits that fail linting.
3. **CI Verification**: The build pipeline runs all linting tools; failure blocks the merge.
