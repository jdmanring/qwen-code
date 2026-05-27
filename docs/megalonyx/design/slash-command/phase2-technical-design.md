# Phase 2 :

## 1. 

### 1.1 

-  13  built-in  `supportedModes`  `non_interactive` / `acp`
-  ACP/non-interactive  IDE 
-  prompt command `SkillTool`  `getModelInvocableCommands()`
-  mid-input slash command 

### 1.2 

- **interactive **: interactive  action  interactive 
- **:**:13  `action`  `executionMode`  Phase 1  10.2  interactive  non-interactive 
- **ACP **:ACP  ANSI  Markdown  IDE 
- ****:`open()``copyToClipboard()` non-interactive/ACP 

---

## 2. Phase 1 

Phase 1 Phase 2 :

- `commandType`  `SlashCommand`  `supportedModes`
- `getEffectiveSupportedModes()` : `supportedModes` -> `CommandKind` 
- `CommandService.getCommandsForMode(mode)`  `ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE` 
- `btw``bug``compress``context``init``summary`  Phase 1 ****
- `createNonInteractiveUI()`  no-op:`addItem``clear``setDebugMessage``setPendingItem``reloadCommands` 

---

## 3. 

 13 :

|        |                                          |                                                                              |
| ---------- | -------------------------------------------- | ------------------------------------------------------------------------------------ |
| **A **   | `export`                                     |  `supportedModes`action                                  |
| **** | `plan``statusline`                         | : `supportedModes: ['interactive']` |
| **A+ **  | `language`                                   |  `supportedModes` +  non-interactive                                   |
| **** | `copy``restore`                            | : `supportedModes: ['interactive']`   |
| **A' **  | `model``approval-mode`                     |  `message` non-interactive  dialog   |
| **B **   | `about``stats``insight``docs``clear` | action  `addItem`/`clear` non-interactive    |

---

## 4. A : `supportedModes`

 `action`  `message`  `submit_prompt` UI `handleCommandResult` 

### 4.1 `/export`

****:`supportedModes: ['interactive']` action  `MessageActionReturn`

****:`md``html``json``jsonl` `supportedModes`  `['interactive', 'non_interactive', 'acp']`

**ACP **:action  `Session exported to markdown: qwen-export-2024-01-01T12-00-00.md` IDE 

> ****:`/export`  `action` `supportedModes` `parseSlashCommand`  `/export` `commandToExecute.action`  undefined`handleSlashCommand`  `no_command`

### 4.2 `/plan`

****:`supportedModes: ['interactive']`action  `MessageActionReturn`  `SubmitPromptActionReturn`

****:`/plan`  `supportedModes: ['interactive']` non-interactive/acp 

### 4.3 `/statusline`

****:`supportedModes: ['interactive']`action  `SubmitPromptActionReturn` subagent  prompt 

****:`/statusline`  subagent  `supportedModes: ['interactive']` non-interactive/acp 

---

## 5. A+ : non-interactive 

### 5.1 `/language`

****:action  `MessageActionReturn`/

****:`setUiLanguage()`  `context.ui.reloadCommands()` UI  no-op

****:

- `ui``output` `SUPPORTED_LANGUAGES`  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
- action 

**ACP **: non-interactive `/language ui zh-CN`  settings  session  session  i18n 

### 5.2 `/copy`

****:action  `copyToClipboard()` ACP/headless clipboard 

****:

1.  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2.  action :

```typescript
//  last AI message
if (context.executionMode !== 'interactive') {
  // /ACP:
  if (!lastAiOutput) {
    return {
      type: 'message',
      messageType: 'info',
      content: 'No output in history.',
    };
  }
  return {
    type: 'message',
    messageType: 'info',
    content: lastAiOutput,
  };
}
// interactive :
await copyToClipboard(lastAiOutput);
return {
  type: 'message',
  messageType: 'info',
  content: 'Last output copied to the clipboard',
};
```

**ACP **:IDE 

### 5.3 `/restore`

****:`supportedModes: ['interactive']`

****: `supportedModes: ['interactive']` non-interactive/acp 

**ACP **:checkpoint  git  gemini client history IDE "" IDE 

---

