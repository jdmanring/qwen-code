# Phase 1 :

## 1. 

### 1.1 

- sourcecommandTypesupportedModesuserInvocable / modelInvocable
-  capability-based  non-interactive/acp 
-  Phase 2/3 

### 1.2 

- ****:non-interactive  acp : MCP_PROMPT  bug fix
- ****:`SlashCommand` 
- ****: ModeAdapter / CommandExecutor  CommandService 
- ****: local  action 

---

## 2. 

### 2.1 

 `packages/cli/src/ui/commands/types.ts` `SlashCommand` 

### 2.2 `ExecutionMode`

```typescript
/**
 * 
 * - interactive:React/Ink UI 
 * - non_interactive: CLI /JSON 
 * - acp:ACP/Zed 
 */
export type ExecutionMode = 'interactive' | 'non_interactive' | 'acp';
```

### 2.3 `CommandSource`

```typescript
/**
 *  Help  badgeACP available commands
 *
 *  CommandKind :
 * - CommandKind 4 
 * - CommandSource 9 
 *
 * 
 */
export type CommandSource =
  | 'builtin-command' // BuiltinCommandLoader
  | 'bundled-skill' //  skillBundledSkillLoader
  | 'skill-dir-command' // / .qwen/commands/ FileCommandLoader
  | 'plugin-command' // FileCommandLoaderextensionName 
  | 'mcp-prompt'; // MCP server  promptMcpPromptLoader
// Phase 1  Loader schema :
// | 'workflow-command'
// | 'plugin-skill'
// | 'dynamic-skill'
// | 'builtin-plugin-skill'
// | 'mcp-skill'
```

### 2.4 `CommandType`

```typescript
/**
 * ""
 *
 * - prompt: submit_prompt skillfile commandMCP prompt
 *    supportedModes  modelInvocable  true
 *
 * - local: React/Ink UI messagestream_messages
 *   submit_prompttool  built-in 
 *    supportedModes  ['interactive'] supportedModes 
 *    Claude Code  supportsNonInteractive: true ----
 *
 * - local-jsx: React/Ink UI  dialog JSX 
 *    supportedModes  ['interactive']
 */
export type CommandType = 'prompt' | 'local' | 'local-jsx';
```

### 2.5  `SlashCommand` 

****:

```typescript
export interface SlashCommand {
  // --  ----------------------------------------------
  name: string;
  altNames?: string[];
  description: string;
  hidden?: boolean;
  completionPriority?: number;
  kind: CommandKind;
  extensionName?: string;
  action?: (...) => ...;
  completion?: (...) => ...;
  subCommands?: SlashCommand[];

  // -- Phase 1 : --------------------------------------
  /**
   *  Help  badgeACP available commands 
   *  Loader 
   *  CommandKind source 
   */
  source?: CommandSource;

  /**
   * 
   * - builtin-command -> "Built-in"
   * - bundled-skill -> "Skill"
   * - skill-dir-command -> "Custom"
   * - plugin-command -> "Plugin: <extensionName>"
   * - mcp-prompt -> "MCP: <serverName>"
   *  Loader 
   */
  sourceLabel?: string;

  /**
   * 
   * -  Loader prompt/local-jsx
   * - built-in local  local-jsx
   *  getEffectiveCommandType()
   */
  commandType?: CommandType;

  // -- Phase 1 : ------------------------------------------
  /**
   * 
   *  commandType  getEffectiveSupportedModes()
   * 
   */
  supportedModes?: ExecutionMode[];

  // -- Phase 1 : ----------------------------------------------
  /**
   *  slash command 
   *  true userInvocable
   */
  userInvocable?: boolean;

  /**
   *  tool call 
   *  falseprompt skillfile commandMCP prompt true
   * built-in commands  false
   */
  modelInvocable?: boolean;

  // -- Phase 3 :Phase 1 ------------------
  /**
   * 
   * :"<model-id>" / "show|list|set <id>" / "[--fast] [<model-id>]"
   */
  argumentHint?: string;

  /**
   * 
   *  modelInvocable  description 
   */
  whenToUse?: string;

  /**
   *  Help 
   */
  examples?: string[];
}
```

---

## 3.  Loader 

### 3.1 

