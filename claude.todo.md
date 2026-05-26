# Claude Tracking — megalonyx-monorepo

_Separate from todo.md (Qwen upstream). This tracks Claude's work on monorepo maintenance._

Last updated: 2026-05-26

---

## Security constraints (always in effect)

- Never commit: `config/settings.json`, `config/megalonyx/secrets.json`, `config/config.yaml`
- Push to `origin` (jdmanring/megalonyx-monorepo) for dev work
- Push contribution branches to `upstream` (jdmanring/qwen-code fork)
- No PRs to QwenLM until user explicitly approves each one

---

## Current state summary

| Area | Status |
|---|---|
| CLI boot | ✅ `node dist/cli.js --version` → 0.16.1 |
| Phase H: vitest 3→4 + vite 5→6 | ✅ Committed, contributed to fork |
| Phase I: web-tree-sitter 0.24→0.26 | ✅ Committed, contributed to fork |
| Phase M: TypeScript 5.3→6.0 | ✅ Committed, contributed to fork |
| QwenLM sync (10 commits) | ✅ LKG-20260526-0117 — integration → develop |
| GitHub notifications | ✅ Cleared 2026-05-26 |
| Pipeline: package-lock.json auto-resolve | ✅ Fixed in upstream_ingest_pipeline.py |

---

## Upstream fork branches (reference only — PRs to QwenLM will NOT be opened)

| Branch | Description |
|---|---|
| `contribute/phase-h-vitest-vite` | vitest 3→4, vite 5→6 |
| `contribute/phase-i-web-tree-sitter` | web-tree-sitter 0.24→0.26 |
| `contribute/phase-m-typescript-6` | TypeScript 5.3→6.0 |

Policy: prepare contribution branches and push to fork, but never open PRs against QwenLM/qwen-code.

---

## Pending dependency upgrades

### Confirmed needed

| Task | Package | From | To | Risk |
|---|---|---|---|---|
| #54 | `eslint` | 9.39.4 | 10.4.0 | Low-Medium |
| #54 | `@eslint/js` | 9.x | 10.0.1 | Low-Medium |
| #54 | `eslint-plugin-react-hooks` | 5.2.0 | 7.1.1 | Low (Dependabot PR open) |
| #55 | `vite` | 6.x | 8.x | Medium |
| #55 | `@vitejs/plugin-react` | 4.7.0 | 6.0.2 | Medium (Dependabot PR open) |
| #56 | `esbuild` | ~0.25.x | latest | Low |

### Deferred (user decision needed)

| Package | From | To | Risk | Notes |
|---|---|---|---|---|
| `tailwindcss` | 3.4.19 | 4.3.0 | High | Config format changed in v4 (CSS vs JS); Dependabot PR open |

### Already absorbed via upstream merges

`@xterm/headless` 6, `chokidar` 5, `iconv-lite` 0.7, `comment-json` 5,
`@anthropic-ai/sdk` 0.98, `@google/genai` 2.6, `@opentelemetry/*` 0.218

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
- `integration-tests/concurrent-runner/runner.py` ruff fixes applied 2026-05-26 (unstaged)
