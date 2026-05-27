# TypeScript Build Errors -- packages/core

**Status:** Active. `tsc --build` exits with code 1 in `packages/core` (and cascades to
`packages/cli` since CLI's tsconfig references core). All errors originate in
QwenLM/qwen-code upstream source; none are in Megalonyx additions.

**Why `tsc --build` fails but tests still run:**
`tsconfig.json` sets `"noEmitOnError": false`, so TypeScript emits `dist/` files even
when there are errors. However, `scripts/build_package.js` calls `execSync('tsc --build')`
which exits non-zero on any error -- this throws and the nx build target fails. Tests bypass
the build step by using vitest aliases that point directly at TypeScript source, so the
test suite is unaffected.

**Root cause of the error volume:** We pin TypeScript to 5.3.3 via pnpm workspace overrides.
QwenLM's code uses APIs added in later TypeScript versions (`AbortSignal.any` in TS 5.5,
`URL.parse` in Node 22 types), and has accumulated type gaps that `noEmitOnError: false`
let them ignore. Upgrading to TypeScript 6 is blocked -- see `todo.md` Phase M.

---

## Error Inventory

### Group 1 -- Missing type declarations: `shell-quote` (6 files)

`@types/shell-quote` is not in `packages/core/package.json` devDependencies, so TypeScript
cannot find type declarations for the `shell-quote` module.

**Fix:** `pnpm add -D @types/shell-quote --filter @qwen-code/qwen-code-core`

Affected locations:
```
src/utils/shellReadOnlyChecker.ts:13
src/utils/shell-utils.ts:11          (+ implicit any at :309 -- token parameter)
src/permissions/rule-parser.ts:10
src/tools/mcp-client.ts:26
src/tools/tool-registry.ts:22
src/tools/shell.ts:55                (+ implicit any at :233, :234 -- key/t parameters)
```

---

### Group 2 -- Missing method: `FileLogExporter.forceFlush` (2 locations, 1 fix)

The `@opentelemetry/sdk-logs` `LogRecordExporter` interface requires `forceFlush(): Promise<void>`.
`FileLogExporter` implements `export()` and `shutdown()` but not `forceFlush`. This was added
to the interface in a recent `@opentelemetry` release.

**Fix:** Add `async forceFlush(): Promise<void> {}` to `FileLogExporter` in
`src/telemetry/file-exporters.ts`.

Affected locations:
```
src/telemetry/file-exporters.ts:55   (TS2420 -- class doesn't implement interface)
src/telemetry/sdk.ts:325             (TS2345 -- consequence of above)
```

---

### Group 3 -- `AbortSignal.any()` not in TypeScript 5.3.3 lib (4 files, 6 locations)

`AbortSignal.any(signals)` was added to the TypeScript DOM lib in TS 5.5. We pin to 5.3.3,
so the static method is not recognized.

**Fix:** Add a global type declaration file `packages/core/src/types/abort-signal.d.ts`:
```typescript
interface AbortSignalConstructor {
  any(signals: AbortSignal[]): AbortSignal;
}
```

Affected locations:
```
src/permissions/classifier.ts:157, :205
src/tools/shell.ts:1515, :1521
src/goals/goalHook.ts:71
src/memory/relevanceSelector.ts:103
```

---

### Group 4 -- MCP content union type not narrowed: `ide-client.ts` (5 locations)

The MCP SDK returns a union type for content items. Accessing `.text` requires narrowing
to `type === 'text'` first. The code accesses `.text` directly without a guard.

**Fix:** Wrap each `.text` access with `if (content.type === 'text')` or use type narrowing.

Affected locations:
```
src/ide/ide-client.ts:275, :356, :366, :368, :378
```

---

### Group 5 -- `Span | undefined` passed where `Span` required (1 location)

An OpenTelemetry span that may be `undefined` is passed to a function requiring a non-optional
`Span`. Likely caused by a version mismatch in `@opentelemetry` where optional spans became
required.

**Fix:** Add a non-null assertion or guard at the call site.

Affected location:
```
src/core/coreToolScheduler.ts:2524
```

---

### Group 6 -- `(string | null)[]` vs `string[]` in git worktree args (1 location)

`gitWorktreeService.ts` builds a git argument array that may contain `null` values and passes
it to `simple-git`'s `TaskOptions`, which requires `string[]`.

**Fix:** Filter nulls before passing: `.filter((x): x is string => x !== null)`