- `source`  `sourceLabel`  Loader  `SlashCommand` 
- `commandType`:Loader built-in 
- `supportedModes`: `getEffectiveSupportedModes()` 
- `modelInvocable`:Loader built-in  `false`prompt  `true`

### 3.2 `BuiltinCommandLoader`

```typescript
//  source/sourceLabel/commandType -- 
//  built-in  commandType  local  local-jsx

//  source  sourceLabel:
for (const cmd of rawCommands) {
  enrichedCommands.push({
    ...cmd,
    source: 'builtin-command',
    sourceLabel: 'Built-in',
    userInvocable: cmd.userInvocable ?? true,
    modelInvocable: false, // built-in 
  });
}
```

### 3.3 `BundledSkillLoader`

```typescript
return skills.map((skill) => ({
  name: skill.name,
  description: skill.description,
  kind: CommandKind.SKILL,
  source: 'bundled-skill' as CommandSource,
  sourceLabel: 'Skill',
  commandType: 'prompt' as CommandType,
  userInvocable: true,
  modelInvocable: true,
  action: async (...) => { ... },
}));
```

### 3.4 `FileCommandLoader`

```typescript
//  createSlashCommandFromDefinition :
return {
  name: baseCommandName,
  description,
  kind: CommandKind.FILE,
  extensionName,
  // source  extensionName :
  source: extensionName ? 'plugin-command' : 'skill-dir-command',
  sourceLabel: extensionName ? `Plugin: ${extensionName}` : 'Custom',
  commandType: 'prompt',
  userInvocable: true,
  modelInvocable: !extensionName, // /
  action: async (...) => { ... },
};
```

> ****:plugin-command `modelInvocable` Phase 

### 3.5 `McpPromptLoader`

```typescript
const newPromptCommand: SlashCommand = {
  name: commandName,
  description: prompt.description || `Invoke prompt ${prompt.name}`,
  kind: CommandKind.MCP_PROMPT,
  source: 'mcp-prompt',
  sourceLabel: `MCP: ${serverName}`,
  commandType: 'prompt',
  userInvocable: true,
  modelInvocable: true,
  // ... 
};
```

---

## 4. Built-in  `commandType` 

### 4.1 

| commandType |                                                                                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `local`     | action  `ui.addItem` `message` / `stream_messages` / `submit_prompt` / `tool` React                                                |
| `local-jsx` | action  `dialog` action  `ui.addItem`  JSX  `HistoryItemHelp``HistoryItemStats` `confirm_action` / `load_history` / `quit` |

> ****:`ui.addItem(message/error/info )`  `local``ui.addItem(help/stats/tools/about  UI )`  `local-jsx`

### 4.2 Built-in 

**`local` ** `commandType: 'local'``supportedModes`  all modes:

|              |      |                                                     |
| -------------------- | ---------- | ------------------------------------------------------- |
| `btwCommand.ts`      | `btw`      |  `submit_prompt`  `stream_messages`               |
| `bugCommand.ts`      | `bug`      |  `submit_prompt`  `stream_messages`               |
| `compressCommand.ts` | `compress` |  executionMode  `message`/`submit_prompt` |
| `contextCommand.ts`  | `context`  |  `message` UI                 |
| `exportCommand.ts`   | `export`   |  I/O `message`                                |
| `initCommand.ts`     | `init`     |  `submit_prompt`/`message`/`confirm_action`         |
| `memoryCommand.ts`   | `memory`   |  `message` I/O                        |
| `planCommand.ts`     | `plan`     |  `submit_prompt`                                    |
| `summaryCommand.ts`  | `summary`  |  executionMode  `submit_prompt`/`message` |
| `insightCommand.ts`  | `insight`  |  `stream_messages`                                  |

> ****:`contextCommand`  `insightCommand`  `addItem`  `local`

**`local-jsx` ** `commandType: 'local-jsx'``supportedModes`  `['interactive']`:

