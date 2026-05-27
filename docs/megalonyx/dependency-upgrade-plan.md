# Dependency Upgrade Plan

**Created:** 2026-05-24  
**Scope:** All packages in the megalonyx-monorepo workspace  
**Baseline:** QwenLM/qwen-code v0.16.1 (upstream HEAD as of 2026-05-24)

All outdated dependencies identified below are upstream debt -- the upstream repo carries the same versions. We are not behind upstream; upstream is behind current ecosystem versions.

---

## Phase A -- Trivial housekeeping
**Risk: None** | Safe to batch into one commit.

| Package | From | To | Location |
|---|---|---|---|
| `nx` | 22.7.2 | 22.7.3 | `package.json` devDeps |
| `mime` | 4.0.7 | 4.1.0 | `packages/core/package.json` |
| `@lydell/node-pty*` | 1.2.0-beta.10 | 1.2.0-beta.12 | `packages/core/package.json` optionalDeps |
| `@teddyzhu/clipboard*` | 0.0.5 | 0.0.10 | `packages/cli/package.json` optionalDeps |
| `@types/archiver` | ^6.0.3 | ^7.0.0 | `packages/cli/package.json` devDeps |
| `@types/supertest` | ^6.0.3 | ^7.0.0 | `packages/cli/package.json` devDeps |
| `@types/react` | ^18.2.0 | ^19.0.0 | `packages/web-templates/package.json` devDeps |
| `@types/react-dom` | ^18.2.0 | ^19.0.0 | `packages/web-templates/package.json` devDeps |
| `@types/diff` | ^7.0.2 | **REMOVE** | cli + core devDeps -- diff 7.x ships own types |
| `@types/dotenv` | ^6.1.1 | **REMOVE** | cli + core devDeps -- dotenv 16.x ships own types |
| `@types/minimatch` | ^5.1.2 | **REMOVE** | core devDeps -- minimatch 9.x ships own types |
| `@types/tar` | ^6.1.13 | **REMOVE** | core devDeps -- tar 7.x ships own types |
| `semver` | ^7.0.0 (7.7.4 installed) | 7.8.1 | lockfile update via `pnpm update semver` |
| `yaml` | ^2.0.0 (2.8.0 installed) | 2.9.0 | lockfile update via `pnpm update yaml` |

**Verification:** `pnpm install && node dist/cli.js --version` returns `0.16.1`

---

## Phase B -- ESLint 9 + @typescript-eslint 8
**Risk: Low** | Flat config (`eslint.config.js`) already written. vscode-ide-companion already on ESLint 9.25.1 as proof of concept.

| Package | From | To | Location |
|---|---|---|---|
| `eslint` | 8.57.1 | ^9.0.0 | `package.json` devDeps |
| `@typescript-eslint/eslint-plugin` | 7.18.0 | ^8.0.0 | `package.json` devDeps |
| `@typescript-eslint/parser` | 7.18.0 | ^8.0.0 | `package.json` devDeps |
| Same for `packages/sdk-typescript/package.json` | 7.13.0 | ^8.0.0 | sdk-typescript devDeps |

**Key files:** `eslint.config.js` (root), `packages/sdk-typescript/.eslintrc*`  
**Process:** Bump -> `pnpm install` -> `pnpm check` -> fix new lint errors  
**Verification:** `pnpm check` exits 0

---

## Phase C -- OpenTelemetry suite
**Risk: Low-Medium** | All packages must move together for OTLP protocol compatibility.

All `@opentelemetry/*` packages in `packages/core/package.json`:
- OTLP exporters (grpc + http for traces, logs, metrics): `^0.203.0` -> `^0.218.0`
- `sdk-node`: `^0.203.0` -> `^0.218.0`
- `sdk-logs`: `^0.203.0` -> `^0.218.0`
- `instrumentation-http`: `^0.203.0` -> `^0.218.0`
- `api-logs`: `^0.203.0` -> `^0.218.0`
- `sdk-trace-node`: `^2.0.0` -> `^2.7.0`