## 6. A' : dialog  non-interactive 

### 6.1 `/model`

****:

|                              |                                                                          |
| -------------------------------- | -------------------------------------------------------------------------------- |
| `/model`               | -> `{ type: 'dialog', dialog: 'model' }`non-interactive  unsupported      |
| `/model <model-id>`              |  `--fast`                                                      |
| `/model --fast` model name | -> `{ type: 'dialog', dialog: 'fast-model' }`non-interactive  unsupported |
| `/model --fast <model-id>`       | -> `MessageActionReturn`                                                        |

****:

1.  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2.  action  dialog  non-interactive :

```typescript
//  dialog: 'model'
if (!args.trim()) {
  if (context.executionMode !== 'interactive') {
    const currentModel = config.getModel() ?? 'unknown';
    return {
      type: 'message',
      messageType: 'info',
      content: `Current model: ${currentModel}\nUse "/model <model-id>" to switch models.`,
    };
  }
  return { type: 'dialog', dialog: 'model' };
}

// --fast  dialog: 'fast-model'
if (args.startsWith('--fast') && !modelName) {
  if (context.executionMode !== 'interactive') {
    const fastModel = context.services.settings?.merged?.fastModel ?? 'not set';
    return {
      type: 'message',
      messageType: 'info',
      content: `Current fast model: ${fastModel}\nUse "/model --fast <model-id>" to set fast model.`,
    };
  }
  return { type: 'dialog', dialog: 'fast-model' };
}
```

**ACP **:IDE `/model <model-id>`

> ****:`/model <model-id>` `--fast` session  `--fast <model-id>`  Phase 2  ACP  `/model <model-id>`  set  Phase 2 "" read-only 

### 6.2 `/approval-mode`

****:

|                        |                                                                             |
| -------------------------- | ----------------------------------------------------------------------------------- |
| `/approval-mode` | -> `{ type: 'dialog', dialog: 'approval-mode' }`non-interactive  unsupported |
| `/approval-mode <mode>`    | -> `MessageActionReturn`                                                           |
| `/approval-mode <invalid>` | -> `MessageActionReturn`error                                                  |

****:

1.  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2. `!args.trim()` non-interactive :

```typescript
if (!args.trim()) {
  if (context.executionMode !== 'interactive') {
    const currentMode = config?.getApprovalMode() ?? 'unknown';
    return {
      type: 'message',
      messageType: 'info',
      content: `Current approval mode: ${currentMode}\nAvailable modes: ${APPROVAL_MODES.join(', ')}\nUse "/approval-mode <mode>" to change.`,
    };
  }
  return { type: 'dialog', dialog: 'approval-mode' };
}
```

---

## 7. B : non-interactive 

 action  interactive  `context.ui.addItem()`  React  `context.ui.clear()` `void` non-interactive  no-op `handleSlashCommand`  `"Command executed successfully."`

****: action **** `executionMode` interactive  ** return**  `message`interactive 

### 7.1 `/about`altName: `status`

****:`getExtendedSystemInfo(context)`  `ExtendedSystemInfo`:`cliVersion``osPlatform``osArch``osRelease``nodeVersion``modelVersion``selectedAuthType``ideClient``sessionId``memoryUsage``baseUrl``apiKeyEnvKey``gitCommit``fastModel` non-interactive context.services.config  settings 

****:

1.  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2.  `getExtendedSystemInfo` interactive :

```typescript
action: async (context) => {
  const systemInfo = await getExtendedSystemInfo(context);

  if (context.executionMode !== 'interactive') {
    const lines = [
      `Qwen Code v${systemInfo.cliVersion}`,
      `Model: ${systemInfo.modelVersion}`,
      `Fast Model: ${systemInfo.fastModel ?? 'not set'}`,
      `Auth: ${systemInfo.selectedAuthType}`,
      `Platform: ${systemInfo.osPlatform} ${systemInfo.osArch} (${systemInfo.osRelease})`,
      `Node.js: ${systemInfo.nodeVersion}`,
      `Session: ${systemInfo.sessionId}`,
      ...(systemInfo.gitCommit ? [`Git commit: ${systemInfo.gitCommit}`] : []),
      ...(systemInfo.ideClient ? [`IDE: ${systemInfo.ideClient}`] : []),
    ];
    return {
      type: 'message',
      messageType: 'info',
      content: lines.join('\n'),
    };
  }

  // interactive : addItem 
  const aboutItem: Omit<HistoryItemAbout, 'id'> = { type: MessageType.ABOUT, systemInfo };
  context.ui.addItem(aboutItem, Date.now());
},
```