|                   |            |  headless                        |
| ------------------------- | ---------------- | ------------------------------------------ |
| `aboutCommand.ts`         | `about`          | `addItem(HistoryItemAbout)` --  UI  |
| `agentsCommand.ts`        | `agents`         | `dialog: subagent_create/subagent_list`    |
| `approvalModeCommand.ts`  | `approval-mode`  | `dialog: approval-mode`                    |
| `arenaCommand.ts`         | `arena`          | `dialog: arena_*`                          |
| `authCommand.ts`          | `auth`           | `dialog: auth`                             |
| `clearCommand.ts`         | `clear`          | `ui.clear()`                   |
| `copyCommand.ts`          | `copy`           |  headless                |
| `directoryCommand.tsx`    | `directory`      | JSX                                    |
| `docsCommand.ts`          | `docs`           |                                  |
| `editorCommand.ts`        | `editor`         | `dialog: editor`                           |
| `extensionsCommand.ts`    | `extensions`     | `dialog: extensions_manage`                |
| `helpCommand.ts`          | `help`           | `addItem(HistoryItemHelp)` --  Help UI  |
| `hooksCommand.ts`         | `hooks`          | `dialog: hooks`                            |
| `ideCommand.ts`           | `ide`            | IDE                          |
| `languageCommand.ts`      | `language`       | `dialog` + `reloadCommands`                |
| `mcpCommand.ts`           | `mcp`            | `dialog: mcp`                              |
| `modelCommand.ts`         | `model`          | `dialog: model/fast-model`                 |
| `permissionsCommand.ts`   | `permissions`    | `dialog: permissions`                      |
| `quitCommand.ts`          | `quit`           | `quit` result                          |
| `restoreCommand.ts`       | `restore`        | `load_history` result                  |
| `resumeCommand.ts`        | `resume`         | `dialog: resume`                           |
| `settingsCommand.ts`      | `settings`       | `dialog: settings`                         |
| `setupGithubCommand.ts`   | `setup-github`   | `confirm_shell_commands` +       |
| `skillsCommand.ts`        | `skills`         | `addItem(HistoryItemSkillsList)` --  UI |
| `statsCommand.ts`         | `stats`          | `addItem(HistoryItemStats)` --  UI      |
| `statuslineCommand.ts`    | `statusline`     | UI                                 |
| `terminalSetupCommand.ts` | `terminal-setup` |                                |
| `themeCommand.ts`         | `theme`          | `dialog: theme`                            |
| `toolsCommand.ts`         | `tools`          | `addItem(HistoryItemTools)` --  UI      |
| `trustCommand.ts`         | `trust`          | `dialog: trust`                            |
| `vimCommand.ts`           | `vim`            | `toggleVimEnabled()` -- UI              |

---

## 5. `getEffectiveSupportedModes` 

 Phase 1  `filterCommandsForMode` 

```typescript
/**
 * 
 *
 * :
 * 1.  supportedModes
 * 2.  commandType 
 * 3.  CommandKind 
 */
export function getEffectiveSupportedModes(cmd: SlashCommand): ExecutionMode[] {
  //  1:
  if (cmd.supportedModes !== undefined) {
    return cmd.supportedModes;
  }

  //  2: commandType 
  if (cmd.commandType !== undefined) {
    switch (cmd.commandType) {
      case 'prompt':
        // prompt  UI 
        return ['interactive', 'non_interactive', 'acp'];
      case 'local':
        // local : interactive
        //  supportedModes Claude Code  supportsNonInteractive: true
        // Phase 2  headless 
        return ['interactive'];
      case 'local-jsx':
        return ['interactive'];
    }
  }

  //  3: CommandKind
  switch (cmd.kind) {
    case CommandKind.BUILT_IN:
      // built-in  commandType interactive only
      //  Phase 1  built-in  commandType
      return ['interactive'];
    case CommandKind.FILE:
    case CommandKind.SKILL:
    case CommandKind.MCP_PROMPT:
      //  action  UI 
      return ['interactive', 'non_interactive', 'acp'];
    default:
      return ['interactive'];
  }
}
```

```typescript
/**
 *  supportedModes 
 *  filterCommandsForNonInteractive 
 */
export function filterCommandsForMode(
  commands: readonly SlashCommand[],
  mode: ExecutionMode,
): SlashCommand[] {
  return commands.filter((cmd) =>
    getEffectiveSupportedModes(cmd).includes(mode),
  );
}
```

---

## 6. `CommandService` 

 `packages/cli/src/services/CommandService.ts` :

