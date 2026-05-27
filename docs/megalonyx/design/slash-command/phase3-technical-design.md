# Phase 3 :

## 1. 

### 1.1 

Phase 3  Phase 1/2  prompt command  slash command :

- alias  session 
-  mid-input slash command  ghost text token 
-  `/help`  Claude Code  tab
-  ACP `available_commands_update` 
-  `/doctor` `/release-notes` 

### 1.2 

- ****:Phase 1/2 
- ****: `SlashCommand``CommandService``handleSlashCommand``useSlashCompletion`  `Help`  `CommandDescriptor` / `CommandExecutor` / `ModeAdapter`
- ** `commandType`**: Phase 1  `commandType` Phase 3 
- **session  recently used**: CLI session 
- **interactive **:helpdoctor  interactive Phase 3 
- **ACP **:`availableCommands[].name``description``input`  `_meta`  ACP 

---

## 2. 

### 2.1  Loader 

`packages/cli/src/ui/commands/types.ts`  `SlashCommand` :

- `source?: CommandSource`
- `sourceLabel?: string`
- `supportedModes?: ExecutionMode[]`
- `userInvocable?: boolean`
- `modelInvocable?: boolean`
- `argumentHint?: string`
- `whenToUse?: string`
- `examples?: string[]`

`CommandSource` :

```typescript
export type CommandSource =
  | 'builtin-command'
  | 'bundled-skill'
  | 'skill-dir-command'
  | 'plugin-command'
  | 'mcp-prompt';
```

 Loader :

| Loader                                  | source                                 | sourceLabel                              | argumentHint     | modelInvocable                                   |
| --------------------------------------- | -------------------------------------- | ---------------------------------------- | ---------------- | ------------------------------------------------ |
| `BuiltinCommandLoader`                  | `builtin-command`                      | `Built-in`                               |        | `false`                                          |
| `BundledSkillLoader`                    | `bundled-skill`                        | `Skill`                                  |  skill       | `!disableModelInvocation`                        |
| `FileCommandLoader` / `command-factory` | `skill-dir-command` / `plugin-command` | `Custom` / `Plugin: <extensionName>`     |  frontmatter | / true description/whenToUse |
| `SkillCommandLoader`                    | `skill-dir-command` / `plugin-command` | `User` / `Project` / `Extension: <name>` |  skill       | / true description/whenToUse |
| `McpPromptLoader`                       | `mcp-prompt`                           | `MCP: <serverName>`                      |            |  `modelInvocable`                  |

> :Phase 1  MCP prompt `modelInvocable: true`Phase 3  MCP prompt MCP prompt  MCP  `SkillTool` 

### 2.2  Phase 3 

|                                                  |                                                                                                 |                                                          |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| mid-input slash  ghost text                      |  `modelInvocable`                                                         | `ui/utils/commandUtils.ts``ui/hooks/useCommandCompletion.tsx`  |
| line-start  argument ghost text                  |  args  `argumentHint`                                                 | `ui/hooks/useCommandCompletion.tsx`                              |
| alias                                        |  alias alias                                            | `ui/hooks/useSlashCompletion.ts`                                 |
| source badge                                         |  MCP  `[MCP]`                                                                                     | `ui/components/SuggestionsDisplay.tsx``ui/components/Help.tsx` |
| `/help`                                              | : Claude Code  tab | `ui/components/Help.tsx`                                         |
| ACP `argumentHint`                                   |  `availableCommands[].input.hint`                                                               | `acp-integration/session/Session.ts`                             |
| ACP source/supportedModes/subcommands/modelInvocable |                                                                                                   | `acp-integration/session/Session.ts`                             |
|                                              | extension  `extensionName.commandName` extension          | `services/CommandService.ts`                                     |
| `/doctor`                                            |  `interactive` / `non_interactive` / `acp`                                                  | `ui/commands/doctorCommand.ts``utils/doctorChecks.ts`          |

