# TASKS.md -- Megalonyx Work Board

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
3. Re-evaluate Blocked -- anything now unblocked moves to Queue
4. `git commit -m "task(#N): complete <subject>"`

**Add a task:**
1. Add a row to Queue with: ID, subject, description, blocked_by (or --)
2. `git commit -m "task(#N): add <subject>"`

**Guardrails:**
- One owner per task. Do not claim a task that already has an owner.
- Do not add task-level items to `ROADMAP.md` -- that is strategy only.
- Do not recreate `todo.md` or `claude.todo.md`.
- Commit `TASKS.md` before ending any session where status changed.

---

## In Progress

| ID | Subject | Owner | Started |
| :--- | :--- | :--- | :--- |
| #81 | INFRA: Implement `.qwen-context` anchors | Qwen-Orchestrator | 2026-05-27 |

---

## Queue

| ID | Subject | Description | Blocked By |
| :--- | :--- | :--- | :--- |
| #55 | Vite 6->8 + @vitejs/plugin-react 4->6 | Bump `vite` in `pnpm-workspace.yaml` overrides to 8.x. Bump `@vitejs/plugin-react` to 6.0.2 in root `package.json`. Run: `pnpm install` -> `pnpm build` -> `pnpm exec vitest run` -> `pnpm check`. Then create fork branch `contribute/phase-55-vite-8`. | -- |
| #70 | TypeScript gate in ingest pipeline | Add a 4th gate to `GateKeeper` in `tooling/sync-upstreams/upstream_ingest_pipeline.py`. After the symmetry gate (gate 3/3), add gate 4/4: run `pnpm install --frozen-lockfile && pnpm build && pnpm run test-all` via `subprocess.run` from `REPO_ROOT`. If it fails, abort and clean the staging branch. Name it `_gate_typescript`. Update the docstring in `UpstreamIngestPipeline` to show 4 gates. Also add a test in `gate_failure_tests.py`. | -- |
| #71 | TypeScript CI on develop + integration branches | Edit `.github/workflows/ci.yml`. Under `on.push.branches` and `on.pull_request.branches`, add `'develop'` and `'integration'` alongside `'main'` and `'release/**'`. This closes the gap where TS failures on develop are invisible to CI. Verify by checking the workflow triggers after commit. | -- |
| #72 | Scheduled upstream watch workflow | Create `.github/workflows/upstream-watch.yml`. Cron: `'0 6 * * *'` (daily 06:00 UTC). Steps: checkout monorepo, install Python (uv), run `python3 tooling/sync-upstreams/fork_sync_pipeline.py --status`. If new commits detected, run `fork_sync_pipeline.py --sync --auto` (add `--auto` flag to skip interactive prompt in non-TTY). Then run `upstream_ingest_pipeline.py`. On failure, open a GitHub issue via `gh issue create` with the error output. This fully automates the QwenLM->fork->integration path. | -- |
| #73 | LKG rollback script | Create `tooling/sync-upstreams/rollback_to_lkg.py`. Args: optional `--tag LKG-YYYYMMDD-HHMM` (defaults to most recent LKG tag). Steps: find tag via `git tag -l 'LKG-*' --sort=-version:refname | head -1`, confirm with user, `git checkout integration`, `git reset --hard <tag>`, `git push --force-with-lease origin integration`. Add rollback instructions to `docs/meta/pipeline-runbook.md`. | -- |
| #74 | Automate integration->develop promotion | After successful LKG tag in `PromotionEngine.promote()`, automatically fast-forward merge `integration` into `develop` if CI is green, or create a PR if not. Simplest version: after tagging, run `git checkout develop && git merge --ff-only integration && git push origin develop && git checkout integration`. Add `--no-auto-promote` flag to skip for manual control. | -- |
| #80 | S-REC: Fix MCP Stdio Race Condition | Root Cause: Aggressive `anyio` task group cancellation on `stdin` EOF. Path: Documentation $\to$ Analysis $\to$ Fix $\to$ Certification. | -- |
| #82 | INFRA: Expand Operational Linter | Add `OPERATIONAL` domain to `tooling/project_standards_linter.py` to audit process markers (e.g., `TASKS.md` updates, commit message links). | #80 |
| #83 | INFRA: Optimize `QWEN.md` for Fast-Activation | Add a high-density " Agent Quick-Start" cheat sheet to the top of `QWEN.md` for immediate constraint activation. | #80 |

---

## Blocked

| ID | Subject | Blocked By | Notes |
| :--- | :--- | :--- | :--- |
| #57 | Final dependency sweep + E2E verification | #55 | `pnpm outdated` (expect nothing). Verify: `node dist/cli.js --version` -> 0.16.1, `pnpm exec vitest run`, `pnpm check`. |
| #61 | tailwindcss 3->4 | -- | **Needs user decision.** High risk: v4 changed to CSS-based config. Do not start without explicit approval. |

---

## Done (recent)

| ID | Subject | Commit |
| :--- | :--- | :--- |
| #80 | S-REC: Fix MCP Stdio Race Condition | 3f3b83d36 |
| #65 | Final isolation validation | 3dae91c77 |
| #64 | Status tool hardening | 3dae91c77 |
| #63 | Memory MCP restoration | 3dae91c77 |
| #62 | Runtime independence: installer overhaul | 3dae91c77 |
| #69 | Runtime Pathing Standards | -- |
| #68 | Onboarding Narrative | -- |
| #67 | Interface Specification | -- |
| #66 | Architecture Visuals | -- |
| #54 | ESLint 9->10 + react-hooks v7 + @eslint/compat | cc8d5b575 |
| #56 | esbuild -- already at latest (0.28.0) | -- |
| #33 | Fork contribution branches (H, I, M, 54) | -- |
| #59 | QwenLM sync 12 commits | LKG-20260526-0324 |
| #60 | Clear GitHub CI notifications | -- |
| #46 | TypeScript 5.3->6.0 | aa5e3e198 |
| #45 | web-tree-sitter 0.24->0.26 | 17e33c7fe |
| #44 | vitest 3->4, vite 5->6 | 7bed05ed9 |