```typescript
export class CommandService {
  // -- ------------------------------------------------
  getCommands(): readonly SlashCommand[] {
    return this.commands;
  }

  // -- Phase 1  --------------------------------------------------

  /**
   * 
   *  + filterCommandsForNonInteractive 
   *
   * @param mode 
   * @returns  hidden 
   */
  getCommandsForMode(mode: ExecutionMode): readonly SlashCommand[] {
    return this.commands.filter((cmd) => {
      if (cmd.hidden) return false;
      return getEffectiveSupportedModes(cmd).includes(mode);
    });
  }

  /**
   *  modelInvocable  true 
   * Phase 2  SkillTool Phase 1 
   *
   * @returns 
   */
  getModelInvocableCommands(): readonly SlashCommand[] {
    return this.commands.filter(
      (cmd) => !cmd.hidden && cmd.modelInvocable === true,
    );
  }
}
```

> ****:`getEffectiveSupportedModes`  `filterCommandsForMode`  `CommandService`  `packages/cli/src/services/commandUtils.ts` 

---

## 7. `nonInteractiveCliCommands.ts` 

### 7.1 

```typescript
//  
export const ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE = [
  'init', 'summary', 'compress', 'btw', 'bug', 'context',
] as const;

//  
function filterCommandsForNonInteractive(
  commands: readonly SlashCommand[],
  allowedBuiltinCommandNames: Set<string>,
): SlashCommand[] { ... }
```

### 7.2 

```typescript
//   commandUtils 
import { filterCommandsForMode } from '../services/commandUtils.js';
```

### 7.3 `handleSlashCommand` 

```typescript
//  
export const handleSlashCommand = async (
  rawQuery: string,
  abortController: AbortController,
  config: Config,
  settings: LoadedSettings,
  allowedBuiltinCommandNames: string[] = [...ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE],
): Promise<NonInteractiveSlashCommandResult>

//   allowedBuiltinCommandNames
export const handleSlashCommand = async (
  rawQuery: string,
  abortController: AbortController,
  config: Config,
  settings: LoadedSettings,
): Promise<NonInteractiveSlashCommandResult>
```

### 7.4 

```typescript
// :
const filteredCommands = filterCommandsForNonInteractive(
  allCommands,
  allowedBuiltinSet,
);

// :
const executionMode = isAcpMode ? 'acp' : 'non_interactive';
const filteredCommands = filterCommandsForMode(allCommands, executionMode);
```

### 7.5 `getAvailableCommands` 

```typescript
//  
export const getAvailableCommands = async (
  config: Config,
  abortSignal: AbortSignal,
  allowedBuiltinCommandNames: string[] = [...ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE],
): Promise<SlashCommand[]>

//  
export const getAvailableCommands = async (
  config: Config,
  abortSignal: AbortSignal,
  mode: ExecutionMode = 'acp',
): Promise<SlashCommand[]>
```

>  `mode` ACP Session  `'acp'`non-interactive  `'non_interactive'`

---

## 8. `Session.ts`ACP

```typescript
//  
const slashCommandResult = await handleSlashCommand(
  inputText,
  abortController,
  this.config,
  this.settings,
  // 
);

//  
const slashCommandResult = await handleSlashCommand(
  inputText,
  abortController,
  this.config,
  this.settings,
);

// -----------------------------------------

//  
const slashCommands = await getAvailableCommands(
  this.config,
  abortController.signal,
);

//   mode
const slashCommands = await getAvailableCommands(
  this.config,
  abortController.signal,
  'acp',
);
```

---

## 9. 

### 9.1 

|                                                                     |                                                                                          |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `packages/cli/src/ui/commands/types.ts`                                 |  `ExecutionMode``CommandSource``CommandType`  `SlashCommand`               |
| `packages/cli/src/services/CommandService.ts`                           |  `getCommandsForMode()``getModelInvocableCommands()`                                   |
| `packages/cli/src/nonInteractiveCliCommands.ts`                         |  `filterCommandsForMode`                 |
| `packages/cli/src/acp-integration/session/Session.ts`                   |  `handleSlashCommand`  `getAvailableCommands`                                          |
| `packages/cli/src/services/BuiltinCommandLoader.ts`                     |  `source: 'builtin-command'``sourceLabel: 'Built-in'``modelInvocable: false` |
| `packages/cli/src/services/BundledSkillLoader.ts`                       |  `source: 'bundled-skill'``commandType: 'prompt'``modelInvocable: true`                  |
| `packages/cli/src/services/FileCommandLoader.ts` / `command-factory.ts` |  `source``commandType: 'prompt'``modelInvocable` extensionName                   |
| `packages/cli/src/services/McpPromptLoader.ts`                          |  `source: 'mcp-prompt'``commandType: 'prompt'``modelInvocable: true`                     |
| ** built-in 10  local + 27  local-jsx**               |  `commandType: 'local'`  `commandType: 'local-jsx'`                                        |