Affected location:
```
src/services/gitWorktreeService.ts:830
```

---

### Group 7 -- `@agentclientprotocol/sdk` types not found (1 location)

`fileSystemService.ts` imports from `@agentclientprotocol/sdk` but the package is not
resolvable in core's node_modules. The ACP SDK is installed in `packages/acp-bridge`,
not in core. Core should be importing from `@qwen-code/acp-bridge` instead, or the ACP
SDK should be added as a dependency.

**Fix:** Verify whether `fileSystemService.ts` should import from `@agentclientprotocol/sdk`
directly or via `@qwen-code/acp-bridge`. If the former, add `@agentclientprotocol/sdk` to
core's dependencies. If the latter, update the import path.

Affected location:
```
src/services/fileSystemService.ts:22   (TS2307 -- module not found)
src/services/fileSystemService.ts:282  (TS4111 -- index signature access, likely consequence)
```

---

### Group 8 -- `URL.parse()` not in type declarations (1 location)

`URL.parse()` was added to the Node.js API in v22.1 and to `@types/node` in a later release.
The method is available at runtime on Node 22 but may not be in the installed `@types/node`
version's type declarations.

**Fix:** Use `new URL(source, base)` instead of `URL.parse(source, base)`, which has
been available since Node 10. The `parse()` static method returns `null` on invalid URLs
rather than throwing -- adjust the guard accordingly if behavior differs.

Affected location:
```
src/extension/github.ts:118
```

---

### Group 9 -- `string | string[]` passed as `string` (1 location)

A parameter that can be `string | string[]` is passed to a function expecting `string`.

**Fix:** Use `Array.isArray(val) ? val.join(' ') : val` or add a type guard.

Affected location:
```
src/extension/claude-converter.ts:127
```

---

### Group 10 -- `(ExtensionUpdateInfo | undefined)[]` vs `ExtensionUpdateInfo[]` (1 location)

A `.map()` call that can produce `undefined` elements is assigned to a typed array.

**Fix:** Add `.filter((x): x is ExtensionUpdateInfo => x !== undefined)` after the map.

Affected location:
```
src/extension/extensionManager.ts:1337
```

---

### Group 11 -- `child` process variable has implicit `any` (2 files, many locations)

`let child;` is declared without a type, then assigned inside a try block. TypeScript cannot
infer the type across the try/catch boundary. Both files use `child_process.spawn`.

**Fix:** Annotate as `let child: ReturnType<typeof spawn> | undefined;` in each file.

Affected files and entry points:
```
src/tools/monitor.ts:334        (child declared) + :428, :433, :438, :443, :446, :450, :452, :455
src/utils/filesearch/crawler.ts:417  (child declared) + :457, :461, :489, :490, :492, :495
```

---

## Fix Order

All fixes are in `packages/core`. Fix in this order to unblock the build:

1. **Group 1** -- `pnpm add -D @types/shell-quote` (eliminates ~10 errors in one step)
2. **Group 2** -- Add `forceFlush()` to `FileLogExporter`
3. **Group 3** -- Add `abort-signal.d.ts` type shim
4. **Group 7** -- Resolve `@agentclientprotocol/sdk` import (investigate first)
5. **Group 8** -- Replace `URL.parse()` with `new URL()` + null guard
6. **Groups 4, 5, 6, 9, 10** -- One-line fixes in individual files
7. **Group 11** -- Annotate `child` variable in monitor.ts and crawler.ts

After fixing all groups, verify with:
```bash
cd packages/core && pnpm exec tsc --build
# Should exit 0
cd packages/cli && pnpm exec tsc --build
# Should exit 0 (inherits core's now-clean output)
```

Then confirm the full test suite still passes:
```bash
pnpm test-all
```

## Upstream eligibility

All errors are in QwenLM upstream source. After fixing locally, the following are candidates
for upstream PRs (see `docs/upstream/upstream-pr-guide.md`):

- Groups 1, 2, 3, 6, 8, 9, 10, 11 -- clean upstream contributions
- Group 7 (`@agentclientprotocol/sdk` import) -- investigate before submitting
- Group 4 (ide-client.ts union narrowing) -- clean fix, worth submitting
- Group 5 (coreToolScheduler Span) -- depends on investigation of OTel version

Do NOT submit before fixing locally and verifying QwenLM's CI would pass. See
`docs/upstream/upstream-pr-checklist.md`.
