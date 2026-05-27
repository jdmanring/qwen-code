/**
 * @license
 * Copyright 2025 Qwen
 * SPDX-License-Identifier: Apache-2.0
 */

//    Qwen Code CLI
//         

export default {
  // ============================================================================
  //  /  
  // ============================================================================
  // Attachment hints
  ' to manage attachments': '  ',
  '<- -> select, Delete to remove,  to exit':
    '<- -> , Delete ,  ',
  'Attachments: ': ': ',
  'Basics:': ':',
  'Add context': ' ',
  'Use {{symbol}} to specify files for context (e.g., {{example}}) to target specific files or folders.':
    ' {{symbol}}      (, {{example}})      ).',
  '@': '@',
  '@src/myFile.ts': '@src/myFile.ts',
  'Shell mode': ' ',
  'YOLO mode': ' YOLO',
  'plan mode': ' ',
  'auto-accept edits': '  ',
  'Accepting edits': ' ',
  '(shift + tab to cycle)': '(Shift + Tab  )',
  '(tab to cycle)': '(Tab  )',
  'Execute shell commands via {{symbol}} (e.g., {{example1}}) or use natural language (e.g., {{example2}}).':
    '    {{symbol}} (, {{example1}})     (, {{example2}}).',
  '!': '!',
  '!npm run start': '!npm run start',
  'Commands:': ':',
  'shell command': ' ',
  'Model Context Protocol command (from external servers)':
    ' Model Context Protocol (  )',
  'Keyboard Shortcuts:': ' :',
  'Toggle this help display': '/  ',
  'Toggle shell mode': '  ',
  'Open command menu': '  ',
  'Add file context': '   ',
  'Accept suggestion / Autocomplete': '  / ',
  'Reverse search history': '   ',
  'Press ? again to close': ' ?  ,  ',
  'Jump through words in the input': '    ',
  'Close dialogs, cancel requests, or quit application':
    ' ,      ',
  'New line': ' ',
  'New line (Alt+Enter works for certain linux distros)':
    '  (Alt+Enter      Linux)',
  'Clear the screen': ' ',
  'Open input in external editor': '    ',
  'Send message': ' ',
  'Initializing...': '...',
  'Connecting to MCP servers... ({{connected}}/{{total}})':
    '  MCP servers... ({{connected}}/{{total}})',
  'Type your message or @path/to/file': '   @//',
  '? for shortcuts': '? --  ',
  "Press 'i' for INSERT mode and 'Esc' for NORMAL mode.":
    " 'i'     'Esc'   .",
  'Cancel operation / Clear input (double press)':
    '  /   ( )',
  'Cycle approval modes': '  ',
  'Cycle through your prompt history': '  ',
  'For a full list of shortcuts, see {{docPath}}':
    '    .  {{docPath}}',
  'docs/keyboard-shortcuts.md': 'docs/keyboard-shortcuts.md',
  'for help on Qwen Code': '  Qwen Code',
  'show version info': '   ',
  'submit a bug report': '   ',
  Status: '',

  // Keyboard shortcuts panel descriptions
  'for shell mode': ' ',
  'for commands': ' ',
  'for file paths': '  ',
  'to clear input': ' ',
  'to cycle approvals': ' ',
  'to quit': '',
  'for newline': ' ',
  'to clear screen': ' ',
  'to search history': '  ',
  'to paste images': ' ',
  'for external editor': ' ',
  'to toggle compact mode': '  ',

  // ============================================================================
  //   
  // ============================================================================
  'Qwen Code': 'Qwen Code',
  Runtime: ' ',
  OS: '',
  Auth: '',
  Model: '',
  'Fast Model': ' ',
  Sandbox: '',
  'Session ID': 'ID ',
  'Base URL': 'Base URL',
  Proxy: '',
  'Memory Usage': ' ',
  'IDE Client': ' IDE',

  // ============================================================================
  //  - 
  // ============================================================================
  'Analyzes the project and creates a tailored QWEN.md file.':
    '      QWEN.md',
  'List available Qwen Code tools. Usage: /tools [desc]':
    '   Qwen Code. : /tools [desc]',
  'List available skills.': '  .',
  'Available Qwen Code CLI tools:': '  Qwen Code CLI:',
  'No tools available': '  ',
  'View or change the approval mode for tool usage':
    '       ',
  'Invalid approval mode "{{arg}}". Valid modes: {{modes}}':
    '   "{{arg}}".  : {{modes}}',
  'Approval mode set to "{{mode}}"':
    '    "{{mode}}"',
  'View or change the language setting':
    '    ',
  'List background tasks (text dump -- interactive dialog opens via the footer pill)':
    '   ( ;       )',
  'Delete a previous session': '  ',
  'Run installation and environment diagnostics':
    '    ',
  'Browse dynamic model catalogs and choose which models stay enabled locally':
    '     ,     ',
  'Generate a one-line session recap now':
    '    ',
  'Rename the current conversation. --auto lets the fast model pick a title.':
    '  . --auto     .',
  'Rewind conversation to a previous turn':
    '    ',
  'Rewind Conversation': ' ',
  'No user turns to rewind to.': '    .',
  'Rewind to: ': ' : ',
  'Restore code and conversation': '   ',
  'Restore conversation only': '  ',
  'Restore code only': '  ',
  'Never mind': '',
  'Computing file changes...': '  ...',
  'Restoring...': '...',
  'Restored {{count}} file(s).': ' : {{count}}.',
  'Failed to restore files: {{error}}':
    '   : {{error}}',
  'Rewind failed: {{error}}': ' : {{error}}',
  'Cannot rewind conversation: no active model client.':
    '  :    .',
  'Code restored, but conversation could not be rewound (no active client).':
    ' ,      (  ).',
  'Conversation rewound. Edit your prompt and press Enter to continue.':
    ' .     Enter,  .',
  'Rewinding does not affect files edited manually or via shell commands.':
    '   ,      shell-.',
  'Cannot rewind to a turn that was compressed. Try a more recent turn.':
    '     .    .',
  'File restore is unavailable for this turn (no captured file changes, or this turn predates the current session).':
    '      (        ).',
  '(+{{insertions}} -{{deletions}} in {{count}} file)':
    '(+{{insertions}} -{{deletions}}  {{count}} )',
  '(+{{insertions}} -{{deletions}} in {{count}} files)':
    '(+{{insertions}} -{{deletions}}  {{count}} )',
  'Failed to restore {{count}} file(s): {{files}}':
    '   {{count}} (): {{files}}',
  'Cannot restore files: this turn was created before file checkpointing was enabled.':
    '  :         .',
  'No files needed to be restored.': '    .',
  ' to navigate  Enter to select  Esc to go back':
    '   Enter   Esc ',
  ' to navigate  Enter to select  Esc to cancel':
    '   Enter   Esc ',
  'Enter/Y to confirm  Esc/N to go back': 'Enter/Y   Esc/N ',
  'change the theme': ' ',
  'Select Theme': ' ',
  Preview: '',
  '(Use Enter to select, Tab to configure scope)':
    '(Enter  , Tab   )',
  '(Use Enter to apply scope, Tab to go back)':
    '(Enter   , Tab  )',
  'Theme configuration unavailable due to NO_COLOR env variable.':
    '   -   NO_COLOR.',
  'Theme "{{themeName}}" not found.': ' "{{themeName}}"  .',
  'Theme "{{themeName}}" not found in selected scope.':
    ' "{{themeName}}"     .',
  'Clear conversation history and free up context':
    '     ',
  'Compresses the context by replacing it with a summary.':
    '     ',
  'open full Qwen Code documentation in your browser':
    '   Qwen Code  ',
  'Configuration not available.': ' .',
  'Connect an LLM provider': '  LLM',
  'Copy the last result or code snippet to clipboard':
    '        ',

  // ============================================================================
  //  - 
  // ============================================================================
  'Manage subagents for specialized task delegation.':
    '     ',
  'Manage existing subagents (view, edit, delete).':
    '   (, , )',
  'Create a new subagent with guided setup.':
    '     ',

  // ============================================================================
  //  -  
  // ============================================================================
  Agents: '',
  'Choose Action': ' ',
  'Edit {{name}}': ' {{name}}',
  'Edit Tools: {{name}}': ' : {{name}}',
  'Edit Color: {{name}}': ' : {{name}}',
  'Delete {{name}}': ' {{name}}',
  'Unknown Step': ' ',
  'Esc to close': 'Esc  ',
  'Enter to select,  to navigate, Esc to close':
    'Enter  ,   , Esc  ',
  'Esc to go back': 'Esc  ',
  'Enter to confirm, Esc to cancel': 'Enter  , Esc  ',
  'Enter to select,  to navigate, Esc to go back':
    'Enter  ,   , Esc  ',
  'Enter to submit, Esc to go back': 'Enter  , Esc  ',
  'Invalid step: {{step}}': ' : {{step}}',
  'No subagents found.': '  .',
  "Use '/agents create' to create your first subagent.":
    " '/agents create'    .",
  '(built-in)': '()',
  '(overridden by project level agent)':
    '(   )',
  'Project Level ({{path}})': '  ({{path}})',
  'User Level ({{path}})': '  ({{path}})',
  'Built-in Agents': ' ',
  'Extension Agents': ' ',
  'Using: {{count}} agents': ': {{count}} ()',
  'View Agent': ' ',
  'Edit Agent': ' ',
  'Delete Agent': ' ',
  Back: '',
  'No agent selected': '  ',
  'File Path: ': '  : ',
  'Tools: ': ': ',
  'Color: ': ': ',
  'Description:': ':',
  'System Prompt:': ' :',
  'Open in editor': '  ',
  'Edit tools': ' ',
  'Edit color': ' ',
  ' Error:': ' :',
  'Are you sure you want to delete agent "{{name}}"?':
    ' ,     "{{name}}"?',
  // ============================================================================
  //  -  
  // ============================================================================
  'Project Level (.qwen/agents/)': '  (.qwen/agents/)',
  'User Level (~/.qwen/agents/)': '  (~/.qwen/agents/)',
  ' Subagent Created Successfully!': '   !',
  'Subagent "{{name}}" has been saved to {{level}} level.':
    ' "{{name}}"    {{level}}.',
  'Name: ': ': ',
  'Location: ': ': ',
  ' Error saving subagent:': '   :',
  'Warnings:': ':',
  'Name "{{name}}" already exists at {{level}} level - will overwrite existing subagent':
    ' "{{name}}"     {{level}} -    ',
  'Name "{{name}}" exists at user level - project level will take precedence':
    ' "{{name}}"     -     ',
  'Name "{{name}}" exists at project level - existing subagent will take precedence':
    ' "{{name}}"     -     ',
  'Description is over {{length}} characters':
    '  {{length}} ',
  'System prompt is over {{length}} characters':
    '   {{length}} ',
  //  -   
  'Step {{n}}: Choose Location': ' {{n}}:  ',
  'Step {{n}}: Choose Generation Method': ' {{n}}:   ',
  'Generate with Qwen Code (Recommended)':
    '   Qwen Code ()',
  'Manual Creation': ' ',
  'Describe what this subagent should do and when it should be used. (Be comprehensive for best results)':
    ',          . (    )',
  'e.g., Expert code reviewer that reviews code based on best practices...':
    ',   ,      ...',
  'Generating subagent configuration...': '  ...',
  'Failed to generate subagent: {{error}}':
    '   : {{error}}',
  'Step {{n}}: Describe Your Subagent': ' {{n}}:  ',
  'Step {{n}}: Enter Subagent Name': ' {{n}}:   ',
  'Step {{n}}: Enter System Prompt': ' {{n}}:   ',
  'Step {{n}}: Enter Description': ' {{n}}:  ',
  //  -  
  'Step {{n}}: Select Tools': ' {{n}}:  ',
  'All Tools (Default)': '  ( )',
  'All Tools': ' ',
  'Read-only Tools': '   ',
  'Read & Edit Tools': '    ',
  'Read & Edit & Execution Tools':
    '  ,   ',
  'All tools selected, including MCP tools':
    '  ,  MCP tools',
  'Selected tools:': ' :',
  'Read-only tools:': '   :',
  'Edit tools:': ' :',
  'Execution tools:': ' :',
  'Step {{n}}: Choose Background Color': ' {{n}}:   ',
  'Step {{n}}: Confirm and Save': ' {{n}}:   ',
  //  -   
  'Esc to cancel': 'Esc  ',
  'Press Enter to save, e to save and edit, Esc to go back':
    'Enter  , e    , Esc  ',
  'Press Enter to continue, {{navigation}}Esc to {{action}}':
    'Enter  , {{navigation}}Esc  {{action}}',
  cancel: '',
  'go back': '',
  ' to navigate, ': '  , ',
  'Enter a clear, unique name for this subagent.':
    ' ,     .',
  'e.g., Code Reviewer': ',  ',
  'Name cannot be empty.': '    .',
  "Write the system prompt that defines this subagent's behavior. Be comprehensive for best results.":
    '  ,   .     .',
  'e.g., You are an expert code reviewer...':
    ',    ...',
  'System prompt cannot be empty.': '     .',
  'Describe when and how this subagent should be used.':
    ',       .',
  'e.g., Reviews code for best practices and potential bugs.':
    ',         .',
  'Description cannot be empty.': '    .',
  'Failed to launch editor: {{error}}':
    '   : {{error}}',
  'Failed to save and edit subagent: {{error}}':
    '     : {{error}}',

  // ============================================================================
  //  -  ()
  // ============================================================================
  'View and edit Qwen Code settings': '    Qwen Code',
  Settings: '',
  'To see changes, Qwen Code must be restarted. Press r to exit and apply changes now.':
    '     Qwen Code.  r     .',
  // ============================================================================
  //  
  // ============================================================================
  'Vim Mode': ' Vim',
  'Attribution: commit': ': ',
  'Terminal Bell Notification': '  ',
  'Enable Usage Statistics': '   ',
  Theme: '',
  'Preferred Editor': ' ',
  'Auto-connect to IDE': '  IDE',
  'Debug Keystroke Logging': '    ',
  'Language: UI': ': ',
  'Language: Model': ': ',
  'Output Format': ' ',
  'Hide Window Title': '  ',
  'Show Status in Title': '   ',
  'Hide Tips': ' ',
  'Show Line Numbers in Code': '    ',
  'Show Citations': ' ',
  'Custom Witty Phrases': '  ',
  'Show Welcome Back Dialog': '  ',
  'Enable User Feedback': '  ',
  'How is Qwen doing this session? (optional)':
    '   Qwen   ? ()',
  Bad: '',
  Fine: '',
  Good: '',
  Dismiss: '',
  'Screen Reader Mode': '    ',
  'Max Session Turns': '.   ',
  'Skip Next Speaker Check': '   ',
  'Skip Loop Detection': '  ',
  'Skip Startup Context': '  ',
  'Enable OpenAI Logging': '  OpenAI',
  'OpenAI Logging Directory': '  OpenAI',
  Timeout: '',
  'Max Retries': '.  ',
  'Load Memory From Include Directories':
    '    ',
  'Respect .gitignore': ' .gitignore',
  'Respect .qwenignore': ' .qwenignore',
  'Enable Recursive File Search': '   ',
  'Interactive Shell (PTY)': '  (PTY)',
  'Show Color': ' ',
  'Auto Accept': '',
  'Use Ripgrep': ' Ripgrep',
  'Use Builtin Ripgrep': '  Ripgrep',
  'Tool Output Truncation Threshold': '   ',
  'Tool Output Truncation Lines': '   ',
  'Folder Trust': '  ',
  'Tool Schema Compliance': ' Tool Schema',
  //   
  'Auto (detect from system)': ' (  )',
  'Auto (detect terminal theme)': ' (  )',
  Auto: '',
  Text: '',
  JSON: 'JSON',
  Plan: '',
  Default: ' ',
  'Auto Edit': '',
  YOLO: 'YOLO',
  'toggle vim mode on/off': '/  vim',
  'check session stats. Usage: /stats [model|tools]':
    '  . : /stats [model|tools]',
  'Show model-specific usage statistics.':
    '   .',
  'Show tool-specific usage statistics.':
    '   .',
  'exit the cli': '  CLI',
  'Manage workspace directories':
    '   ',
  'Add directories to the workspace. Use comma to separate multiple paths':
    '    .     ',
  'Show all directories in the workspace':
    '     ',
  'set external editor preference':
    '   ',
  'Select Editor': ' ',
  'Editor Preference': ' ',
  'These editors are currently supported. Please note that some editors cannot be used in sandbox mode.':
    '     .  ,        .',
  'Your preferred editor is:': '  :',
  'Manage extensions': ' ',
  'Manage installed extensions': '  ',
  'Disable an extension': ' ',
  'Enable an extension': ' ',
  'Install an extension from a git repo or local path':
    '   Git-   ',
  'Uninstall an extension': ' ',
  'No extensions installed.': '  .',
  'Extension "{{name}}" not found.': ' "{{name}}"  .',
  'No extensions to update.': '   .',
  'Usage: /extensions install <source>':
    ': /extensions install <>',
  'Installing extension from "{{source}}"...':
    '   "{{source}}"...',
  'Extension "{{name}}" installed successfully.':
    ' "{{name}}"  .',
  'Failed to install extension from "{{source}}": {{error}}':
    '     "{{source}}": {{error}}',
  'Do you want to continue? [Y/n]: ': ' ? [Y/n]: ',
  'Do you want to continue?': ' ?',
  'Installing extension "{{name}}".': '  "{{name}}".',
  '**Extensions may introduce unexpected behavior. Ensure you have investigated the extension source and trust the author.**':
    '**    . ,        .**',
  'This extension will run the following MCP servers:':
    '    MCP servers:',
  local: '',
  remote: '',
  'This extension will add the following commands: {{commands}}.':
    '    : {{commands}}.',
  'This extension will append info to your QWEN.md context using {{fileName}}':
    '       QWEN.md   {{fileName}}',
  'This extension will install the following skills:':
    '    :',
  'This extension will install the following subagents:':
    '    :',
  'Installation cancelled for "{{name}}".': ' "{{name}}" .',
  'You are installing an extension from {{originSource}}. Some features may not work perfectly with Qwen Code.':
    '    {{originSource}}.        Qwen Code.',
  '--ref and --auto-update are not applicable for marketplace extensions.':
    '--ref  --auto-update     .',
  'Extension "{{name}}" installed successfully and enabled.':
    ' "{{name}}"    .',
  'The github URL, local path, or marketplace source (marketplace-url:plugin-name) of the extension to install.':
    'URL GitHub,       (marketplace-url:plugin-name)  .',
  'The git ref to install from.': 'Git-  .',
  'Enable auto-update for this extension.':
    '    .',
  'Enable pre-release versions for this extension.':
    ' -    .',
  'Acknowledge the security risks of installing an extension and skip the confirmation prompt.':
    '        .',
  'The source argument must be provided.':
    '   .',
  'Extension "{{name}}" successfully uninstalled.':
    ' "{{name}}"  .',
  'Uninstalls an extension.': ' .',
  'The name or source path of the extension to uninstall.':
    '      .',
  'Please include the name of the extension to uninstall as a positional argument.':
    ',       .',
  'Enables an extension.': ' .',
  'The name of the extension to enable.': '  .',
  'The scope to enable the extenison in. If not set, will be enabled in all scopes.':
    '   .   ,     .',
  'Extension "{{name}}" successfully enabled for scope "{{scope}}".':
    ' "{{name}}"     "{{scope}}".',
  'Extension "{{name}}" successfully enabled in all scopes.':
    ' "{{name}}"     .',
  'Invalid scope: {{scope}}. Please use one of {{scopes}}.':
    ' : {{scope}}. ,    {{scopes}}.',
  'Disables an extension.': ' .',
  'The name of the extension to disable.': '  .',
  'The scope to disable the extenison in.':
    '   .',
  'Extension "{{name}}" successfully disabled for scope "{{scope}}".':
    ' "{{name}}"     "{{scope}}".',
  'Extension "{{name}}" successfully updated: {{oldVersion}} -> {{newVersion}}.':
    ' "{{name}}"  : {{oldVersion}} -> {{newVersion}}.',
  'Unable to install extension "{{name}}" due to missing install metadata':
    '   "{{name}}" -   ',
  'Extension "{{name}}" is already up to date.':
    ' "{{name}}"  .',
  'Updates all extensions or a named extension to the latest version.':
    '        .',
  'The name of the extension to update.': '  .',
  'Update all extensions.': '  .',
  'Either an extension name or --all must be provided':
    '     --all',
  'Lists installed extensions.': '  .',
  'Path:': ':',
  'Source:': ':',
  'Type:': ':',
  'Ref:': ':',
  'Release tag:': ' :',
  'Enabled (User):': ' ():',
  'Enabled (Workspace):': ' ( ):',
  'Context files:': ' :',
  'Skills:': ':',
  'Agents:': ':',
  'MCP servers:': 'MCP servers:',
  'Link extension failed to install.':
    '    .',
  'Extension "{{name}}" linked successfully and enabled.':
    ' "{{name}}"    .',
  'Links an extension from a local path. Updates made to the local path will always be reflected.':
    '    .       .',
  'The name of the extension to link.': '  .',
  'Set a specific setting for an extension.':
    '    .',
  'Name of the extension to configure.': '  .',
  'The setting to configure (name or env var).':
    '   (   ).',
  'The scope to set the setting in.': '   .',
  'List all settings for an extension.': '   .',
  'Name of the extension.': ' .',
  'Extension "{{name}}" has no settings to configure.':
    ' "{{name}}"     .',
  'Settings for "{{name}}":': '  "{{name}}":',
  '(workspace)': '( )',
  '(user)': '()',
  '[not set]': '[ ]',
  '[value stored in keychain]': '[    ]',
  'Manage extension settings.': '  .',
  'You need to specify a command (set or list).':
    '   (set  list).',
  // ============================================================================
  // Plugin Choice / Marketplace
  // ============================================================================
  'No plugins available in this marketplace.':
    '     .',
  'Select a plugin to install from marketplace "{{name}}":':
    '      "{{name}}":',
  'Plugin selection cancelled.': '  .',
  'Select a plugin from "{{name}}"': '   "{{name}}"',
  'Use  or j/k to navigate, Enter to select, Escape to cancel':
    '   j/k  , Enter  , Escape  ',
  '{{count}} more above': ' {{count}} ',
  '{{count}} more below': ' {{count}} ',
  'manage IDE integration': '   IDE',
  'check status of IDE integration': '    IDE',
  'install required IDE companion for {{ideName}}':
    '   IDE  {{ideName}}',
  'enable IDE integration': '   IDE',
  'disable IDE integration': '   IDE',
  'IDE integration is not supported in your current environment. To use this feature, run Qwen Code in one of these supported IDEs: VS Code or VS Code forks.':
    '  IDE     .      Qwen Code     IDE: VS Code   VS Code.',
  'Set up GitHub Actions': ' GitHub Actions',
  'Configure terminal keybindings for multiline input (VS Code, Cursor, Windsurf, Trae)':
    '       (VS Code, Cursor, Windsurf, Trae)',
  'Please restart your terminal for the changes to take effect.':
    ',     .',
  'Failed to configure terminal: {{error}}':
    '   : {{error}}',
  'Could not determine {{terminalName}} config path on Windows: APPDATA environment variable is not set.':
    '     {{terminalName}}  Windows:   APPDATA  .',
  '{{terminalName}} keybindings.json exists but is not a valid JSON array. Please fix the file manually or delete it to allow automatic configuration.':
    '{{terminalName}} keybindings.json ,      JSON. ,         .',
  'File: {{file}}': ': {{file}}',
  'Failed to parse {{terminalName}} keybindings.json. The file contains invalid JSON. Please fix the file manually or delete it to allow automatic configuration.':
    '   {{terminalName}} keybindings.json.    JSON. ,         .',
  'Error: {{error}}': ': {{error}}',
  'Shift+Enter binding already exists': ' Shift+Enter  ',
  'Ctrl+Enter binding already exists': ' Ctrl+Enter  ',
  'Existing keybindings detected. Will not modify to avoid conflicts.':
    '   .      .',
  'Please check and modify manually if needed: {{file}}':
    ',      : {{file}}',
  'Added Shift+Enter and Ctrl+Enter keybindings to {{terminalName}}.':
    '  Shift+Enter  Ctrl+Enter  {{terminalName}}.',
  'Modified: {{file}}': ': {{file}}',
  '{{terminalName}} keybindings already configured.':
    '  {{terminalName}}  .',
  'Failed to configure {{terminalName}}.':
    '   {{terminalName}}.',
  'Your terminal is already configured for an optimal experience with multiline input (Shift+Enter and Ctrl+Enter).':
    '          (Shift+Enter  Ctrl+Enter).',
  // ============================================================================
  // Commands - Hooks
  // ============================================================================
  'Manage Qwen Code hooks': '  Qwen Code',
  'List all configured hooks': '   ',
  // Hooks - Dialog
  Hooks: '',
  'Loading hooks...': ' ...',
  'Error loading hooks:': '  :',
  'Press Escape to close': ' Escape  ',
  'Press Escape, Ctrl+C, or Ctrl+D to cancel':
    ' Escape, Ctrl+C  Ctrl+D  ',
  'Press Space, Enter, or Escape to dismiss':
    ' Space, Enter  Escape  ',
  'No hook selected': '  ',
  // Hooks - List Step
  'No hook events found.': '   .',
  '{{count}} hook configured': '{{count}}  ',
  '{{count}} hooks configured': '{{count}}  ',
  'This menu is read-only. To add or modify hooks, edit settings.json directly or ask Qwen Code.':
    '    .     ,  settings.json    Qwen Code.',
  'Enter to select  Esc to cancel': 'Enter    Esc  ',
  // Hooks - Detail Step
  'Exit codes:': ' :',
  'Configured hooks:': ' :',
  'No hooks configured for this event.':
    '     .',
  'To add hooks, edit settings.json directly or ask Qwen.':
    '  ,  settings.json    Qwen.',
  'Enter to select  Esc to go back': 'Enter    Esc  ',
  // Hooks - Config Detail Step
  'Hook details': ' ',
  'Event:': ':',
  'Extension:': ':',
  'Desc:': ':',
  'No hook config selected': '   ',
  'To modify or remove this hook, edit settings.json directly or ask Qwen to help.':
    '     ,  settings.json    Qwen.',
  // Hooks - Disabled Step
  'Hook Configuration - Disabled': '  - ',
  'All hooks are currently disabled. You have {{count}} that are not running.':
    '     .   {{count}}  .',
  '{{count}} configured hook': '{{count}}  ',
  '{{count}} configured hooks': '{{count}}  ',
  'When hooks are disabled:': '  :',
  'No hook commands will execute': '     ',
  'StatusLine will not be displayed': 'StatusLine   ',
  'Tool operations will proceed without hook validation':
    '      ',
  'To re-enable hooks, remove "disableAllHooks" from settings.json or ask Qwen Code.':
    '   ,  "disableAllHooks"  settings.json   Qwen Code.',
  // Hooks - Source
  Project: '',
  User: '',
  Skill: '',
  System: '',
  Extension: '',
  'Local Settings': ' ',
  'User Settings': ' ',
  'System Settings': ' ',
  Extensions: '',
  'Session (temporary)': ' ()',
  // Hooks - Event Descriptions (short)
  'Before tool execution': '  ',
  'After tool execution': '  ',
  'After tool execution fails': '   ',
  'When notifications are sent': '  ',
  'When the user submits a prompt': '   ',
  'When a new session is started': '   ',
  'Right before Qwen Code concludes its response':
    '    Qwen Code',
  'When a subagent (Agent tool call) is started':
    '   (  Agent)',
  'Right before a subagent concludes its response':
    '    ',
  'Before conversation compaction': '  ',
  'When a session is ending': '  ',
  'When a permission dialog is displayed': '   ',
  'When a new todo item is created': '   ',
  'When a todo item is marked as completed':
    '    ',
  // Hooks - Event Descriptions (detailed)
  'Input to command is JSON of tool call arguments.':
    '   --  JSON   .',
  'Input to command is JSON with fields "inputs" (tool call arguments) and "response" (tool call response).':
    '   --  JSON   "inputs" (  )  "response" (  ).',
  'Input to command is JSON with tool_name, tool_input, tool_use_id, error, error_type, is_interrupt, and is_timeout.':
    '   --  JSON  tool_name, tool_input, tool_use_id, error, error_type, is_interrupt  is_timeout.',
  'Input to command is JSON with notification message and type.':
    '   --  JSON     .',
  'Input to command is JSON with original user prompt text.':
    '   --  JSON     .',
  'Input to command is JSON with session start source.':
    '   --  JSON    .',
  'Input to command is JSON with session end reason.':
    '   --  JSON    .',
  'Input to command is JSON with agent_id and agent_type.':
    '   --  JSON  agent_id  agent_type.',
  'Input to command is JSON with agent_id, agent_type, and agent_transcript_path.':
    '   --  JSON  agent_id, agent_type  agent_transcript_path.',
  'Input to command is JSON with compaction details.':
    '   --  JSON   .',
  'Input to command is JSON with tool_name, tool_input, and tool_use_id. Output JSON with hookSpecificOutput containing decision to allow or deny.':
    '   --  JSON  tool_name, tool_input  tool_use_id.  -- JSON  hookSpecificOutput,      .',
  'Input to command is JSON with todo_id, todo_content, todo_status, all_todos, and phase. In validation, output JSON with decision (allow/block/deny) and reason. In postWrite, block/deny is ignored.':
    '   --  JSON  todo_id, todo_content, todo_status, all_todos  phase.  validation  -- JSON  decision (allow/block/deny)  reason.  postWrite block/deny .',
  'Input to command is JSON with todo_id, todo_content, previous_status, all_todos, and phase. In validation, output JSON with decision (allow/block/deny) and reason. In postWrite, block/deny is ignored.':
    '   --  JSON  todo_id, todo_content, previous_status, all_todos  phase.  validation  -- JSON  decision (allow/block/deny)  reason.  postWrite block/deny .',
  // Hooks - Exit Code Descriptions
  'stdout/stderr not shown': 'stdout/stderr  ',
  'show stderr to model and continue conversation':
    ' stderr    ',
  'show stderr to user only': ' stderr  ',
  'stdout shown in transcript mode (ctrl+o)':
    'stdout     (ctrl+o)',
  'show stderr to model immediately': ' stderr  ',
  'show stderr to user only but continue with tool call':
    ' stderr  ,    ',
  'block processing, erase original prompt, and show stderr to user only':
    ' ,      stderr  ',
  'stdout shown to Qwen': 'stdout  Qwen',
  'show stderr to user only (blocking errors ignored)':
    ' stderr   (  )',
  'command completes successfully': '  ',
  'stdout shown to subagent': 'stdout  ',
  'show stderr to subagent and continue having it run':
    ' stderr     ',
  'stdout appended as custom compact instructions':
    'stdout     ',
  'block compaction': ' ',
  'show stderr to user only but continue with compaction':
    ' stderr  ,   ',
  'use hook decision if provided':
    '  ,  ',
  'allow todo creation': '  ',
  'block todo creation and show reason to model':
    '      ',
  'allow todo completion': '  ',
  'block todo completion and show reason to model':
    '      ',
  // Hooks - Messages
  'Config not loaded.': '  .',
  'Hooks are not enabled. Enable hooks in settings to use this feature.':
    '  .    ,    .',
  // ============================================================================
  // Commands - Session Export
  // ============================================================================
  'Export current session message history to a file':
    '      ',
  'Export session to HTML format': '    HTML',
  'Export session to JSON format': '    JSON',
  'Export session to JSONL format (one message per line)':
    '    JSONL (   )',
  'Export session to markdown format':
    '    Markdown',

  // ============================================================================
  // Commands - Insights
  // ============================================================================
  'generate personalized programming insights from your chat history':
    '        ',

  // ============================================================================
  // Commands - Session History
  // ============================================================================
  'Resume a previous session': '  ',
  'Fork the current conversation into a new session':
    '      ',
  'Cannot branch while a response or tool call is in progress. Wait for it to finish or resolve the pending tool call.':
    '  ,      .       .',
  'No conversation to branch.': '    .',
  'Restore a tool call. This will reset the conversation and file history to the state it was in when the tool call was suggested':
    '  .          ,      ',
  'Could not detect terminal type. Supported terminals: VS Code, Cursor, Windsurf, and Trae.':
    '    .  : VS Code, Cursor, Windsurf  Trae.',
  'Terminal "{{terminal}}" is not supported yet.':
    ' "{{terminal}}"   .',

  // ============================================================================
  //  - 
  // ============================================================================
  'Invalid language. Available: {{options}}':
    ' . : {{options}}',
  'Language subcommands do not accept additional arguments.':
    '     .',
  'Current UI language: {{lang}}': '  : {{lang}}',
  'Current LLM output language: {{lang}}': '   LLM: {{lang}}',
  'Set UI language': '  ',
  'Set LLM output language': '   LLM',
  'Usage: /language ui [{{options}}]':
    ': /language ui [{{options}}]',
  'Usage: /language output <language>':
    ': /language output <language>',
  'Example: /language output ': ': /language output ',
  'Example: /language output English': ': /language output English',
  'Example: /language output ': ': /language output ',
  'UI language changed to {{lang}}': '    {{lang}}',
  'LLM output language set to {{lang}}':
    '  LLM   {{lang}}',
  'Please restart the application for the changes to take effect.':
    ',     .',
  'Failed to generate LLM output language rule file: {{error}}':
    '       LLM: {{error}}',
  'Invalid command. Available subcommands:':
    ' .  :',
  'Available subcommands:': ' :',
  'To request additional UI language packs, please open an issue on GitHub.':
    '     , ,    GitHub.',
  'Available options:': ' :',
  'Set UI language to {{name}}': '    {{name}}',

  // ============================================================================
  //  -  
  // ============================================================================
  'Tool Approval Mode': '  ',
  '{{mode}} mode': ' {{mode}}',
  'Analyze only, do not modify files or execute commands':
    ' ,      ',
  'Require approval for file edits or shell commands':
    '       ',
  'Automatically approve file edits':
    '   ',
  'Automatically approve all tools':
    '   ',
  'Workspace approval mode exists and takes priority. User-level change will have no effect.':
    '       .        .',
  'Apply To': ' ',
  'Workspace Settings': '  ',
  'Open auto-memory folder': '  ',
  'Auto-memory: {{status}}': ': {{status}}',
  'Auto-dream: {{status}}  {{lastDream}}  /dream to run':
    ': {{status}}  {{lastDream}}  /dream  ',
  never: '',
  on: '',
  off: '',
  'Remove matching entries from managed auto-memory.':
    '     .',
  'Usage: /forget <memory text to remove>':
    ': /forget <   >',
  'No managed auto-memory entries matched: {{query}}':
    '    : {{query}}',
  'Consolidate managed auto-memory topic files.':
    '    .',
  'Could not retrieve tool registry.':
    '    .',
  "Successfully authenticated and refreshed tools for '{{name}}'.":
    "      '{{name}}'.",
  "Re-discovering tools from '{{name}}'...":
    "    '{{name}}'...",
  "Discovered {{count}} tool(s) from '{{name}}'.":
    " {{count}} ()  '{{name}}'.",
  'Authentication complete. Returning to server details...':
    ' .    ...',
  'Authentication successful.': ' .',
  // =========================================================
  //  - 
  // ============================================================================
  'Generate a project summary and save it to .qwen/PROJECT_SUMMARY.md':
    '       .qwen/PROJECT_SUMMARY.md',
  'No chat client available to generate summary.':
    '  -   .',
  'Already generating summary, wait for previous request to complete':
    '   ,    ',
  'No conversation found to summarize.':
    '     .',
  'Failed to generate project context summary: {{error}}':
    '     : {{error}}',
  'Saved project summary to {{filePathForDisplay}}.':
    '    {{filePathForDisplay}}',
  'Saving project summary...': '  ...',
  'Generating project summary...': '  ...',
  'Processing summary...': ' ...',
  'Project summary generated and saved successfully!':
    '     !',
  'Saved to: {{filePath}}': ' : {{filePath}}',
  'Stopped because': ',  ',
  'Failed to generate summary - no text content received from LLM response':
    '    -       LLM',

  // ============================================================================
  //  - 
  // ============================================================================
  'Switch the model for this session (--fast for suggestion model, [model-id] to switch immediately).':
    '     (--fast   )',
  'Set a lighter model for prompt suggestions and speculative execution':
    '       ',
  'Content generator configuration not available.':
    '   .',
  'Authentication type not available.': '  .',
  'No models available for the current authentication type ({{authType}}).':
    '       ({{authType}}).',
  // Needs translation

  // ============================================================================
  //  - 
  // ============================================================================
  'Starting a new session, resetting chat, and clearing terminal.':
    '  ,     .',
  'Starting a new session and clearing.': '    .',

  // ============================================================================
  //  - 
  // ============================================================================
  'Already compressing, wait for previous request to complete':
    '  ,    ',
  'Failed to compress chat history.': '    .',
  'Failed to compress chat history: {{error}}':
    '    : {{error}}',
  'Compressing chat history': '  ',
  'Chat history compressed from {{originalTokens}} to {{newTokens}} tokens.':
    '    {{originalTokens}}  {{newTokens}} .',
  'Compression was not beneficial for this history size.':
    '       .',
  'Chat history compression did not reduce size. This may indicate issues with the compression prompt.':
    '     .        .',
  'Could not compress chat history due to a token counting error.':
    '     -   .',
  // ============================================================================
  //  - 
  // ============================================================================
  'Configuration is not available.': ' .',
  'Please provide at least one path to add.':
    ',       .',
  'The /directory add command is not supported in restrictive sandbox profiles. Please use --include-directories when starting the session instead.':
    ' /directory add      . ,  --include-directories   .',
  "Error adding '{{path}}': {{error}}":
    "   '{{path}}': {{error}}",
  'Successfully added QWEN.md files from the following directories if there are:\n- {{directories}}':
    '   QWEN.md    (  ):\n- {{directories}}',
  'Error refreshing memory: {{error}}':
    '   : {{error}}',
  'Successfully added directories:\n- {{directories}}':
    '  :\n- {{directories}}',
  'Current workspace directories:\n{{directories}}':
    '   :\n{{directories}}',

  // ============================================================================
  //  - 
  // ============================================================================
  'Please open the following URL in your browser to view the documentation:\n{{url}}':
    ',   URL     :\n{{url}}',
  'Opening documentation in your browser: {{url}}':
    '   : {{url}}',

  // ============================================================================
  //  -  
  // ============================================================================
  'Do you want to proceed?': '  ?',
  'Yes, allow once': ',   ',
  'Allow always': ' ',
  Yes: '',
  No: '',
  'No (esc)': ' (esc)',
  // MCP Management - Core translations
  Disable: '',
  Enable: '',
  Authenticate: '',
  'Re-authenticate': ' ',
  'Clear Authentication': ' ',
  disabled: '',
  enabled: '',
  'Server:': ':',
  Reconnect: '',
  'View tools': ' ',
  'Error:': ':',
  tool: '',
  connected: '',
  connecting: '',
  disconnected: '',
  error: '',
  // Invalid tool related translations
  '{{count}} invalid tools': '{{count}}  ',
  invalid: '',
  'invalid: {{reason}}': ': {{reason}}',
  'missing name': ' ',
  'missing description': ' ',
  '(unnamed)': '( )',
  'Warning: This tool cannot be called by the LLM':
    ':       LLM',
  Reason: '',
  'Tools must have both name and description to be used by the LLM.':
    '    ,   ,   LLM.',
  'Modify in progress:': ' :',
  'Save and close external editor to continue':
    '      ',
  'Apply this change?': '  ?',
  'Yes, allow always': ',  ',
  'Modify with external editor': '   ',
  'No, suggest changes (esc)': ',   (esc)',
  "Allow execution of: '{{command}}'?": " : '{{command}}'?",
  'Always allow in this project': '    ',
  'Always allow {{action}} in this project':
    '  {{action}}   ',
  'Always allow for this user': '    ',
  'Always allow {{action}} for this user':
    '  {{action}}   ',
  'Yes, restore previous mode ({{mode}})':
    ',    ({{mode}})',
  'Yes, and auto-accept edits': ',    ',
  'Yes, and manually approve edits': ',    ',
  'No, keep planning (esc)': ',   (esc)',
  'URLs to fetch:': 'URL  :',
  'MCP Server: {{server}}': 'MCP Server: {{server}}',
  'Tool: {{tool}}': ': {{tool}}',
  'Allow execution of MCP tool "{{tool}}" from server "{{server}}"?':
    '  MCP tool "{{tool}}"  MCP server "{{server}}"?',
  // ============================================================================
  //  -  
  // ============================================================================
  'Shell Command Execution': '  ',
  'A custom command wants to run the following shell commands:':
    '      :',
  // ============================================================================
  //  -   
  // ============================================================================
  'Current Plan:': ' :',
  'Progress: {{done}}/{{total}} tasks completed':
    ': {{done}}/{{total}}  ',
  ', {{inProgress}} in progress': ', {{inProgress}}  ',
  'Pending Tasks:': ' :',
  'What would you like to do?': '   ?',
  'Choose how to proceed with your session:':
    ',   :',
  'Start new chat session': '   ',
  'Continue previous conversation': '  ',
  ' Welcome back! (Last updated: {{timeAgo}})':
    '  ! ( : {{timeAgo}})',
  ' Overall Goal:': '  :',
  'Connect a Provider': ' ',
  'You must connect a provider to proceed. Press Ctrl+C again to exit.':
    '    .  Ctrl+C   .',
  'Terms of Services and Privacy Notice':
    '     ',
  'Qwen OAuth': 'Qwen OAuth',
  'Discontinued -- switch to Coding Plan or API Key':
    ' --   Coding Plan  API Key',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Please select Coding Plan or API Key instead.':
    '  Qwen OAuth  2026-04-15.  Coding Plan  API Key.',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Please select a model from another provider or run /auth to switch.':
    '  Qwen OAuth   2026-04-15. ,        /auth  .',
  '\n Qwen OAuth free tier was discontinued on 2026-04-15. Please select another option.\n':
    '\n   Qwen OAuth  2026-04-15.   .\n',
  'Paid \u00B7 Up to 6,000 requests/5 hrs \u00B7 All Alibaba Cloud Coding Plan Models':
    ' \u00B7  6 000 /5  \u00B7   Alibaba Cloud Coding Plan',
  'Alibaba Cloud Coding Plan': 'Alibaba Cloud Coding Plan',
  'Bring your own API key': '  API Key',
  'Browser-based authentication with third-party providers (e.g. OpenRouter, ModelScope)':
    '      (, OpenRouter, ModelScope)',
  'Authentication is enforced to be {{enforcedType}}, but you are currently using {{currentType}}.':
    '   {{enforcedType}},     {{currentType}}.',
  'Qwen OAuth Authentication': ' Qwen OAuth',
  'Please visit this URL to authorize:':
    ',   URL  :',
  'Waiting for authorization': ' ',
  'Time remaining:': ' :',
  'Qwen OAuth Authentication Timeout': '  Qwen OAuth',
  'OAuth token expired (over {{seconds}} seconds). Please select authentication method again.':
    ' OAuth  ( {{seconds}} ). ,    .',
  'Press any key to return to authentication type selection.':
    '        .',
  'Waiting for Qwen OAuth authentication...':
    '  Qwen OAuth...',
  'Authentication timed out. Please try again.':
    '   . ,  .',
  'Waiting for auth... (Press ESC or CTRL+C to cancel)':
    ' ... ( ESC  CTRL+C  )',
  'Missing API key for OpenAI-compatible auth. Set settings.security.auth.apiKey, or set the {{envKeyHint}} environment variable.':
    ' API Key  ,   OpenAI.  settings.security.auth.apiKey    {{envKeyHint}}.',
  '{{envKeyHint}} environment variable not found. Please set it in your .env file or environment variables.':
    '  {{envKeyHint}}  .     .env    .',
  '{{envKeyHint}} environment variable not found (or set settings.security.auth.apiKey). Please set it in your .env file or environment variables.':
    '  {{envKeyHint}}   (  settings.security.auth.apiKey).     .env    .',
  'Missing API key for OpenAI-compatible auth. Set the {{envKeyHint}} environment variable.':
    ' API Key  ,   OpenAI.    {{envKeyHint}}.',
  'Anthropic provider missing required baseUrl in modelProviders[].baseUrl.':
    '  Anthropic   baseUrl  modelProviders[].baseUrl.',
  'ANTHROPIC_BASE_URL environment variable not found.':
    '  ANTHROPIC_BASE_URL  .',
  'Invalid auth method selected.': '   .',
  'Failed to authenticate. Message: {{message}}':
    '  . : {{message}}',
  'Authenticated successfully with {{authType}} credentials.':
    '     {{authType}}.',
  'Invalid QWEN_DEFAULT_AUTH_TYPE value: "{{value}}". Valid values are: {{validValues}}':
    '  QWEN_DEFAULT_AUTH_TYPE: "{{value}}".  : {{validValues}}',
  // ============================================================================
  //  - 
  // ============================================================================
  'Select Model': ' ',
  'API Key': 'API Key',
  '(default)': '( )',
  '(not set)': '( )',
  Modality: '',
  'Context Window': ' ',
  text: '',
  'text-only': ' ',
  image: '',
  pdf: 'PDF',
  audio: '',
  video: '',
  'not set': ' ',
  none: '',
  unknown: '',
  // ============================================================================
  //  - 
  // ============================================================================
  'Manage folder trust settings': '    ',
  'Manage permission rules': ' permission rules',
  Allow: '',
  Ask: '',
  Deny: '',
  Workspace: ' ',
  "Qwen Code won't ask before using allowed tools.":
    'Qwen Code       .',
  'Qwen Code will ask before using these tools.':
    'Qwen Code     .',
  'Qwen Code is not allowed to use denied tools.':
    'Qwen Code     .',
  'Manage trusted directories for this workspace.':
    '      .',
  'Any use of the {{tool}} tool': '   {{tool}}',
  "{{tool}} commands matching '{{pattern}}'":
    " {{tool}},  '{{pattern}}'",
  'From user settings': '  ',
  'From project settings': '  ',
  'From session': ' ',
  'Project settings': ' ',
  'Checked in at .qwen/settings.json': '  .qwen/settings.json',
  'User settings': ' ',
  'Saved in at ~/.qwen/settings.json': '  ~/.qwen/settings.json',
  'Add a new rule...': '  ...',
  'Add {{type}} permission rule': ' {{type}} permission rule',
  'Permission rules are a tool name, optionally followed by a specifier in parentheses.':
    'permission rules --   ,       .',
  'e.g.,': '.',
  or: '',
  'Enter permission rule...': ' permission rule...',
  'Enter to submit  Esc to cancel': 'Enter    Esc  ',
  'Where should this rule be saved?': '   ?',
  'Enter to confirm  Esc to cancel':
    'Enter    Esc  ',
  'Delete {{type}} rule?': '  {{type}}?',
  'Are you sure you want to delete this permission rule?':
    ' ,     permission rule?',
  'Permissions:': ':',
  '(<-/-> or tab to cycle)': '(<-/->  Tab  )',
  'Press  to navigate  Enter to select  Type to search  Esc to cancel':
    '   Enter       Esc ',
  'Search...': '...',
  // Workspace directory management
  'Add directory...': ' ...',
  'Add directory to workspace': '    ',
  'Qwen Code can read files in the workspace, and make edits when auto-accept edits is on.':
    'Qwen Code         ,    .',
  'Qwen Code will be able to read files in this directory and make edits when auto-accept edits is on.':
    'Qwen Code         ,    .',
  'Enter the path to the directory:': '   :',
  'Enter directory path...': '   ...',
  'Tab to complete  Enter to add  Esc to cancel':
    'Tab    Enter    Esc  ',
  'Remove directory?': ' ?',
  'Are you sure you want to remove this directory from the workspace?':
    ' ,        ?',
  '  (Original working directory)': '  (  )',
  '  (from settings)': '  ( )',
  'Directory does not exist.': '  .',
  'Path is not a directory.': '   .',
  'This directory is already in the workspace.':
    '      .',
  'Already covered by existing directory: {{dir}}':
    '   : {{dir}}',

  // ============================================================================
  //  
  // ============================================================================
  'Using:': ':',
  '{{count}} open file': '{{count}}  ',
  '{{count}} open files': '{{count}}  ()',
  '(ctrl+g to view)': '(ctrl+g  )',
  '{{count}} {{name}} file': '{{count}}  {{name}}',
  '{{count}} {{name}} files': '{{count}} () {{name}}',
  '{{count}} MCP server': '{{count}} MCP server',
  '{{count}} MCP servers': '{{count}} MCP servers',
  '{{count}} Blocked': '{{count}} ()',
  '(ctrl+t to view)': '(ctrl+t  )',
  '(ctrl+t to toggle)': '(ctrl+t  )',
  'Press Ctrl+C again to exit.': ' Ctrl+C   .',
  'Press Ctrl+D again to exit.': ' Ctrl+D   .',
  'Press Esc again to clear.': ' Esc   .',
  'Press  to edit queued messages':
    '      ',

  // ============================================================================
  //  MCP
  // ============================================================================
  'No MCP servers configured.': 'MCP servers  .',
  ' MCP servers are starting up ({{count}} initializing)...':
    ' MCP servers  ({{count}} )...',
  'Note: First startup may take longer. Tool availability will update automatically.':
    ':      .    .',
  'Configured MCP servers:': ' MCP servers:',
  Ready: '',
  'Starting... (first startup may take longer)':
    '... (     )',
  Disconnected: '',
  '{{count}} tool': '{{count}} ',
  '{{count}} tools': '{{count}} ()',
  '{{count}} prompt': '{{count}} ',
  '{{count}} prompts': '{{count}} ()',
  '(from {{extensionName}})': '( {{extensionName}})',
  OAuth: 'OAuth',
  'OAuth expired': 'OAuth ',
  'OAuth not authenticated': 'OAuth  ',
  'tools and prompts will appear when ready':
    '   ,   ',
  '{{count}} tools cached': '{{count}} ()  ',
  'Tools:': ':',
  'Parameters:': ':',
  'Prompts:': ':',
  Blocked: '',
  ' Tips:': ' :',
  Use: '',
  'to show server and tool descriptions':
    '     ',
  'to show tool parameter schemas': '  tool parameter schemas',
  'to hide descriptions': '  ',
  'to authenticate with OAuth-enabled servers':
    '      OAuth',
  Press: '',
  'to toggle tool descriptions on/off':
    '   ',
  "Starting OAuth authentication for MCP server '{{name}}'...":
    "  OAuth  MCP server '{{name}}'...",
  // ============================================================================
  //   
  // ============================================================================

  // ============================================================================
  //   / 
  // ============================================================================
  'Agent powering down. Goodbye!': '  .  !',
  'To continue this session, run': '   , ',
  'Interaction Summary': ' ',
  'Session ID:': 'ID :',
  'Tool Calls:': ' :',
  'Success Rate:': ' :',
  'User Agreement:': ' :',
  reviewed: '',
  'Code Changes:': ' :',
  Performance: '',
  'Wall Time:': ' :',
  'Agent Active:': ' :',
  'API Time:': ' API:',
  'Tool Time:': ' :',
  'Session Stats': ' ',
  'Model Usage': ' ',
  Reqs: '',
  'Input Tokens': ' ',
  'Output Tokens': ' ',
  'Savings Highlight:': ':',
  'of input tokens were served from the cache, reducing costs.':
    '    ,  .',
  'Tip: For a full token breakdown, run `/stats model`.':
    ':      `/stats model`.',
  'Model Stats For Nerds': '   ',
  'Tool Stats For Nerds': '   ',
  Metric: '',
  API: 'API',
  Requests: '',
  Errors: '',
  'Avg Latency': ' ',
  Tokens: '',
  Total: '',
  Prompt: '',
  Cached: '',
  Thoughts: '',
  Output: '',
  'No API calls have been made in this session.':
    '      API.',
  'Tool Name': ' ',
  Calls: '',
  'Success Rate': ' ',
  'Avg Duration': ' ',
  'User Decision Summary': '  ',
  'Total Reviewed Suggestions:': '  :',
  '  Accepted:': '  :',
  '  Rejected:': '  :',
  '  Modified:': '  :',
  ' Overall Agreement Rate:': '   :',
  'No tool calls have been made in this session.':
    '      .',
  'Session start time is unavailable, cannot calculate stats.':
    '   ,   .',

  // ============================================================================
  // Command Format Migration
  // ============================================================================
  'Command Format Migration': '  ',
  'Found {{count}} TOML command file:': ' {{count}}   TOML:',
  'Found {{count}} TOML command files:':
    ' {{count}}   TOML:',
  'Current tasks': ' ',
  '... and {{count}} more': '...   {{count}}',
  'The TOML format is deprecated. Would you like to migrate them to Markdown format?':
    ' TOML .      Markdown?',
  '(Backups will be created and original files will be preserved)':
    '(   ,    )',

  // ============================================================================
  // Loading Phrases
  // ============================================================================
  'Waiting for user confirmation...':
    '   ...',
  // ============================================================================

  // ============================================================================
  // Loading Phrases
  // ============================================================================
  WITTY_LOADING_PHRASES: [
    ' !',
    ' ... ',
    '   ...',
    '  ..',
    '   ...',
    ' ...',
    ' -...',
    '  ...',
    '  ...',
    ' ...',
    '   (  )...',
    '  ...',
    ' ...',
    '  ...',
    '    ...',
    ',  ...',
    ' ...',
    ' ...',
    ' ...',
    ' yumor.exe...',
    '  ...',
    '  ...',
    ',   ...',
    ' ...',
    '  ...',
    ' ,   ...',
    '   ...',
    ' ...   ...',
    ' ...  ,  ...',
    '  ...',
    '   (    )...',
    '   ',
    ' ...    ...',
    ' ...  ...',
    ' ...',
    '   ...',
    '  ...',
    ' ...',
    '    ...',
    '  ...',
    ' ...',
    '  ...',
    '  ...',
    ' ...',
    '    ...',
    '   ...',
    '   ...',
    ',   ...',
    '   ...',
    ',  ...',
    ',  ...',
    ',  ...',
    ',  ...',
    ',  ...',
    ',  ...',
    '- ...',
    '  ...',
    ' ...',
    '   ...',
    ' - ... ...',
    ' ...',
    '...  !',
    ' ...',
    '      12 ...',
    ' --  ,    ...',
    '    ...',
    ',   ...',
    " 'A'  ...",
    '  ...',
    ' ...',
    '     ...',
    '    ...',
    ' ... ...',
    '     ...',
    '   ...',
    ' ...',
    ' ...',
    'Never gonna give you up, never gonna let you down...',
    ' -...',
    '   ...',
    '  ,   ...',
    'Is this the real life? Is this just fantasy?...',
    '   ...',
    ' ... ( ...)',
    '  ...',
    ',    ...',
    '...  ...',
    '  ,   ? ...',
    '  ?     ...',
    '      ?    ...',
    '    ?       ...',
    '  ?      ...',
    '     ?  --  ...',
    '   ...',
    ',    ...',
    ',       ...',
    '   Vim...',
    '   ...',
    '  ,  ...',
    '!',
    ' ...  .',
    '   --  ...',
    '   ...',
    '  ...',
    '  ,   ...',
    '  ...',
    '  ,  , ,   ... ,   .',
    '  ...',
    '    ? -.',
    ' Java-   ?    ...',
    ' ... -!',
    '  ... !',
    '   ...  , .',
    ' -.',
    '...     .',
    '     ...',
    ' ...  .',
    '   ?!       ?!',
    '  ...  ,  .',
    ',    dial-up ...',
    ' .',
    '     .',
    ', -    ...',
    '...  ...   .',
    '  ,  ...  .',
    '    ? ( ,  !)',
    '   ...',
  ],

  // ============================================================================
  // Extension Settings Input
  // ============================================================================
  'Enter value...': ' ...',
  'Enter sensitive value...': '  ...',
  'Press Enter to submit, Escape to cancel':
    ' Enter  , Escape  ',

  // ============================================================================
  // Command Migration Tool
  // ============================================================================
  'Markdown file already exists: {{filename}}':
    'Markdown-  : {{filename}}',
  'TOML Command Format Deprecation Notice':
    '    TOML',
  'Found {{count}} command file(s) in TOML format:':
    ' {{count}} ()    TOML:',
  'The TOML format for commands is being deprecated in favor of Markdown format.':
    ' TOML       Markdown.',
  'Markdown format is more readable and easier to edit.':
    ' Markdown      .',
  'You can migrate these files automatically using:':
    '       :',
  'Or manually convert each file:': '    :',
  'TOML: prompt = "..." / description = "..."':
    'TOML: prompt = "..." / description = "..."',
  'Markdown: YAML frontmatter + content':
    'Markdown: YAML frontmatter + ',
  'The migration tool will:': ' :',
  'Convert TOML files to Markdown': ' TOML-  Markdown',
  'Create backups of original files': '    ',
  'Preserve all command functionality': '   ',
  'TOML format will continue to work for now, but migration is recommended.':
    ' TOML   ,   .',

  // ============================================================================
  // Extensions - Explore Command
  // ============================================================================
  'Open extensions page in your browser':
    '    ',
  'Unknown extensions source: {{source}}.':
    '  : {{source}}.',
  'Would open extensions page in your browser: {{url}} (skipped in test environment)':
    '      : {{url}} (   )',
  'View available extensions at {{url}}':
    '    {{url}}',
  'Opening extensions page in your browser: {{url}}':
    '    : {{url}}',
  'Failed to open browser. Check out the extensions gallery at {{url}}':
    '   .      {{url}}',
  'Use /compress when the conversation gets long to summarize history and free up context.':
    ' /compress,    ,      .',
  'Start a fresh idea with /clear or /new; the previous session stays available in history.':
    '    /clear  /new;     .',
  'Use /bug to submit issues to the maintainers when something goes off.':
    ' /bug,     .',
  'Switch auth type quickly with /auth.':
    '      /auth.',
  'You can run any shell commands from Qwen Code using ! (e.g. !ls).':
    '    shell-  Qwen Code   ! (, !ls).',
  'Type / to open the command popup; Tab autocompletes slash commands and saved prompts.':
    ' /,    ; Tab  -   .',
  'You can resume a previous conversation by running qwen --continue or qwen --resume.':
    '    ,  qwen --continue  qwen --resume.',
  'You can switch permission mode quickly with Shift+Tab or /approval-mode.':
    '        Shift+Tab  /approval-mode.',
  'You can switch permission mode quickly with Tab or /approval-mode.':
    '        Tab  /approval-mode.',
  'Try /insight to generate personalized insights from your chat history.':
    ' /insight,       .',
  'Press Ctrl+O to toggle compact mode -- hide tool output and thinking for a cleaner view.':
    ' Ctrl+O     --     .',
  'Add a QWEN.md file to give Qwen Code persistent project context.':
    '  QWEN.md,   Qwen Code   .',
  'Use /btw to ask a quick side question without disrupting the conversation.':
    ' /btw,     ,    .',
  'Context is almost full! Run /compress now or start /new to continue.':
    '  !  /compress    /new,  .',
  'Context is getting full. Use /compress to free up space.':
    ' .  /compress,   .',
  'Long conversation? /compress summarizes history to free context.':
    ' ? /compress   ,   .',

  // ============================================================================
  // Custom API Key Configuration
  // ============================================================================
  'You can configure your API key and models in settings.json':
    '   API Key    settings.json',
  'Refer to the documentation for setup instructions':
    '   .  ',

  // ============================================================================
  // Coding Plan Authentication
  // ============================================================================
  'API key cannot be empty.': 'API Key    .',
  'You can get your Coding Plan API key here':
    '   API Key Coding Plan ',
  'Failed to update Coding Plan configuration: {{message}}':
    '    Coding Plan: {{message}}',

  // ============================================================================
  // Auth Dialog - View Titles and Labels
  // ============================================================================
  'Coding Plan': 'Coding Plan',
  Custom: '',
  'Select Region for Coding Plan': '  Coding Plan',
  'Choose based on where your account is registered':
    '       ',
  'Enter Coding Plan API Key': ' API Key Coding Plan',

  // ============================================================================
  // Coding Plan International Updates
  // ============================================================================
  'New model configurations are available for {{region}}. Update now?':
    '     {{region}}.  ?',
  '{{region}} configuration updated successfully. Model switched to "{{model}}".':
    ' {{region}}  .    "{{model}}".',
  // ============================================================================
  // Context Usage Component
  // ============================================================================
  'Context Usage': ' ',
  '% used': '% ',
  '% context used': '%  ',
  'Context exceeds limit! Use /compress or /clear to reduce.':
    '  !  /compress  /clear  .',
  'No API response yet. Send a message to see actual usage.':
    '    API.  ,    .',
  'Estimated pre-conversation overhead':
    '    ',
  'Context window': ' ',
  tokens: '',
  Used: '',
  Free: '',
  'Autocompact buffer': ' ',
  'Usage by category': '  ',
  'System prompt': ' ',
  'Built-in tools': ' ',
  'MCP tools': 'MCP tools',
  'Memory files': ' ',
  Skills: '',
  Messages: '',
  'Run /context detail for per-item breakdown.':
    ' /context detail    .',
  active: '',
  'body loaded': ' ',
  memory: '',
  'Server Detail': ' ',
  'Tool Detail': ' ',
  'Loading...': '...',
  'Unknown step': ' ',
  'Esc to back': 'Esc  ',
  ' to navigate  Enter to select  Esc to close':
    '   Enter   Esc ',
  ' to navigate  Enter to select  Esc to back':
    '   Enter   Esc ',
  ' to navigate  Enter to confirm  Esc to back':
    '   Enter   Esc ',
  'User Settings (global)': '  ()',
  'Workspace Settings (project-specific)':
    '   ()',
  'Disable server:': ' :',
  'Select where to add the server to the exclude list:':
    ',      :',
  'Press Enter to confirm, Esc to cancel':
    'Enter  , Esc  ',
  'Status:': ':',
  'Command:': ':',
  'Working Directory:': ' :',
  'No server selected': '  ',

  // MCP Server List
  'User MCPs': 'MCP ',
  'Project MCPs': 'MCP ',
  'Extension MCPs': 'MCP ',
  server: '',
  servers: '',
  'Add MCP servers to your settings to get started.':
    ' MCP servers  ,  .',
  'Run qwen --debug to see error logs':
    ' qwen --debug    ',

  // MCP OAuth Authentication
  'OAuth Authentication': 'OAuth-',
  'Authenticating... Please complete the login in your browser.':
    '... ,    .',
  // MCP Tool List
  'No tools available for this server.':
    '     .',
  destructive: '',
  'read-only': ' ',
  'open-world': ' ',
  idempotent: '',
  'Tools for {{serverName}}': '  {{serverName}}',
  '{{current}}/{{total}}': '{{current}}/{{total}}',

  // MCP Tool Detail
  required: '',
  Parameters: '',
  'No tool selected': '  ',
  Server: '',
  '{{region}} configuration updated successfully.':
    ' {{region}}  .',
  'Authenticated successfully with {{region}}. API key and model configs saved to settings.json.':
    '   {{region}}. API Key      settings.json.',
  'Tip: Use /model to switch between available Coding Plan models.':
    ':  /model      Coding Plan.',
  'Type something...': ' -...',
  Submit: '',
  'Submit answers': ' ',
  Cancel: '',
  'Your answers:': ' :',
  '(not answered)': '( )',
  'Ready to submit your answers?': '   ?',
  '/: Navigate | <-/->: Switch tabs | Enter: Select':
    '/:  | <-/->:   | Enter: ',
  '/: Navigate | Enter: Select | Esc: Cancel':
    '/:  | Enter:  | Esc: ',
  'Authenticate using Qwen OAuth': '  Qwen OAuth',
  'Authenticate using Alibaba Cloud Coding Plan':
    '  Alibaba Cloud Coding Plan',
  'Region for Coding Plan (china/global)':
    '  Coding Plan (china/global)',
  'API key for Coding Plan': 'API Key  Coding Plan',
  'Show current authentication status':
    '   ',
  'Authentication completed successfully.': '  .',
  'Starting Qwen OAuth authentication...':
    '  Qwen OAuth...',
  'Successfully authenticated with Qwen OAuth.':
    '   Qwen OAuth.',
  'Failed to authenticate with Qwen OAuth: {{error}}':
    '   Qwen OAuth: {{error}}',
  'Processing Alibaba Cloud Coding Plan authentication...':
    '  Alibaba Cloud Coding Plan...',
  'Successfully authenticated with Alibaba Cloud Coding Plan.':
    '   Alibaba Cloud Coding Plan.',
  'Failed to authenticate with Coding Plan: {{error}}':
    '   Coding Plan: {{error}}',
  ' (aliyun.com)': ' (aliyun.com)',
  Global: '',
  'Alibaba Cloud (alibabacloud.com)': 'Alibaba Cloud (alibabacloud.com)',
  'Select region for Coding Plan:': '   Coding Plan:',
  'Enter your Coding Plan API key: ': '  API Key Coding Plan: ',
  'Select authentication method:': '  :',
  '\n=== Authentication Status ===\n': '\n===   ===\n',
  '  No authentication method configured.\n':
    '     .\n',
  'Run one of the following commands to get started:\n':
    '      :\n',
  '  qwen auth qwen-oauth     - Authenticate with Qwen OAuth (discontinued)':
    '  qwen auth qwen-oauth     -   Qwen OAuth ()',
  'Or simply run:': '  :',
  '  qwen auth                - Interactive authentication setup\n':
    '  qwen auth                -   \n',
  ' Authentication Method: Qwen OAuth': '  : Qwen OAuth',
  '  Type: Free tier (discontinued 2026-04-15)':
    '  :   ( 2026-04-15)',
  '  Limit: No longer available': '  :   ',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Run /auth to switch to Coding Plan, OpenRouter, Fireworks AI, or another provider.':
    '  Qwen OAuth  2026-04-15.  /auth    Coding Plan, OpenRouter, Fireworks AI   .',
  ' Authentication Method: Alibaba Cloud Coding Plan':
    '  : Alibaba Cloud Coding Plan',
  'Global - Alibaba Cloud': ' - Alibaba Cloud',
  '  Region: {{region}}': '  : {{region}}',
  '  Current Model: {{model}}': '   : {{model}}',
  '  Config Version: {{version}}': '   : {{version}}',
  '  Status: API key configured\n': '  : API Key \n',
  '  Authentication Method: Alibaba Cloud Coding Plan (Incomplete)':
    '   : Alibaba Cloud Coding Plan ( )',
  '  Issue: API key not found in environment or settings\n':
    '  : API Key      \n',
  '  Run `qwen auth coding-plan` to re-configure.\n':
    '   `qwen auth coding-plan`   .\n',
  ' Authentication Method: {{type}}': '  : {{type}}',
  '  Status: Configured\n': '  : \n',
  'Failed to check authentication status: {{error}}':
    '    : {{error}}',
  'Select an option:': ' :',
  'Raw mode not available. Please run in an interactive terminal.':
    'Raw- . ,    .',
  '(Use   arrows to navigate, Enter to select, Ctrl+C to exit)\n':
    '(    , Enter  , Ctrl+C  )\n',
  'Hide tool output and thinking for a cleaner view (toggle with Ctrl+O).':
    '          (   Ctrl+O).',
  'Press Ctrl+O to show full tool output':
    ' Ctrl+O     ',
  'Switch to plan mode or exit plan mode':
    '        ',
  'Exited plan mode. Previous approval mode restored.':
    '  .    .',
  'Enabled plan mode. The agent will analyze and plan without executing tools.':
    '  .        .',
  'Already in plan mode. Use "/plan exit" to exit plan mode.':
    '   .  "/plan exit"     .',
  'Not in plan mode. Use "/plan" to enter plan mode first.':
    '   .   "/plan"     .',
  "Set up Qwen Code's status line UI":
    '    Qwen Code',

  // === Core: added from PR #3328 ===
  'Open the memory manager.': '  .',
  'Save a durable memory to the memory system.':
    '     .',
  Tools: '',
  prompts: '',
  tools: '',
  'Open MCP management dialog': '   MCP',
  'Manage MCP servers': ' MCP servers',
  'Manage extension settings': '  ',
  'Manage Extensions': ' ',
  'Extension Details': '  ',
  'View Extension': ' ',
  'Update Extension': ' ',
  'Disable Extension': ' ',
  'Enable Extension': ' ',
  'Uninstall Extension': ' ',
  'Select Scope': ' ',
  'User Scope': ' ',
  'Workspace Scope': '  ',
  'No extensions found.': '  .',
  'Are you sure you want to uninstall extension "{{name}}"?':
    ' ,     "{{name}}"?',
  'This action cannot be undone.': '   .',
  'Extension "{{name}}" updated successfully.':
    ' "{{name}}"  .',
  'Name:': ':',
  'MCP Servers:': 'MCP Servers:',
  'Settings:': ':',
  'View Details': ' ',
  'Update failed:': ' :',
  'Updating {{name}}...': ' {{name}}...',
  'Update complete!': ' !',
  'User (global)': ' ()',
  'Workspace (project-specific)': '  ( )',
  'Disable "{{name}}" - Select Scope': ' "{{name}}" -  ',
  'Enable "{{name}}" - Select Scope': ' "{{name}}" -  ',
  'No extension selected': '  ',
  '{{count}} extensions installed': ' : {{count}}',
  'up to date': '',
  'update available': ' ',
  'checking...': '...',
  'not updatable': ' ',
  'Ask a quick side question without affecting the main conversation':
    '   ,    ',
  'Manage Arena sessions': '  Arena',
  'Start an Arena session with multiple models competing on the same task':
    '  Arena,          ',
  'Stop the current Arena session': '   Arena',
  'Show the current Arena session status':
    '    Arena',
  'Select a model result and merge its diff into the current workspace':
    '      diff    ',
  'No running Arena session found.': '  Arena  .',
  'No Arena session found. Start one with /arena start.':
    ' Arena  .     /arena start.',
  'Arena session is still running. Wait for it to complete or use /arena stop first.':
    ' Arena   .       /arena stop.',
  'No successful agent results to select from. All agents failed or were cancelled.':
    '     .        .',
  'Use /arena stop to end the session.':
    ' /arena stop   .',
  'No idle agent found matching "{{name}}".':
    '   ,  "{{name}}".',
  'Failed to apply changes from {{label}}: {{error}}':
    '     {{label}}: {{error}}',
  'Applied changes from {{label}} to workspace. Arena session complete.':
    '  {{label}}    .  Arena .',
  'Discard all Arena results and clean up worktrees?':
    '   Arena    ?',
  'Arena results discarded. All worktrees cleaned up.':
    ' Arena .    .',
  'Arena is not supported in non-interactive mode. Use interactive mode to start an Arena session.':
    'Arena     .       Arena.',
  'Arena is not supported in non-interactive mode. Use interactive mode to stop an Arena session.':
    'Arena     .       Arena.',
  'Arena is not supported in non-interactive mode.':
    'Arena     .',
  'An Arena session exists. Use /arena stop or /arena select to end it before starting a new one.':
    ' Arena  .  /arena stop  /arena select      .',
  'Usage: /arena start --models model1,model2 <task>':
    ': /arena start --models model1,model2 <>',
  'Models to compete (required, at least 2)':
    '   (,  2)',
  'Format: authType:modelId or just modelId':
    ': authType:modelId   modelId',
  'Arena requires at least 2 models. Use --models model1,model2 to specify.':
    'Arena   2 .  --models model1,model2  .',
  'Arena started with {{count}} agents on task: "{{task}}"\nModels:\n{{modelList}}':
    'Arena   {{count}}   : "{{task}}"\n:\n{{modelList}}',
  'Arena panes are running in tmux. Attach with: `{{command}}`':
    ' Arena   tmux.   : `{{command}}`',
  '[{{label}}] failed: {{error}}': '[{{label}}] : {{error}}',
  'Loading suggestions...': ' ...',
  'Show context window usage breakdown. Use "/context detail" for per-item breakdown.':
    '    .  "/context detail"    .',
  'Show per-item context usage breakdown.':
    '     .',

  // === Missing key backfill ===
  'Updating...': '...',
  Unknown: '',
  Error: '',
  'Version:': ':',
  "Use '/extensions install' to install your first extension.":
    " '/extensions install',    .",
  'Value:': ':',
  'Press c to copy the authorization URL to your clipboard.':
    ' c,   URL    .',
  'Copy request sent to your terminal. If paste is empty, copy the URL above manually.':
    '    .   ,  URL  .',
  'Cannot write to terminal -- copy the URL above manually.':
    '     --  URL  .',
  'Tips:': ':',
  'Retrying in {{seconds}} seconds... (attempt {{attempt}}/{{maxRetries}})':
    '  {{seconds}} ... ( {{attempt}}/{{maxRetries}})',
  'Press Ctrl+Y to retry': ' Ctrl+Y,  ',
  'No failed request to retry.': '    .',
  'to retry last request': '   ',
  'Invalid API key. Coding Plan API keys start with "sk-sp-". Please check.':
    ' API Key. Coding Plan API Keys   "sk-sp-". .',
  'Lock release warning': '   ',
  'Metadata write warning': '   ',
  "Subsequent dreams may be skipped as locked until the next session's staleness sweep cleans the file.":
    ' dream-    ,        .',
  "The scheduler gate did not see this dream's timestamp; the next dream cycle may re-fire sooner than usual.":
    '      dream-;   dream    .',
  // === Same-as-English optimization ===
  ' (not in model registry)': ' (   )',
  'start server': ' ',
  ' (China)': '',
  ' (China) - ': ' - ',
};