### 9.2 

|                                         |                                                                        |
| ------------------------------------------- | -------------------------------------------------------------------------- |
| `packages/cli/src/services/commandUtils.ts` | `getEffectiveSupportedModes()``filterCommandsForMode()`  |

### 9.3 

- `packages/cli/src/utils/commands.ts``parseSlashCommand` 
- `packages/cli/src/ui/hooks/slashCommandProcessor.ts`interactive 
- `packages/cli/src/ui/noninteractive/nonInteractiveUi.ts`stub UI 
-  `action` Phase 1 

---

## 10. 

### 10.1 

|                                  |                        |                                                    |         |
| ------------------------------------ | ---------------------------- | -------------------------------------------------------- | ----------- |
| non-interactive  `/init`       |              |  `commandType: local`                          |       |
| non-interactive  `/summary`    |                        |                                                    |       |
| non-interactive  `/compress`   |                        |                                                    |       |
| non-interactive  `/btw`        |                        |                                                    |       |
| non-interactive  `/bug`        |                        |                                                    |       |
| non-interactive  `/context`    |                        |                                                    |       |
| non-interactive  `/model`      |  unsupported               |  unsupported`commandType: local-jsx`               |       |
| non-interactive  file command  |  CommandKind.FILE  |  `commandType: prompt`                         |       |
| non-interactive  bundled skill |  CommandKind.SKILL |  `commandType: prompt`                         |       |
| non-interactive  MCP prompt    |   CommandKind        |  `commandType: prompt`                         | **Bug fix** |
| non-interactive  `/export`     |                  |  `commandType: local` interactive only |       |
| non-interactive  `/memory`     |                  |  `commandType: local` interactive only |       |
| non-interactive  `/plan`       |                  |  `commandType: local` interactive only |       |

> ** `local` **:`commandType: 'local'`  `supportedModes`  `['interactive']` Claude Code ----`local`  `supportsNonInteractive: true` Phase 1  6 `init``summary``compress``btw``bug``context` `supportedModes: ['interactive', 'non_interactive', 'acp']` Phase 2  `/export``/memory``/plan` action  headless-friendly 

---

## 10.2 Phase 2 :

 Phase 2 " UI" `/model` **** `action` 

 Claude Code  `/context`  `src/commands/context/index.ts`: `Command`  `local-jsx`  interactive `local`  non-interactive `isEnabled()` 

Qwen Code  Phase 2  `supportedModes`  `isEnabled()` :

```typescript
//  :local-jsx interactive
export const modelCommandInteractive: SlashCommand = {
  name: 'model',
  kind: CommandKind.BUILT_IN,
  commandType: 'local-jsx',
  supportedModes: ['interactive'], // 
  // action:  dialog  model
};

//  /acp :local headless 
export const modelCommandHeadless: SlashCommand = {
  name: 'model',
  kind: CommandKind.BUILT_IN,
  commandType: 'local',
  supportedModes: ['non_interactive', 'acp'], // 
  // action: / model message
};
```

`supportedModes` `filterCommandsForMode`  Claude Code  `isEnabled()` `supportedModes` 

**Phase 1 ** Phase 2 

---

## 11. 

### 11.1 

 `packages/cli/src/services/commandUtils.test.ts`:

```typescript
describe('getEffectiveSupportedModes', () => {
  it(' supportedModes  commandType ', () => {
    const cmd: SlashCommand = {
      name: 'test', description: '', kind: CommandKind.BUILT_IN,
      commandType: 'local',
      supportedModes: ['interactive'], // 
    };
    expect(getEffectiveSupportedModes(cmd)).toEqual(['interactive']);
  });

  it('commandType: local  all modes', () => {
    const cmd: SlashCommand = { name: 'test', description: '', kind: CommandKind.BUILT_IN, commandType: 'local' };
    expect(getEffectiveSupportedModes(cmd)).toEqual(['interactive', 'non_interactive', 'acp']);
  });

  it('commandType: local-jsx  interactive only', () => {
    const cmd: SlashCommand = { name: 'test', description: '', kind: CommandKind.BUILT_IN, commandType: 'local-jsx' };
    expect(getEffectiveSupportedModes(cmd)).toEqual(['interactive']);
  });

  it('commandType: prompt  all modes', () => {
    const cmd: SlashCommand = { name: 'test', description: '', kind: CommandKind.SKILL, commandType: 'prompt' };
    expect(getEffectiveSupportedModes(cmd)).toEqual(['interactive', 'non_interactive', 'acp']);
  });

  it(' commandType  CommandKind.BUILT_IN interactive', () => {
    const cmd: SlashCommand = { name: 'test', description: '', kind: CommandKind.BUILT_IN };
    expect(getEffectiveSupportedModes(cmd)).toEqual(['interactive']);
  });

  it(' commandType  CommandKind.FILE all modes', () => {
    const cmd: SlashCommand = { name: 'test', description: '', kind: CommandKind.FILE };
    expect(getEffectiveSupportedModes(cmd)).toEqual(['interactive', 'non_interactive', 'acp']);
  });

  it(' commandType  CommandKind.MCP_PROMPT all modes', () => {
    const cmd: SlashCommand = { name: 'test', description: '', kind: CommandKind.MCP_PROMPT };
    expect(getEffectiveSupportedModes(cmd)).toEqual(['interactive', 'non_interactive', 'acp']);
  });
});

describe('filterCommandsForMode', () => {
  it(' non_interactive ', () => { ... });
  it(' acp ', () => { ... });
  it(' hidden filterCommandsForMode  hiddenCommandService ', () => { ... });
});
```

### 11.2  `nonInteractiveCliCommands.test.ts`

-  `ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE` 
-  `allowedBuiltinCommandNames` 
- : commandType: local  non-interactive 
- : commandType: local-jsx  non-interactive 
- : file command / skill command  non-interactive 

### 11.3  `CommandService.test.ts`

-  `getCommandsForMode` 
-  `getModelInvocableCommands` 

### 11.4  Loader 

- `BuiltinCommandLoader.test.ts`: `source: 'builtin-command'`
- `BundledSkillLoader.test.ts`: `source: 'bundled-skill'`  `modelInvocable: true`
- `FileCommandLoader.test.ts`: `source: 'skill-dir-command'` `source: 'plugin-command'`
- `McpPromptLoader.test.ts`: `source: 'mcp-prompt'`  `modelInvocable: true`

---

## 12. 

 commit  review:

**Step 1**~30min: `types.ts` `ExecutionMode``CommandSource``CommandType`  `SlashCommand` 
-> TypeScript 

**Step 2**~1h: `commandUtils.ts` `getEffectiveSupportedModes`  `filterCommandsForMode` `commandUtils.test.ts`
-> 

**Step 3**~1h: `nonInteractiveCliCommands.ts` `filterCommandsForMode`
-> Phase 1 :local  `supportedModes: ['interactive']`

**Step 4**~30min: `CommandService.ts`

**Step 5**~2h: built-in  `commandType` 
-> 

**Step 6**~1.5h: Loader `source``sourceLabel``commandType``modelInvocable`

**Step 7**~30min: `Session.ts` 

**Step 8**~1h:

**Step 9**~30min:CR :

---

## 13.  Checklist

- [ ] TypeScript `npm run typecheck`
- [ ] `npm run lint`  lint 
- [ ] `cd packages/cli && npx vitest run`
- [ ] `commandUtils.test.ts` 
- [ ] `getEffectiveSupportedModes`  7  case
- [ ] `filterCommandsForMode`  interactive / non_interactive / acp 
- [ ] `ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE` `grep` 
- [ ] `filterCommandsForNonInteractive` 
- [ ]  built-in  `commandType` 
- [ ]  Loader  `source`  `sourceLabel` 
- [ ] `BundledSkillLoader` / `FileCommandLoader`/ `McpPromptLoader`  `modelInvocable: true`
- [ ] `BuiltinCommandLoader`  `modelInvocable: false`
- [ ] `CommandService.getCommandsForMode('non_interactive')` 
- [ ] MCP prompt  non-interactive 