### 2.3 Claude Code 

 `/Users/mochi/code/claude-code` :

- `src/types/command.ts`: `argumentHint``whenToUse``aliases``loadedFrom``kind``immediate``isSensitive``userFacingName``supportsNonInteractive` /
- `src/utils/suggestions/commandSuggestions.ts`:alias prefixfuzzyskill usagealias  alias
- `src/utils/suggestions/commandSuggestions.ts`:mid-input slash  `findMidInputSlashCommand()``getBestCommandMatch()`  `findSlashCommandPositions()`  ghost text 
- `src/components/HelpV2/Commands.tsx`:Help V2 
- `src/commands.ts`:Claude Code  `/doctor``/release-notes` Qwen Code  `/doctor` `/release-notes`

Phase 3 ""

---

## 3. 

### 3.1 

|                                                     |                                                                   |
| ------------------------------------------------------- | ------------------------------------------------------------------------- |
| `packages/cli/src/ui/components/SuggestionsDisplay.tsx` |  `Suggestion`  source badgeargumentHintaliasHit         |
| `packages/cli/src/ui/hooks/useSlashCompletion.ts`       |  recently used alias                |
| `packages/cli/src/ui/hooks/useCommandCompletion.tsx`    | mid-input ghost text  argument/source  UI   |
| `packages/cli/src/ui/utils/commandUtils.ts`             |  slash token                |
| `packages/cli/src/ui/components/InputPrompt.tsx`        |  slash command token  Tab  ghost text               |
| `packages/cli/src/ui/components/Help.tsx`               |  Claude Code  tab                     |
| `packages/cli/src/ui/commands/helpCommand.ts`           |  non-interactive/acp  action interactive UI |
| `packages/cli/src/acp-integration/session/Session.ts`   |  ACP update                                             |
| `packages/cli/src/ui/commands/*Command.ts`              |  built-in  `argumentHint`                                   |

### 3.2 

 `packages/cli/src/services/commandMetadata.ts` HelpCompletionACP :

```typescript
export function getCommandSourceBadge(cmd: SlashCommand): string | null;
export function getCommandSourceGroup(cmd: SlashCommand): CommandSourceGroup;
export function formatSupportedModes(cmd: SlashCommand): string;
export function getCommandDisplayName(cmd: SlashCommand): string;
export function getCommandSubcommandNames(cmd: SlashCommand): string[];
```

 Loader Loader  UI 

---

## 4. Phase 3.1:

### 4.1  `Suggestion` 

:

```typescript
export interface Suggestion {
  label: string;
  value: string;
  description?: string;
  matchedIndex?: number;
  commandKind?: CommandKind;
}
```

:

```typescript
export interface Suggestion {
  label: string;
  value: string;
  description?: string;
  matchedIndex?: number;
  commandKind?: CommandKind;

  // Phase 3
  source?: CommandSource;
  sourceLabel?: string;
  sourceBadge?: string;
  argumentHint?: string;
  matchedAlias?: string;
  supportedModes?: ExecutionMode[];
  modelInvocable?: boolean;
}
```

`mode !== 'slash'` reverse search 

### 4.2 source badge 

 `SuggestionsDisplay`  `CommandKind.MCP_PROMPT`  `[MCP]`Phase 3  `source` / `sourceLabel`  badge:

| source / sourceLabel              | badge                                      |
| --------------------------------- | ------------------------------------------ |
| `builtin-command`                 | `[Built-in]`: |
| `bundled-skill` / `Skill`         | `[Skill]`                                  |
| `skill-dir-command` / `User`      | `[User]`                                   |
| `skill-dir-command` / `Project`   | `[Project]`                                |
| `skill-dir-command` / `Custom`    | `[Custom]`                                 |
| `plugin-command` / `Plugin: x`    | `[Plugin]`  `[Plugin: x]`                |
| `plugin-command` / `Extension: x` | `[Extension]`  `[Extension: x]`          |
| `mcp-prompt`                      | `[MCP]`                                    |