**Critical test paths:** `packages/core/src/telemetry/sdk.ts` -- gRPC/HTTP export, log->span bridging, session context  
**Verification:** `pnpm --filter @qwen-code/qwen-code-core test`

---

## Phase D -- iconv-lite 0.6 -> 0.7
**Risk: Low** | Single file: `packages/core/src/utils/iconvHelper.ts`

- Check if default import pattern still works in 0.7 (currently uses CJS/ESM bridge)
- Verify `as unknown as IconvLite` cast is still valid  
**Verification:** Core test suite passes

---

## Phase E -- comment-json 4 -> 5
**Risk: Low** | Single file: `packages/cli/src/utils/commentJson.ts`

- API: `parse()`, `stringify()` -- verify signatures unchanged  
**Verification:** Settings file round-trip test

---

## Phase F -- chokidar 4 -> 5
**Risk: Low** | Single file: `packages/core/src/skills/skill-manager.ts`

- API: `watch()`, `FSWatcher`, `.close()` -- verify unchanged  
**Verification:** Skill manager tests

---

## Phase G -- esbuild 0.25 -> 0.28
**Risk: Low-Medium** | Build tool only; pre-1.0 minor versions can break.

- `package.json` root devDeps: `"^0.25.0"` -> `"^0.28.0"`
- Rebuild: `node esbuild.config.js` -> verify `dist/cli.js` produced  
**Verification:** `node dist/cli.js --version` returns `0.16.1`, `node dist/cli.js --help` renders

---

## Phase H -- vitest 3 -> 4 + vite 5 -> 6
**Risk: Medium** | No custom plugins. Override pins in `pnpm-workspace.yaml` control all packages.

| File | Change |
|---|---|
| `pnpm-workspace.yaml` overrides | `vitest: "3.2.4"` -> `"^4.0.0"` |
| `pnpm-workspace.yaml` overrides | `@vitest/coverage-v8: "3.2.4"` -> `"^4.0.0"` |
| `pnpm-workspace.yaml` overrides | `vite: "5.0.0"` -> `"^6.0.0"` |
| `package.json` root devDeps | same vitest/coverage-v8 bumps |
| `packages/webui/package.json` | `@vitejs/plugin-react: "^4.2.0"` -> `"^6.0.0"` |
| `packages/web-templates/package.json` | `@vitejs/plugin-react: "^4.2.0"` -> `"^6.0.0"` |

**Verification:** `pnpm test-all` green; `pnpm --filter @qwen-code/webui build` succeeds

---

## Phase I -- web-tree-sitter 0.24 -> 0.26
**Risk: Medium** | WASM loading is fragile. Both bundle mode and dev mode must work.

- `packages/core/package.json`: `"^0.24.7"` -> `"^0.26.0"`
- Key file: `packages/core/src/utils/shellAstParser.ts` -- `Parser.init()`, WASM binary path
- Test shell permission system (read-only command detection)  
**Verification:** Shell AST tests pass; bundle smoke test with `node dist/cli.js --version`

---

## Phase J -- @xterm/headless 5 -> 6
**Risk: Medium-High** | Core shell I/O chain. IBufferCell interface, ColorMode enums, buffer API.

- `packages/core/package.json`: `"5.5.0"` -> `"^6.0.0"`
- Key files:
  - `packages/core/src/services/shellExecutionService.ts`
  - `packages/core/src/utils/terminalSerializer.ts`
- Check: `IBufferCell` members, `ColorMode` enum values, `buffer.active` API  
**Verification:** Shell execution tests; ANSI color serialization tests; PTY integration test

---

## Phase K -- @anthropic-ai/sdk 0.36 -> 0.98
**Risk: High** | 62-version jump. Streaming event types, beta headers, thinking budget.

