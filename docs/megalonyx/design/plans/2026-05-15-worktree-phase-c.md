# Worktree Phase C Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:**  worktree hooksPath Footer  worktree  `--resume` 

**Architecture:**  `WorktreeSession` sidecar JSON  JSONL session `EnterWorktree` `ExitWorktree` CLI  `useWorktreeSession` hook  `UIState.activeWorktree`Footer  worktree `WorktreeExitDialog`  worktree  Ctrl+C

**Tech Stack:** TypeScript, React (Ink), Node.js `fs.watch`, `simple-git`, Vitest

---

## 

|  |                                                          |                                                                           |
| ---- | ------------------------------------------------------------ | ----------------------------------------------------------------------------- |
|  | `packages/core/src/services/worktreeSessionService.ts`       | WorktreeSession  +                                            |
|  | `packages/core/src/services/worktreeSessionService.test.ts`  |                                                                       |
|  | `packages/core/src/services/sessionService.ts`               |  `getWorktreeSessionPath()`                                       |
|  | `packages/core/src/services/gitWorktreeService.ts`           | `createUserWorktree()` / `createAgentWorktree()`  `core.hooksPath`  |
|  | `packages/core/src/services/gitWorktreeService.test.ts`      | hooksPath                                                                 |
|  | `packages/core/src/tools/enter-worktree.ts`                  |  worktree  WorktreeSession                                          |
|  | `packages/core/src/tools/enter-worktree.test.ts`             | session                                                               |
|  | `packages/core/src/tools/exit-worktree.ts`                   |  worktree  WorktreeSession                                          |
|  | `packages/core/src/tools/exit-worktree.test.ts`              | session                                                               |
|  | `packages/cli/src/ui/hooks/useWorktreeSession.ts`            |  sidecar  WorktreeSession                                   |
|  | `packages/cli/src/ui/contexts/UIStateContext.tsx`            |  `activeWorktree`                                                     |
|  | `packages/cli/src/ui/AppContainer.tsx`                       |  `activeWorktree` resume                            |
|  | `packages/cli/src/ui/hooks/useStatusLine.ts`                 | `StatusLineCommandInput`  `worktree`                                  |
|  | `packages/cli/src/ui/components/Footer.tsx`                  |  worktree                                                           |
|  | `packages/cli/src/ui/components/WorktreeExitDialog.tsx`      |                                                                 |
|  | `packages/cli/src/ui/components/WorktreeExitDialog.test.tsx` |                                                                       |
|  | `packages/cli/src/ui/components/DialogManager.tsx`           |  WorktreeExitDialog                                                       |

---

## Task 1: WorktreeSession sidecar 

**Files:**

- Create: `packages/core/src/services/worktreeSessionService.ts`
- Create: `packages/core/src/services/worktreeSessionService.test.ts`
- Modify: `packages/core/src/services/sessionService.ts`

- [ ] **Step 1:  `worktreeSessionService.ts`**

```typescript
// packages/core/src/services/worktreeSessionService.ts
import * as fs from 'node:fs/promises';
import { isNodeError } from '../utils/errors.js';

export interface WorktreeSession {
  slug: string;
  worktreePath: string;
  worktreeBranch: string;
  originalCwd: string;
  originalBranch: string;
  /** HEAD commit SHA at the moment the worktree was created. Used by WorktreeExitDialog to count new commits. */
  originalHeadCommit: string;
}

export async function readWorktreeSession(
  filePath: string,
): Promise<WorktreeSession | null> {
  try {
    const raw = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(raw) as WorktreeSession;
  } catch (error) {
    if (isNodeError(error) && error.code === 'ENOENT') return null;
    throw error;
  }
}

export async function writeWorktreeSession(
  filePath: string,
  session: WorktreeSession,
): Promise<void> {
  await fs.mkdir(require('node:path').dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(session, null, 2), 'utf-8');
}

export async function clearWorktreeSession(filePath: string): Promise<void> {
  try {
    await fs.unlink(filePath);
  } catch (error) {
    if (isNodeError(error) && error.code === 'ENOENT') return;
    throw error;
  }
}
```

- [ ] **Step 2: **

