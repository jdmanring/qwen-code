# Slash Command 

## 

 Qwen  95%  Claude Code  command prompt command 

---

## 

1. ** Phase  ship**: Phase 
2. **Phase 1 **: MCP_PROMPT 
3. ****:Phase 1 Phase 2 
4. ** Claude Code **:

---

## Phase 1:

### 

 Phase 

### 

#### 1.1  `SlashCommand` 

 `SlashCommand` :

****

- `source: CommandSource`:`builtin-command` / `bundled-skill` / `skill-dir-command` / `plugin-command` / `mcp-prompt` 
- `sourceLabel?: string`: `"Built-in"` / `"MCP: github-server"`

****

- `supportedModes: ExecutionMode[]`:`interactive` / `non_interactive` / `acp`

****

- `commandType: CommandType`:`prompt` / `local` / `local-jsx`

****

- `userInvocable: boolean`: slash command  `true`
- `modelInvocable: boolean`: tool call  `false`

**** Phase 3 Phase 1 

- `argumentHint?: string`: `"<model-id>"` / `"show|list|set"`
- `whenToUse?: string`:
- `examples?: string[]`:

#### 1.2 Loader  source/commandType 

 Loader  `SlashCommand`  `source`  `commandType`:

| Loader                           | source              | commandType                           |
| -------------------------------- | ------------------- | ------------------------------------- |
| `BuiltinCommandLoader`           | `builtin-command`   | `local` / `local-jsx` |
| `BundledSkillLoader`             | `bundled-skill`     | `prompt`                              |
| `FileCommandLoader`/ | `skill-dir-command` | `prompt`                              |
| `FileCommandLoader`      | `plugin-command`    | `prompt`                              |
| `McpPromptLoader`                | `mcp-prompt`        | `prompt`                              |

#### 1.3  `supportedModes`  `commandType`

 built-in :

- `commandType`:`local` UI  `local-jsx` dialog/React
- `supportedModes`:`local`  `['interactive', 'non_interactive', 'acp']``local-jsx`  `['interactive']`

#### 1.4  capability-based 

-  `ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE` 
-  `filterCommandsForNonInteractive` 
-  `filterCommandsForMode(commands, mode)`  `supportedModes` 
-  `getEffectiveSupportedModes(cmd)`  CommandKind 
-  `handleSlashCommand` / `getAvailableCommands`  `allowedBuiltinCommandNames` 

#### 1.5 CommandService  Registry

-  `getCommandsForMode(mode: ExecutionMode)` 
-  `getModelInvocableCommands()` Phase 2/3 Phase 1 
-  `getCommands()` interactive 

### 

- [ ] `SlashCommand` TypeScript 
- [ ]  Loader  `source`  `commandType` 
- [ ]  built-in  `commandType`  `supportedModes`
- [ ] `ALLOWED_BUILTIN_COMMANDS_NON_INTERACTIVE`  capability filter 
- [ ] **non-interactive ** break
- [ ] MCP prompt commands  non-interactive/acp 
- [ ] `CommandService.getCommandsForMode('non_interactive')` 
- [ ] 

---

## Phase 2: prompt command 

### 

 Phase 1  prompt command 

### 

#### 2.1  non-interactive / acp 

**ACP **

 ACP/non-interactive :

1. ****:ACP  IDEZed/VS Code  Markdown  terminal  ANSI 
2. ****: `action` ----interactive  UI non_interactive/acp  `message`  `submit_prompt` `action` 
3. ****: CLI `-p` `/model set``/language set`  session 
4. ** vs **: `/about``/stats` `/model set``/language set`
5. ****:`/docs``/insight``/copy` non_interactive/acp  URL 

****

> :`btw``bug``compress``context``init``summary`  Phase 1 

 13  Phase 2  `non_interactive`  `acp` :

**A :action  `message`  `submit_prompt` `supportedModes`  ACP **

|           |         | ACP/non-interactive                        |
| ------------- | --------------- | -------------------------------------------------- |
| `/copy`       | `message`       | ACP  |
| `/export`     | `message`       |                              |
| `/plan`       | `submit_prompt` |                              |
| `/restore`    | `message`       |                              |
| `/language`   | `message`       |                      |
| `/statusline` | `submit_prompt` |                              |

**A' : dialog non-interactive **

|              |  interactive  |  non_interactive/acp  |
| ---------------- | ----------------------- | ------------------------------- |
| `/model`         |  dialog     |       |
| `/approval-mode` |  dialog     |       |

