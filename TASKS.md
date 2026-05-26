# TASKS.md — Megalonyx Work Board

Single source of truth for all planned and active work.
Read at session start. Commit every status change.

---

## Workflow

**Claim a task:**
1. Pick any row from Queue with no `Blocked By`
2. Move it to In Progress, set `Owner` to your agent ID
3. Run `todo_write` with the task subject to load your session tracker
4. `git commit -m "task(#N): start <subject>"`

**Complete a task:**
1. Move row to Done, record the commit hash
2. Remove it from In Progress
3. Re-evaluate Blocked — anything now unblocked moves to Queue
4. `git commit -m "task(#N): complete <subject>"`

**Add a task:**
1. Add a row to Queue with: ID, subject, description, blocked_by (or —)
2. `git commit -m "task(#N): add <subject>"`

**Guardrails:**
- One owner per task. Do not claim a task that already has an owner.
- Do not add task-level items to `ROADMAP.md` — that is strategy only.
- Do not recreate `todo.md` or `claude.todo.md`.
- Commit `TASKS.md` before ending any session where status changed.

---

## In Progress

| ID | Subject | Owner | Started |
| :--- | :--- | :--- | :--- |

---

## Queue

| ID | Subject | Description | Blocked By |
| :--- | :--- | :--- | :--- |
| #55 | Vite 6→8 + @vitejs/plugin-react 4→6 | Bump `vite` in `pnpm-workspace.yaml` overrides to 8.x. Bump `@vitejs/plugin-react` to 6.0.2 in root `package.json`. Run: `pnpm install` → `pnpm build` → `pnpm exec vitest run` → `pnpm check`. Then create fork branch `contribute/phase-55-vite-8`. | — |
| #62 | Runtime independence: installer overhaul | Replace symlinks with physical copies to `~/.local/share/megalonyx/`. Create venv at `$STACK_ROOT/py/venv` via `uv venv --clear`. Update all `mega-` wrappers. Unify all components on `megalonyx_memory.sock`. File: `scripts/megalonyx/install-megalonyx-stack.sh` | — |

---

## Blocked

| ID | Subject | Blocked By | Notes |
| :--- | :--- | :--- | :--- |
| #57 | Final dependency sweep + E2E verification | #55 | `pnpm outdated` (expect nothing). Verify: `node dist/cli.js --version` → 0.16.1, `pnpm exec vitest run`, `pnpm check`. |
| #63 | Memory MCP restoration | #62 | Deploy daemon to `$STACK_ROOT`; kill stale sockets; verify JSON-RPC handshake on `megalonyx_memory.sock`. |
| #64 | Status tool hardening | #62 | Replace PID checks with socket pings in `mega-status` and `mega-memory-manager`. |
| #65 | Final isolation validation | #63, #64 | Path audit + unmount test — zero monorepo deps at runtime. |
| #61 | tailwindcss 3→4 | — | **Needs user decision.** High risk: v4 changed to CSS-based config. Do not start without explicit approval. |

---

## Done (recent)

| ID | Subject | Commit |
| :--- | :--- | :--- |
| #69 | Runtime Pathing Standards | — |
| #68 | Onboarding Narrative | — |
| #67 | Interface Specification | — |
| #66 | Architecture Visuals | — |
| #54 | ESLint 9→10 + react-hooks v7 + @eslint/compat | cc8d5b575 |
| #56 | esbuild — already at latest (0.28.0) | — |
| #33 | Fork contribution branches (H, I, M, 54) | — |
| #59 | QwenLM sync 12 commits | LKG-20260526-0324 |
| #60 | Clear GitHub CI notifications | — |
| #46 | TypeScript 5.3→6.0 | aa5e3e198 |
| #45 | web-tree-sitter 0.24→0.26 | 17e33c7fe |
| #44 | vitest 3→4, vite 5→6 | 7bed05ed9 |