```typescript
// packages/core/src/services/worktreeSessionService.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'node:fs/promises';
import * as os from 'node:os';
import * as path from 'node:path';
import {
  readWorktreeSession,
  writeWorktreeSession,
  clearWorktreeSession,
  type WorktreeSession,
} from './worktreeSessionService.js';

const sample: WorktreeSession = {
  slug: 'my-feature',
  worktreePath: '/repo/.qwen/worktrees/my-feature',
  worktreeBranch: 'worktree-my-feature',
  originalCwd: '/repo',
  originalBranch: 'main',
};

let tmpDir: string;
let filePath: string;

beforeEach(async () => {
  tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'wt-session-test-'));
  filePath = path.join(tmpDir, 'test.worktree.json');
});
afterEach(async () => {
  await fs.rm(tmpDir, { recursive: true, force: true });
});

describe('readWorktreeSession', () => {
  it('returns null when file does not exist', async () => {
    expect(await readWorktreeSession(filePath)).toBeNull();
  });

  it('reads back what was written', async () => {
    await fs.writeFile(filePath, JSON.stringify(sample), 'utf-8');
    expect(await readWorktreeSession(filePath)).toEqual(sample);
  });
});

describe('writeWorktreeSession', () => {
  it('writes a readable JSON file', async () => {
    await writeWorktreeSession(filePath, sample);
    const raw = await fs.readFile(filePath, 'utf-8');
    expect(JSON.parse(raw)).toEqual(sample);
  });

  it('overwrites existing file', async () => {
    await writeWorktreeSession(filePath, sample);
    const updated = { ...sample, slug: 'updated' };
    await writeWorktreeSession(filePath, updated);
    expect(await readWorktreeSession(filePath)).toEqual(updated);
  });
});

describe('clearWorktreeSession', () => {
  it('deletes the file', async () => {
    await writeWorktreeSession(filePath, sample);
    await clearWorktreeSession(filePath);
    expect(await readWorktreeSession(filePath)).toBeNull();
  });

  it('is a no-op when file does not exist', async () => {
    await expect(clearWorktreeSession(filePath)).resolves.not.toThrow();
  });
});
```

- [ ] **Step 3: **

```bash
cd packages/core
npx vitest run src/services/worktreeSessionService.test.ts
```

:`FAIL` -- 

- [ ] **Step 4:  `writeWorktreeSession`  require **

`worktreeSessionService.ts`  `path.dirname` `node:path`:

```typescript
//  "require('node:path').dirname(filePath)" 
import * as path from 'node:path';

export async function writeWorktreeSession(
  filePath: string,
  session: WorktreeSession,
): Promise<void> {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(session, null, 2), 'utf-8');
}
```

- [ ] **Step 5: **

```bash
cd packages/core
npx vitest run src/services/worktreeSessionService.test.ts
```

:`PASS` -- 6 tests passed

- [ ] **Step 6:  `SessionService`  `getWorktreeSessionPath()`**

 `packages/core/src/services/sessionService.ts`  `private getChatsDir()`  180:

```typescript
getWorktreeSessionPath(sessionId: string): string {
  return path.join(this.getChatsDir(), `${sessionId}.worktree.json`);
}
```

- [ ] **Step 7: **

```bash
cd packages/core
npm run typecheck
```

:

- [ ] **Step 8: **

```bash
git add packages/core/src/services/worktreeSessionService.ts \
        packages/core/src/services/worktreeSessionService.test.ts \
        packages/core/src/services/sessionService.ts
git commit -m "feat(worktree): add WorktreeSession sidecar storage"
```

---

## Task 2: hooksPath post-creation setup

**Files:**

- Modify: `packages/core/src/services/gitWorktreeService.ts:1133-1158``createUserWorktree`
- Modify: `packages/core/src/services/gitWorktreeService.test.ts`

- [ ] **Step 1: **

 `gitWorktreeService.test.ts`  `createUserWorktree` :

```typescript
it('configures core.hooksPath to main repo after creation', async () => {
  const result = await service.createUserWorktree('hooks-test');
  expect(result.success).toBe(true);

  const worktreePath = result.worktree!.path;
  const worktreeGit = simpleGit(worktreePath);
  const hooksPath = await worktreeGit.raw([
    'config',
    '--local',
    'core.hooksPath',
  ]);
  // Should point to the main repo's .git/hooks
  expect(hooksPath.trim()).toContain('.git/hooks');
});
```

- [ ] **Step 2: **

```bash
cd packages/core
npx vitest run src/services/gitWorktreeService.test.ts -t "configures core.hooksPath"
```

:`FAIL` -- hooksPath 

- [ ] **Step 3:  `createUserWorktree`  hooksPath **

 `gitWorktreeService.ts`  `createUserWorktree`  `git worktree add`  1140 `return { success: true, worktree }` :