- `packages/core/package.json`: `"^0.36.1"` -> `"^0.98.0"`
- Key files (all in `packages/core/src/core/anthropicContentGenerator/`):
  - `anthropicContentGenerator.ts` (1013 lines) -- lines 232/258 (messages.create), 356-394 (beta headers), 681-757 (thinking), 771-968 (stream events)
  - `converter.ts` (845 lines) -- type conversions
  - `usage.ts` -- token metadata
- **Process:** Read CHANGELOG 0.37->0.98 focusing on `RawMessageStreamEvent`, `MessageCreateParams`, Tool types, streaming  
**Verification:** Anthropic provider: non-streaming, streaming, tool calling, thinking, caching, DeepSeek proxy

---

## Phase L -- @google/genai 1 -> 2
**Risk: High** | Widespread type imports across 60+ files. Core model methods.

- `packages/core/package.json`: `"1.30.0"` -> `"^2.0.0"`
- Key files:
  - `packages/core/src/core/geminiContentGenerator/geminiContentGenerator.ts` -- `GoogleGenAI` instantiation, `models.generateContent/Stream/countTokens/embedContent`
  - `packages/core/src/core/geminiRequest.ts` -- type definitions
  - `packages/core/src/core/geminiChat.ts` -- `createUserContent()`, `mcpToTool()` helpers
  - `packages/core/src/core/anthropicContentGenerator/converter.ts` -- cross-SDK types
  - 60+ files with type-only imports -- find all via `tsc --noEmit`
- **Process:** Read v2 migration guide -> update instantiation -> run `tsc --noEmit` -> fix all type errors  
**Verification:** Gemini provider: non-streaming, streaming, tool calling, thinking, token counting, embedding

---

## Phase M -- TypeScript 5.3.3 -> 6.x
**Risk: High** | All packages. May surface previously-hidden type errors.

- `pnpm-workspace.yaml` overrides: `typescript: "5.3.3"` -> `"^6.0.0"`
- `packages/sdk-typescript/package.json`: align TypeScript version
- **Pre-work:** Investigate why `packages/cli/tsconfig.json` excludes 97 test files
- **Pre-work:** Add `strict: true` to `packages/vscode-ide-companion/tsconfig.json`
- **Process:** Bump -> `pnpm install` -> `tsc --noEmit` per package -> fix errors -> rebuild -> smoke test  
**Verification:** `pnpm check` (lint) + full `tsc --noEmit` green + `node dist/cli.js --version` returns `0.16.1`

---

## End-to-End Verification (after all phases)

```bash
pnpm install
node packages/web-templates/build.mjs
for pkg in packages/core packages/channels/base packages/channels/telegram \
  packages/channels/weixin packages/channels/dingtalk packages/acp-bridge; do
  (cd $pkg && node ../../scripts/build_package.js)
done
node esbuild.config.js
node scripts/copy_bundle_assets.js
node dist/cli.js --version          # must print 0.16.1
node dist/cli.js --help             # must render full command tree
pnpm test-all                       # full test suite green
pnpm check                          # lint green
```

---

## Risk Summary

| Phase | Description | Risk | Effort |
|---|---|---|---|
| A | Trivial bumps + remove deprecated @types | None | 20 min |
| B | ESLint 9 + @typescript-eslint 8 | Low | 1-2 hr |
| C | OpenTelemetry suite | Low-Med | 1 hr |
| D | iconv-lite | Low | 30 min |
| E | comment-json | Low | 30 min |
| F | chokidar | Low | 30 min |
| G | esbuild | Low-Med | 30 min |
| H | vitest 4 + vite 6 | Medium | 2-3 hr |
| I | web-tree-sitter | Medium | 1-2 hr |
| J | @xterm/headless | Med-High | 2-3 hr |
| K | @anthropic-ai/sdk | High | 3-4 hr |
| L | @google/genai | High | 3-4 hr |
| M | TypeScript 6 | High | 4-6 hr |
