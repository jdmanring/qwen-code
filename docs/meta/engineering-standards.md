# Engineering Standards

This document defines the mandatory requirements for any code entering the monorepo. Non-compliant code is rejected during intake normalization and migration.

## 1. Technical Requirements

- **Type Safety**
    - Python: All public functions must have full type hints (PEP 484).
    - TypeScript: `noImplicitAny` must be true; `any` is forbidden except in documented edge cases.
- **Determinism**
    - No magic strings or hardcoded paths. All paths must be resolved relative to the workspace root.
    - All external API calls must be wrapped in a standard `Result` or `Either` pattern for error handling.
- **Formatting**
    - Python: must pass `uv run ruff check` and `uv run ruff format`.
    - TypeScript: must pass `eslint`.
    - Max line length: 80 characters.

## 2. Naming Requirements

Names must be immediately descriptive. An AI or engineer reading a name should be able to predict what it contains or does without opening it.

- **What this means in practice**: prefer `gate_failure_tests.py` over `chaos_tests.py`, `intake_normalization` over `sovereign_scrub`, `upstream_sync_pipeline` over `orchestrator`.
- **Case conventions**
    - Python: `snake_case` for files and functions.
    - JS/TS: `camelCase` for functions, `PascalCase` for classes/components.
    - Docs/Config: `kebab-case` for all files.
- **Prohibited**: project-specific metaphors, dramatic labels, abbreviations without expansion, names that require context to interpret.

## 3. Structure Requirements

- **Context files**: Every directory containing logic must have a `.qwen-context` file explaining its purpose and dependencies.
- **Symmetry**: Any change to a configuration file in `config/` must be mirrored by a corresponding update in `docs/`.

## 4. Migration Filter

When importing code from an external source, it passes through intake normalization before being merged:

`External code` → `Lint check` → `Format check` → `Type check` → `Naming review` → `Symmetry update` → `Merge`
