# Worktree 

## 

qwen-code  Arena  worktree `GitWorktreeService` worktree AgentTool  subagent  worktree 

 worktree  Agent  Arena 

## 

|                               | qwen-code       | claude-code |     |
| --------------------------------- | --------------- | ----------- | ------- |
| `EnterWorktree`               | Phase A   |           | --       |
| `ExitWorktree`                | Phase A   |           | --       |
| AgentTool `isolation: 'worktree'` | Phase B   |           | --       |
|  worktree             | Phase B   |           | --       |
| worktree      |               |           | Phase C |
| Post-creation setuphooks  |               |           | Phase C |
| StatusLine worktree       |               |           | Phase C |
| WorktreeExitDialog    |               |           | Phase C |
| `--worktree` CLI          |               |           | Phase D |
| node_modules    |               |           | Phase D |
| sparse checkout                   |               |           | Future  |
| tmux                          |               |           | Future  |
| Arena  worktree         | qwen  |           | --       |
| stash + copy        |               |           | --       |
| Baseline commit               | qwen  |           | --       |

## 

**worktree Arena **

-  worktree :`EnterWorktree`/`ExitWorktree` AgentTool `isolation` 
- Arena :`worktreeBaseDir`  diff  `GitWorktreeService.setupWorktrees()` 

AgentTool  `isolation: 'worktree'` Arena  worktree

## 

###  worktree 

 `EnterWorktree`  AgentTool `isolation: 'worktree'`  worktree :

```
{git }/.qwen/worktrees/{slug}
```

slug :

-  worktree::`{}-{}-{4}`
- Agent worktree:`agent-{7 hex}`

### Arena worktree 

Arena  worktree  `agents.arena.worktreeBaseDir`  `~/.qwen/arena``ArenaManager.ts:125`

### 

|                         |        |                                                            |     |
| ----------------------------- | ---------- | -------------------------------------------------------------- | ------- |
| `worktree.symlinkDirectories` | `string[]` |  `node_modules` worktree | Phase D |
| `worktree.sparsePaths`        | `string[]` | git sparse-checkout cone  monorepo     | Future  |

Phase A / B / C 

## 

### EnterWorktree

**:**  "start a worktree""use a worktree""create a worktree" " bug"""

** schema:**

```
name?: string  // slug ://// 64 
```

**:**

1.  worktree 
2.  git 
3.  `GitWorktreeService`  worktree `.qwen/worktrees/{slug}`
4.  worktree  `SessionService`
5.  worktree 
6. 

**:** `worktreePath``worktreeBranch``message`

### ExitWorktree

**:**  "exit the worktree""leave the worktree""go back" 

** schema:**

```
action: 'keep' | 'remove'
discard_changes?: boolean  //  action='remove' 
```

**:**

-  `EnterWorktree`  worktree
- `action='remove'`  `discard_changes: true`

**:**

- `keep`: worktree  worktree 
- `remove`: worktree  git 

**:** `action``originalCwd``worktreePath``worktreeBranch`

## 

|            |                                                      |  |
| -------------- | -------------------------------------------------------- | -------- |
|  |  " worktree " ->  EnterWorktree | Phase A  |
| Agent      |  subagent  `isolation: 'worktree'`             | Phase B  |
| CLI    | `qwen --worktree my-feature`                             | Phase D  |

 worktree `isolation: 'worktree'` 

## 

### Phase A: worktree

**:**  /  worktree

**:**

- `EnterWorktree` : worktree
- `ExitWorktree` :keep / remove 
- `GitWorktreeService` : `createUserWorktree()` / `removeUserWorktree()`  git  Arena 
- `SessionService` : `WorktreeSession`  `{ slug, worktreePath, worktreeBranch, originalCwd, originalBranch }``--resume`  worktree 
-  prompt:

**:**

|                                                |                                       |
| -------------------------------------------------- | --------------------------------------------- |
| `packages/core/src/tools/tool-names.ts`            |  `ENTER_WORKTREE``EXIT_WORKTREE`    |
| `packages/core/src/tools/EnterWorktreeTool/`       | :`EnterWorktreeTool.ts``prompt.ts` |
| `packages/core/src/tools/ExitWorktreeTool/`        | :`ExitWorktreeTool.ts``prompt.ts`  |
| `packages/core/src/services/gitWorktreeService.ts` |  Arena        |
| `packages/core/src/services/sessionService.ts`     |  `WorktreeSession`          |
| `packages/core/src/tools/`                 |                                     |

** Phase A :**

- Agent Phase B
- hooks  post-creation setupPhase C
- UI Phase C

---

### Phase B:Agent AgentTool `isolation: 'worktree'`+ 

**:**  subagent  worktreeagent 

**:**

_Agent :_