:

```typescript
function getCommandSourceBadge(cmd: SlashCommand): string | null {
  switch (cmd.source) {
    case 'bundled-skill':
      return '[Skill]';
    case 'skill-dir-command':
      return cmd.sourceLabel === 'User'
        ? '[User]'
        : cmd.sourceLabel === 'Project'
          ? '[Project]'
          : '[Custom]';
    case 'plugin-command':
      return '[Plugin]';
    case 'mcp-prompt':
      return '[MCP]';
    case 'builtin-command':
    default:
      return null;
  }
}
```

>  `[Built-in]`  UI Help  Built-in  built-in badge badge

### 4.3 argument hint 

 `argumentHint`:

```text
/model <model-id>              Switch model
/export md|html|json|jsonl     Export current session
/review [pr-number] [--comment] [Skill] Review changed code
```

:

- `useSlashCompletion`  `finalSuggestions`  `argumentHint: cmd.argumentHint`
- `SuggestionsDisplay`  label  `theme.text.secondary`  `argumentHint`
- `commandColumnWidth`  label + hint + badge
-  `argumentHint`

 built-in  `argumentHint`:

|              | argumentHint            |
| ---------------- | ----------------------- | ------------------ | -------- | ------------- | ------- |
| `/model`         | `[--fast] [<model-id>]` |
| `/approval-mode` | `<mode>`                |
| `/language`      | `ui                     | output <language>` |
| `/export`        | `md                     | html               | json     | jsonl [path]` |
| `/memory`        | `show                   | add                | refresh` |
| `/mcp`           | `desc                   | nodesc             | schema   | auth          | noauth` |
| `/stats`         | `[model                 | tools]`            |
| `/docs`          |               |
| `/doctor`        |               |

### 4.4 recently used 

#### 4.4.1 

 `useSlashCommandProcessor`  `AppContainer`  session :

```typescript
type RecentSlashCommand = {
  name: string;
  usedAt: number;
  count: number;
};
```

 `Map<string, RecentSlashCommand>` key  `cmd.name`

#### 4.4.2 

 `useSlashCommandProcessor.handleSlashCommand`  `commandToExecute` :

- 
- hidden 
- alias  canonical `commandToExecute.name` 
- 

#### 4.4.3 

 `compareRankedCommandMatches()` :

1. matchStrength
2. completionPriority
3. fzf score
4. match start
5. item length
6. original index

Phase 3  `recentScore`:

```typescript
return (
  right.matchStrength - left.matchStrength ||
  right.completionPriority - left.completionPriority ||
  right.recentScore - left.recentScore ||
  right.score - left.score ||
  left.start - right.start ||
  left.itemLength - right.itemLength ||
  left.originalIndex - right.originalIndex
);
```

`recentScore` :

```typescript
const RECENT_DECAY_MS = 10 * 60 * 1000;
const recentScore = count * 10 + Math.max(0, 10 - ageMs / RECENT_DECAY_MS);
```

 query  `/`recently used  query 

### 4.5 alias 

 alias  `AsyncFzf`  prefix fallback `formatSlashCommandLabel()`  alias:

```text
help (?)
compress (summarize)
```

Phase 3 :

- : alias
-  alias: `help (alias: ?)`
- `Suggestion.matchedAlias` 

:

```typescript
function findMatchedAlias(
  cmd: SlashCommand,
  query: string,
): string | undefined {
  return cmd.altNames?.find((alt) =>
    alt.toLowerCase().startsWith(query.toLowerCase()),
  );
}
```

 FZF  `result.item`  `altNames` `matchedAlias`prefix fallback 

---

## 5. Phase 3.2:mid-input slash command 

### 5.1 

 `findMidInputSlashCommand()` " `/xxx` token" cursor  token `getBestSlashCommandMatch()`  `modelInvocable`  prefix 

 Phase 2  Phase 3 