### 7.2 `/stats` `model``tools`

****:`context.session.stats``SessionStatsState` `sessionStartTime``metrics``SessionMetrics`:`models``tools``files``promptCount` non-interactive `sessionStartTime` `metrics`  `uiTelemetryService.getMetrics()``promptCount`  1

****:

1.  `stats`  `model``tools`  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2.  action :

```typescript
// /stats 
action: (context) => {
  if (context.executionMode !== 'interactive') {
    const now = new Date();
    const { sessionStartTime, promptCount, metrics } = context.session.stats;
    if (!sessionStartTime) {
      return { type: 'message', messageType: 'error', content: 'Session start time unavailable.' };
    }
    const wallDuration = now.getTime() - sessionStartTime.getTime();

    //  model  token 
    let totalPromptTokens = 0, totalCandidateTokens = 0, totalRequests = 0;
    for (const modelMetrics of Object.values(metrics.models)) {
      totalPromptTokens += modelMetrics.tokens.prompt;
      totalCandidateTokens += modelMetrics.tokens.candidates;
      totalRequests += modelMetrics.api.totalRequests;
    }

    const lines = [
      `Session duration: ${formatDuration(wallDuration)}`,
      `Prompts: ${promptCount}`,
      `API requests: ${totalRequests}`,
      `Tokens -- prompt: ${totalPromptTokens}, output: ${totalCandidateTokens}`,
      `Tool calls: ${metrics.tools.totalCalls} (${metrics.tools.totalSuccess} ok, ${metrics.tools.totalFail} fail)`,
      `Files: +${metrics.files.totalLinesAdded} / -${metrics.files.totalLinesRemoved} lines`,
    ];
    return { type: 'message', messageType: 'info', content: lines.join('\n') };
  }

  // interactive : addItem 
  const statsItem: HistoryItemStats = { type: MessageType.STATS, duration: formatDuration(wallDuration) };
  context.ui.addItem(statsItem, Date.now());
},
```

 `model`  `tools` model  model name  token tools  tool 

****: non-interactive metrics  sessionACP Session 

### 7.3 `/insight`

****:action  `void` `addItem`  `open(outputPath)`  `insightGenerator.generateStaticInsight()`  HTML 

****:

1.  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2.  `executionMode` :
   - `non_interactive`: `message`
   - `acp`: `stream_messages` `encodeInsightProgressMessage``encodeInsightReadyMessage` IDE
   - `interactive`: `addItem` + `setPendingItem` + `open()` 

```typescript
// non_interactive 
if (context.executionMode === 'non_interactive') {
  const outputPath = await insightGenerator.generateStaticInsight(
    projectsDir,
    () => {}, // no-op progress
  );
  return {
    type: 'message',
    messageType: 'info',
    content: t('Insight report generated at: {{path}}', { path: outputPath }),
  };
}

// acp :stream_messages
if (context.executionMode === 'acp') {
  // ...  streamMessages async generatoryield encodeInsightProgressMessage / encodeInsightReadyMessage ...
  return { type: 'stream_messages', messages: streamMessages() };
}

// interactive :
```

****:`non_interactive` CLI  `stream_messages` `message`ACP IDE  `stream_messages`  streaming 

**ACP **:`encodeInsightProgressMessage(stage, progress, detail?)`  IDE `encodeInsightReadyMessage(outputPath)`  IDE  IDE 

### 7.4 `/docs`

****:action  `void` `addItem`  `open(docsUrl)`  `SANDBOX`  addItem

****:

1.  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2.  action  `Promise<void | MessageActionReturn>`
3.  action  non-interactive :