```typescript
// Configure hooksPath so commits inside this worktree run the main
// repo's hooks. Priority: .husky/ (common) -> .git/hooks (fallback).
// Mirrors claude-code's performPostCreationSetup() logic.
try {
  const huskyPath = path.join(this.sourceRepoPath, '.husky');
  const gitHooksPath = path.join(this.sourceRepoPath, '.git', 'hooks');
  let hooksPath: string | null = null;
  for (const candidate of [huskyPath, gitHooksPath]) {
    try {
      await fs.stat(candidate);
      hooksPath = candidate;
      break;
    } catch {
      // Not found -- try next.
    }
  }
  if (hooksPath) {
    const worktreeGit = simpleGit(worktreePath);
    // Skip the subprocess if core.hooksPath is already set to the same value
    // (~14ms spawn overhead per claude-code's comment on parseGitConfigValue).
    let existing = '';
    try {
      existing = (
        await worktreeGit.raw(['config', '--local', 'core.hooksPath'])
      ).trim();
    } catch {
      // Key not set -- empty string means "proceed".
    }
    if (existing !== hooksPath) {
      await worktreeGit.raw(['config', 'core.hooksPath', hooksPath]);
    }
  }
} catch (hookError) {
  debugLogger.warn(
    `createUserWorktree: failed to set core.hooksPath: ${hookError}`,
  );
  // Non-fatal: worktree is usable, just without inherited hooks.
}
```

`this.sourceRepoPath`  `GitWorktreeService` `this.sourceRepoPath = path.resolve(sourceRepoPath)` 224 `import * as fs from 'node:fs/promises'`

- [ ] **Step 4:  `createAgentWorktree` **

 `createAgentWorktree`  `git worktree add`  hooksPath  Step 3 `slug`  agent worktree 

- [ ] **Step 5: **

```bash
cd packages/core
npx vitest run src/services/gitWorktreeService.test.ts -t "configures core.hooksPath"
```

:`PASS`

- [ ] **Step 6: **

```bash
git add packages/core/src/services/gitWorktreeService.ts \
        packages/core/src/services/gitWorktreeService.test.ts
git commit -m "feat(worktree): configure core.hooksPath after worktree creation"
```

---

## Task 3: EnterWorktreeTool  WorktreeSession

**Files:**

- Modify: `packages/core/src/tools/enter-worktree.ts`
- Modify: `packages/core/src/tools/enter-worktree.test.ts`

- [ ] **Step 1: **

 `enter-worktree.test.ts` :

```typescript
import { readWorktreeSession } from '../services/worktreeSessionService.js';

it('writes WorktreeSession sidecar after creating worktree', async () => {
  // Arrange: use the existing test setup that creates a real git repo
  // and invokes the tool (copy from existing "custom name" test)
  const result = await invokeTool(tool, { name: 'session-test' });
  expect(result.error).toBeUndefined();

  const sessionPath = config
    .getSessionService()
    .getWorktreeSessionPath(config.getSessionId());
  const session = await readWorktreeSession(sessionPath);

  expect(session).not.toBeNull();
  expect(session!.slug).toBe('session-test');
  expect(session!.worktreePath).toContain('session-test');
  expect(session!.worktreeBranch).toBe('worktree-session-test');
  expect(session!.originalCwd).toBeTruthy();
  expect(session!.originalBranch).toBeTruthy();
  expect(session!.originalHeadCommit).toMatch(/^[0-9a-f]{7,40}$/);
});
```

- [ ] **Step 2: **

```bash
cd packages/core
npx vitest run src/tools/enter-worktree.test.ts -t "writes WorktreeSession"
```

:`FAIL` -- session file is null

- [ ] **Step 3:  `enter-worktree.ts` session**

 `enter-worktree.ts`  import:

```typescript
import { writeWorktreeSession } from '../services/worktreeSessionService.js';
```

 `execute()`  baseBranch `createUserWorktree()`  HEAD commit SHA:

```typescript
// Capture HEAD before branching -- WorktreeExitDialog uses this to count
// new commits created inside the worktree (mirrors claude-code approach).
let originalHeadCommit = '';
try {
  originalHeadCommit = await service.getHeadCommit();
} catch {
  // Non-fatal.
}
```

 `GitWorktreeService` `gitWorktreeService.ts` `getCurrentBranch()` :

```typescript
async getHeadCommit(): Promise<string> {
  try {
    return (await this.git.raw(['rev-parse', '--short', 'HEAD'])).trim();
  } catch {
    return '';
  }
}
```

 `writeWorktreeSessionMarker(...)` :