### 5.2 ghost text 

:mid-input slash  `modelInvocable`  slash command 

:

-  prefix  `useSlashCompletion`  `completionPriority`  recently used
- :

```typescript
export type BestSlashCommandMatch = {
  suffix: string;
  fullCommand: string;
  command: SlashCommand;
  sourceBadge?: string;
  argumentHint?: string;
};
```

### 5.3 mid-input source badge  argument hint

 ghost text  badge  hint  ghost text :

- ghost text  `please /rev`  `iew`
-  token  `argumentHint`  cursor  `/review [pr-number] [--comment]`
- source badge  dropdown  mid-input  dropdown badge

### 5.4  token 

 Claude Code `findSlashCommandPositions()` `InputPrompt.renderLineWithHighlighting()`  slash command token 

:

```typescript
export type SlashCommandToken = {
  start: number;
  end: number;
  commandName: string;
  valid: boolean;
};

export function findSlashCommandTokens(
  text: string,
  commands: readonly SlashCommand[],
): SlashCommandToken[];
```

:

- token 
- token  `/[a-zA-Z][a-zA-Z0-9:_-]*`
-  mid-input  `modelInvocable`  valid
- line-start token  interactive  valid
- valid token  accent invalid token  `/usr/bin` 

---

## 6. Phase 3.3:Help 

### 6.1 

`Help.tsx` :

- Basics
-  `Commands:`
- `[MCP]` 
- Keyboard Shortcuts

:

- skillcustompluginMCP 
-  `argumentHint`
-  `supportedModes`
-  `modelInvocable`
- /mode

### 6.2 

 `source` / `sourceLabel` :

1. **Built-in Commands**:`source === 'builtin-command'`
2. **Bundled Skills**:`source === 'bundled-skill'`
3. **Custom Commands**:`source === 'skill-dir-command'` `Custom` / `User` / `Project`
4. **Plugin Commands**:`source === 'plugin-command'` `Plugin:*` / `Extension:*`
5. **MCP Commands**:`source === 'mcp-prompt'`
6. **Other Commands**:source 

hidden 

### 6.3 

:

```text
/model [--fast] [<model-id>]  Switch model
  source: Built-in  modes: interactive, non_interactive, acp

/review [pr-number] [--comment]  Review changed code
  source: Skill  modes: interactive, non_interactive, acp  model: yes
```

 Help :

```text
 /review [pr-number] [--comment] [Skill] [all] [model] - Review changed code
```

mode badge :

| supportedModes                      | badge            |
| ----------------------------------- | ---------------- |
| `interactive` only                  | `[interactive]`  |
| `interactive, non_interactive, acp` | `[all]`          |
| `non_interactive, acp`              | `[headless]`     |
|                             | `[i] [ni] [acp]` |

### 6.4 `/help`  headless

 `/help`  non-interactive/acp `/help`  `supportedModes: ['interactive']`

Phase 3  headless :

- `supportedModes`  all modes
- interactive: `HistoryItemHelp`
- non_interactive/acp: `message`

 scope  interactive `Help` headless `/help` 

---

## 7. Phase 3.4:ACP available commands 

### 7.1  ACP 

`Session.sendAvailableCommandsUpdate()`  `SlashCommand[]` :

```typescript
{
  name: cmd.name,
  description: cmd.description,
  input: cmd.argumentHint ? { hint: cmd.argumentHint } : null,
}
```

 `argumentHint`  `input.hint` 

### 7.2 

ACP protocol  `AvailableCommand`  `_meta` :

```typescript
const availableCommands: AvailableCommand[] = slashCommands.map((cmd) => ({
  name: cmd.name,
  description: cmd.description,
  input: cmd.argumentHint ? { hint: cmd.argumentHint } : null,
  _meta: {
    argumentHint: cmd.argumentHint,
    source: cmd.source,
    sourceLabel: cmd.sourceLabel,
    supportedModes: cmd.supportedModes ?? getEffectiveSupportedModes(cmd),
    subcommands: cmd.subCommands
      ?.filter((sub) => !sub.hidden)
      .map((sub) => sub.name),
    modelInvocable: cmd.modelInvocable === true,
  },
}));
```

 `AvailableCommand` :

