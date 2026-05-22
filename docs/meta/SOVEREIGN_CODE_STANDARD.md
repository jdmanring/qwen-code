# 📜 Sovereign Code Standard

This document defines the mandatory requirements for any code entering the `megacode-sovereign-stack`. Non-compliant code will be rejected during the migration/integration process.

## 1. Technical Requirements
- **Type Safety**: 
    - Python: All public functions MUST have full type hints (PEP 484).
    - TypeScript: `noImplicitAny` must be true; `any` is forbidden except in documented edge cases.
- **Determinism**: 
    - No "magic strings" or hardcoded paths. All paths must be resolved relative to the workspace root.
    - All external API calls must be wrapped in a standard `Result` or `Either` pattern for error handling.
- **Formatting**: 
    - Must pass `ruff check` (Python) and `eslint` (TS).
    - Max line length: 80 characters.

## 2. Cognitive Requirements
- **Naming**: 
    - Python: `snake_case` for files and functions.
    - JS/TS: `camelCase` for functions, `PascalCase` for classes/components.
    - Docs/Config: `kebab-case` for all files.
- **Anchoring**: 
    - Every directory containing logic MUST have a `.qwen-context` file explaining its purpose, local laws, and dependencies.
- **Symmetry**: 
    - Any change to a configuration file in `config/` must be mirrored by a corresponding update in `docs/`.

## 3. The Migration Filter
During the Great Migration, code will be processed as follows:
`Legacy Code` $\to$ `Linter Check` $\to$ `Sovereign Refactor` $\to$ `Symmetry Update` $\to$ `Sovereign Commit`