```typescript
// Persist worktree session so --resume can restore context.
try {
  await writeWorktreeSession(
    this.config
      .getSessionService()
      .getWorktreeSessionPath(this.config.getSessionId()),
    {
      slug,
      worktreePath: result.worktree.path,
      worktreeBranch: result.worktree.branch,
      originalCwd: projectRoot,
      originalBranch: baseBranch ?? 'HEAD',
      originalHeadCommit,
    },
  );
} catch (error) {
  debugLogger.warn(`enter_worktree: failed to write session state: ${error}`);
}
```

- [ ] **Step 4: **

```bash
cd packages/core
npx vitest run src/tools/enter-worktree.test.ts
```

:

- [ ] **Step 5: **

```bash
cd packages/core && npm run typecheck
```

- [ ] **Step 6: **

```bash
git add packages/core/src/tools/enter-worktree.ts \
        packages/core/src/tools/enter-worktree.test.ts
git commit -m "feat(worktree): persist WorktreeSession in EnterWorktreeTool"
```

---

## Task 4: ExitWorktreeTool  WorktreeSession

**Files:**

- Modify: `packages/core/src/tools/exit-worktree.ts`
- Modify: `packages/core/src/tools/exit-worktree.test.ts`

- [ ] **Step 1: **

 `exit-worktree.test.ts` keep  remove  session:

```typescript
import {
  writeWorktreeSession,
  readWorktreeSession,
} from '../services/worktreeSessionService.js';

async function seedSession(cfg: Config, slug: string) {
  await writeWorktreeSession(
    cfg.getSessionService().getWorktreeSessionPath(cfg.getSessionId()),
    {
      slug,
      worktreePath: `/repo/.qwen/worktrees/${slug}`,
      worktreeBranch: `worktree-${slug}`,
      originalCwd: '/repo',
      originalBranch: 'main',
    },
  );
}

it('clears WorktreeSession after keep', async () => {
  await seedSession(config, 'exit-keep-test');
  // Create the worktree first so exit_worktree can find it
  await config.getWorktreeService().createUserWorktree('exit-keep-test');
  await invokeTool(tool, { name: 'exit-keep-test', action: 'keep' });

  const sessionPath = config
    .getSessionService()
    .getWorktreeSessionPath(config.getSessionId());
  expect(await readWorktreeSession(sessionPath)).toBeNull();
});

it('clears WorktreeSession after remove', async () => {
  await seedSession(config, 'exit-remove-test');
  await config.getWorktreeService().createUserWorktree('exit-remove-test');
  await invokeTool(tool, { name: 'exit-remove-test', action: 'remove' });

  const sessionPath = config
    .getSessionService()
    .getWorktreeSessionPath(config.getSessionId());
  expect(await readWorktreeSession(sessionPath)).toBeNull();
});
```

- [ ] **Step 2: **

```bash
cd packages/core
npx vitest run src/tools/exit-worktree.test.ts -t "clears WorktreeSession"
```

:`FAIL`

- [ ] **Step 3:  `exit-worktree.ts`**

 import:

```typescript
import { clearWorktreeSession } from '../services/worktreeSessionService.js';
```

 `action === 'keep'`  184-196 `return { llmContent: ..., returnDisplay: ... }` :

```typescript
try {
  await clearWorktreeSession(
    this.config
      .getSessionService()
      .getWorktreeSessionPath(this.config.getSessionId()),
  );
} catch (error) {
  debugLogger.warn(`exit_worktree: failed to clear session state: ${error}`);
}
```

 `action === 'remove'` `removeUserWorktree`  `clearWorktreeSession` 

- [ ] **Step 4: **

```bash
cd packages/core
npx vitest run src/tools/exit-worktree.test.ts
```

:

- [ ] **Step 5: **

```bash
git add packages/core/src/tools/exit-worktree.ts \
        packages/core/src/tools/exit-worktree.test.ts
git commit -m "feat(worktree): clear WorktreeSession in ExitWorktreeTool"
```

---

## Task 5: useWorktreeSession hook + UIState.activeWorktree

**Files:**

- Create: `packages/cli/src/ui/hooks/useWorktreeSession.ts`
- Modify: `packages/cli/src/ui/contexts/UIStateContext.tsx`
- Modify: `packages/cli/src/ui/AppContainer.tsx`

- [ ] **Step 1:  `UIStateContext.tsx`  `activeWorktree` **

 `UIState` interface 85 `branchName: string | undefined;` :

```typescript
activeWorktree: {
  slug: string;
  branch: string;
  path: string;
  originalCwd: string;
  originalBranch: string;
  originalHeadCommit: string;
} | null;
```

 UIState  `AppContainer.tsx`  UIState provider  `createContext`  defaultValue `activeWorktree: null`

