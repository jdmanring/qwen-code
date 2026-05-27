# Qwen Code Command 

## 1. 

:

- ** Claude Code**
- ** 95%  Claude Code**

"":

1. 
2. 
3.  mid-input slash command 
4. ACP / non-interactive 
5. prompt command / skill 

 `SlashCommand`  command "interactive UI "" interactive / ACP / non-interactive / model "

---

## 2. 

Qwen  command :

1.  interactive 
2.  Claude 
3. ACP / non-interactive 
4. command 
5. prompt command  skill 

:

1. ** Claude Code **
2. ** Qwen  outcome **
3. ** registry / resolver / executor / adapter **
4. **ACP available commands**

---

## 3. 

### 3.1 

:

- 
- 
- 
- effect / outcome 

:

- 
- 
- ACP / non-interactive 
- prompt command 

:

1. 
2. 
3. 
4. 

### 3.2  Qwen  outcome 

 Claude 

Qwen :

- UI 
- /
- tool 
- prompt 
- 

 Claude  command  UI 

### 3.3 

 command :

1. ****:
2. ****:
3. ****:
4. ****:

---

## 4.  Claude Code 

### 4.1 

Qwen :

1. `prompt`
2. `local`
3. `local-jsx`

### 4.2 

Qwen  command schema :

1. built-in commands
2. bundled skills
3. skill dir commands
4. workflow commands
5. plugin commands
6. plugin skills
7. dynamic skills
8. mcp prompts
9. mcp skills

""

### 4.3 

:

1. `argumentHint`
2. `whenToUse`
3. `examples`
4. `sourceLabel`
5. `userFacingName`
6. `alias`
7. `immediate`
8. `isSensitive`
9. `userInvocable`
10. `modelInvocable`
11. `supportedModes`
12. `requiresUi`

### 4.4 

:

1. alias 
2. source badge
3. 
4. recently used 
5. mid-input slash command 
6.  Help
7. ACP available commands 

---

## 5.  command 

## 5.1 

 `CommandDescriptor`

:

1. `identity`
2. `metadata`
3. `capabilities`
4. `handler`

### `identity`

- `id`
- `name`
- `altNames`
- `canonicalPath`

### `metadata`

- `description`
- `argumentHint`
- `whenToUse`
- `examples`
- `group`
- `source`
- `sourceLabel`
- `userFacingName`
- `hidden`

### `capabilities`

- `type`: `prompt | local | local-jsx`
- `supportedModes`: `interactive | acp | non_interactive`
- `requiresUi`
- `supportsDialog`
- `supportsStreaming`
- `supportsToolInvocation`
- `supportsConfirmation`
- `remoteSafe`
- `readOnly`
- `immediate`
- `isSensitive`
- `userInvocable`
- `modelInvocable`

### `handler`

- `resolveArgs()`
- `execute()`
- `completion()`
- `fallback()`

---

## 5.2 

### `prompt`

:

- skills
- file commands
- workflow prompt commands
- plugin skills
- mcp prompt / skill

:

-  prompt / skill 
-  interactive / ACP / non-interactive
- 

### `local`

:

- 
- 
- headless 
-  built-in commands 

:

-  UI
-  ACP / non-interactive 

### `local-jsx`

:

- picker
- 
- wizard
- interactive UI shell

:

-  interactive UI
- 
-  fallback  local 

---

## 6. 

## 6.1 

 Claude Code :

- `builtin-command`
- `bundled-skill`
- `skill-dir-command`
- `workflow-command`
- `plugin-command`
- `plugin-skill`
- `dynamic-skill`
- `builtin-plugin-skill`
- `mcp-prompt`
- `mcp-skill`

:

- Help 
- Completion source badge
- ACP available commands
- 

## 6.2 

:

- `providerType`
- `artifactType`
- `activationMode`
- `builtinProvided`
- `originPath`
- `namespace`

:

-  Claude 
-  Qwen 

## 6.3 

 `id` :

1. `id`:
2. `name`:
3. `userFacingName`:/

:

1. built-in
2. bundled / skill-dir / workflow
3. plugin / builtin-plugin
4. dynamic
5. mcp  namespace

---

## 7. 

## 7.1 `CommandRegistry`

:

1.  loader/provider
2. 
3. ACP
4. 

 provider:

1. `BuiltinCommandLoader`
2. `BundledSkillLoader`
3. `FileCommandLoader`
4. `McpPromptLoader`
5. `WorkflowCommandLoader`
6. `PluginCommandLoader`
7. `PluginSkillLoader`
8. `DynamicSkillProvider`
9. `BuiltinPluginSkillLoader`

 provider schema  API 

## 7.2 `CommandResolver`

:

1.  slash command
2.  alias
3.  subcommand path
4.  mid-input slash token
5.  canonical resolved command

## 7.3 `CommandExecutor`

:

1.  capability 
2.  `prompt | local | local-jsx`
3.  outcome
4.  fallback / unsupported

## 7.4 `ModeAdapter`

 adapter:

1. `InteractiveModeAdapter`
2. `AcpModeAdapter`
3. `NonInteractiveModeAdapter`

 command registry  executor

---

## 8. UI :

 ACP  non-interactive 

" dialog":

1.  interactive shell
2.  local 

### 

1. `/model`
2. `/permissions`
3. `/mcp`
4. `/resume`
5. `/hooks`
6. `/extensions`
7. `/agents`
8. `/approval-mode`

### 

#### `/model`

- `/model`
- `/model show`
- `/model list`
- `/model set <id>`

#### `/permissions`

- `/permissions`
- `/permissions show`
- `/permissions set <mode>`
- `/permissions allow <tool>`
- `/permissions deny <tool>`

#### `/mcp`

- `/mcp`
- `/mcp list`
- `/mcp show <server>`
- `/mcp enable <server>`
- `/mcp disable <server>`

---

## 9. Prompt Command / Skill 

 P0

## 9.1 

 **Model-Invocable Prompt Command Registry**:

1. bundled skills
2. file commands
3. workflow prompt commands
4. plugin skills
5. mcp prompts / mcp skills

## 9.2 

:

1. `userInvocable`
2. `modelInvocable`
3. `allowedTools`
4. `whenToUse`
5. `argSchema` 
6. `contextMode: inline | fork`
7. `agent`
8. `effort`

## 9.3  `SkillTool` 

 `SkillTool`  skills

:

1. `CommandRegistry.getModelInvocablePromptCommands()` 
2. `SkillTool`  command tool 
3.  slash command  skill invocation  prompt-command 

 Qwen  Claude  `/review``/commit``/openspec-apply` 

---

## 10. Help / Completion / Discoverability 

## 10.1 Completion

:

1. `label`
2. `description`
3. `argumentHint`
4. `sourceBadge`
5. `modeBadges`
6. `aliasHit`
7. `recentlyUsedScore`

:

1. 
2. alias 
3. 
4. prefix 
5. fuzzy 

## 10.2 Mid-input slash command

:

1.  slash token 
2. ghost text 
3. Tab 
4.  token 

""

## 10.3 Help

Help 

:

1. Built-in Commands
2. Bundled Skills
3. Skill Dir Commands
4. Workflow Commands
5. Plugin Commands
6. Plugin Skills
7. Dynamic Skills
8. Builtin Plugin Skills
9. MCP Commands / MCP Skills

:

1. 
2. 
3. 
4. 
5. 
6. 
7. 

---

## 11. ACP / Non-Interactive 

## 11.1 

:

- built-in allowlist
- FILE / SKILL 
-  unsupported

:

-  capability
- registry 
- adapter  fallback

## 11.2 outcome 

### interactive

- `submit_prompt`
- `message`
- `stream_messages`
- `tool`
- `dialog`
- `load_history`
- `confirm_action`
- `confirm_shell_commands`

### acp

- `submit_prompt`
- `message`
- `stream_messages`
- `tool`
- `confirm_action`
- `confirm_shell_commands`
- `dialog fallback`

### non_interactive

- `submit_prompt`
- `message`
- `stream_messages`
- `tool`
- `confirm_action`
- `confirm_shell_commands`
- `dialog fallback / structured failure`

## 11.3 ACP available commands 

:

1. `name`
2. `description`
3. `argumentHint`
4. `source`
5. `examples`
6. `supportedModes`
7. `interactiveOnly`
8. `subcommands`
9. `modelInvocable`

---

## 12. 

 registry :

1. Help
2. Completion
3. ACP available commands
4. 

""

---

## 13. 

## Phase 1:

:

1.  `CommandDescriptor`
2.  schema
3. capability 
4. `userInvocable / modelInvocable`
5. `CommandRegistry`
6. `CommandResolver`
7. `CommandExecutor`
8.  `ModeAdapter`
9. `getModelInvocablePromptCommands()`

## Phase 2:

:

1. `/model`
2. `/permissions`
3. `/mcp`
4. `/resume`
5. `/hooks`
6. `/extensions`
7. `/agents`
8. `/approval-mode`

"interactive shell + local "

## Phase 3:

:

1. `SkillTool`  registry 
2. file command / bundled skill / mcp prompt / plugin skill  model-invocable 
3. prompt command  skill 

## Phase 4: Claude

:

1. recently used 
2. source badge
3. argument hint
4. mode badge
5.  help 
6. mid-input slash command 
7. 

---

## 14. 

:

1. ACP
2.  UI  built-in command  ACP / non-interactive 
3. prompt command  skill 
4. mid-input  Claude Code 95% 
5.  built-in allowlist  ACP / non-interactive 

---

## 15. 

" SlashCommand ":

- ** Qwen  95%  Claude Code  command **

:

-  Claude
-  Claude