```typescript
{
  name,
  description,
  input,
  argumentHint,
  source,
  supportedModes,
  subcommands,
  modelInvocable,
}
```

 `_meta` 

### 7.3 subcommands 

 `subcommands` :

```typescript
subcommands: cmd.subCommands?.map((sub) => sub.name) ?? [];
```

 ACP :

```typescript
type AcpSubcommandMeta = {
  name: string;
  description?: string;
  argumentHint?: string;
  subcommands?: AcpSubcommandMeta[];
};
```

---

## 8. Phase 3.5:Claude Code 

### 8.1 `/doctor`:

 `doctorCommand` :

- :`packages/cli/src/ui/commands/doctorCommand.ts`
- :`BuiltinCommandLoader`
- :`['interactive', 'non_interactive', 'acp']`
- interactive: `HistoryItemDoctor`
- non_interactive/acp: JSON `message`
- :`packages/cli/src/utils/doctorChecks.ts`

Phase 3  Help  `/doctor` mode headless JSON  Markdown

### 8.2 `/release-notes`:

`/release-notes`  Phase 3  built-in

---

## 9. 

 `CommandService` :

- extension/plugin  `extensionName.commandName`
- :`extensionName.commandName1`
-  extension 

Phase 3  Help/Completion 

:

-  plugin command  `[Plugin]` badge
- Help  Plugin Commands 
- ACP 

> "built-in > bundled/skill-dir > plugin > mcp"" extension "Phase 3  `CommandService`  Phase /

---

## 10. 

### 10.1 

:

- `packages/cli/src/ui/hooks/useSlashCompletion.test.ts`
- `packages/cli/src/ui/hooks/useCommandCompletion.test.ts`
- `packages/cli/src/ui/components/SuggestionsDisplay.test.tsx`

:

- source badge:Skill/Custom/Plugin/MCP 
- argumentHint: hint
- recently used: `/`  query 
- alias : `?`  `help (alias: ?)` `he`  alias 
- mid-input ghost: `/rev`  modelInvocable `/review` 
- mid-input  built-in: `/sta`  `/stats` built-in 

### 10.2 Help 

:`packages/cli/src/ui/components/Help.test.tsx`

:

-  Built-in/Bundled Skills/Custom/Plugin/MCP 
- hidden 
- 
- `argumentHint`source badgemode badgemodel badge 
- altNames 

### 10.3 ACP 

:`packages/cli/src/acp-integration/session/Session.test.ts`

:

- `availableCommands[].input.hint` 
-  `argumentHint``source``sourceLabel``supportedModes``subcommands``modelInvocable`
-  `argumentHint`  `input: null` 
- `getAvailableCommands(config, signal, 'acp')` 

### 10.4 

 `/release-notes`  built-in  `/doctor` 

### 10.5 E2E 

Phase 3  TUI slash command ACP command metadataE2E :

1. ** CLI**: `npm run build && npm run bundle` `node dist/cli.js` 
2. **Interactive / tmux **:ghost textTab Help  TUI 
3. **Headless / JSON **: non-interactive slash command  TUI
4. **ACP integration **: `available_commands_update` 

#### 10.5.1 E2E 

```bash
npm run build && npm run bundle
```

Interactive :

```bash
tmux new-session -d -s qwen-slash-phase3 -x 200 -y 50 \
  "cd /tmp/qwen-slash-phase3 && /Users/mochi/code/qwen-code-test/dist/cli.js --approval-mode yolo"
sleep 3
```

 TUI :

```bash
tmux send-keys -t qwen-slash-phase3 "/help"
sleep 0.5
tmux send-keys -t qwen-slash-phase3 Enter
```