- [ ] **Step 2:  `useWorktreeSession.ts`**

```typescript
// packages/cli/src/ui/hooks/useWorktreeSession.ts
import { useState, useEffect } from 'react';
import * as fs from 'node:fs';
import {
  readWorktreeSession,
  type WorktreeSession,
} from '@qwen-code/qwen-code-core';
import { useConfig } from '../contexts/ConfigContext.js';

export function useWorktreeSession(): WorktreeSession | null {
  const config = useConfig();
  const [session, setSession] = useState<WorktreeSession | null>(null);

  useEffect(() => {
    const sessionService = config.getSessionService();
    const sessionId = config.getSessionId();
    const filePath = sessionService.getWorktreeSessionPath(sessionId);

    let watcher: fs.FSWatcher | undefined;

    const load = async () => {
      try {
        const ws = await readWorktreeSession(filePath);
        setSession(ws);
      } catch {
        setSession(null);
      }
    };

    void load();

    try {
      watcher = fs.watch(filePath, () => void load());
    } catch {
      // File does not exist yet -- watcher set up on next write event via load()
    }

    return () => {
      watcher?.close();
    };
  }, [config]);

  return session;
}
```

:`readWorktreeSession`  `WorktreeSession`  `@qwen-code/qwen-code-core`  `packages/core/src/index.ts` :

```typescript
export {
  readWorktreeSession,
  writeWorktreeSession,
  clearWorktreeSession,
  type WorktreeSession,
} from './services/worktreeSessionService.js';
```

- [ ] **Step 3:  `AppContainer.tsx`  hook  `activeWorktree`**

 `AppContainer.tsx`  import:

```typescript
import { useWorktreeSession } from './hooks/useWorktreeSession.js';
```

 `AppContainer`  `branchName` :

```typescript
const worktreeSession = useWorktreeSession();
```

 `UIStateContext.Provider`  value :

```typescript
activeWorktree: worktreeSession
  ? {
      slug: worktreeSession.slug,
      branch: worktreeSession.worktreeBranch,
      path: worktreeSession.worktreePath,
      originalCwd: worktreeSession.originalCwd,
      originalBranch: worktreeSession.originalBranch,
      originalHeadCommit: worktreeSession.originalHeadCommit,
    }
  : null,
```

- [ ] **Step 4: **

```bash
npm run typecheck
```

 workspace :

- [ ] **Step 5: **

```bash
git add packages/core/src/services/worktreeSessionService.ts \
        packages/core/src/index.ts \
        packages/cli/src/ui/hooks/useWorktreeSession.ts \
        packages/cli/src/ui/contexts/UIStateContext.tsx \
        packages/cli/src/ui/AppContainer.tsx
git commit -m "feat(worktree): add useWorktreeSession hook and UIState.activeWorktree"
```

---

## Task 6: StatusLineCommandInput.worktree  + Footer worktree 

**Files:**

- Modify: `packages/cli/src/ui/hooks/useStatusLine.ts`
- Modify: `packages/cli/src/ui/components/Footer.tsx`

- [ ] **Step 1:  `useStatusLine.ts`  `worktree` **

 `StatusLineCommandInput` interface 21 `git?: { branch: string }` :

```typescript
worktree?: {
  /** worktree slug "my-feature" */
  name: string;
  /** worktree  */
  path: string;
  /** git  "worktree-my-feature" */
  branch: string;
  /**  worktree  */
  original_cwd: string;
  /**  worktree  */
  original_branch: string;
};
```

 claude-code  qwen-code  claude-code  statusline 

 `doUpdate`  `input: StatusLineCommandInput`  225 `...(ui.branchName && { git: { branch: ui.branchName } })` :

```typescript
...(uiStateRef.current.activeWorktree && {
  worktree: {
    name: uiStateRef.current.activeWorktree.slug,
    path: uiStateRef.current.activeWorktree.path,
    branch: uiStateRef.current.activeWorktree.branch,
    original_cwd: uiStateRef.current.activeWorktree.originalCwd,
    original_branch: uiStateRef.current.activeWorktree.originalBranch,
  },
}),
```

:`UIState.activeWorktree`  `originalCwd`  `originalBranch`  Task 5  AppContainer 

- [ ] **Step 2:  `Footer.tsx`  worktree **

 `Footer.tsx`  `useUIState`

 `statusLineLines`  140-148:

```tsx
{
  statusLineLines.length > 0 &&
    !uiState.ctrlCPressedOnce &&
    !uiState.ctrlDPressedOnce &&
    statusLineLines.map((line, i) => (
      <Text key={`status-line-${i}`} dimColor wrap="truncate">
        {line}
      </Text>
    ));
}
```

 worktree  `activeWorktree`  statusline :

```tsx
{
  uiState.activeWorktree &&
    !uiState.ctrlCPressedOnce &&
    !uiState.ctrlDPressedOnce &&
    statusLineLines.length === 0 && (
      <Text dimColor wrap="truncate">
        {` ${uiState.activeWorktree.branch} (${uiState.activeWorktree.slug})`}
      </Text>
    );
}
```

- [ ] **Step 3:  + **

```bash
npm run typecheck && npm run build
```

:

- [ ] **Step 4: **

```bash
git add packages/cli/src/ui/hooks/useStatusLine.ts \
        packages/cli/src/ui/components/Footer.tsx
git commit -m "feat(worktree): show active worktree in Footer and StatusLine payload"
```

---

## Task 7: --resume worktree 

**Files:**

- Modify: `packages/cli/src/ui/AppContainer.tsx:459-489`

- [ ] **Step 1:  resume  worktree **

 `AppContainer.tsx`  resume  459-489:

```typescript
const resumedSessionData = config.getResumedSessionData();
if (resumedSessionData) {
  const historyItems = buildResumedHistoryItems(resumedSessionData, config);
  historyManager.loadHistory(historyItems);
  // ...
}
```

:

```typescript
const resumedSessionData = config.getResumedSessionData();
if (resumedSessionData) {
  const historyItems = buildResumedHistoryItems(resumedSessionData, config);
  historyManager.loadHistory(historyItems);

  // If there is an active worktree session, inject a context reminder so
  // the model immediately knows to continue using the worktree path.
  const ws = await readWorktreeSession(
    config.getSessionService().getWorktreeSessionPath(config.getSessionId()),
  );
  if (ws) {
    // Verify the worktree directory still exists before treating it as active.
    const worktreeAlive = await fs
      .stat(ws.worktreePath)
      .then((s) => s.isDirectory())
      .catch(() => false);

    if (worktreeAlive) {
      historyManager.addItem(
        {
          type: MessageType.INFO,
          text:
            `[Resumed] Active worktree: "${ws.slug}" at ${ws.worktreePath} ` +
            `(branch: ${ws.worktreeBranch}). Continue using this path for all file operations.`,
        },
        Date.now(),
      );
    } else {
      // Stale sidecar -- worktree was deleted externally, clean up.
      await clearWorktreeSession(
        config
          .getSessionService()
          .getWorktreeSessionPath(config.getSessionId()),
      );
    }
  }

  // ... rest of existing resume code (background agents, session name)
}
```

 import:

```typescript
import {
  readWorktreeSession,
  clearWorktreeSession,
} from '@qwen-code/qwen-code-core';
import * as fs from 'node:fs/promises';
```

`fs` 

- [ ] **Step 2: **

```bash
npm run typecheck
```

- [ ] **Step 3: **

```bash
git add packages/cli/src/ui/AppContainer.tsx
git commit -m "feat(worktree): inject context message on --resume when worktree is active"
```

---

## Task 8: WorktreeExitDialog

**Files:**

- Create: `packages/cli/src/ui/components/WorktreeExitDialog.tsx`
- Create: `packages/cli/src/ui/components/WorktreeExitDialog.test.tsx`
- Modify: `packages/cli/src/ui/components/DialogManager.tsx`
- Modify: `packages/cli/src/ui/contexts/UIStateContext.tsx`
- Modify: `packages/cli/src/ui/AppContainer.tsx`

- [ ] **Step 1:  `AppContainer.tsx`  dialog **

`showWelcomeBackDialog`  dialog  hook  AppContainer UIState value  Provider WorktreeExitDialog :

 `AppContainer.tsx` :

```typescript
const [showWorktreeExitDialog, setShowWorktreeExitDialog] = useState(false);
```

 UIState Provider  value :

```typescript
showWorktreeExitDialog,
```

 `UIState` interface  dialog :

```typescript
showWorktreeExitDialog: boolean;
```

- [ ] **Step 2: **

```typescript
// packages/cli/src/ui/components/WorktreeExitDialog.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render } from 'ink-testing-library';
import React from 'react';
import { WorktreeExitDialog } from './WorktreeExitDialog.js';

describe('WorktreeExitDialog', () => {
  it('shows loading state initially', () => {
    const { lastFrame } = render(
      <WorktreeExitDialog
        slug="my-feature"
        branch="worktree-my-feature"
        worktreePath="/tmp/repo/.qwen/worktrees/my-feature"
        originalHeadCommit="abc1234"
        onKeep={vi.fn()}
        onRemove={vi.fn()}
        onCancel={vi.fn()}
      />,
    );
    // Should show loading spinner immediately before git status resolves
    expect(lastFrame()).toContain('Checking');
  });

  it('renders slug, branch, and options after loading (no changes)', async () => {
    // Use vi.mock to stub execFileNoThrow / execFile so git status returns empty
    // and rev-list returns "0". See existing dialog tests for the mock pattern.
    // After async effect resolves:
    //   - shows "my-feature" and "worktree-my-feature"
    //   - shows Keep and Remove options
    //   - shows "no uncommitted changes" or similar
  });
});
```

- [ ] **Step 3: **

```bash
cd packages/cli
npx vitest run src/ui/components/WorktreeExitDialog.test.tsx
```

:`FAIL` -- 

- [ ] **Step 4:  `WorktreeExitDialog.tsx`**

 `WelcomeBackDialog.tsx`  RadioSelect  mount  claude-code `WorktreeExitDialog.tsx`  `loadChanges` :

```tsx
// packages/cli/src/ui/components/WorktreeExitDialog.tsx
import React, { useEffect, useState } from 'react';
import { Box, Text } from 'ink';
import { execa } from 'execa';
import { RadioSelect } from '../shared/RadioSelect.js';
import type { RadioSelectItem } from '../shared/RadioSelect.js';
import { theme } from '../semantic-colors.js';

interface WorktreeExitDialogProps {
  slug: string;
  branch: string;
  worktreePath: string;
  originalHeadCommit: string;
  onKeep: () => void;
  onRemove: () => void;
  onCancel: () => void;
}

type Choice = 'keep' | 'remove' | 'cancel';

export const WorktreeExitDialog: React.FC<WorktreeExitDialogProps> = ({
  slug,
  branch,
  worktreePath,
  originalHeadCommit,
  onKeep,
  onRemove,
  onCancel,
}) => {
  const [loading, setLoading] = useState(true);
  const [changedFiles, setChangedFiles] = useState<string[]>([]);
  const [commitCount, setCommitCount] = useState(0);
  const [selected, setSelected] = useState<Choice>('keep');

  useEffect(() => {
    async function loadDirtyState() {
      try {
        // Uncommitted changes (tracked + untracked)
        const { stdout: statusOut } = await execa(
          'git',
          ['status', '--porcelain'],
          { cwd: worktreePath },
        );
        const files = statusOut.split('\n').filter((l) => l.trim().length > 0);
        setChangedFiles(files);

        // New commits since worktree was created
        if (originalHeadCommit) {
          const { stdout: countOut } = await execa(
            'git',
            ['rev-list', '--count', `${originalHeadCommit}..HEAD`],
            { cwd: worktreePath },
          );
          setCommitCount(parseInt(countOut.trim(), 10) || 0);
        }
      } catch {
        // If git fails, show dialog without counts.
      } finally {
        setLoading(false);
      }
    }
    void loadDirtyState();
  }, [worktreePath, originalHeadCommit]);

  const options: Array<RadioSelectItem<Choice>> = [
    {
      key: 'keep',
      label: 'Keep worktree (exit without deleting)',
      value: 'keep',
    },
    {
      key: 'remove',
      label:
        changedFiles.length > 0 || commitCount > 0
          ? `Remove worktree and branch (discards ${commitCount} commit(s), ${changedFiles.length} file(s))`
          : 'Remove worktree and branch',
      value: 'remove',
    },
    { key: 'cancel', label: 'Cancel (stay in session)', value: 'cancel' },
  ];

  if (loading) {
    return (
      <Box marginY={1} paddingX={2}>
        <Text color={theme.text.secondary}>Checking worktree status...</Text>
      </Box>
    );
  }

  return (
    <Box flexDirection="column" marginY={1} paddingX={2}>
      <Text color={theme.status.warning}>
        {`Active worktree: "${slug}" (${branch})`}
      </Text>
      {(changedFiles.length > 0 || commitCount > 0) && (
        <Box flexDirection="column" marginBottom={1}>
          {commitCount > 0 && (
            <Text color={theme.text.secondary}>
              {`  ${commitCount} new commit(s) on ${branch}`}
            </Text>
          )}
          {changedFiles.length > 0 && (
            <Text color={theme.text.secondary}>
              {`  ${changedFiles.length} uncommitted file(s)`}
            </Text>
          )}
        </Box>
      )}
      <Text color={theme.text.secondary}>What would you like to do?</Text>
      <RadioSelect
        items={options}
        selectedValue={selected}
        onSelect={(value) => {
          if (value === 'keep') onKeep();
          else if (value === 'remove') onRemove();
          else onCancel();
        }}
        onChange={setSelected}
      />
    </Box>
  );
};
```

