# Claude Tracking — megalonyx-monorepo

_Separate from todo.md (Qwen upstream). This tracks Claude's work on monorepo maintenance._

Last updated: 2026-05-26 (Phase 54 contributed to fork; QwenLM commit 641a1a73 synced, LKG-20260526-0324)

---

## Security constraints (always in effect)

- Never commit: `config/settings.json`, `config/megalonyx/secrets.json`, `config/config.yaml`
- Push to `origin` (jdmanring/megalonyx-monorepo) for dev work
- Push contribution branches to `upstream` (jdmanring/qwen-code fork)
- No PRs to QwenLM — ever (permanent policy)

---

## Current state summary

| Area | Status |
|---|---|
| CLI boot | ✅ `node dist/cli.js --version` → 0.16.1 |
| Phase H: vitest 3→4 + vite 5→6 | ✅ Committed, contributed to fork |
| Phase I: web-tree-sitter 0.24→0.26 | ✅ Committed, contributed to fork |
| Phase M: TypeScript 5.3→6.0 | ✅ Committed, contributed to fork |
| Phase 54: ESLint 9→10 | ✅ Committed cc8d5b575; contributed to fork (`contribute/phase-54-eslint-10`) |
| QwenLM sync (12 commits) | ✅ LKG-20260526-0324 — integration → develop |
| GitHub notifications | ✅ Cleared 2026-05-26 |
| Pipeline: package-lock.json auto-resolve | ✅ Fixed in upstream_ingest_pipeline.py |
| Pre-commit hook: branch safety | ✅ Hook gracefully skips standards linter on contribution branches |

---

## Upstream fork branches (reference only — PRs to QwenLM will NOT be opened)

| Branch | Description |
|---|---|
| `contribute/phase-h-vitest-vite` | vitest 3→4, vite 5→6 |
| `contribute/phase-i-web-tree-sitter` | web-tree-sitter 0.24→0.26 |
| `contribute/phase-m-typescript-6` | TypeScript 5.3→6.0 |
| `contribute/phase-54-eslint-10` | ESLint 9→10, react-hooks v5→v7, @eslint/compat bridge |

Policy: prepare contribution branches and push to fork, but never open PRs against QwenLM/qwen-code.

---

## Pending dependency upgrades

### Confirmed needed

| Task | Package | From | To | Risk |
|---|---|---|---|---|
| #55 | `vite` | 6.x | 8.x | Medium |
| #55 | `@vitejs/plugin-react` | 4.7.0 | 6.0.2 | Medium (Dependabot PR open) |

### Deferred (user decision needed)

| Package | From | To | Risk | Notes |
|---|---|---|---|---|
| `tailwindcss` | 3.4.19 | 4.3.0 | High | Config format changed in v4 (CSS vs JS); Dependabot PR open |

### Already done

| Package | Version | Notes |
|---|---|---|
| `eslint` | 10.4.0 | Phase 54 — cc8d5b575 |
| `@eslint/js` | 10.0.1 | Phase 54 |
| `eslint-plugin-react-hooks` | 7.1.1 | Phase 54 — compat bridge required |
| `@eslint/compat` | 2.1.0 | Phase 54 — NEW; wraps react + import plugins |
| `jiti` | 2.4.2 | Phase 54 — ESLint 10 peer dep |
| `esbuild` | 0.28.0 | Already at latest; task #56 closed |
| `@xterm/headless` | 6 | Absorbed via upstream |
| `chokidar` | 5 | Absorbed via upstream |
| `iconv-lite` | 0.7 | Absorbed via upstream |
| `comment-json` | 5 | Absorbed via upstream |
| `@anthropic-ai/sdk` | 0.98 | Absorbed via upstream |
| `@google/genai` | 2.6 | Absorbed via upstream |
| `@opentelemetry/*` | 0.218 | Absorbed via upstream |

### ESLint 10 maintenance note

`eslint-plugin-react` and `eslint-plugin-import` are wrapped with `@eslint/compat`
`fixupConfigRules`/`fixupPluginRules` because they use context APIs removed in ESLint 10.
Upstream fixes are in progress:
- eslint-plugin-react PR #3979
- eslint-plugin-import PR #3230

When both land and new versions are published: remove the compat wrappers and `@eslint/compat`.
Until then, **do not remove the fixup* wrappers** — lint will error out.

13 react-hooks v7 rules and 2 ESLint 10 core rules are downgraded to `'warn'` in `eslint.config.js`.
These are tracked — see `docs/meta/engineering-standards.md` Section 5 for the full list.

---

## Ingest pipeline notes

- Script: `tooling/sync-upstreams/upstream_ingest_pipeline.py`
- Run from `integration` branch
- `package-lock.json` conflicts auto-resolved (keep ours — we use pnpm)
- `git merge --continue` uses `core.editor=true` to suppress editor prompt
- `PROTECTED_FILES` restored after each upstream merge to prevent silent overwrite
- Fork sync script: `tooling/sync-upstreams/fork_sync_pipeline.py --sync`
- Contribution script: `tooling/sync-upstreams/fork_sync_pipeline.py --contribute <hash> <name>`

---

## Known issues (not blocking)

- `vscode-ide-companion` has 20+ TypeScript errors (phantom deps + upstream API changes)
  — does NOT block `pnpm build`; tracked in todo.md Phase 4.8
- `test_socket_resp.py` at repo root is an ad-hoc debug script (untracked, not committed)
- `integration-tests/concurrent-runner/runner.py` ruff fixes committed to fork contribute branch 2026-05-26
- E2E Tests CI failures on `jdmanring/qwen-code` fork are persistent infrastructure issue (missing OPENAI_API_KEY secret on fork runners). Same commit passes on QwenLM. Not fixable without adding fork secrets.
