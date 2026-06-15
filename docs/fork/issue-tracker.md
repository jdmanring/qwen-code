# Issue Tracker

All issues for this fork are on GitHub.

---

## Workflow

**Issue first, branch second.** Every piece of work starts with a GitHub Issue.

1. Create issue.
2. Determine branch origin:
   - upstream-candidate → branch from `upstream-mirror`
   - fork-only → branch from `develop`
3. Do the work; commit cleanly.
4. Merge/cherry-pick to `develop`.
5. If upstream-candidate: update `docs/fork/upstream/pr-status.md`.

---

## Current Open Issues

| #                                                       | Title                              | Label              | Branch                         | Upstream Ref  |
| ------------------------------------------------------- | ---------------------------------- | ------------------ | ------------------------------ | ------------- |
| [#1](https://github.com/jdmanring/qwen-code/issues/1)   | Audit existing contributions       | upstream-candidate | `TBD`                          | N/A           |
| [#2](https://github.com/jdmanring/qwen-code/issues/2)   | Upgrade ESLint 9 → 10              | upstream-candidate | `feat/eslint-10`               | #4419         |
| [#3](https://github.com/jdmanring/qwen-code/issues/3)   | Trivial dependency bumps           | upstream-candidate | `chore/trivial-deps-bumps`     | General Maint |
| [#4](https://github.com/jdmanring/qwen-code/issues/4)   | OpenTelemetry integration          | upstream-candidate | `chore/opentelemetry-upgrade`  | #3731, #3917  |
| [#5](https://github.com/jdmanring/qwen-code/issues/5)   | iconv, comment, and chokidar fixes | upstream-candidate | `chore/util-deps-upgrade`      | General Maint |
| [#6](https://github.com/jdmanring/qwen-code/issues/6)   | Vitest and Vite upgrades           | upstream-candidate | `feat/vitest-vite-upgrade`     | #5027, #3226  |
| [#7](https://github.com/jdmanring/qwen-code/issues/7)   | Web Tree-Sitter integration        | upstream-candidate | `feat/web-tree-sitter-upgrade` | General Maint |
| [#8](https://github.com/jdmanring/qwen-code/issues/8)   | xterm.js 6 upgrade                 | upstream-candidate | `feat/xterm-headless-upgrade`  | General Maint |
| [#9](https://github.com/jdmanring/qwen-code/issues/9)   | Anthropic SDK upgrade              | upstream-candidate | `feat/anthropic-sdk-upgrade`   | General Maint |
| [#10](https://github.com/jdmanring/qwen-code/issues/10) | Google GenAI SDK upgrade           | upstream-candidate | `feat/google-genai-upgrade`    | General Maint |
| [#11](https://github.com/jdmanring/qwen-code/issues/11) | TypeScript 6.0.3 upgrade           | upstream-candidate | `feat/typescript-6-upgrade`    | #5027, #3225  |
| [#12](https://github.com/jdmanring/qwen-code/issues/12) | ACP SDK integration                | upstream-candidate | `chore/acp-sdk-upgrade`        | #4227, #4782  |
| [#13](https://github.com/jdmanring/qwen-code/issues/13) | Marked library upgrade             | upstream-candidate | `chore/marked-deps-upgrade`    | General Maint |
| [#14](https://github.com/jdmanring/qwen-code/issues/14) | OpenAI and yargs upgrades          | upstream-candidate | `chore/openai-yargs-upgrade`   | General Maint |
| [#15](https://github.com/jdmanring/qwen-code/issues/15) | Safe library upgrade               | upstream-candidate | `chore/safe-tier2-bumps`       | General Maint |
| [#16](https://github.com/jdmanring/qwen-code/issues/16) | Undici and glob upgrades           | upstream-candidate | `chore/undici-glob-upgrade`    | General Maint |
| [#TBD](https://github.com/jdmanring/qwen-code/issues/)  | pnpm Migration                     | upstream-candidate | `feat/migrate-to-pnpm`         | #5027         |