:`execa`  `execFileNoThrow` claude-code  `packages/cli/package.json`  exec  `execa` Node.js  `execFile` 

- [ ] **Step 5: **

```bash
cd packages/cli
npx vitest run src/ui/components/WorktreeExitDialog.test.tsx
```

:loading 

- [ ] **Step 6:  `DialogManager.tsx` **

 `DialogManager`  dialog :

```tsx
import { WorktreeExitDialog } from './WorktreeExitDialog.js';

//  DialogManager  JSX  dialog :
{
  uiState.showWorktreeExitDialog && uiState.activeWorktree && (
    <WorktreeExitDialog
      slug={uiState.activeWorktree.slug}
      branch={uiState.activeWorktree.branch}
      worktreePath={uiState.activeWorktree.path}
      originalHeadCommit={uiState.activeWorktree.originalHeadCommit}
      onKeep={() => {
        setShowWorktreeExitDialog(false);
        handleSlashCommand('/quit');
      }}
      onRemove={async () => {
        setShowWorktreeExitDialog(false);
        // Remove the worktree directly via service (no tool call needed).
        try {
          const svc = new GitWorktreeService(config.getTargetDir());
          await svc.removeUserWorktree(uiState.activeWorktree!.slug, {
            deleteBranch: true,
          });
          await clearWorktreeSession(
            config
              .getSessionService()
              .getWorktreeSessionPath(config.getSessionId()),
          );
        } catch {
          // Non-fatal -- exit anyway.
        }
        handleSlashCommand('/quit');
      }}
      onCancel={() => {
        setShowWorktreeExitDialog(false);
      }}
    />
  );
}
```

`setShowWorktreeExitDialog`  Step 1  AppContainer  useState props  DialogManager  dialog 

- [ ] **Step 7:  `AppContainer.tsx`  Ctrl+C**

 `handleExit`  2387 `pressedOnce`  `true`  `handleSlashCommand('/quit')` :

```typescript
// Fast double-press: Direct quit (preserve user habit)
if (pressedOnce) {
  if (timerRef.current) {
    clearTimeout(timerRef.current);
  }
  // Exit directly
  handleSlashCommand('/quit');
  return;
}
```

:

```typescript
if (pressedOnce) {
  if (timerRef.current) {
    clearTimeout(timerRef.current);
  }
  // If inside a worktree, show the exit dialog instead of quitting directly.
  if (worktreeSession) {
    setShowWorktreeExitDialog(true);
    return;
  }
  handleSlashCommand('/quit');
  return;
}
```

`worktreeSession`  Step 1  `useWorktreeSession()`  AppContainer  `handleExit`  `useCallback` `setShowWorktreeExitDialog`  Step 1  useState

- [ ] **Step 9:  + **

```bash
npm run typecheck
cd packages/core && npx vitest run
cd packages/cli && npx vitest run
```

:

- [ ] **Step 10: **

```bash
npm run build && npm run bundle
```

:`dist/cli.js` 

- [ ] **Step 11: **

```bash
git add packages/cli/src/ui/components/WorktreeExitDialog.tsx \
        packages/cli/src/ui/components/WorktreeExitDialog.test.tsx \
        packages/cli/src/ui/components/DialogManager.tsx \
        packages/cli/src/ui/contexts/UIStateContext.tsx \
        packages/cli/src/ui/AppContainer.tsx
git commit -m "feat(worktree): add WorktreeExitDialog -- intercept Ctrl+C when worktree is active"
```

---

## 

|                           |                                                     |
| ----------------------------- | ----------------------------------------------------------- |
| `enter_worktree`        | `<sessionId>.worktree.json`  slug / path / branch |
| `exit_worktree`         | `<sessionId>.worktree.json`                           |
| `--resume`  worktree  | Footer  worktree INFO                   |
| `--resume`  worktree  | sidecar  worktree                       |
| worktree  Ctrl+C      |  "Press Ctrl+C again to exit."                          |
| worktree  Ctrl+C      |  WorktreeExitDialogkeep / remove / cancel           |
|  worktree  Ctrl+C |                                         |
|  worktree           | `core.hooksPath`  hookspre-commit       |
| statusline  stdin         | JSON payload  `worktree.slug`  `worktree.branch`        |