- `AgentTool`  `isolation?: 'worktree'` 
- Agent  worktreeslug:`agent-{7hex}`:`.qwen/worktrees/agent-{7hex}`
- Agent :
-  worktree : `.qwen/worktrees/` `agent-{7hex}`  30 fail-closed 

_:_

- `AgentTool` description  `isolation: 'worktree'`  claude-code `AgentTool/prompt.ts:272`
-  `buildWorktreeNotice()`: fork subagent  worktree  worktree agent claude-code `forkSubagent.ts:buildWorktreeNotice`

_:_

- review skill`SKILL.md`:review  `.qwen/tmp/review-pr-<n>` `qwen review fetch-pr`  worktree 

**Arena :** Arena  `isolation`  worktree Arena 

**:**

|                                                |                                                |
| -------------------------------------------------- | ------------------------------------------------------ |
| `packages/core/src/tools/agent/agent.ts`           |  `isolation`  worktree /         |
| `packages/core/src/tools/agent/fork-subagent.ts`   |  `buildWorktreeNotice()`  worktree   |
| `packages/core/src/services/gitWorktreeService.ts` |  `createAgentWorktree()` / `removeAgentWorktree()` |
| `packages/core/src/services/worktreeCleanup.ts`    | : worktree                        |

---

### Phase C:SessionService  + UI 

**:** worktree  worktree 

**:**

_SessionService worktree  + `--resume` :_

- `SessionService`  `WorktreeSession`  `{ slug, worktreePath, worktreeBranch, originalCwd, originalBranch }`
- `EnterWorktreeTool`  `sessionService.setWorktreeSession()` 
- `ExitWorktreeTool`  `sessionService.clearWorktreeSession()` 
- `--resume`  `targetDir` 

_Post-creation setup:_

-  worktree  `git config core.hooksPath <mainRepo>/.git/hooks` worktree  hooks 

_StatusLine worktree :_

- `UIStateContext`  `activeWorktree`  session  /  worktree 
- `StatusLineCommandInput` payload  `worktree?: { slug: string; branch: string }`  statusline 
- `Footer`  `activeWorktree`  ` <branch> (<slug>)` statusline 

_WorktreeExitDialog:_

-  `WorktreeExitDialog.tsx`  Dialog 
- Ctrl+C / Ctrl+D: `activeWorktree`  Dialog  keep  remove
- keep / remove  `ExitWorktreeTool` 

**:**

|                                                           |                                                                       |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `packages/core/src/services/sessionService.ts`                |  `WorktreeSession`                                          |
| `packages/core/src/tools/enter-worktree.ts`                   |  `sessionService.setWorktreeSession()`                                    |
| `packages/core/src/tools/exit-worktree.ts`                    |  `sessionService.clearWorktreeSession()`                                  |
| `packages/core/src/services/gitWorktreeService.ts`            | `createUserWorktree()` / `createAgentWorktree()`  `core.hooksPath`  |
| `packages/cli/src/ui/contexts/UIStateContext.tsx`             |  `activeWorktree`  set/clear action                                 |
| `packages/cli/src/ui/hooks/useStatusLine.ts`                  | `StatusLineCommandInput`  `worktree`                                  |
| `packages/cli/src/ui/components/Footer.tsx`                   |  worktree                                                           |
| `packages/cli/src/ui/components/WorktreeExitDialog.tsx`       |                                                                           |
| `packages/cli/src/ui/components/DialogManager.tsx`            |  `WorktreeExitDialog`                                                     |
| `packages/cli/src/ui/components/ExitWarning.tsx`  |  `activeWorktree`                                               |

---

### Phase D:`--worktree` CLI  + 

**:**  worktree

**:**

_`--worktree [name]` CLI :_

- `packages/cli/src/args.ts`  `--worktree [name]` 
-  `createUserWorktree()` `targetDir`  worktree  SessionService 
-  worktree  WorktreeExitDialog

_`worktree.symlinkDirectories` :_

- settings schema  `worktree.symlinkDirectories: string[]`
- `createUserWorktree()`  `fs.symlink()`  worktree
- 

**:**

|                                                |                                     |
| -------------------------------------------------- | ------------------------------------------- |
| `packages/cli/src/args.ts`                         |  `--worktree [name]`                |
| `packages/cli/src/main.ts`           |  `--worktree`  worktree |
| `packages/core/src/services/gitWorktreeService.ts` | `createUserWorktree()`  symlink   |
| `packages/core/src/config/`settings schema     |  `worktree.symlinkDirectories`      |

---

### Future:



|                     |                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| sparse checkout         | `worktree.sparsePaths`  monorepo  checkout    |
| `.worktreeinclude`  |  gitignore `.env``secrets.json`  worktree                         |
| tmux                | `--worktree --tmux`  tmux  worktree                                         |
| PR              | `--worktree=#123`  fetch PR  worktree Phase D `--worktree`  |