**B :action  `context.ui.addItem()`  React **

|        | interactive           | non_interactive/acp                                                         |
| ---------- | ------------------------- | ----------------------------------------------------------------------------------- |
| `/about`   | / React   |                                               |
| `/stats`   |  token/   | session                                                         |
| `/insight` |  +  | `non_interactive` `acp`  `stream_messages`  |
| `/docs`    |  +  |  URL                                                          |

**C :**

|      | interactive                        | non_interactive/acp                                                                             |
| -------- | -------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `/clear` |  `context.ui.clear()`  |  message `"Context cleared. Previous messages are no longer in context."` |

#### 2.2 prompt command 

-  `CommandService` `CommandRegistry` `getModelInvocableCommands()` `modelInvocable: true` 
-  `BundledSkillLoader``FileCommandLoader`/ `modelInvocable: true`
- **MCP prompt  `modelInvocable`**:MCP prompt  MCP tool call  `SkillTool` 
-  `SkillTool`: `SkillManager.listSkills()`  `CommandService.getModelInvocableCommands()`
-  `SkillTool`  description

#### 2.3 mid-input slash command 

-  `InputPrompt`  slash token
-  slash token  inline ghost text Tab 
- **** dropdown argument hintssource badge Phase 3 
- ghost text  `modelInvocable: true` skill / file command

### 

**2.1 **

- [ ] A :`/copy``/export``/plan``/restore``/language``/statusline`  non-interactive  acp 
- [ ] A' :`/model``/approval-mode`  non-interactive/acp  dialog
- [ ] B :`/about``/stats``/docs`  non-interactive/acp `/docs` `/insight`  `non_interactive`  message `acp`  `stream_messages` 
- [ ] C :`/clear`  non-interactive/acp  message `context.ui.clear()`
- [ ]  interactive 

**2.2 **

- [ ]  `SkillTool`  bundled skillfile command/
- [ ] MCP prompt  `SkillTool` MCP tool call 
- [ ]  built-in commands`userInvocable: true``modelInvocable: false`
- [ ] `SkillTool`  description  `modelInvocable` 

**2.3 mid-input slash**

- [ ] mid-input slash: `/`  inline ghost text Tab 

---

## Phase 3: + Claude Code 

### 

 Phase 1/2  Claude Code  Qwen Code 

### 

#### 3.1 

**source badge**

- `[MCP]`  `[Skill]``[Custom]` 
-  `source` / `sourceLabel` 

**argument hint**

-  `argumentHint` `set <model-id>`
- `argumentHint`  Phase 1 

**recently used **

- session 
- 

**alias **

-  `altNames`  `help (alias: ?)`

****

- :built-in > bundled/skill-dir > plugin > mcp
-  `pluginName.commandName`

#### 3.2 mid-input slash command 

-  Phase 2  argument hints  source badge 
- ghost text  `/he`  `/help` 
-  token  slash command 

#### 3.3 Help 

 `/help` :

- **Built-in Commands**local + local-jsx mode
- **Bundled Skills**
- **Custom Commands**/ file commands
- **Plugin Commands**
- **MCP Commands**

:argumentHintdescriptionsourcesupportedModes 

#### 3.4 ACP available commands 

 `sendAvailableCommandsUpdate()`  ACP :

- `argumentHint`
- `source`
- `supportedModes`
- `subcommands`
- `modelInvocable`

#### 3.5 Claude Code 

 Qwen Code  `/doctor` `/release-notes`  built-in 

|       |     |                                  |
| --------- | ------- | ------------------------------------ |
| `/doctor` | `local` | // |

> :`/review``/commit`  bundled skill 

### 

- [ ]  source badge`[MCP]``[Skill]``[Custom]`
- [ ]  argumentHint `set <model-id>`
- [ ] 
- [ ] alias 
- [ ] mid-input slash:ghost text 
- [ ] `/help`  Claude Code  tab 
- [ ] ACP available commands  `argumentHint``source``subcommands` 
- [ ] `/doctor` 
- [ ] `/doctor`  non-interactive  `message`
- [ ]  `/release-notes`

---

##  Phase 

```
Phase 1 + 
    |
    |---- Phase 2
    |        |
    |        |---- slash command 
    |        \_-- prompt command  getModelInvocableCommands()
    |
    \_-- Phase 3
             |
             |---- source badge Phase 1 source 
             |---- argument hint Phase 1 argumentHint 
             \_-- Help  Phase 1 source 
```

Phase 2  Phase 3 