```typescript
action: async (context) => {
  const langPath = getCurrentLanguage()?.startsWith('zh') ? 'zh' : 'en';
  const docsUrl = `https://qwenlm.github.io/qwen-code-docs/${langPath}`;

  if (context.executionMode !== 'interactive') {
    // /ACP: URL addItem
    return {
      type: 'message',
      messageType: 'info',
      content: `Qwen Code documentation: ${docsUrl}`,
    };
  }

  // interactive : SANDBOX  + addItem + open() 
  if (process.env['SANDBOX'] && ...) {
    context.ui.addItem(...);
  } else {
    context.ui.addItem(...);
    await open(docsUrl);
  }
},
```

### 7.5 `/clear`altNames: `reset``new`

****:action  `void`:

1. `config.getHookSystem()?.fireSessionEndEvent()` --  hook
2. `config.startNewSession()` --  session ID
3. `uiTelemetryService.reset()` --  telemetry 
4. `skillTool.clearLoadedSkills()` --  skill 
5. `context.ui.clear()` --  UI**UI non-interactive  no-op**
6. `geminiClient.resetChat()` --  chat 
7. `config.getHookSystem()?.fireSessionStartEvent()` --  hook

**non-interactive/ACP **:

- `ui.clear()`  non-interactive  no-op
- `geminiClient.resetChat()`: ACP Session  chat  non-interactive  session`resetChat` 
- `config.startNewSession()`: ACP  session ID non-interactive 
- `fireSessionEndEvent` / `fireSessionStartEvent`: ACP  hook

****:non-interactive/ACP resetChatstartNewSessionhook events `ui.clear()` no-op message

****:

1.  `supportedModes`  `['interactive', 'non_interactive', 'acp']`
2.  action  `Promise<void | MessageActionReturn>`
3.  action `context.ui.clear()` :

```typescript
action: async (context, _args) => {
  const { config } = context.services;

  if (config) {
    config.getHookSystem()?.fireSessionEndEvent(SessionEndReason.Clear).catch(...);

    const newSessionId = config.startNewSession();
    uiTelemetryService.reset();

    const skillTool = config.getToolRegistry()?.getAllTools().find(...);
    if (skillTool instanceof SkillTool) skillTool.clearLoadedSkills();

    if (newSessionId && context.session.startNewSession) {
      context.session.startNewSession(newSessionId);
    }

    // ui.clear()  no-op
    context.ui.clear();

    const geminiClient = config.getGeminiClient();
    if (geminiClient) {
      await geminiClient.resetChat();
    }

    config.getHookSystem()?.fireSessionStartEvent(...).catch(...);
  } else {
    context.ui.clear();
  }

  // 
  if (context.executionMode !== 'interactive') {
    return {
      type: 'message',
      messageType: 'info',
      content: 'Context cleared. Previous messages are no longer in context.',
    };
  }
  // interactive :voidReact UI  ui.clear() 
},
```

**ACP **:IDE  session "" chat 

---

## 8. `handleCommandResult` 

**:**

Phase 2 non-interactive/ACP  `message`  `submit_prompt` `handleCommandResult`  switch 

---

## 9. `createNonInteractiveUI()` 

**:**

 no-op `addItem``clear``setPendingItem`  no-op  B  non-interactive  returninteractive 

---

## 10. Phase 2.2:prompt command 

Phase 1  `CommandService.getModelInvocableCommands()` `BundledSkillLoader``FileCommandLoader`/`McpPromptLoader`  `modelInvocable: true`

Phase 2.2  `SkillTool`  `SkillManager.listSkills()`  `CommandService.getModelInvocableCommands()`

****:`packages/core/src/tools/SkillTool.ts`

****:

1. `SkillTool`  `CommandService` `getModelInvocableCommands()` 
2.  tool description  `listSkills()`  `getModelInvocableCommands()` 
3.  built-in commands`modelInvocable: false` tool description 

> ****:`SkillTool`  `packages/core`  core 

---

## 11. Phase 2.3:mid-input slash command 

 `InputPrompt`  slash token

****:

-  `/`  token 
-  `getCommandsForMode('interactive')` 
-  + description argumentHint Phase 3 

>  UI  Phase 2.3  Phase 2.1/2.2 

---

## 12. 

### 12.1 Phase 2.1

|                      |  |                                                                                                                              |
| ------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `exportCommand.ts`       | A      |  + 4 :`supportedModes` -> all modes                                                                                    |
| `planCommand.ts`         |    | : `supportedModes: ['interactive']`                                                                             |
| `statuslineCommand.ts`   |    | : `supportedModes: ['interactive']`                                                                             |
| `languageCommand.ts`     | A+     |  + `ui`/`output`  +  language :`supportedModes` -> all modes                                                   |
| `copyCommand.ts`         |    | : `supportedModes: ['interactive']`                                                                             |
| `restoreCommand.ts`      |    | : `supportedModes: ['interactive']`                                                                             |
| `modelCommand.ts`        | A'     | `supportedModes` -> all modes + / fast model                                                                |
| `approvalModeCommand.ts` | A'     | `supportedModes` -> all modes +                                                                               |
| `aboutCommand.ts`        | B      | `supportedModes` -> all modes +  `message`//                                                        |
| `statsCommand.ts`        | B      | `supportedModes` -> all modes +  `message`stats                                                 |
| `insightCommand.ts`      | B      | `supportedModes` -> all modes + `non_interactive`  `message``acp`  `stream_messages`  |
| `docsCommand.ts`         | B      | `supportedModes` -> all modes +  `message` URL                                                    |
| `clearCommand.ts`        | B      | `supportedModes` -> all modes + action  `message`  `void`                                                           |

### 12.2 

|                                                 |                                                           |
| --------------------------------------------------- | ----------------------------------------------------------------- |
| `packages/core/src/tools/SkillTool.ts`              | Phase 2.2: `getModelInvocableCommands()` |
| `packages/cli/src/ui/InputPrompt.tsx` | Phase 2.3:mid-input slash                                |

### 12.3 

- `packages/cli/src/nonInteractiveCliCommands.ts``handleCommandResult``handleSlashCommand` 
- `packages/cli/src/ui/noninteractive/nonInteractiveUi.ts`stub UI 
- `packages/cli/src/services/commandUtils.ts``filterCommandsForMode``getEffectiveSupportedModes` 
- `packages/cli/src/services/CommandService.ts``getCommandsForMode``getModelInvocableCommands`  Phase 1 

---

## 13. 

### 13.1 

`*.test.ts` case:

**A/A+ **`export``language`:

- `supportedModes`  `non_interactive`  `acp`
-  `executionMode: 'non_interactive'` action  `MessageActionReturn`  `SubmitPromptActionReturn` `ui.addItem`  `ui.clear`
- Interactive 

****`plan``statusline``copy``restore`:

- `supportedModes`  `['interactive']`
-  non-interactive  `unsupported`

**A' **`model``approval-mode`:

-  + `executionMode: 'non_interactive'` ->  `message` `dialog`
-  + `executionMode: 'non_interactive'` ->  `message` 
- Interactive : -> `dialog` -> `message`

**B **`about``stats``insight``docs``clear`:

- `executionMode: 'non_interactive'` action  `MessageActionReturn` `ui.*` 
-  `content` URL 
- Interactive :`ui.addItem` `action`  `void`

**`clear`  case**:

- `executionMode: 'non_interactive'` `geminiClient.resetChat()` 
-  `message` `'Context cleared. Previous messages are no longer in context.'`

### 13.2 `handleSlashCommand`

 `nonInteractiveCli.test.ts` :

- `handleSlashCommand('/about', ...)`  non-interactive  `{ type: 'message', content:  }`
- `handleSlashCommand('/stats', ...)`  non-interactive  `{ type: 'message', content:  'Session duration' }`
- `handleSlashCommand('/docs', ...)`  non-interactive  `{ type: 'message', content:  'qwenlm.github.io' }`
- `handleSlashCommand('/clear', ...)`  non-interactive  `{ type: 'message', content: 'Context cleared.' }`
- `handleSlashCommand('/plan', ...)`  non-interactive  `unsupported`
-  non-interactive `btw``bug` 

### 13.3 `commandUtils` 

`commandUtils.test.ts` :

- `export``language`  `filterCommandsForMode(commands, 'non_interactive')`  `filterCommandsForMode(commands, 'acp')` 
- `plan``statusline``copy``restore` `filterCommandsForMode(commands, 'non_interactive')` 

---

## 14. 

|                                          | Phase 2                                             | Phase 2                      |                |
| -------------------------------------------- | --------------------------------------------------------- | ---------------------------------- | ------------------ |
| non-interactive  `/export md`          |  unsupported                                  |   message            |            |
| non-interactive  `/plan <task>`        |  unsupported                                            |  unsupported: |                |
| non-interactive  `/statusline`         |  unsupported                                            |  unsupported: |                |
| non-interactive  `/language ui zh-CN`  |  unsupported                                            |   message      |            |
| non-interactive  `/copy`               |  unsupported                                            |  unsupported: |                |
| non-interactive  `/restore`  |  unsupported                                            |  unsupported: |                |
| non-interactive  `/restore <id>`       |  unsupported                                            |  unsupported: |                |
| non-interactive  `/model`              |  unsupporteddialog                                  |                  |            |
| non-interactive  `/model <id>`         |  unsupported                                            |  Phase 2 :      |    |
| non-interactive  `/approval-mode`      |  unsupporteddialog                                  |                  |            |
| non-interactive  `/approval-mode yolo` |  unsupported                                            |                |            |
| non-interactive  `/about`              |   "Command executed successfully."addItem no-op |  //          | Bug fix +  |
| non-interactive  `/stats`              |   "Command executed successfully."                  |   session            | Bug fix +  |
| non-interactive  `/insight`            |   "Command executed successfully."  |                | Bug fix +  |
| non-interactive  `/docs`               |   "Command executed successfully."                  |   URL                    | Bug fix +  |
| non-interactive  `/clear`              |   "Command executed successfully."                  |   message          | Bug fix +  |
| interactive                |                                                 |                |                |

---

## 15. 

 commit  review:

**Batch 1**~30min:A  --  `supportedModes`

 `exportCommand.ts`

**Batch 2**~45min:A+  -- 

 `languageCommand.ts``copyCommand.ts`  `restoreCommand.ts` 

**Batch 3**~45min:A'  -- dialog 

 `modelCommand.ts``approvalModeCommand.ts`

**Batch 4**~1.5h:B  -- 

 `aboutCommand.ts``statsCommand.ts``docsCommand.ts`

**Batch 5**~1h:B  -- `insightCommand.ts``clearCommand.ts`

 commit

**Batch 6**~2h:Phase 2.2 -- prompt command 

 `SkillTool` `getModelInvocableCommands()` SkillTool 

**Batch 7**~2h:Phase 2.3 -- mid-input slash 

 `InputPrompt`  UI 

**Batch 8**~30min: + 

 `npm run typecheck``cd packages/cli && npx vitest run`

---

## 16.  Checklist

**Phase 2.1 **

- [ ] A :`/export``/plan``/statusline`  non-interactive  acp 
- [ ] A+ :`/language` non-interactive 
- [ ] A+ :`/copy`  non-interactive/acp  AI 
- [ ] A+ :`/restore`  non-interactive  checkpoint  message `type: 'tool'`
- [ ] A' :`/model`  non-interactive/acp  dialog`/model --fast <id>` 
- [ ] A' :`/approval-mode`  non-interactive/acp  dialog
- [ ] B :`/about`  non-interactive/acp 
- [ ] B :`/stats` non-interactive/acp 
- [ ] B :`/insight`  non-interactive/acp  insight 
- [ ] B :`/docs`  non-interactive/acp  URL
- [ ] B :`/clear`  non-interactive/acp  message`geminiClient.resetChat()` 
- [ ]  13  interactive 
- [ ] TypeScript `npm run typecheck`
- [ ] `npm run lint` 
- [ ] `cd packages/cli && npx vitest run`

**Phase 2.2 **

- [ ]  `SkillTool`  bundled skillfile command/MCP prompt
- [ ]  built-in commands
- [ ] `SkillTool`  tool description  `modelInvocable: true`  description

**Phase 2.3 mid-input slash**

- [ ]  `/` 
- [ ]  + description
- [ ] 
