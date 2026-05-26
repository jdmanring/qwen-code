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

- **What this means in practice**: prefer `gate_failure_tests.py` over `chaos_tests.py`, `intake_normalization` over `standalone_scrub`, `upstream_sync_pipeline` over `orchestrator`. An AI reading the name alone should predict the contents or behavior correctly at least 95% of the time.
- **Case conventions**
    - Python files: `snake_case.py` — never `kebab-case.py`.
    - Python classes: `PascalCase`. Shell scripts: `kebab-case.sh`. Bin/CLI entrypoints: `kebab-case` (no extension).
    - JS/TS: `camelCase` for functions, `PascalCase` for classes/components.
    - Docs/Config files: `kebab-case`.
- **File-class alignment**: A Python file containing exactly one public class must use the `snake_case` form of that class name (e.g., `SystemLogger` => `system_logger.py`).
- **No version suffixes in file names**: `v2`, `_new`, `_old` are prohibited. Use git history for versions.
- **Prohibited**: project-specific metaphors, dramatic labels, abbreviations without expansion, names that require context to interpret, `DEBUG` print statements in committed code.
- **Enforcement**: Ruff `N` rules catch mechanical casing violations. `project_standards_linter.py` (`CODE-04`, `CODE-05`) catches debug prints and file/class mismatches.

## 3. Structure Requirements

- **Context files**: Every directory containing logic must have a `.qwen-context` file explaining its purpose and dependencies.
- **Symmetry**: Any change to a configuration file in `config/` must be mirrored by a corresponding update in `docs/`.

## 4. Migration Filter

When importing code from an external source, it passes through intake normalization before being merged:

`External code` → `Lint check` → `Format check` → `Type check` → `Naming review` → `Symmetry update` → `Merge`

---

## 5. TypeScript Lint Toolchain

### Current versions (as of 2026-05-26)

| Package | Version | Role |
|---|---|---|
| `eslint` | ^10.4.0 | Core linter |
| `@eslint/js` | ^10.0.1 | ESLint recommended config |
| `typescript-eslint` | ^8.x | TypeScript-aware rules |
| `eslint-plugin-react` | ^7.x | JSX/React rules |
| `eslint-plugin-react-hooks` | ^7.1.1 | Hooks rules |
| `eslint-plugin-import` | ^2.x | Import resolution rules |
| `@eslint/compat` | ^2.1.0 | Legacy plugin bridge (required) |
| `jiti` | ^2.4.2 | ESLint 10 peer dep for config loading |

**Run lint:** `pnpm -w run check`

### ESLint 10 compatibility bridge

ESLint 10 removed several deprecated context methods (`context.getFilename()`,
`context.parserOptions`). Two plugins still rely on those APIs:

- `eslint-plugin-react` — uses `context.getFilename()` (upstream ESLint 10 PR #3979 in progress)
- `eslint-plugin-import` — uses `context.parserOptions.sourceType` (upstream ESLint 10 PR #3230 in progress)

**Do not remove the compat wrappers** until both PRs are merged and new plugin versions are
released. The bridge is applied in `eslint.config.js`:

```js
import { fixupConfigRules, fixupPluginRules } from '@eslint/compat';

const fixedImportPlugin = fixupPluginRules(importPlugin);
// ...
...fixupConfigRules(reactPlugin.configs.flat.recommended),
...fixupConfigRules(reactPlugin.configs.flat['jsx-runtime']),
// import plugin used as: plugins: { import: fixedImportPlugin }
```

When the upstream PRs land, remove the `fixup*` wrappers and the `@eslint/compat` import,
then run `pnpm -w run check` to confirm no regressions.

### Downgraded rules (warn, not error)

The following rules are intentionally set to `'warn'` until dedicated code passes address them.
Do not promote them to `'error'` without first cleaning up the violations.

**react-hooks v7 new rules** — added at `'error'` in v7 but require upstream code changes:

| Rule | Why warn |
|---|---|
| `react-hooks/static-components` | Needs component structure changes |
| `react-hooks/use-memo` | Needs memoization audit |
| `react-hooks/void-use-memo` | Needs memoization audit |
| `react-hooks/preserve-manual-memoization` | Needs memoization audit |
| `react-hooks/immutability` | Needs immutability pass |
| `react-hooks/globals` | Needs globals audit |
| `react-hooks/refs` | Needs refs audit |
| `react-hooks/set-state-in-effect` | Needs effect cleanup pass |
| `react-hooks/error-boundaries` | Needs error boundary audit |
| `react-hooks/purity` | Needs purity pass |
| `react-hooks/set-state-in-render` | Needs render-time setState audit |
| `react-hooks/config` | Needs config pass |
| `react-hooks/gating` | Needs gating pass |

**ESLint 10 new core rules** — added to `eslint:recommended` in v10:

| Rule | What it catches | Why warn |
|---|---|---|
| `preserve-caught-error` | Re-throws missing `{ cause: e }` | Upstream catch blocks need updates |
| `no-useless-assignment` | Assignments whose value is never read | Upstream dead assignment cleanup needed |

### react-hooks v7 flat config entry point

The v7 plugin changed the flat-config entry point. Use `configs.flat['recommended-latest']`,
not `configs['recommended-latest']`:

```js
// Correct (v7+):
reactHooks.configs.flat['recommended-latest']

// Wrong — throws "plugins must be object format" in ESLint 10:
reactHooks.configs['recommended-latest']
```