:

```bash
tmux capture-pane -t qwen-slash-phase3 -p -S -100
```

:

```bash
tmux kill-session -t qwen-slash-phase3
```

#### 10.5.2 E2E 

|                     |              |                                                                                     |                                                                                                                                   |
| ----------------------- | ---------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
|  source badge       | interactive/tmux |  `/`                                                                  | skill/custom/plugin/MCP  source badgebuilt-in  badge                                                                |
|  argument hint      | interactive/tmux |  `/model``/export`                                                                |  `argumentHint` hint                                                                                    |
| recently used       | interactive/tmux |  `/help` `/`                                                              | `/help`  query  query                                                                             |
| alias           | interactive/tmux |  `/?`                                                                               |  `help (alias: ?)` `/he`  alias                                                                             |
| mid-input ghost text    | interactive/tmux |  `please /rev`                                                              |  `/review`  ghost text Tab                                                                                              |
| mid-input token     | interactive/tmux |  `/review`                                                                |  model-invocable slash token  `/usr/bin`                                                            |
| Help            | interactive/tmux |  `/help`                                                                            |  Built-in CommandsBundled SkillsCustom CommandsPlugin CommandsMCP Commands  source/mode/hint            |
| `/doctor` headless  | headless/json    |  `node dist/cli.js "/doctor" --approval-mode yolo --output-format json 2>/dev/null` |  `message` TUI-only                                                                                                   |
| ACP metadata            | integration      |  ACP session  `available_commands_update`                                     |  command  `name``description``input.hint` `argumentHint``source``supportedModes``subcommands``modelInvocable` |

#### 10.5.3 Headless 

`/release-notes` headless  `/doctor` 

### 10.6 

 AGENTS.md:

```bash
cd packages/cli && npx vitest run src/ui/hooks/useSlashCompletion.test.ts
cd packages/cli && npx vitest run src/ui/hooks/useCommandCompletion.test.ts
cd packages/cli && npx vitest run src/ui/components/Help.test.tsx
cd packages/cli && npx vitest run src/acp-integration/session/Session.test.ts
```

:

```bash
npm run build && npm run typecheck
npm run build && npm run bundle
```

---

## 11. 

### 11.1 

- [ ]  source badge `[MCP]``[Skill]``[Custom]``[Plugin]`
- [ ]  `argumentHint`
- [ ] session  `/` 
- [ ] alias  `alias: <alias>` alias 
- [ ] plugin/extension 

### 11.2 mid-input slash

- [ ]  `/review`  model-invocable  ghost text 
- [ ] Tab  mid-input ghost text
- [ ]  mid-input slash command token 
- [ ] built-in 
- [ ]  args 

### 11.3 Help

- [ ] `/help` 
- [ ] `argumentHint`descriptionsourcesupportedModes 
- [ ] model-invocable 
- [ ] 
- [ ] hidden 

### 11.4 ACP

- [ ] ACP `available_commands_update`  `name``description``input.hint`
- [ ] ACP command  `argumentHint``source``supportedModes``subcommands``modelInvocable`
- [ ] 

### 11.5 

- [ ] `/doctor`  non-interactive  `message`
- [ ]  `/release-notes`

---

## 12. 

 Phase 3:

-  workflow command / dynamic skill / mcp skill  Loader
-  command usage tracking
-  `SkillTool` 
-  MCP prompt 
-  command  mode adapter
-  user/project command 

---

## 13. 

1. ** badge/hint **: `Suggestion`  `SuggestionsDisplay`
2. ** built-in `argumentHint`**: ghost text  ACP `input.hint` 
3. **recently used **: `useSlashCompletion`  recent score
4. **alias **: FZF/prefix  `matchedAlias`
5. **Help  tab **: Claude Code  General / Commands / Custom Commands 
6. **ACP **: `Session.sendAvailableCommandsUpdate()` `_meta` 
7. **mid-input **:
