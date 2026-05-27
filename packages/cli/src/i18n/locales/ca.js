/**
 * @license
 * Copyright 2025 Qwen
 * SPDX-License-Identifier: Apache-2.0
 */

// Traduccions en catal per al CLI de Qwen Code per Jordi Mas i Hernndez <jmas@softcatala.org>

export default {
  // ============================================================================
  // Ajuda / Components de la interfcie
  // ============================================================================
  ' to manage attachments': ' per gestionar els adjunts',
  '<- -> select, Delete to remove,  to exit':
    '<- -> seleccionar, Delete per eliminar,  per sortir',
  'Attachments: ': 'Adjunts: ',
  'Basics:': 'Bsic:',
  'Add context': 'Afegir context',
  'Use {{symbol}} to specify files for context (e.g., {{example}}) to target specific files or folders.':
    'Useu {{symbol}} per especificar fitxers de context (p. ex., {{example}}) per seleccionar fitxers o carpetes especfics.',
  '@': '@',
  '@src/myFile.ts': '@src/myFile.ts',
  'Shell mode': 'Mode shell',
  'YOLO mode': 'Mode YOLO',
  'plan mode': 'mode de planificaci',
  'auto-accept edits': 'acceptaci automtica de canvis',
  'Accepting edits': 'Acceptant canvis',
  '(shift + tab to cycle)': '(Shift + Tab per canviar)',
  '(tab to cycle)': '(Tab per canviar)',
  'Execute shell commands via {{symbol}} (e.g., {{example1}}) or use natural language (e.g., {{example2}}).':
    'Executeu ordres shell amb {{symbol}} (p. ex., {{example1}}) o useu el llenguatge natural (p. ex., {{example2}}).',
  '!': '!',
  '!npm run start': '!npm run start',
  'start server': 'iniciar el servidor',
  'Commands:': 'Ordres:',
  'shell command': 'ordre shell',
  'Model Context Protocol command (from external servers)':
    'Ordre del protocol de context del model (des de servidors externs)',
  'Keyboard Shortcuts:': 'Dreceres de teclat:',
  'Toggle this help display': 'Mostrar/amagar aquesta ajuda',
  'Toggle shell mode': 'Canviar el mode shell',
  'Open command menu': "Obrir el men d'ordres",
  'Add file context': 'Afegir context de fitxer',
  'Accept suggestion / Autocomplete': 'Acceptar suggeriment / Autocompleci',
  'Reverse search history': "Cerca inversa a l'historial",
  'Press ? again to close': 'Premeu ? de nou per tancar',
  'for shell mode': 'per al mode shell',
  'for commands': 'per a les ordres',
  'for file paths': 'per als camins de fitxers',
  'to clear input': "per esborrar l'entrada",
  'to cycle approvals': 'per canviar les aprovacions',
  'to quit': 'per sortir',
  'for newline': 'per a nova lnia',
  'to clear screen': 'per netejar la pantalla',
  'to search history': "per cercar a l'historial",
  'to paste images': 'per enganxar imatges',
  'for external editor': 'per a editor extern',
  'to toggle compact mode': 'per canviar el mode compacte',
  'Jump through words in the input': "Saltar entre paraules a l'entrada",
  'Close dialogs, cancel requests, or quit application':
    "Tancar dilegs, cancellar peticions o sortir de l'aplicaci",
  'New line': 'Nova lnia',
  'New line (Alt+Enter works for certain linux distros)':
    'Nova lnia (Alt+Enter funciona en certes distribucions de Linux)',
  'Clear the screen': 'Netejar la pantalla',
  'Open input in external editor': "Obrir l'entrada en un editor extern",
  'Send message': 'Enviar missatge',
  'Initializing...': 'Inicialitzant...',
  'Connecting to MCP servers... ({{connected}}/{{total}})':
    'Connectant a MCP servers... ({{connected}}/{{total}})',
  'Type your message or @path/to/file':
    'Escriviu el vostre missatge o @cam/al/fitxer',
  '? for shortcuts': '? per a dreceres',
  "Press 'i' for INSERT mode and 'Esc' for NORMAL mode.":
    "Premeu 'i' per al mode INSERCI i 'Esc' per al mode NORMAL.",
  'Cancel operation / Clear input (double press)':
    'Cancellar operaci / Esborrar entrada (doble premuda)',
  'Cycle approval modes': "Canviar els modes d'aprovaci",
  'Cycle through your prompt history': "Navegar per l'historial de missatges",
  'For a full list of shortcuts, see {{docPath}}':
    'Per a una llista completa de dreceres, vegeu {{docPath}}',
  'docs/keyboard-shortcuts.md': 'docs/keyboard-shortcuts.md',
  'for help on Qwen Code': 'per a ajuda sobre Qwen Code',
  'show version info': 'mostrar informaci de la versi',
  'submit a bug report': "enviar un informe d'error",
  Status: 'Estat',

  // ============================================================================
  // Informaci del sistema
  // ============================================================================
  'Qwen Code': 'Qwen Code',
  Runtime: "Entorn d'execuci",
  OS: 'SO',
  Auth: 'Autenticaci',
  Model: 'Model',
  'Fast Model': 'Model rpid',
  Sandbox: 'Entorn allat',
  'Session ID': 'ID de sessi',
  'Base URL': 'Base URL',
  Proxy: 'Proxy',
  'Memory Usage': 's de memria',
  'IDE Client': 'Client IDE',

  // ============================================================================
  // Ordres - General
  // ============================================================================
  'Analyzes the project and creates a tailored QWEN.md file.':
    'Analitza el projecte i crea un fitxer QWEN.md personalitzat.',
  'List available Qwen Code tools. Usage: /tools [desc]':
    'Llistar les eines disponibles de Qwen Code. s: /tools [desc]',
  'List available skills.': 'Llistar les habilitats disponibles.',
  'Available Qwen Code CLI tools:': 'Eines del CLI de Qwen Code disponibles:',
  'No tools available': 'No hi ha eines disponibles',
  'View or change the approval mode for tool usage':
    "Veure o canviar el mode d'aprovaci per a l's d'eines",
  'Invalid approval mode "{{arg}}". Valid modes: {{modes}}':
    'Mode d\'aprovaci no vlid "{{arg}}". Modes vlids: {{modes}}',
  'Approval mode set to "{{mode}}"': 'Mode d\'aprovaci establert a "{{mode}}"',
  'View or change the language setting':
    "Veure o canviar la configuraci d'idioma",
  'List background tasks (text dump -- interactive dialog opens via the footer pill)':
    "Llistar les tasques en segon pla (sortida de text; el dileg interactiu es pot obrir des de l'indicador del peu de pgina)",
  'Delete a previous session': 'Suprimir una sessi anterior',
  'Run installation and environment diagnostics':
    "Executar diagnstics d'installaci i d'entorn",
  'Browse dynamic model catalogs and choose which models stay enabled locally':
    'Explorar els catlegs dinmics de models i triar quins models continuen activats localment',
  'Generate a one-line session recap now':
    'Generar ara un resum de la sessi en una sola lnia',
  'Rename the current conversation. --auto lets the fast model pick a title.':
    'Canviar el nom de la conversa actual. --auto permet que el model rpid tri un ttol.',
  'Rewind conversation to a previous turn':
    'Rebobinar la conversa fins a un torn anterior',
  'Rewind Conversation': 'Rebobinar la conversa',
  'No user turns to rewind to.': "No hi ha torns d'usuari per rebobinar.",
  'Rewind to: ': 'Rebobinar a: ',
  'Restore code and conversation': 'Restaura el codi i la conversa',
  'Restore conversation only': 'Restaura noms la conversa',
  'Restore code only': 'Restaura noms el codi',
  'Never mind': 'Tant s',
  'Computing file changes...': "S'estan calculant els canvis als fitxers...",
  'Restoring...': "S'est restaurant...",
  'Restored {{count}} file(s).': "S'han restaurat {{count}} fitxer(s).",
  'Failed to restore files: {{error}}':
    'Error en restaurar els fitxers: {{error}}',
  'Rewind failed: {{error}}': 'Error en retrocedir: {{error}}',
  'Cannot rewind conversation: no active model client.':
    'No es pot retrocedir la conversa: cap client de model actiu.',
  'Code restored, but conversation could not be rewound (no active client).':
    'Codi restaurat, per la conversa no s'ha pogut retrocedir (cap client actiu).',
  'Conversation rewound. Edit your prompt and press Enter to continue.':
    'Conversa retrocedida. Edita la teva indicaci i prem Retorn per continuar.',
  'Rewinding does not affect files edited manually or via shell commands.':
    'El retrocs no afecta els fitxers editats manualment o mitjanant comandes de shell.',
  'Cannot rewind to a turn that was compressed. Try a more recent turn.':
    'No es pot retrocedir a un torn que ha estat comprimit. Prova amb un torn ms recent.',
  'File restore is unavailable for this turn (no captured file changes, or this turn predates the current session).':
    'La restauraci de fitxers no est disponible per a aquest torn (no s'han capturat canvis, o aquest torn s anterior a la sessi actual).',
  '(+{{insertions}} -{{deletions}} in {{count}} file)':
    '(+{{insertions}} -{{deletions}} en {{count}} fitxer)',
  '(+{{insertions}} -{{deletions}} in {{count}} files)':
    '(+{{insertions}} -{{deletions}} en {{count}} fitxers)',
  'Failed to restore {{count}} file(s): {{files}}':
    'Error en restaurar {{count}} fitxer(s): {{files}}',
  'Cannot restore files: this turn was created before file checkpointing was enabled.':
    'No es poden restaurar els fitxers: aquest torn es va crear abans que el punt de control de fitxers estigus habilitat.',
  'No files needed to be restored.': 'Cap fitxer necessitava restauraci.',
  ' to navigate  Enter to select  Esc to go back':
    ' per navegar  Enter per seleccionar  Esc per tornar',
  ' to navigate  Enter to select  Esc to cancel':
    ' per navegar  Enter per seleccionar  Esc per cancellar',
  'Enter/Y to confirm  Esc/N to go back':
    'Enter/Y per confirmar  Esc/N per tornar',
  'change the theme': 'canviar el tema',
  'Select Theme': 'Seleccionar tema',
  Preview: 'Previsualitzaci',
  '(Use Enter to select, Tab to configure scope)':
    "(Useu Enter per seleccionar, Tab per configurar l'mbit)",
  '(Use Enter to apply scope, Tab to go back)':
    "(Useu Enter per aplicar l'mbit, Tab per tornar enrere)",
  'Theme configuration unavailable due to NO_COLOR env variable.':
    "La configuraci del tema no est disponible degut a la variable d'entorn NO_COLOR.",
  'Theme "{{themeName}}" not found.': 'Tema "{{themeName}}" no trobat.',
  'Theme "{{themeName}}" not found in selected scope.':
    'Tema "{{themeName}}" no trobat en l\'mbit seleccionat.',
  'Clear conversation history and free up context':
    "Esborrar l'historial de la conversa i alliberar context",
  'Compresses the context by replacing it with a summary.':
    'Comprimeix el context substituint-lo per un resum.',
  'open full Qwen Code documentation in your browser':
    'obrir la documentaci completa de Qwen Code al navegador',
  'Configuration not available.': 'Configuraci no disponible.',
  'Connect an LLM provider': 'Connectar un provedor LLM',
  'Copy the last result or code snippet to clipboard':
    "Copiar l'ltim resultat o fragment de codi al porta-retalls",

  // ============================================================================
  // Ordres - Agents
  // ============================================================================
  'Manage subagents for specialized task delegation.':
    'Gestionar subagents per a la delegaci de tasques especialitzades.',
  'Manage existing subagents (view, edit, delete).':
    'Gestionar subagents existents (veure, editar, eliminar).',
  'Create a new subagent with guided setup.':
    'Crear un nou subagent amb configuraci guiada.',

  // ============================================================================
  // Agents - Dileg de gesti
  // ============================================================================
  Agents: 'Agents',
  'Choose Action': 'Triar acci',
  'Edit {{name}}': 'Editar {{name}}',
  'Edit Tools: {{name}}': 'Editar eines: {{name}}',
  'Edit Color: {{name}}': 'Editar color: {{name}}',
  'Delete {{name}}': 'Eliminar {{name}}',
  'Unknown Step': 'Pas desconegut',
  'Esc to close': 'Esc per tancar',
  'Enter to select,  to navigate, Esc to close':
    'Enter per seleccionar,  per navegar, Esc per tancar',
  'Esc to go back': 'Esc per tornar enrere',
  'Enter to confirm, Esc to cancel': 'Enter per confirmar, Esc per cancellar',
  'Enter to select,  to navigate, Esc to go back':
    'Enter per seleccionar,  per navegar, Esc per tornar enrere',
  'Enter to submit, Esc to go back': 'Enter per enviar, Esc per tornar enrere',
  'Invalid step: {{step}}': 'Pas no vlid: {{step}}',
  'No subagents found.': "No s'han trobat subagents.",
  "Use '/agents create' to create your first subagent.":
    "Useu '/agents create' per crear el vostre primer subagent.",
  '(built-in)': '(integrat)',
  '(overridden by project level agent)':
    '(sobreescrit per un agent de nivell de projecte)',
  'Project Level ({{path}})': 'Nivell de projecte ({{path}})',
  'User Level ({{path}})': "Nivell d'usuari ({{path}})",
  'Built-in Agents': 'Agents integrats',
  'Extension Agents': "Agents d'extensi",
  'Using: {{count}} agents': 'En s: {{count}} agents',
  'View Agent': 'Veure agent',
  'Edit Agent': 'Editar agent',
  'Delete Agent': 'Eliminar agent',
  Back: 'Enrere',
  'No agent selected': 'Cap agent seleccionat',
  'File Path: ': 'Cam del fitxer: ',
  'Tools: ': 'Eines: ',
  'Color: ': 'Color: ',
  'Description:': 'Descripci:',
  'System Prompt:': 'Missatge del sistema:',
  'Open in editor': "Obrir a l'editor",
  'Edit tools': 'Editar eines',
  'Edit color': 'Editar color',
  ' Error:': ' Error:',
  'Are you sure you want to delete agent "{{name}}"?':
    'Esteu segur que voleu eliminar l\'agent "{{name}}"?',

  // ============================================================================
  // Agents - Assistent de creaci
  // ============================================================================
  'Project Level (.qwen/agents/)': 'Nivell de projecte (.qwen/agents/)',
  'User Level (~/.qwen/agents/)': "Nivell d'usuari (~/.qwen/agents/)",
  ' Subagent Created Successfully!': ' Subagent creat correctament!',
  'Subagent "{{name}}" has been saved to {{level}} level.':
    'El subagent "{{name}}" s\'ha desat al nivell {{level}}.',
  'Name: ': 'Nom: ',
  'Location: ': 'Ubicaci: ',
  ' Error saving subagent:': ' Error en desar el subagent:',
  'Warnings:': 'Advertncies:',
  'Name "{{name}}" already exists at {{level}} level - will overwrite existing subagent':
    'El nom "{{name}}" ja existeix al nivell {{level}} - sobreescriur el subagent existent',
  'Name "{{name}}" exists at user level - project level will take precedence':
    'El nom "{{name}}" existeix al nivell d\'usuari - el nivell de projecte tindr prioritat',
  'Name "{{name}}" exists at project level - existing subagent will take precedence':
    'El nom "{{name}}" existeix al nivell de projecte - el subagent existent tindr prioritat',
  'Description is over {{length}} characters':
    'La descripci supera els {{length}} carcters',
  'System prompt is over {{length}} characters':
    'El missatge del sistema supera els {{length}} carcters',
  'Step {{n}}: Choose Location': 'Pas {{n}}: Triar ubicaci',
  'Step {{n}}: Choose Generation Method':
    'Pas {{n}}: Triar mtode de generaci',
  'Generate with Qwen Code (Recommended)': 'Generar amb Qwen Code (Recomanat)',
  'Manual Creation': 'Creaci manual',
  'Describe what this subagent should do and when it should be used. (Be comprehensive for best results)':
    "Descriviu qu ha de fer aquest subagent i quan s'ha d'usar. (Sigueu exhaustiu per obtenir els millors resultats)",
  'e.g., Expert code reviewer that reviews code based on best practices...':
    'p. ex., Revisor de codi expert que revisa el codi seguint les millors prctiques...',
  'Generating subagent configuration...':
    'Generant la configuraci del subagent...',
  'Failed to generate subagent: {{error}}':
    'Error en generar el subagent: {{error}}',
  'Step {{n}}: Describe Your Subagent':
    'Pas {{n}}: Descriure el vostre subagent',
  'Step {{n}}: Enter Subagent Name': 'Pas {{n}}: Introduir el nom del subagent',
  'Step {{n}}: Enter System Prompt':
    'Pas {{n}}: Introduir el missatge del sistema',
  'Step {{n}}: Enter Description': 'Pas {{n}}: Introduir la descripci',
  'Step {{n}}: Select Tools': 'Pas {{n}}: Seleccionar eines',
  'All Tools (Default)': 'Totes les eines (per defecte)',
  'All Tools': 'Totes les eines',
  'Read-only Tools': 'Eines de noms lectura',
  'Read & Edit Tools': 'Eines de lectura i edici',
  'Read & Edit & Execution Tools': 'Eines de lectura, edici i execuci',
  'All tools selected, including MCP tools':
    'Totes les eines seleccionades, inclosos MCP tools',
  'Selected tools:': 'Eines seleccionades:',
  'Read-only tools:': 'Eines de noms lectura:',
  'Edit tools:': "Eines d'edici:",
  'Execution tools:': "Eines d'execuci:",
  'Step {{n}}: Choose Background Color': 'Pas {{n}}: Triar el color de fons',
  'Step {{n}}: Confirm and Save': 'Pas {{n}}: Confirmar i desar',
  'Esc to cancel': 'Esc per cancellar',
  'Press Enter to save, e to save and edit, Esc to go back':
    'Premeu Enter per desar, e per desar i editar, Esc per tornar enrere',
  'Press Enter to continue, {{navigation}}Esc to {{action}}':
    'Premeu Enter per continuar, {{navigation}}Esc per {{action}}',
  cancel: 'cancellar',
  'go back': 'tornar enrere',
  ' to navigate, ': ' per navegar, ',
  'Enter a clear, unique name for this subagent.':
    'Introduu un nom clar i nic per a aquest subagent.',
  'e.g., Code Reviewer': 'p. ex., Revisor de codi',
  'Name cannot be empty.': 'El nom no pot estar buit.',
  "Write the system prompt that defines this subagent's behavior. Be comprehensive for best results.":
    "Escriviu el missatge del sistema que defineix el comportament d'aquest subagent. Sigueu exhaustiu per obtenir els millors resultats.",
  'e.g., You are an expert code reviewer...':
    'p. ex., Sou un revisor de codi expert...',
  'System prompt cannot be empty.':
    'El missatge del sistema no pot estar buit.',
  'Describe when and how this subagent should be used.':
    "Descriviu quan i com s'ha d'usar aquest subagent.",
  'e.g., Reviews code for best practices and potential bugs.':
    'p. ex., Revisa el codi seguint les millors prctiques i detectant errors potencials.',
  'Description cannot be empty.': 'La descripci no pot estar buida.',
  'Failed to launch editor: {{error}}': "Error en iniciar l'editor: {{error}}",
  'Failed to save and edit subagent: {{error}}':
    'Error en desar i editar el subagent: {{error}}',

  // ============================================================================
  // Extensions - Dileg de gesti
  // ============================================================================
  'Manage Extensions': 'Gestionar extensions',
  'Extension Details': "Detalls de l'extensi",
  'View Extension': "Veure l'extensi",
  'Update Extension': "Actualitzar l'extensi",
  'Disable Extension': "Desactivar l'extensi",
  'Enable Extension': "Activar l'extensi",
  'Uninstall Extension': "Desinstallar l'extensi",
  'Select Scope': "Seleccionar l'mbit",
  'User Scope': "mbit d'usuari",
  'Workspace Scope': "mbit de l'espai de treball",
  'No extensions found.': "No s'han trobat extensions.",
  'Updating...': 'Actualitzant...',
  Unknown: 'Desconegut',
  Error: 'Error',
  'Stopped because': 'Aturat perqu',
  'Version:': 'Versi:',
  'Status:': 'Estat:',
  'Are you sure you want to uninstall extension "{{name}}"?':
    'Esteu segur que voleu desinstallar l\'extensi "{{name}}"?',
  'This action cannot be undone.': 'Aquesta acci no es pot desfer.',
  'Extension "{{name}}" updated successfully.':
    'L\'extensi "{{name}}" s\'ha actualitzat correctament.',
  'Name:': 'Nom:',
  'MCP Servers:': 'MCP Servers:',
  'Settings:': 'Configuraci:',
  active: 'activa',
  disabled: 'desactivada',
  enabled: 'activada',
  'View Details': 'Veure detalls',
  'Update failed:': "Error en l'actualitzaci:",
  'Updating {{name}}...': 'Actualitzant {{name}}...',
  'Update complete!': 'Actualitzaci completada!',
  'User (global)': 'Usuari (global)',
  'Workspace (project-specific)': 'Espai de treball (especfic del projecte)',
  'Disable "{{name}}" - Select Scope':
    'Desactivar "{{name}}" - Seleccionar mbit',
  'Enable "{{name}}" - Select Scope': 'Activar "{{name}}" - Seleccionar mbit',
  'No extension selected': 'Cap extensi seleccionada',
  '{{count}} extensions installed': '{{count}} extensions installades',
  "Use '/extensions install' to install your first extension.":
    "Useu '/extensions install' per installar la vostra primera extensi.",
  'up to date': 'al dia',
  'update available': 'actualitzaci disponible',
  'checking...': 'comprovant...',
  'not updatable': 'no actualitzable',
  error: 'error',

  // ============================================================================
  // Ordres - General (continuaci)
  // ============================================================================
  'View and edit Qwen Code settings':
    'Veure i editar la configuraci de Qwen Code',
  Settings: 'Configuraci',
  'To see changes, Qwen Code must be restarted. Press r to exit and apply changes now.':
    'Per veure els canvis, cal reiniciar Qwen Code. Premeu r per sortir i aplicar els canvis ara.',
  // ============================================================================
  // Etiquetes de configuraci
  // ============================================================================
  'Vim Mode': 'Mode Vim',
  'Attribution: commit': 'Atribuci: commit',
  'Terminal Bell Notification': 'Notificaci de campana del terminal',
  'Enable Usage Statistics': "Activar estadstiques d's",
  Theme: 'Tema',
  'Preferred Editor': 'Editor preferit',
  'Auto-connect to IDE': 'Connexi automtica a IDE',
  'Debug Keystroke Logging': 'Registre de tecles per a depuraci',
  'Language: UI': 'Idioma: Interfcie',
  'Language: Model': 'Idioma: Model',
  'Output Format': 'Format de sortida',
  'Hide Window Title': 'Amagar el ttol de la finestra',
  'Show Status in Title': "Mostrar l'estat al ttol",
  'Hide Tips': 'Amagar consells',
  'Show Line Numbers in Code': 'Mostrar nmeros de lnia al codi',
  'Show Citations': 'Mostrar cites',
  'Custom Witty Phrases': 'Frases enginyoses personalitzades',
  'Show Welcome Back Dialog': 'Mostrar el dileg de benvinguda',
  'Enable User Feedback': 'Activar les valoracions dels usuaris',
  'How is Qwen doing this session? (optional)':
    'Com va Qwen en aquesta sessi? (opcional)',
  Bad: 'Malament',
  Fine: 'B',
  Good: 'Molt b',
  Dismiss: 'Descartar',
  'Screen Reader Mode': 'Mode de lector de pantalla',
  'Max Session Turns': 'Torns mxims de sessi',
  'Skip Next Speaker Check': 'Ometre la comprovaci del proper parlant',
  'Skip Loop Detection': 'Ometre la detecci de bucles',
  'Skip Startup Context': "Ometre el context d'inici",
  'Enable OpenAI Logging': "Activar el registre d'OpenAI",
  'OpenAI Logging Directory': "Directori de registres d'OpenAI",
  Timeout: "Temps d'espera",
  'Max Retries': 'Reintents mxims',
  'Load Memory From Include Directories':
    'Carregar memria des dels directoris inclosos',
  'Respect .gitignore': 'Respectar .gitignore',
  'Respect .qwenignore': 'Respectar .qwenignore',
  'Enable Recursive File Search': 'Activar la cerca recursiva de fitxers',
  'Interactive Shell (PTY)': 'Shell interactiva (PTY)',
  'Show Color': 'Mostrar color',
  'Auto Accept': 'Acceptaci automtica',
  'Use Ripgrep': 'Usar Ripgrep',
  'Use Builtin Ripgrep': 'Usar Ripgrep integrat',
  'Tool Output Truncation Threshold':
    "Llindar de truncament de la sortida d'eines",
  'Tool Output Truncation Lines': "Lnies de truncament de la sortida d'eines",
  'Folder Trust': 'Confiana de carpeta',
  'Tool Schema Compliance': 'Compliment de Tool Schema',
  'Auto (detect from system)': 'Automtic (detectar del sistema)',
  'Auto (detect terminal theme)': 'Automtic (detectar el tema del terminal)',
  Auto: 'Automtic',
  Text: 'Text',
  JSON: 'JSON',
  Plan: 'Planificaci',
  Default: 'Per defecte',
  'Auto Edit': 'Edici automtica',
  YOLO: 'YOLO',
  'toggle vim mode on/off': 'activar/desactivar el mode Vim',
  'check session stats. Usage: /stats [model|tools]':
    'comprovar les estadstiques de la sessi. s: /stats [model|tools]',
  'Show model-specific usage statistics.':
    "Mostrar les estadstiques d's especfiques del model.",
  'Show tool-specific usage statistics.':
    "Mostrar les estadstiques d's especfiques de les eines.",
  'exit the cli': 'sortir del CLI',
  'Manage workspace directories':
    "Gestionar els directoris de l'espai de treball",
  'Add directories to the workspace. Use comma to separate multiple paths':
    "Afegir directoris a l'espai de treball. Useu comes per separar mltiples camins",
  'Show all directories in the workspace':
    "Mostrar tots els directoris de l'espai de treball",
  'set external editor preference': "establir la preferncia d'editor extern",
  'Select Editor': 'Seleccionar editor',
  'Editor Preference': "Preferncia d'editor",
  'These editors are currently supported. Please note that some editors cannot be used in sandbox mode.':
    'Aquests editors estan suportats. Cal tenir en compte que alguns editors no es poden usar en mode allat.',
  'Your preferred editor is:': 'El vostre editor preferit s:',
  'Manage extensions': 'Gestionar extensions',
  'Manage installed extensions': 'Gestionar les extensions installades',
  'Disable an extension': 'Desactivar una extensi',
  'Enable an extension': 'Activar una extensi',
  'Install an extension from a git repo or local path':
    "Installar una extensi des d'un repositori git o cam local",
  'Uninstall an extension': 'Desinstallar una extensi',
  'No extensions installed.': 'No hi ha extensions installades.',
  'Extension "{{name}}" not found.': 'Extensi "{{name}}" no trobada.',
  'No extensions to update.': 'No hi ha extensions per actualitzar.',
  'Usage: /extensions install <source>': 's: /extensions install <font>',
  'Installing extension from "{{source}}"...':
    'Installant extensi des de "{{source}}"...',
  'Extension "{{name}}" installed successfully.':
    'L\'extensi "{{name}}" s\'ha installat correctament.',
  'Failed to install extension from "{{source}}": {{error}}':
    'Error en installar l\'extensi des de "{{source}}": {{error}}',
  'Do you want to continue? [Y/n]: ': 'Voleu continuar? [S/n]: ',
  'Do you want to continue?': 'Voleu continuar?',
  'Installing extension "{{name}}".': 'Installant l\'extensi "{{name}}".',
  '**Extensions may introduce unexpected behavior. Ensure you have investigated the extension source and trust the author.**':
    "**Les extensions poden introduir comportaments inesperats. Assegureu-vos d'haver investigat la font de l'extensi i de confiar en l'autor.**",
  'This extension will run the following MCP servers:':
    'Aquesta extensi executar els segents MCP servers:',
  local: 'local',
  remote: 'remot',
  'This extension will add the following commands: {{commands}}.':
    'Aquesta extensi afegir les ordres segents: {{commands}}.',
  'This extension will append info to your QWEN.md context using {{fileName}}':
    'Aquesta extensi afegir informaci al vostre context QWEN.md usant {{fileName}}',
  'This extension will install the following skills:':
    'Aquesta extensi installar les habilitats segents:',
  'This extension will install the following subagents:':
    'Aquesta extensi installar els subagents segents:',
  'Installation cancelled for "{{name}}".':
    'Installaci cancellada per a "{{name}}".',
  'You are installing an extension from {{originSource}}. Some features may not work perfectly with Qwen Code.':
    'Esteu installant una extensi des de {{originSource}}. Algunes funcions poden no funcionar perfectament amb Qwen Code.',
  '--ref and --auto-update are not applicable for marketplace extensions.':
    "--ref i --auto-update no s'apliquen a les extensions del mercat.",
  'Extension "{{name}}" installed successfully and enabled.':
    'L\'extensi "{{name}}" s\'ha installat i activat correctament.',
  'The github URL, local path, or marketplace source (marketplace-url:plugin-name) of the extension to install.':
    "La URL de GitHub, el cam local o la font del mercat (marketplace-url:nom-del-connector) de l'extensi a installar.",
  'The git ref to install from.':
    'La referncia git des de la qual installar.',
  'Enable auto-update for this extension.':
    "Activar l'actualitzaci automtica per a aquesta extensi.",
  'Enable pre-release versions for this extension.':
    'Activar les versions preliminars per a aquesta extensi.',
  'Acknowledge the security risks of installing an extension and skip the confirmation prompt.':
    "Acceptar els riscos de seguretat d'installar una extensi i ometre el missatge de confirmaci.",
  'The source argument must be provided.': "Cal proporcionar l'argument font.",
  'Extension "{{name}}" successfully uninstalled.':
    'L\'extensi "{{name}}" s\'ha desinstallat correctament.',
  'Uninstalls an extension.': 'Desinstalla una extensi.',
  'The name or source path of the extension to uninstall.':
    "El nom o cam font de l'extensi a desinstallar.",
  'Please include the name of the extension to uninstall as a positional argument.':
    "Incloeu el nom de l'extensi a desinstallar com a argument posicional.",
  'Enables an extension.': 'Activa una extensi.',
  'The name of the extension to enable.': "El nom de l'extensi a activar.",
  'The scope to enable the extenison in. If not set, will be enabled in all scopes.':
    "L'mbit en el qual activar l'extensi. Si no s'estableix, s'activar en tots els mbits.",
  'Extension "{{name}}" successfully enabled for scope "{{scope}}".':
    'L\'extensi "{{name}}" s\'ha activat correctament per a l\'mbit "{{scope}}".',
  'Extension "{{name}}" successfully enabled in all scopes.':
    'L\'extensi "{{name}}" s\'ha activat correctament en tots els mbits.',
  'Invalid scope: {{scope}}. Please use one of {{scopes}}.':
    'mbit no vlid: {{scope}}. Useu un dels segents: {{scopes}}.',
  'Disables an extension.': 'Desactiva una extensi.',
  'The name of the extension to disable.': "El nom de l'extensi a desactivar.",
  'The scope to disable the extenison in.':
    "L'mbit en el qual desactivar l'extensi.",
  'Extension "{{name}}" successfully disabled for scope "{{scope}}".':
    'L\'extensi "{{name}}" s\'ha desactivat correctament per a l\'mbit "{{scope}}".',
  'Extension "{{name}}" successfully updated: {{oldVersion}} -> {{newVersion}}.':
    'L\'extensi "{{name}}" s\'ha actualitzat correctament: {{oldVersion}} -> {{newVersion}}.',
  'Unable to install extension "{{name}}" due to missing install metadata':
    'No es pot installar l\'extensi "{{name}}" per manca de metadades d\'installaci',
  'Extension "{{name}}" is already up to date.':
    'L\'extensi "{{name}}" ja s al dia.',
  'Updates all extensions or a named extension to the latest version.':
    "Actualitza totes les extensions o una extensi especfica a l'ltima versi.",
  'Update all extensions.': 'Actualitzar totes les extensions.',
  'The name of the extension to update.': "El nom de l'extensi a actualitzar.",
  'Either an extension name or --all must be provided':
    "Cal proporcionar un nom d'extensi o --all",
  'Lists installed extensions.': 'Llista les extensions installades.',
  'Path:': 'Cam:',
  'Source:': 'Font:',
  'Type:': 'Tipus:',
  'Release tag:': 'Etiqueta de versi:',
  'Enabled (User):': 'Activada (Usuari):',
  'Enabled (Workspace):': 'Activada (Espai de treball):',
  'Context files:': 'Fitxers de context:',
  'Skills:': 'Habilitats:',
  'Agents:': 'Agents:',
  'MCP servers:': 'MCP servers:',
  'Link extension failed to install.':
    "No s'ha pogut installar l'extensi d'enlla.",
  'Extension "{{name}}" linked successfully and enabled.':
    'L\'extensi "{{name}}" s\'ha enllaat i activat correctament.',
  'Links an extension from a local path. Updates made to the local path will always be reflected.':
    "Enllaa una extensi des d'un cam local. Els canvis al cam local sempre es reflectiran.",
  'The name of the extension to link.': "El nom de l'extensi a enllaar.",
  'Set a specific setting for an extension.':
    'Establir una configuraci especfica per a una extensi.',
  'Name of the extension to configure.': "Nom de l'extensi a configurar.",
  'The setting to configure (name or env var).':
    "La configuraci a establir (nom o variable d'entorn).",
  'The scope to set the setting in.': "L'mbit on establir la configuraci.",
  'List all settings for an extension.':
    "Llistar tota la configuraci d'una extensi.",
  'Name of the extension.': "Nom de l'extensi.",
  'Extension "{{name}}" has no settings to configure.':
    'L\'extensi "{{name}}" no t cap configuraci.',
  'Settings for "{{name}}":': 'Configuraci per a "{{name}}":',
  '(workspace)': '(espai de treball)',
  '(user)': '(usuari)',
  '[not set]': '[no establert]',
  '[value stored in keychain]': '[valor emmagatzemat al clauer]',
  'Value:': 'Valor:',
  'Manage extension settings.': 'Gestionar la configuraci de les extensions.',
  'You need to specify a command (set or list).':
    'Cal especificar una ordre (set o list).',

  // ============================================================================
  // Selecci de connector / Mercat
  // ============================================================================
  'No plugins available in this marketplace.':
    'No hi ha connectors disponibles en aquest mercat.',
  'Select a plugin to install from marketplace "{{name}}":':
    'Seleccioneu un connector per installar des del mercat "{{name}}":',
  'Plugin selection cancelled.': 'Selecci de connector cancellada.',
  'Select a plugin from "{{name}}"': 'Seleccionar un connector de "{{name}}"',
  'Use  or j/k to navigate, Enter to select, Escape to cancel':
    'Useu  o j/k per navegar, Enter per seleccionar, Escape per cancellar',
  '{{count}} more above': '{{count}} ms amunt',
  '{{count}} more below': '{{count}} ms avall',
  'manage IDE integration': "gestionar la integraci de l'IDE",
  'check status of IDE integration':
    "comprovar l'estat de la integraci de l'IDE",
  'install required IDE companion for {{ideName}}':
    'installar el complement IDE necessari per a {{ideName}}',
  'enable IDE integration': "activar la integraci de l'IDE",
  'disable IDE integration': "desactivar la integraci de l'IDE",
  'IDE integration is not supported in your current environment. To use this feature, run Qwen Code in one of these supported IDEs: VS Code or VS Code forks.':
    "La integraci de l'IDE no s compatible en el vostre entorn actual. Per usar aquesta funci, executeu Qwen Code en un dels IDEs compatibles: VS Code o bifurcacions de VS Code.",
  'Set up GitHub Actions': 'Configurar GitHub Actions',
  'Configure terminal keybindings for multiline input (VS Code, Cursor, Windsurf, Trae)':
    'Configurar les dreceres del terminal per a entrada multilnia (VS Code, Cursor, Windsurf, Trae)',
  'Please restart your terminal for the changes to take effect.':
    'Reinicieu el terminal perqu els canvis tinguin efecte.',
  'Failed to configure terminal: {{error}}':
    'Error en configurar el terminal: {{error}}',
  'Could not determine {{terminalName}} config path on Windows: APPDATA environment variable is not set.':
    "No s'ha pogut determinar el cam de configuraci de {{terminalName}} a Windows: la variable d'entorn APPDATA no est establerta.",
  '{{terminalName}} keybindings.json exists but is not a valid JSON array. Please fix the file manually or delete it to allow automatic configuration.':
    '{{terminalName}} keybindings.json existeix per no s un array JSON vlid. Corregiu el fitxer manualment o elimineu-lo per permetre la configuraci automtica.',
  'File: {{file}}': 'Fitxer: {{file}}',
  'Failed to parse {{terminalName}} keybindings.json. The file contains invalid JSON. Please fix the file manually or delete it to allow automatic configuration.':
    'Error en analitzar {{terminalName}} keybindings.json. El fitxer cont JSON no vlid. Corregiu el fitxer manualment o elimineu-lo per permetre la configuraci automtica.',
  'Error: {{error}}': 'Error: {{error}}',
  'Shift+Enter binding already exists': 'La drecera Shift+Enter ja existeix',
  'Ctrl+Enter binding already exists': 'La drecera Ctrl+Enter ja existeix',
  'Existing keybindings detected. Will not modify to avoid conflicts.':
    "S'han detectat dreceres existents. No es modificaran per evitar conflictes.",
  'Please check and modify manually if needed: {{file}}':
    'Comproveu i modifiqueu manualment si cal: {{file}}',
  'Added Shift+Enter and Ctrl+Enter keybindings to {{terminalName}}.':
    "S'han afegit les dreceres Shift+Enter i Ctrl+Enter a {{terminalName}}.",
  'Modified: {{file}}': 'Modificat: {{file}}',
  '{{terminalName}} keybindings already configured.':
    'Les dreceres de {{terminalName}} ja estan configurades.',
  'Failed to configure {{terminalName}}.':
    'Error en configurar {{terminalName}}.',
  'Your terminal is already configured for an optimal experience with multiline input (Shift+Enter and Ctrl+Enter).':
    'El vostre terminal ja est configurat per a una experincia ptima amb entrada multilnia (Shift+Enter i Ctrl+Enter).',

  // ============================================================================
  // Ordres - Hooks
  // ============================================================================
  'Manage Qwen Code hooks': 'Gestionar els hooks de Qwen Code',
  'List all configured hooks': 'Llistar tots els hooks configurats',
  Hooks: 'Hooks',
  'Loading hooks...': 'Carregant hooks...',
  'Error loading hooks:': 'Error en carregar els hooks:',
  'Press Escape to close': 'Premeu Escape per tancar',
  'Press Escape, Ctrl+C, or Ctrl+D to cancel':
    'Premeu Escape, Ctrl+C o Ctrl+D per cancellar',
  'Press Space, Enter, or Escape to dismiss':
    'Premeu Space, Enter o Escape per descartar',
  'No hook selected': 'Cap hook seleccionat',
  'No hook events found.': "No s'han trobat esdeveniments de hook.",
  '{{count}} hook configured': '{{count}} hook configurat',
  '{{count}} hooks configured': '{{count}} hooks configurats',
  'This menu is read-only. To add or modify hooks, edit settings.json directly or ask Qwen Code.':
    'Aquest men s de noms lectura. Per afegir o modificar hooks, editeu settings.json directament o demaneu-ho a Qwen Code.',
  'Enter to select  Esc to cancel':
    'Enter per seleccionar  Esc per cancellar',
  'Exit codes:': 'Codis de sortida:',
  'Configured hooks:': 'Hooks configurats:',
  'No hooks configured for this event.':
    'No hi ha hooks configurats per a aquest esdeveniment.',
  'To add hooks, edit settings.json directly or ask Qwen.':
    'Per afegir hooks, editeu settings.json directament o demaneu-ho a Qwen.',
  'Enter to select  Esc to go back':
    'Enter per seleccionar  Esc per tornar enrere',
  'Hook details': 'Detalls del hook',
  'Event:': 'Esdeveniment:',
  'Extension:': 'Extensi:',
  'No hook config selected': 'Cap configuraci de hook seleccionada',
  'To modify or remove this hook, edit settings.json directly or ask Qwen to help.':
    'Per modificar o eliminar aquest hook, editeu settings.json directament o demaneu ajuda a Qwen.',
  'Hook Configuration - Disabled': 'Configuraci de hooks - Desactivats',
  'All hooks are currently disabled. You have {{count}} that are not running.':
    'Tots els hooks estan desactivats. En teniu {{count}} que no estan en execuci.',
  '{{count}} configured hook': '{{count}} hook configurat',
  '{{count}} configured hooks': '{{count}} hooks configurats',
  'When hooks are disabled:': 'Quan els hooks estan desactivats:',
  'No hook commands will execute': "Cap ordre de hook s'executar",
  'StatusLine will not be displayed': "La barra d'estat no es mostrar",
  'Tool operations will proceed without hook validation':
    "Les operacions d'eines continuaran sense validaci de hook",
  'To re-enable hooks, remove "disableAllHooks" from settings.json or ask Qwen Code.':
    'Per tornar a activar els hooks, elimineu "disableAllHooks" de settings.json o demaneu-ho a Qwen Code.',
  Project: 'Projecte',
  User: 'Usuari',
  Skill: 'Habilitat',
  System: 'Sistema',
  Extension: 'Extensi',
  'Local Settings': 'Configuraci local',
  'User Settings': "Configuraci d'usuari",
  'System Settings': 'Configuraci del sistema',
  Extensions: 'Extensions',
  'Session (temporary)': 'Sessi (temporal)',
  'Before tool execution': "Abans de l'execuci de l'eina",
  'After tool execution': "Desprs de l'execuci de l'eina",
  'After tool execution fails': "Quan falla l'execuci de l'eina",
  'When notifications are sent': "Quan s'envien notificacions",
  'When the user submits a prompt': "Quan l'usuari envia un missatge",
  'When a new session is started': "Quan s'inicia una nova sessi",
  'Right before Qwen Code concludes its response':
    'Immediatament abans que Qwen Code conclou la seva resposta',
  'When a subagent (Agent tool call) is started':
    "Quan s'inicia un subagent (crida a l'eina Agent)",
  'Right before a subagent concludes its response':
    'Immediatament abans que un subagent conclou la seva resposta',
  'Before conversation compaction': 'Abans de la compactaci de la conversa',
  'When a session is ending': "Quan una sessi s'est acabant",
  'When a permission dialog is displayed':
    'Quan es mostra un dileg de permisos',
  'Input to command is JSON of tool call arguments.':
    "L'entrada a l'ordre s JSON dels arguments de la crida a l'eina.",
  'Input to command is JSON with fields "inputs" (tool call arguments) and "response" (tool call response).':
    'L\'entrada a l\'ordre s JSON amb els camps "inputs" (arguments de la crida a l\'eina) i "response" (resposta de la crida a l\'eina).',
  'Input to command is JSON with tool_name, tool_input, tool_use_id, error, error_type, is_interrupt, and is_timeout.':
    "L'entrada a l'ordre s JSON amb tool_name, tool_input, tool_use_id, error, error_type, is_interrupt i is_timeout.",
  'Input to command is JSON with notification message and type.':
    "L'entrada a l'ordre s JSON amb el missatge de notificaci i el tipus.",
  'Input to command is JSON with original user prompt text.':
    "L'entrada a l'ordre s JSON amb el text original del missatge de l'usuari.",
  'Input to command is JSON with session start source.':
    "L'entrada a l'ordre s JSON amb la font d'inici de sessi.",
  'Input to command is JSON with session end reason.':
    "L'entrada a l'ordre s JSON amb el motiu de fi de sessi.",
  'Input to command is JSON with agent_id and agent_type.':
    "L'entrada a l'ordre s JSON amb agent_id i agent_type.",
  'Input to command is JSON with agent_id, agent_type, and agent_transcript_path.':
    "L'entrada a l'ordre s JSON amb agent_id, agent_type i agent_transcript_path.",
  'Input to command is JSON with compaction details.':
    "L'entrada a l'ordre s JSON amb els detalls de compactaci.",
  'Input to command is JSON with tool_name, tool_input, and tool_use_id. Output JSON with hookSpecificOutput containing decision to allow or deny.':
    "L'entrada a l'ordre s JSON amb tool_name, tool_input i tool_use_id. La sortida JSON amb hookSpecificOutput cont la decisi de permetre o denegar.",
  'stdout/stderr not shown': 'stdout/stderr no es mostra',
  'show stderr to model and continue conversation':
    'mostrar stderr al model i continuar la conversa',
  'show stderr to user only': "mostrar stderr noms a l'usuari",
  'stdout shown in transcript mode (ctrl+o)':
    'stdout mostrat en mode transcripci (ctrl+o)',
  'show stderr to model immediately': 'mostrar stderr al model immediatament',
  'show stderr to user only but continue with tool call':
    "mostrar stderr noms a l'usuari per continuar amb la crida a l'eina",
  'block processing, erase original prompt, and show stderr to user only':
    "blocar el processament, esborrar el missatge original i mostrar stderr noms a l'usuari",
  'stdout shown to Qwen': 'stdout mostrat a Qwen',
  'show stderr to user only (blocking errors ignored)':
    "mostrar stderr noms a l'usuari (errors de bloqueig ignorats)",
  'command completes successfully': "l'ordre es completa correctament",
  'stdout shown to subagent': 'stdout mostrat al subagent',
  'show stderr to subagent and continue having it run':
    'mostrar stderr al subagent i continuar la seva execuci',
  'stdout appended as custom compact instructions':
    'stdout afegit com a instruccions compactes personalitzades',
  'block compaction': 'blocar la compactaci',
  'show stderr to user only but continue with compaction':
    "mostrar stderr noms a l'usuari per continuar amb la compactaci",
  'use hook decision if provided': 'usar la decisi del hook si es proporciona',
  'Config not loaded.': 'Configuraci no carregada.',
  'Hooks are not enabled. Enable hooks in settings to use this feature.':
    'Els hooks no estan activats. Activeu els hooks a la configuraci per usar aquesta funci.',
  // ============================================================================
  // Ordres - Exportaci de sessi
  // ============================================================================
  'Export current session message history to a file':
    "Exportar l'historial de missatges de la sessi actual a un fitxer",
  'Export session to HTML format': 'Exportar la sessi en format HTML',
  'Export session to JSON format': 'Exportar la sessi en format JSON',
  'Export session to JSONL format (one message per line)':
    'Exportar la sessi en format JSONL (un missatge per lnia)',
  'Export session to markdown format': 'Exportar la sessi en format markdown',

  // ============================================================================
  // Ordres - Idees
  // ============================================================================
  'generate personalized programming insights from your chat history':
    'generar idees de programaci personalitzades a partir del vostre historial de xat',

  // ============================================================================
  // Ordres - Historial de sessi
  // ============================================================================
  'Resume a previous session': 'Reprendre una sessi anterior',
  'Fork the current conversation into a new session':
    'Bifurca la conversa actual en una sessi nova',
  'Cannot branch while a response or tool call is in progress. Wait for it to finish or resolve the pending tool call.':
    "No es pot bifurcar mentre hi ha una resposta o una crida a una eina en curs. Espereu que acabi o resolgueu la crida a l'eina pendent.",
  'No conversation to branch.': 'No hi ha cap conversa per bifurcar.',
  'Restore a tool call. This will reset the conversation and file history to the state it was in when the tool call was suggested':
    "Restaurar una crida a una eina. Aix restablir la conversa i l'historial de fitxers a l'estat en qu es trobaven quan es va suggerir la crida a l'eina",
  'Could not detect terminal type. Supported terminals: VS Code, Cursor, Windsurf, and Trae.':
    "No s'ha pogut detectar el tipus de terminal. Terminals compatibles: VS Code, Cursor, Windsurf i Trae.",
  'Terminal "{{terminal}}" is not supported yet.':
    'El terminal "{{terminal}}" no s compatible encara.',

  // ============================================================================
  // Ordres - Idioma
  // ============================================================================
  'Invalid language. Available: {{options}}':
    'Idioma no vlid. Disponibles: {{options}}',
  'Language subcommands do not accept additional arguments.':
    "Les subordres d'idioma no accepten arguments addicionals.",
  'Current UI language: {{lang}}': 'Idioma actual de la interfcie: {{lang}}',
  'Current LLM output language: {{lang}}':
    'Idioma actual de la sortida del model: {{lang}}',
  'Set UI language': "Establir l'idioma de la interfcie",
  'Set LLM output language': "Establir l'idioma de sortida del model",
  'Usage: /language ui [{{options}}]': 's: /language ui [{{options}}]',
  'Usage: /language output <language>': 's: /language output <idioma>',
  'Example: /language output ': 'Exemple: /language output ',
  'Example: /language output English': 'Exemple: /language output English',
  'Example: /language output ': 'Exemple: /language output ',
  'UI language changed to {{lang}}':
    'Idioma de la interfcie canviat a {{lang}}',
  'LLM output language set to {{lang}}':
    'Idioma de sortida del model establert a {{lang}}',
  'Please restart the application for the changes to take effect.':
    "Reinicieu l'aplicaci perqu els canvis tinguin efecte.",
  'Failed to generate LLM output language rule file: {{error}}':
    "Error en generar el fitxer de regles d'idioma de sortida del model: {{error}}",
  'Invalid command. Available subcommands:':
    'Ordre no vlida. Subordres disponibles:',
  'Available subcommands:': 'Subordres disponibles:',
  'To request additional UI language packs, please open an issue on GitHub.':
    "Per sollicitar paquets d'idioma addicionals per a la interfcie, obriu una incidncia a GitHub.",
  'Available options:': 'Opcions disponibles:',
  'Set UI language to {{name}}':
    "Establir l'idioma de la interfcie a {{name}}",

  // ============================================================================
  // Ordres - Mode d'aprovaci
  // ============================================================================
  'Tool Approval Mode': "Mode d'aprovaci d'eines",
  '{{mode}} mode': 'Mode {{mode}}',
  'Analyze only, do not modify files or execute commands':
    'Analitzar noms, sense modificar fitxers ni executar ordres',
  'Require approval for file edits or shell commands':
    'Requerir aprovaci per a edicions de fitxers o ordres shell',
  'Automatically approve file edits':
    'Aprovar automticament les edicions de fitxers',
  'Automatically approve all tools': 'Aprovar automticament totes les eines',
  'Workspace approval mode exists and takes priority. User-level change will have no effect.':
    "Existeix un mode d'aprovaci de l'espai de treball i t prioritat. El canvi a nivell d'usuari no tindr cap efecte.",
  'Apply To': 'Aplicar a',
  'Workspace Settings': "Configuraci de l'espai de treball",
  'Open auto-memory folder': 'Obrir la carpeta de memria automtica',
  'Auto-memory: {{status}}': 'Memria automtica: {{status}}',
  'Auto-dream: {{status}}  {{lastDream}}  /dream to run':
    'Auto-dream: {{status}}  {{lastDream}}  /dream per executar',
  never: 'mai',
  on: 'activada',
  off: 'desactivada',
  'Remove matching entries from managed auto-memory.':
    'Eliminar les entrades coincidents de la memria automtica gestionada.',
  'Usage: /forget <memory text to remove>':
    's: /forget <text de memria a eliminar>',
  'No managed auto-memory entries matched: {{query}}':
    'Cap entrada de memria automtica gestionada coincideix: {{query}}',
  'Consolidate managed auto-memory topic files.':
    'Consolidar els fitxers de temes de memria automtica gestionada.',
  'Open MCP management dialog': 'Obrir el dileg de gesti MCP',
  'Could not retrieve tool registry.':
    "No s'ha pogut recuperar el registre d'eines.",
  "Successfully authenticated and refreshed tools for '{{name}}'.":
    "S'ha autenticat correctament i s'han actualitzat les eines per a '{{name}}'.",
  "Re-discovering tools from '{{name}}'...":
    "Redescobrint les eines de '{{name}}'...",
  "Discovered {{count}} tool(s) from '{{name}}'.":
    "S'han descobert {{count}} eina(es) de '{{name}}'.",
  'Authentication complete. Returning to server details...':
    'Autenticaci completada. Tornant als detalls del servidor...',
  'Authentication successful.': 'Autenticaci correcta.',
  // ============================================================================
  // Dileg de gesti MCP
  // ============================================================================
  'Manage MCP servers': 'Gestionar MCP servers',
  'Server Detail': 'Detalls del servidor',
  Tools: 'Eines',
  'Tool Detail': "Detalls de l'eina",
  'Loading...': 'Carregant...',
  'Unknown step': 'Pas desconegut',
  'Esc to back': 'Esc per tornar',
  ' to navigate  Enter to select  Esc to close':
    ' per navegar  Enter per seleccionar  Esc per tancar',
  ' to navigate  Enter to select  Esc to back':
    ' per navegar  Enter per seleccionar  Esc per tornar',
  ' to navigate  Enter to confirm  Esc to back':
    ' per navegar  Enter per confirmar  Esc per tornar',
  'User Settings (global)': "Configuraci d'usuari (global)",
  'Workspace Settings (project-specific)':
    "Configuraci de l'espai de treball (especfica del projecte)",
  'Disable server:': 'Desactivar el servidor:',
  'Select where to add the server to the exclude list:':
    "Seleccioneu on afegir el servidor a la llista d'exclusi:",
  'Press Enter to confirm, Esc to cancel':
    'Premeu Enter per confirmar, Esc per cancellar',
  'View tools': 'Veure eines',
  Reconnect: 'Reconnectar',
  Enable: 'Activar',
  Disable: 'Desactivar',
  Authenticate: 'Autenticar',
  'Re-authenticate': 'Tornar a autenticar',
  'Clear Authentication': "Esborrar l'autenticaci",
  'Server:': 'Servidor:',
  'Command:': 'Ordre:',
  'Working Directory:': 'Directori de treball:',
  'No server selected': 'Cap servidor seleccionat',
  prompts: 'missatges',
  'Error:': 'Error:',
  tool: 'eina',
  tools: 'eines',
  connected: 'connectat',
  connecting: 'connectant',
  disconnected: 'desconnectat',
  'User MCPs': "MCPs de l'usuari",
  'Project MCPs': 'MCPs del projecte',
  'Extension MCPs': 'MCPs de les extensions',
  server: 'servidor',
  servers: 'servidors',
  'Add MCP servers to your settings to get started.':
    'Afegiu MCP servers a la configuraci per comenar.',
  'Run qwen --debug to see error logs':
    "Executeu qwen --debug per veure els registres d'errors",
  'OAuth Authentication': 'Autenticaci OAuth',
  'Authenticating... Please complete the login in your browser.':
    "Autenticant... Completeu l'inici de sessi al vostre navegador.",
  'Press c to copy the authorization URL to your clipboard.':
    "Premeu c per copiar la URL d'autoritzaci al porta-retalls.",
  'Copy request sent to your terminal. If paste is empty, copy the URL above manually.':
    'Sollicitud de cpia enviada al vostre terminal. Si el que enganxeu s buit, copieu la URL anterior manualment.',
  'Cannot write to terminal -- copy the URL above manually.':
    'No es pot escriure al terminal -- copieu la URL anterior manualment.',
  'No tools available for this server.':
    'No hi ha eines disponibles per a aquest servidor.',
  destructive: 'destructiu',
  'read-only': 'noms lectura',
  'open-world': 'mn obert',
  idempotent: 'idempotent',
  'Tools for {{serverName}}': 'Eines per a {{serverName}}',
  '{{current}}/{{total}}': '{{current}}/{{total}}',
  required: 'obligatori',
  Parameters: 'Parmetres',
  'No tool selected': 'Cap eina seleccionada',
  Server: 'Servidor',
  '{{count}} invalid tools': '{{count}} eines no vlides',
  invalid: 'no vlid',
  'invalid: {{reason}}': 'no vlid: {{reason}}',
  'missing name': 'nom absent',
  'missing description': 'descripci absent',
  '(unnamed)': '(sense nom)',
  'Warning: This tool cannot be called by the LLM':
    'Advertncia: el model no pot cridar aquesta eina',
  Reason: 'Motiu',
  'Tools must have both name and description to be used by the LLM.':
    'Les eines han de tenir nom i descripci per poder ser usades pel model.',
  // ===========================================================
  // Ordres - Resum
  // ============================================================================
  'Generate a project summary and save it to .qwen/PROJECT_SUMMARY.md':
    'Generar un resum del projecte i desar-lo a .qwen/PROJECT_SUMMARY.md',
  'No chat client available to generate summary.':
    'No hi ha cap client de xat disponible per generar el resum.',
  'Already generating summary, wait for previous request to complete':
    "Ja s'est generant el resum, espereu que acabi la sollicitud anterior",
  'No conversation found to summarize.':
    "No s'ha trobat cap conversa per resumir.",
  'Failed to generate project context summary: {{error}}':
    'Error en generar el resum del context del projecte: {{error}}',
  'Saved project summary to {{filePathForDisplay}}.':
    'Resum del projecte desat a {{filePathForDisplay}}.',
  'Saving project summary...': 'Desant el resum del projecte...',
  'Generating project summary...': 'Generant el resum del projecte...',
  'Processing summary...': 'Processant el resum...',
  'Project summary generated and saved successfully!':
    "El resum del projecte s'ha generat i desat correctament!",
  'Saved to: {{filePath}}': 'Desat a: {{filePath}}',
  'Failed to generate summary - no text content received from LLM response':
    "Error en generar el resum - no s'ha rebut contingut de text de la resposta del model",

  // ============================================================================
  // Ordres - Model
  // ============================================================================
  'Switch the model for this session (--fast for suggestion model, [model-id] to switch immediately).':
    'Canviar el model per a aquesta sessi (--fast per al model de suggeriments)',
  'Set a lighter model for prompt suggestions and speculative execution':
    'Establir un model ms lleuger per a suggeriments de missatges i execuci especulativa',
  'Content generator configuration not available.':
    'Configuraci del generador de contingut no disponible.',
  'Authentication type not available.': "Tipus d'autenticaci no disponible.",
  'No models available for the current authentication type ({{authType}}).':
    "No hi ha models disponibles per al tipus d'autenticaci actual ({{authType}}).",
  // Needs translation
  ' (not in model registry)': ' (not in model registry)',

  // ============================================================================
  // Ordres - Netejar
  // ============================================================================
  'Starting a new session, resetting chat, and clearing terminal.':
    'Iniciant una nova sessi, restablint el xat i netejant el terminal.',
  'Starting a new session and clearing.':
    'Iniciant una nova sessi i netejant.',

  // ============================================================================
  // Ordres - Comprimir
  // ============================================================================
  'Already compressing, wait for previous request to complete':
    "Ja s'est comprimint, espereu que acabi la sollicitud anterior",
  'Failed to compress chat history.': "Error en comprimir l'historial del xat.",
  'Failed to compress chat history: {{error}}':
    "Error en comprimir l'historial del xat: {{error}}",
  'Compressing chat history': "Comprimint l'historial del xat",
  'Chat history compressed from {{originalTokens}} to {{newTokens}} tokens.':
    "L'historial del xat s'ha comprimit de {{originalTokens}} a {{newTokens}} tokens.",
  'Compression was not beneficial for this history size.':
    "La compressi no ha estat beneficiosa per a aquesta mida d'historial.",
  'Chat history compression did not reduce size. This may indicate issues with the compression prompt.':
    "La compressi de l'historial del xat no ha redut la mida. Aix pot indicar problemes amb el missatge de compressi.",
  'Could not compress chat history due to a token counting error.':
    "No s'ha pogut comprimir l'historial del xat per un error de recompte de tokens.",
  // ============================================================================
  // Ordres - Directori
  // ============================================================================
  'Configuration is not available.': 'Configuraci no disponible.',
  'Please provide at least one path to add.':
    'Proporcioneu almenys un cam per afegir.',
  'The /directory add command is not supported in restrictive sandbox profiles. Please use --include-directories when starting the session instead.':
    "L'ordre /directory add no s compatible en perfils d'entorn allat restrictius. En el seu lloc, useu --include-directories en iniciar la sessi.",
  "Error adding '{{path}}': {{error}}": "Error en afegir '{{path}}': {{error}}",
  'Successfully added QWEN.md files from the following directories if there are:\n- {{directories}}':
    "S'han afegit correctament els fitxers QWEN.md dels directoris segents si n'hi ha:\n- {{directories}}",
  'Error refreshing memory: {{error}}':
    'Error en actualitzar la memria: {{error}}',
  'Successfully added directories:\n- {{directories}}':
    "S'han afegit correctament els directoris:\n- {{directories}}",
  'Current workspace directories:\n{{directories}}':
    "Directoris actuals de l'espai de treball:\n{{directories}}",

  // ============================================================================
  // Ordres - Documentaci
  // ============================================================================
  'Please open the following URL in your browser to view the documentation:\n{{url}}':
    'Obriu la URL segent al vostre navegador per veure la documentaci:\n{{url}}',
  'Opening documentation in your browser: {{url}}':
    'Obrint la documentaci al vostre navegador: {{url}}',

  // ============================================================================
  // Dilegs - Confirmaci d'eines
  // ============================================================================
  'Do you want to proceed?': 'Voleu continuar?',
  'Yes, allow once': 'S, permetre una vegada',
  'Allow always': 'Permetre sempre',
  Yes: 'S',
  No: 'No',
  'No (esc)': 'No (esc)',
  'Modify in progress:': 'Modificaci en curs:',
  'Save and close external editor to continue':
    "Deseu i tanqueu l'editor extern per continuar",
  'Apply this change?': 'Aplicar aquest canvi?',
  'Yes, allow always': 'S, permetre sempre',
  'Modify with external editor': 'Modificar amb editor extern',
  'No, suggest changes (esc)': 'No, suggerir canvis (esc)',
  "Allow execution of: '{{command}}'?":
    "Permetre l'execuci de: '{{command}}'?",
  'Always allow in this project': 'Permetre sempre en aquest projecte',
  'Always allow {{action}} in this project':
    'Permetre sempre {{action}} en aquest projecte',
  'Always allow for this user': 'Permetre sempre per a aquest usuari',
  'Always allow {{action}} for this user':
    'Permetre sempre {{action}} per a aquest usuari',
  'Yes, restore previous mode ({{mode}})':
    'S, restaurar el mode anterior ({{mode}})',
  'Yes, and auto-accept edits': 'S, i acceptar els canvis automticament',
  'Yes, and manually approve edits': 'S, i aprovar els canvis manualment',
  'No, keep planning (esc)': 'No, seguir planificant (esc)',
  'URLs to fetch:': 'URLs a recuperar:',
  'MCP Server: {{server}}': 'MCP Server: {{server}}',
  'Tool: {{tool}}': 'Eina: {{tool}}',
  'Allow execution of MCP tool "{{tool}}" from server "{{server}}"?':
    'Permetre l\'execuci de MCP tool "{{tool}}" des de MCP server "{{server}}"?',
  // ============================================================================
  // Dilegs - Confirmaci de shell
  // ============================================================================
  'Shell Command Execution': "Execuci d'ordres shell",
  'A custom command wants to run the following shell commands:':
    'Una ordre personalitzada vol executar les ordres shell segents:',
  // ============================================================================
  // Dilegs - Benvinguda
  // ============================================================================
  'Current Plan:': 'Pla actual:',
  'Progress: {{done}}/{{total}} tasks completed':
    'Progrs: {{done}}/{{total}} tasques completades',
  ', {{inProgress}} in progress': ', {{inProgress}} en curs',
  'Pending Tasks:': 'Tasques pendents:',
  'What would you like to do?': 'Qu voleu fer?',
  'Choose how to proceed with your session:':
    'Trieu com voleu continuar la vostra sessi:',
  'Start new chat session': 'Iniciar una nova sessi de xat',
  'Continue previous conversation': 'Continuar la conversa anterior',
  ' Welcome back! (Last updated: {{timeAgo}})':
    ' Benvingut de nou! (Darrera actualitzaci: {{timeAgo}})',
  ' Overall Goal:': ' Objectiu general:',
  'Connect a Provider': 'Connectar un provedor',
  'You must connect a provider to proceed. Press Ctrl+C again to exit.':
    'Cal connectar un provedor per continuar. Premeu Ctrl+C de nou per sortir.',
  'Terms of Services and Privacy Notice':
    'Termes de servei i avs de privacitat',
  'Qwen OAuth': 'Qwen OAuth',
  'Discontinued -- switch to Coding Plan or API Key':
    'Descontinuat -- canvieu a Coding Plan o API Key',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Please select Coding Plan or API Key instead.':
    'El nivell gratut de Qwen OAuth es va descontinuar el 15-04-2026. Seleccioneu Coding Plan o API Key en el seu lloc.',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Please select a model from another provider or run /auth to switch.':
    "El nivell gratut de Qwen OAuth es va descontinuar el 15-04-2026. Seleccioneu un model d'un altre provedor o executeu /auth per canviar.",
  '\n Qwen OAuth free tier was discontinued on 2026-04-15. Please select another option.\n':
    '\n El nivell gratut de Qwen OAuth es va descontinuar el 15-04-2026. Seleccioneu una altra opci.\n',
  'Paid  Up to 6,000 requests/5 hrs  All Alibaba Cloud Coding Plan Models':
    "De pagament  Fins a 6.000 sollicituds/5 h  Tots els models de Coding Plan d'Alibaba Cloud",
  'Alibaba Cloud Coding Plan': "Coding Plan d'Alibaba Cloud",
  'Bring your own API key': 'Porteu la vostra prpia API Key',
  'Authentication is enforced to be {{enforcedType}}, but you are currently using {{currentType}}.':
    "L'autenticaci ha de ser {{enforcedType}}, per actualment esteu usant {{currentType}}.",
  'Qwen OAuth Authentication': 'Autenticaci Qwen OAuth',
  'Please visit this URL to authorize:': 'Visiteu aquesta URL per autoritzar:',
  'Waiting for authorization': "Esperant l'autoritzaci",
  'Time remaining:': 'Temps restant:',
  'Qwen OAuth Authentication Timeout':
    "Temps d'espera de l'autenticaci Qwen OAuth esgotat",
  'OAuth token expired (over {{seconds}} seconds). Please select authentication method again.':
    "El token OAuth ha expirat (ms de {{seconds}} segons). Seleccioneu el mtode d'autenticaci de nou.",
  'Press any key to return to authentication type selection.':
    "Premeu qualsevol tecla per tornar a la selecci del tipus d'autenticaci.",
  'Waiting for Qwen OAuth authentication...':
    "Esperant l'autenticaci Qwen OAuth...",
  'Authentication timed out. Please try again.':
    "L'autenticaci ha expirat. Torneu-ho a intentar.",
  'Waiting for auth... (Press ESC or CTRL+C to cancel)':
    "Esperant l'autenticaci... (Premeu ESC o CTRL+C per cancellar)",
  'Missing API key for OpenAI-compatible auth. Set settings.security.auth.apiKey, or set the {{envKeyHint}} environment variable.':
    "Manca l'API Key per a l'autenticaci compatible amb OpenAI. Establiu settings.security.auth.apiKey o la variable d'entorn {{envKeyHint}}.",
  '{{envKeyHint}} environment variable not found. Please set it in your .env file or environment variables.':
    "La variable d'entorn {{envKeyHint}} no s'ha trobat. Establiu-la al fitxer .env o a les variables d'entorn.",
  '{{envKeyHint}} environment variable not found (or set settings.security.auth.apiKey). Please set it in your .env file or environment variables.':
    "La variable d'entorn {{envKeyHint}} no s'ha trobat (o establiu settings.security.auth.apiKey). Establiu-la al fitxer .env o a les variables d'entorn.",
  'Missing API key for OpenAI-compatible auth. Set the {{envKeyHint}} environment variable.':
    "Manca l'API Key per a l'autenticaci compatible amb OpenAI. Establiu la variable d'entorn {{envKeyHint}}.",
  'Anthropic provider missing required baseUrl in modelProviders[].baseUrl.':
    'El provedor Anthropic no t la baseUrl obligatria a modelProviders[].baseUrl.',
  'ANTHROPIC_BASE_URL environment variable not found.':
    "La variable d'entorn ANTHROPIC_BASE_URL no s'ha trobat.",
  'Invalid auth method selected.':
    "S'ha seleccionat un mtode d'autenticaci no vlid.",
  'Failed to authenticate. Message: {{message}}':
    'Error en autenticar-se. Missatge: {{message}}',
  'Authenticated successfully with {{authType}} credentials.':
    "S'ha autenticat correctament amb les credencials {{authType}}.",
  'Invalid QWEN_DEFAULT_AUTH_TYPE value: "{{value}}". Valid values are: {{validValues}}':
    'Valor de QWEN_DEFAULT_AUTH_TYPE no vlid: "{{value}}". Els valors vlids sn: {{validValues}}',
  // ============================================================================
  // Dilegs - Model
  // ============================================================================
  'Select Model': 'Seleccioneu el model',
  'API Key': 'API Key',
  '(default)': '(per defecte)',
  '(not set)': '(no establert)',
  Modality: 'Modalitat',
  'Context Window': 'Fin. de context',
  text: 'text',
  'text-only': 'noms text',
  image: 'imatge',
  pdf: 'pdf',
  audio: 'udio',
  video: 'vdeo',
  'not set': 'no establert',
  none: 'cap',
  unknown: 'desconegut',
  // ============================================================================
  // Dilegs - Permisos
  // ============================================================================
  'Manage folder trust settings':
    'Gestionar la configuraci de confiana de carpetes',
  'Manage permission rules': 'Gestionar permission rules',
  Allow: 'Permetre',
  Ask: 'Preguntar',
  Deny: 'Denegar',
  Workspace: 'Espai de treball',
  "Qwen Code won't ask before using allowed tools.":
    "Qwen Code no preguntar abans d'usar les eines permeses.",
  'Qwen Code will ask before using these tools.':
    "Qwen Code preguntar abans d'usar aquestes eines.",
  'Qwen Code is not allowed to use denied tools.':
    'Qwen Code no t perms per usar les eines denegades.',
  'Manage trusted directories for this workspace.':
    "Gestionar els directoris de confiana d'aquest espai de treball.",
  'Any use of the {{tool}} tool': "Qualsevol s de l'eina {{tool}}",
  "{{tool}} commands matching '{{pattern}}'":
    "Ordres de {{tool}} que coincideixen amb '{{pattern}}'",
  'From user settings': "Des de la configuraci d'usuari",
  'From project settings': 'Des de la configuraci del projecte',
  'From session': 'Des de la sessi',
  'Project settings': 'Configuraci del projecte',
  'Checked in at .qwen/settings.json': 'Registrat a .qwen/settings.json',
  'User settings': "Configuraci d'usuari",
  'Saved in at ~/.qwen/settings.json': 'Desat a ~/.qwen/settings.json',
  'Add a new rule...': 'Afegir una nova regla...',
  'Add {{type}} permission rule': 'Afegir {{type}} permission rule',
  'Permission rules are a tool name, optionally followed by a specifier in parentheses.':
    "permission rules sn un nom d'eina, seguit opcionalment d'un especificador entre parntesis.",
  'e.g.,': 'p. ex.,',
  or: 'o',
  'Enter permission rule...': 'Introduu permission rule...',
  'Enter to submit  Esc to cancel': 'Enter per enviar  Esc per cancellar',
  'Where should this rule be saved?': "On s'ha de desar aquesta regla?",
  'Enter to confirm  Esc to cancel':
    'Enter per confirmar  Esc per cancellar',
  'Delete {{type}} rule?': 'Eliminar la regla {{type}}?',
  'Are you sure you want to delete this permission rule?':
    'Esteu segur que voleu eliminar aquesta permission rule?',
  'Permissions:': 'Permisos:',
  '(<-/-> or tab to cycle)': '(<-/-> o Tab per canviar)',
  'Press  to navigate  Enter to select  Type to search  Esc to cancel':
    'Premeu  per navegar  Enter per seleccionar  Escriviu per cercar  Esc per cancellar',
  'Search...': 'Cercar...',
  'Add directory...': 'Afegir directori...',
  'Add directory to workspace': "Afegir directori a l'espai de treball",
  'Qwen Code can read files in the workspace, and make edits when auto-accept edits is on.':
    "Qwen Code pot llegir fitxers a l'espai de treball i fer canvis quan l'acceptaci automtica de canvis est activada.",
  'Qwen Code will be able to read files in this directory and make edits when auto-accept edits is on.':
    "Qwen Code podr llegir fitxers en aquest directori i fer canvis quan l'acceptaci automtica de canvis est activada.",
  'Enter the path to the directory:': 'Introduu el cam del directori:',
  'Enter directory path...': 'Introduu el cam del directori...',
  'Tab to complete  Enter to add  Esc to cancel':
    'Tab per completar  Enter per afegir  Esc per cancellar',
  'Remove directory?': 'Eliminar el directori?',
  'Are you sure you want to remove this directory from the workspace?':
    "Esteu segur que voleu eliminar aquest directori de l'espai de treball?",
  '  (Original working directory)': '  (Directori de treball original)',
  '  (from settings)': '  (des de la configuraci)',
  'Directory does not exist.': 'El directori no existeix.',
  'Path is not a directory.': 'El cam no s un directori.',
  'This directory is already in the workspace.':
    "Aquest directori ja s a l'espai de treball.",
  'Already covered by existing directory: {{dir}}':
    'Ja cobert per un directori existent: {{dir}}',

  // ============================================================================
  // Barra d'estat
  // ============================================================================
  'Using:': 'En s:',
  '{{count}} open file': '{{count}} fitxer obert',
  '{{count}} open files': '{{count}} fitxers oberts',
  '(ctrl+g to view)': '(ctrl+g per veure)',
  '{{count}} {{name}} file': '{{count}} fitxer {{name}}',
  '{{count}} {{name}} files': '{{count}} fitxers {{name}}',
  '{{count}} MCP server': '{{count}} MCP server',
  '{{count}} MCP servers': '{{count}} MCP servers',
  '{{count}} Blocked': '{{count}} bloquejats',
  '(ctrl+t to view)': '(ctrl+t per veure)',
  '(ctrl+t to toggle)': '(ctrl+t per canviar)',
  'Press Ctrl+C again to exit.': 'Premeu Ctrl+C de nou per sortir.',
  'Press Ctrl+D again to exit.': 'Premeu Ctrl+D de nou per sortir.',
  'Press Esc again to clear.': 'Premeu Esc de nou per esborrar.',
  'Press  to edit queued messages': 'Premeu  per editar els missatges en cua',

  // ============================================================================
  // Estat MCP
  // ============================================================================
  'No MCP servers configured.': 'No hi ha MCP servers configurats.',
  ' MCP servers are starting up ({{count}} initializing)...':
    " MCP servers s'estan iniciant ({{count}} inicialitzant)...",
  'Note: First startup may take longer. Tool availability will update automatically.':
    "Nota: El primer inici pot tardar ms. La disponibilitat de les eines s'actualitzar automticament.",
  'Configured MCP servers:': 'MCP servers configurats:',
  Ready: 'Preparat',
  'Starting... (first startup may take longer)':
    'Iniciant... (el primer inici pot tardar ms)',
  Disconnected: 'Desconnectat',
  '{{count}} tool': '{{count}} eina',
  '{{count}} tools': '{{count}} eines',
  '{{count}} prompt': '{{count}} missatge',
  '{{count}} prompts': '{{count}} missatges',
  '(from {{extensionName}})': '(de {{extensionName}})',
  OAuth: 'OAuth',
  'OAuth expired': 'OAuth expirat',
  'OAuth not authenticated': 'OAuth no autenticat',
  'tools and prompts will appear when ready':
    'les eines i els missatges apareixeran quan estiguin a punt',
  '{{count}} tools cached': '{{count}} eines en memria cau',
  'Tools:': 'Eines:',
  'Parameters:': 'Parmetres:',
  'Prompts:': 'Missatges:',
  Blocked: 'Bloquejat',
  ' Tips:': ' Consells:',
  Use: 'Useu',
  'to show server and tool descriptions':
    'per mostrar les descripcions del servidor i de les eines',
  'to show tool parameter schemas': 'per mostrar tool parameter schemas',
  'to hide descriptions': 'per amagar les descripcions',
  'to authenticate with OAuth-enabled servers':
    'per autenticar-vos amb servidors OAuth',
  Press: 'Premeu',
  'to toggle tool descriptions on/off':
    'per activar/desactivar les descripcions de les eines',
  "Starting OAuth authentication for MCP server '{{name}}'...":
    "Iniciant l'autenticaci OAuth per a MCP server '{{name}}'...",
  // ============================================================================
  // Consells d'inici
  // ============================================================================
  'Tips:': 'Consells:',
  'Use /compress when the conversation gets long to summarize history and free up context.':
    "Useu /compress quan la conversa sigui llarga per resumir l'historial i alliberar context.",
  'Start a fresh idea with /clear or /new; the previous session stays available in history.':
    "Comenceu una idea nova amb /clear o /new; la sessi anterior segueix disponible a l'historial.",
  'Use /bug to submit issues to the maintainers when something goes off.':
    'Useu /bug per enviar incidncies als mantenidors quan alguna cosa vagi malament.',
  'Switch auth type quickly with /auth.':
    "Canvieu rpidament el tipus d'autenticaci amb /auth.",
  'You can run any shell commands from Qwen Code using ! (e.g. !ls).':
    'Podeu executar qualsevol ordre shell des de Qwen Code usant ! (p. ex. !ls).',
  'Type / to open the command popup; Tab autocompletes slash commands and saved prompts.':
    "Escriviu / per obrir el men emergent d'ordres; Tab completa automticament les ordres de barra i els missatges desats.",
  'You can resume a previous conversation by running qwen --continue or qwen --resume.':
    'Podeu reprendre una conversa anterior executant qwen --continue o qwen --resume.',
  'You can switch permission mode quickly with Shift+Tab or /approval-mode.':
    'Podeu canviar rpidament el mode de permisos amb Shift+Tab o /approval-mode.',
  'You can switch permission mode quickly with Tab or /approval-mode.':
    'Podeu canviar rpidament el mode de permisos amb Tab o /approval-mode.',
  'Try /insight to generate personalized insights from your chat history.':
    'Proveu /insight per generar idees personalitzades a partir del vostre historial de xat.',
  'Press Ctrl+O to toggle compact mode -- hide tool output and thinking for a cleaner view.':
    'Premeu Ctrl+O per canviar el mode compacte -- amagueu la sortida de les eines i el pensament per a una vista ms neta.',
  'Add a QWEN.md file to give Qwen Code persistent project context.':
    'Afegiu un fitxer QWEN.md per donar a Qwen Code un context persistent del projecte.',
  'Use /btw to ask a quick side question without disrupting the conversation.':
    'Useu /btw per fer una pregunta rpida sense interrompre la conversa.',
  'Context is almost full! Run /compress now or start /new to continue.':
    'El context gaireb s ple! Executeu /compress ara o inicieu /new per continuar.',
  'Context is getting full. Use /compress to free up space.':
    "El context s'omple. Useu /compress per alliberar espai.",
  'Long conversation? /compress summarizes history to free context.':
    "Conversa llarga? /compress resumeix l'historial per alliberar context.",

  // ============================================================================
  // Pantalla de sortida / Estadstiques
  // ============================================================================
  'Agent powering down. Goodbye!': "L'agent s'apaga. Fins aviat!",
  'To continue this session, run': 'Per continuar aquesta sessi, executeu',
  'Interaction Summary': 'Resum de la interacci',
  'Session ID:': 'ID de sessi:',
  'Tool Calls:': 'Crides a eines:',
  'Success Rate:': "Taxa d'xit:",
  'User Agreement:': "Acord de l'usuari:",
  reviewed: 'revisades',
  'Code Changes:': 'Canvis de codi:',
  Performance: 'Rendiment',
  'Wall Time:': 'Temps real:',
  'Agent Active:': 'Agent actiu:',
  'API Time:': "Temps de l'API:",
  'Tool Time:': "Temps d'eines:",
  'Session Stats': 'Estadstiques de la sessi',
  'Model Usage': 's del model',
  Reqs: 'Sollicituds',
  'Input Tokens': "Tokens d'entrada",
  'Output Tokens': 'Tokens de sortida',
  'Savings Highlight:': 'Estalvis destacats:',
  'of input tokens were served from the cache, reducing costs.':
    "dels tokens d'entrada s'han servit des de la memria cau, reduint els costos.",
  'Tip: For a full token breakdown, run `/stats model`.':
    'Consell: Per a un desglossament complet de tokens, executeu `/stats model`.',
  'Model Stats For Nerds': 'Estadstiques del model per a nerds',
  'Tool Stats For Nerds': "Estadstiques d'eines per a nerds",
  Metric: 'Mtrica',
  API: 'API',
  Requests: 'Sollicituds',
  Errors: 'Errors',
  'Avg Latency': 'Latncia mitjana',
  Tokens: 'Tokens',
  Total: 'Total',
  Prompt: 'Missatge',
  Cached: 'En memria cau',
  Thoughts: 'Pensaments',
  Output: 'Sortida',
  'No API calls have been made in this session.':
    "No s'ha realitzat cap crida a l'API en aquesta sessi.",
  'Tool Name': "Nom de l'eina",
  Calls: 'Crides',
  'Success Rate': "Taxa d'xit",
  'Avg Duration': 'Durada mitjana',
  'User Decision Summary': "Resum de decisions de l'usuari",
  'Total Reviewed Suggestions:': 'Total de suggeriments revisats:',
  '  Accepted:': '  Acceptats:',
  '  Rejected:': '  Rebutjats:',
  '  Modified:': '  Modificats:',
  ' Overall Agreement Rate:': " Taxa d'acord global:",
  'No tool calls have been made in this session.':
    "No s'ha realitzat cap crida a eines en aquesta sessi.",
  'Session start time is unavailable, cannot calculate stats.':
    "L'hora d'inici de la sessi no est disponible, no es poden calcular les estadstiques.",

  // ============================================================================
  // Migraci del format d'ordres
  // ============================================================================
  'Command Format Migration': "Migraci del format d'ordres",
  'Found {{count}} TOML command file:':
    "S'ha trobat {{count}} fitxer d'ordres TOML:",
  'Found {{count}} TOML command files:':
    "S'han trobat {{count}} fitxers d'ordres TOML:",
  'Current tasks': 'Tasques actuals',
  '... and {{count}} more': '... i {{count}} ms',
  'The TOML format is deprecated. Would you like to migrate them to Markdown format?':
    'El format TOML s obsolet. Voleu migrar-los al format Markdown?',
  '(Backups will be created and original files will be preserved)':
    '(Es crearan cpies de seguretat i els fitxers originals es conservaran)',

  // ============================================================================
  // Frases de crrega
  // ============================================================================
  'Waiting for user confirmation...': "Esperant la confirmaci de l'usuari...",
  // ============================================================================
  // Frases de crrega enginyoses
  // ============================================================================
  WITTY_LOADING_PHRASES: [
    'Em sento afortunat',
    'Enviant el millor...',
    "Setze jutges d'un jutjat mengen fetge d'un penjat.",
    'Navegant pel fong mucilagins...',
    'Consultant els esperits digitals...',
    'Desperta ferro...',
    'Escalfant els hmsters de la IA...',
    'Preguntant a la petxina mgica...',
    'Generant una rplica enginyosa...',
    'Polint els algorismes...',
    'No correu la perfecci (ni el meu codi)...',
    'Preparant bytes frescos...',
    'Comptant electrons...',
    'Activant els processadors cognitius...',
    "Buscant errors de sintaxi a l'univers...",
    "Un moment, optimitzant l'humor...",
    'Barrejant les grcies...',
    'Desenredant les xarxes neuronals...',
    'Compilant la brillantor...',
    'Carregant grcia.exe...',
    'Invocant el nvol de saviesa...',
    'Preparant una resposta enginyosa...',
    'Un segon, estic depurant la realitat...',
    'Donant els ltims cops de...',
    'Afinant les freqncies csmiques...',
    'Elaborant una resposta digna de la vostra pacincia...',
    'Compilant els 1 i els 0...',
    'Resolent dependncies... i crisis existencials...',
    'Desfragmentant records... tant de RAM com personals...',
    "Reiniciant el mdul de l'humor...",
    'Emmagatzemant en memria cau el necessari (principalment mems de gats)...',
    'Optimitzant per a velocitat ridcula',
    'Intercanviant bits... que no ho spiguen els bytes...',
    'Recollint brossa... torno de seguida...',
    'Assemblant les internets...',
    'Convertint caf en codi...',
    'Actualitzant la sintaxi de la realitat...',
    'Reconnectant les sinapsis...',
    'Buscant un punt i coma mal posat...',
    'Engreixant els engranatges de la mquina...',
    'Precalfant els servidors...',
    'Calibrant el condensador de flux...',
    'Activant el motor de improbabilitat...',
    'Canalitzant la Fora...',
    'Alineant les estrelles per a una resposta ptima...',
    'I tots ho diem...',
    'Carregant la propera gran idea...',
    'Un moment, estic en el meu element...',
    'Preparant-me per impressionar-vos amb brillantor...',
    'Un moment, polint el meu enginy...',
    'Aguanteu, estic creant una obra mestra...',
    "Un moment, depurant l'univers...",
    'Un moment, alineant els pxels...',
    "Un segon, optimitzant l'humor...",
    'Un moment, afinant els algorismes...',
    'Velocitat de curvatura activada...',
    'Preparant la segent jugada mestre...',
    'No us espanteu...',
    'Seguint el conill blanc...',
    'La veritat s aqu... en algun lloc...',
    'Bufant al cartutx...',
    'Carregant... Feu un gir de barril!',
    'Esperant la reaparici...',
    'Pacincia, pensa que Rodalies encara va ms lent...',
    "El pasts no s una mentida, simplement s'est carregant...",
    'Tafanejant la pantalla de creaci de personatge...',
    'Un moment, trobo el meme adequat...',
    "Prement 'A' per continuar...",
    'Pasturant gats digitals...',
    'Polint els pxels...',
    'Buscant un acudit per a la pantalla de crrega...',
    'Distreu-vos amb aquesta frase enginyosa...',
    'Gaireb a punt... probablement...',
    'Els nostres hmsters treballen tan rpid com poden...',
    'Donant un copet al cap a Cloudy...',
    'Fent festes al gat...',
    'Endavant les atxes...',
    'Mai no us deixar anar, mai no us decebr...',
    'Tocant el baix...',
    'Vaig a buscar ratafia...',
    'Vaig a tota velocitat, vaig a tota marxa...',
    's la vida real? s sols fantasia?...',
    'Tinc bon pressentiment sobre aix...',
    'Tocant el tigre...',
    'Investigant els ltims mems...',
    'Pensant com fer aix ms enginys...',
    'Hmm... deixeu-me pensar...',
    'Suant la cansalada...',
    'Trient el fetge per la boca...',
    "Posar fil a l'agulla...",
    'Un moment, ho tenim a tocar..',
    'Aix s bufar i fer ampolles',
    'Qu pots fer amb un llapis trencat? Res, no t punta...',
    'Aplicant manteniment percussiu...',
    "Buscant l'orientaci correcta de l'USB...",
    'Assegurant que el fum mgic quedi dins dels cables...',
    'Intentant sortir del Vim...',
    'Girant la roda del hmster...',
    'Aix no s un error, s una caracterstica no documentada...',
    'Endavant.',
    'Tornar... amb una resposta.',
    'El meu altre procs s una TARDIS...',
    'Posant oli als engranatges...',
    'Deixant que els pensaments macerin...',
    'Acabo de recordar on he deixat les claus...',
    "Ponderant l'orbe...",
    'He vist coses que no creureu... com un usuari que llegeix els missatges de crrega.',
    'Iniciant la mirada pensativa...',
    "Quin s el berenar preferit d'un computador? Xips micro.",
    'Per qu els programadors de Java porten ulleres? Perqu no veuen en C#.',
    'Carregant el lser... piu piu!',
    'Dividint per zero... s broma!',
    'Buscant un supervisor adult... s a dir, processant.',
    'Fent que faci xup xup.',
    'Emmarcant... perqu fins i tot les IA necessiten un moment.',
    'Entrellaant partcules quntiques per a una resposta ms rpida...',
    'Polint el crom... dels algorismes.',
    'No esteu entretinguts? (Hi estem treballant!)',
    'Invocant els follets del codi... per ajudar, s clar.',
    'Esperant que acabi el so del mdem de marcaci...',
    "Recalibrant el mesurament de l'humor.",
    'La meva altra pantalla de crrega s fins i tot ms divertida.',
    'Estic bastant segur que hi ha un gat caminant per algun teclat...',
    'Millorant... millorant... encara carregant.',
    "No s un error, s una caracterstica... d'aquesta pantalla de crrega.",
    'Heu provat apagar-ho i tornar-lo a encendre? (La pantalla de crrega, no jo.)',
    'Construint pil addicionals...',
  ],

  // ============================================================================
  // Entrada de configuraci d'extensions
  // ============================================================================
  'Enter value...': 'Introduu el valor...',
  'Enter sensitive value...': 'Introduu el valor sensible...',
  'Press Enter to submit, Escape to cancel':
    'Premeu Enter per enviar, Escape per cancellar',

  // ============================================================================
  // Eina de migraci d'ordres
  // ============================================================================
  'Markdown file already exists: {{filename}}':
    'El fitxer Markdown ja existeix: {{filename}}',
  'TOML Command Format Deprecation Notice':
    "Avs d'obsolescncia del format d'ordres TOML",
  'Found {{count}} command file(s) in TOML format:':
    "S'ha(n) trobat {{count}} fitxer(s) d'ordres en format TOML:",
  'The TOML format for commands is being deprecated in favor of Markdown format.':
    "El format TOML per a ordres s'est fent obsolet en favor del format Markdown.",
  'Markdown format is more readable and easier to edit.':
    "El format Markdown s ms llegible i fcil d'editar.",
  'You can migrate these files automatically using:':
    'Podeu migrar aquests fitxers automticament usant:',
  'Or manually convert each file:': 'O convertiu cada fitxer manualment:',
  'TOML: prompt = "..." / description = "..."':
    'TOML: prompt = "..." / description = "..."',
  'Markdown: YAML frontmatter + content':
    'Markdown: capalera YAML + contingut',
  'The migration tool will:': "L'eina de migraci far:",
  'Convert TOML files to Markdown': 'Convertir fitxers TOML a Markdown',
  'Create backups of original files':
    'Crear cpies de seguretat dels fitxers originals',
  'Preserve all command functionality':
    'Preservar tota la funcionalitat de les ordres',
  'TOML format will continue to work for now, but migration is recommended.':
    'El format TOML seguir funcionant de moment, per es recomana la migraci.',

  // ============================================================================
  // Extensions - Ordre d'explorar
  // ============================================================================
  'Open extensions page in your browser':
    "Obrir la pgina d'extensions al vostre navegador",
  'Unknown extensions source: {{source}}.':
    "Font d'extensions desconeguda: {{source}}.",
  'Would open extensions page in your browser: {{url}} (skipped in test environment)':
    "Obriria la pgina d'extensions al vostre navegador: {{url}} (oms en entorn de proves)",
  'View available extensions at {{url}}':
    'Veure les extensions disponibles a {{url}}',
  'Opening extensions page in your browser: {{url}}':
    "Obrint la pgina d'extensions al vostre navegador: {{url}}",
  'Failed to open browser. Check out the extensions gallery at {{url}}':
    "Error en obrir el navegador. Visiteu la galeria d'extensions a {{url}}",
  'Retrying in {{seconds}} seconds... (attempt {{attempt}}/{{maxRetries}})':
    'Reintentant en {{seconds}} segons... (intent {{attempt}}/{{maxRetries}})',
  'Press Ctrl+Y to retry': 'Premeu Ctrl+Y per reintentar',
  'No failed request to retry.':
    'No hi ha cap sollicitud fallida per reintentar.',
  'to retry last request': "per reintentar l'ltima sollicitud",

  // ============================================================================
  // Autenticaci de Coding Plan
  // ============================================================================
  'API key cannot be empty.': 'La API Key no pot estar buida.',
  'Invalid API key. Coding Plan API keys start with "sk-sp-". Please check.':
    'API Key no vlida. Les API Keys de Coding Plan comencen per "sk-sp-". Comproveu-la.',
  'You can get your Coding Plan API key here':
    'Podeu obtenir la vostra API Key de Coding Plan aqu',
  'Failed to update Coding Plan configuration: {{message}}':
    'Error en actualitzar la configuraci de Coding Plan: {{message}}',

  // ============================================================================
  // Configuraci de API Key personalitzada
  // ============================================================================
  'You can configure your API key and models in settings.json':
    'Podeu configurar la vostra API Key i els models a settings.json',
  'Refer to the documentation for setup instructions':
    'Consulteu la documentaci per a les instruccions de configuraci',

  // ============================================================================
  // Dileg d'autenticaci - Ttols i etiquetes
  // ============================================================================
  'Coding Plan': 'Coding Plan',
  Custom: 'Personalitzat',
  'Select Region for Coding Plan': 'Seleccioneu la regi per a Coding Plan',
  'Choose based on where your account is registered':
    "Trieu en funci d'on teniu registrat el compte",
  'Enter Coding Plan API Key': 'Introduu la API Key de Coding Plan',

  // ============================================================================
  // Actualitzacions internacionals de Coding Plan
  // ============================================================================
  'New model configurations are available for {{region}}. Update now?':
    'Hi ha noves configuracions de model disponibles per a {{region}}. Actualitzeu ara?',
  '{{region}} configuration updated successfully. Model switched to "{{model}}".':
    'La configuraci de {{region}} s\'ha actualitzat correctament. El model ha canviat a "{{model}}".',
  // ============================================================================
  // Component d's del context
  // ============================================================================
  'Context Usage': 's del context',
  '% used': '% usat',
  '% context used': '% del context usat',
  'Context exceeds limit! Use /compress or /clear to reduce.':
    'El context supera el lmit! Useu /compress o /clear per reduir-lo.',
  'No API response yet. Send a message to see actual usage.':
    "Encara no hi ha cap resposta de l'API. Envieu un missatge per veure l's real.",
  'Estimated pre-conversation overhead':
    'Crrega estimada prvia a la conversa',
  'Context window': 'Finestra de context',
  tokens: 'tokens',
  Used: 'Usat',
  Free: 'Lliure',
  'Autocompact buffer': 'Memria intermdia de compactaci automtica',
  'Usage by category': 's per categoria',
  'System prompt': 'Missatge del sistema',
  'Built-in tools': 'Eines integrades',
  'MCP tools': 'MCP tools',
  'Memory files': 'Fitxers de memria',
  Skills: 'Habilitats',
  Messages: 'Missatges',
  'Run /context detail for per-item breakdown.':
    'Executeu /context detail per a un desglossament per element.',
  'Show context window usage breakdown. Use "/context detail" for per-item breakdown.':
    'Mostrar el desglossament de l\'s de la finestra de context. Useu "/context detail" per a un desglossament per element.',
  'body loaded': 'cos carregat',
  memory: 'memria',
  '{{region}} configuration updated successfully.':
    "La configuraci de {{region}} s'ha actualitzat correctament.",
  'Authenticated successfully with {{region}}. API key and model configs saved to settings.json.':
    "S'ha autenticat correctament amb {{region}}. La API Key i les configuracions del model s'han desat a settings.json.",
  'Tip: Use /model to switch between available Coding Plan models.':
    'Consell: Useu /model per canviar entre els models de Coding Plan disponibles.',
  'Type something...': 'Escriviu alguna cosa...',
  Submit: 'Enviar',
  'Submit answers': 'Enviar respostes',
  Cancel: 'Cancellar',
  'Your answers:': 'Les vostres respostes:',
  '(not answered)': '(sense resposta)',
  'Ready to submit your answers?':
    'Preparats per enviar les vostres respostes?',
  '/: Navigate | <-/->: Switch tabs | Enter: Select':
    '/: Navegar | <-/->: Canviar pestanyes | Enter: Seleccionar',
  '/: Navigate | Enter: Select | Esc: Cancel':
    '/: Navegar | Enter: Seleccionar | Esc: Cancellar',
  'Authenticate using Qwen OAuth': 'Autenticar-se usant Qwen OAuth',
  'Authenticate using Alibaba Cloud Coding Plan':
    "Autenticar-se usant el Coding Plan d'Alibaba Cloud",
  'Region for Coding Plan (china/global)':
    'Regi per a Coding Plan (china/global)',
  'API key for Coding Plan': 'API Key per a Coding Plan',
  'Show current authentication status': "Mostrar l'estat d'autenticaci actual",
  'Authentication completed successfully.':
    "L'autenticaci s'ha completat correctament.",
  'Starting Qwen OAuth authentication...':
    "Iniciant l'autenticaci Qwen OAuth...",
  'Successfully authenticated with Qwen OAuth.':
    "S'ha autenticat correctament amb Qwen OAuth.",
  'Failed to authenticate with Qwen OAuth: {{error}}':
    'Error en autenticar-se amb Qwen OAuth: {{error}}',
  'Processing Alibaba Cloud Coding Plan authentication...':
    "Processant l'autenticaci de Coding Plan d'Alibaba Cloud...",
  'Successfully authenticated with Alibaba Cloud Coding Plan.':
    "S'ha autenticat correctament amb el Coding Plan d'Alibaba Cloud.",
  'Failed to authenticate with Coding Plan: {{error}}':
    'Error en autenticar-se amb el Coding Plan: {{error}}',
  ' (aliyun.com)': ' (aliyun.com)',
  Global: 'Global',
  'Alibaba Cloud (alibabacloud.com)': 'Alibaba Cloud (alibabacloud.com)',
  'Select region for Coding Plan:': 'Seleccioneu la regi per a Coding Plan:',
  'Enter your Coding Plan API key: ':
    'Introduu la vostra API Key de Coding Plan: ',
  'Select authentication method:': "Seleccioneu el mtode d'autenticaci:",
  '\n=== Authentication Status ===\n': "\n=== Estat d'autenticaci ===\n",
  '  No authentication method configured.\n':
    "  Cap mtode d'autenticaci configurat.\n",
  'Run one of the following commands to get started:\n':
    'Executeu una de les ordres segents per comenar:\n',
  '  qwen auth qwen-oauth     - Authenticate with Qwen OAuth (discontinued)':
    '  qwen auth qwen-oauth     - Autenticar-se amb Qwen OAuth (descontinuat)',
  'Or simply run:': 'O simplement executeu:',
  '  qwen auth                - Interactive authentication setup\n':
    "  qwen auth                - Configuraci interactiva de l'autenticaci\n",
  ' Authentication Method: Qwen OAuth': " Mtode d'autenticaci: Qwen OAuth",
  '  Type: Free tier (discontinued 2026-04-15)':
    '  Tipus: Nivell gratut (descontinuat el 15-04-2026)',
  '  Limit: No longer available': '  Lmit: Ja no disponible',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Run /auth to switch to Coding Plan, OpenRouter, Fireworks AI, or another provider.':
    'El nivell gratut de Qwen OAuth es va descontinuar el 15-04-2026. Executeu /auth per canviar a Coding Plan, OpenRouter, Fireworks AI o un altre provedor.',
  ' Authentication Method: Alibaba Cloud Coding Plan':
    " Mtode d'autenticaci: Coding Plan d'Alibaba Cloud",
  'Global - Alibaba Cloud': 'Global - Alibaba Cloud',
  '  Region: {{region}}': '  Regi: {{region}}',
  '  Current Model: {{model}}': '  Model actual: {{model}}',
  '  Config Version: {{version}}': '  Versi de configuraci: {{version}}',
  '  Status: API key configured\n': '  Estat: API Key configurada\n',
  '  Authentication Method: Alibaba Cloud Coding Plan (Incomplete)':
    "  Mtode d'autenticaci: Coding Plan d'Alibaba Cloud (Incomplet)",
  '  Issue: API key not found in environment or settings\n':
    "  Problema: API Key no trobada a l'entorn o la configuraci\n",
  '  Run `qwen auth coding-plan` to re-configure.\n':
    '  Executeu `qwen auth coding-plan` per tornar a configurar.\n',
  ' Authentication Method: {{type}}': " Mtode d'autenticaci: {{type}}",
  '  Status: Configured\n': '  Estat: Configurat\n',
  'Failed to check authentication status: {{error}}':
    "Error en comprovar l'estat d'autenticaci: {{error}}",
  'Select an option:': 'Seleccioneu una opci:',
  'Raw mode not available. Please run in an interactive terminal.':
    'El mode raw no est disponible. Executeu en un terminal interactiu.',
  '(Use   arrows to navigate, Enter to select, Ctrl+C to exit)\n':
    '(Useu les fletxes   per navegar, Enter per seleccionar, Ctrl+C per sortir)\n',
  'Hide tool output and thinking for a cleaner view (toggle with Ctrl+O).':
    'Amagueu la sortida de les eines i el pensament per a una vista ms neta (canvieu amb Ctrl+O).',
  'Press Ctrl+O to show full tool output':
    'Premeu Ctrl+O per mostrar la sortida completa de les eines',
  'Switch to plan mode or exit plan mode':
    'Canviar al mode de planificaci o sortir del mode de planificaci',
  'Exited plan mode. Previous approval mode restored.':
    "S'ha sortit del mode de planificaci. S'ha restaurat el mode d'aprovaci anterior.",
  'Enabled plan mode. The agent will analyze and plan without executing tools.':
    "S'ha activat el mode de planificaci. L'agent analitzar i planificar sense executar eines.",
  'Already in plan mode. Use "/plan exit" to exit plan mode.':
    'Ja esteu en mode de planificaci. Useu "/plan exit" per sortir del mode de planificaci.',
  'Not in plan mode. Use "/plan" to enter plan mode first.':
    'No esteu en mode de planificaci. Useu "/plan" per entrar al mode de planificaci primer.',
  "Set up Qwen Code's status line UI":
    "Configurar la interfcie de la barra d'estat de Qwen Code",

  // === Core: added from PR #3328 ===
  'Open the memory manager.': 'Obrir el gestor de memria.',
  'Save a durable memory to the memory system.':
    'Desar una memria duradora al sistema de memria.',
  'Ask a quick side question without affecting the main conversation':
    'Fer una pregunta rpida sense afectar la conversa principal',
  'Browser-based authentication with third-party providers (e.g. OpenRouter, ModelScope)':
    'Autenticaci basada en navegador amb provedors de tercers (p. ex. OpenRouter, ModelScope)',
  'Manage Arena sessions': "Gestionar sessions d'Arena",
  'Start an Arena session with multiple models competing on the same task':
    "Iniciar una sessi d'Arena amb mltiples models competint en la mateixa tasca",
  'Stop the current Arena session': "Aturar la sessi d'Arena actual",
  'Show the current Arena session status':
    "Mostrar l'estat de la sessi d'Arena actual",
  'Select a model result and merge its diff into the current workspace':
    "Seleccionar un resultat de model i fusionar-ne el diff a l'espai de treball actual",
  'No running Arena session found.':
    "No s'ha trobat cap sessi d'Arena en execuci.",
  'No Arena session found. Start one with /arena start.':
    "No s'ha trobat cap sessi d'Arena. Inicieu-ne una amb /arena start.",
  'Arena session is still running. Wait for it to complete or use /arena stop first.':
    "La sessi d'Arena encara s'est executant. Espereu que finalitzi o utilitzeu primer /arena stop.",
  'No successful agent results to select from. All agents failed or were cancelled.':
    "No hi ha resultats d'agent amb xit per seleccionar. Tots els agents han fallat o s'han cancellat.",
  'Use /arena stop to end the session.':
    'Utilitzeu /arena stop per finalitzar la sessi.',
  'No idle agent found matching "{{name}}".':
    'No s\'ha trobat cap agent inactiu que coincideixi amb "{{name}}".',
  'Failed to apply changes from {{label}}: {{error}}':
    "No s'han pogut aplicar els canvis de {{label}}: {{error}}",
  'Applied changes from {{label}} to workspace. Arena session complete.':
    "S'han aplicat els canvis de {{label}} a l'espai de treball. Sessi d'Arena completada.",
  'Discard all Arena results and clean up worktrees?':
    "Descartar tots els resultats d'Arena i netejar els arbres de treball?",
  'Arena results discarded. All worktrees cleaned up.':
    "Resultats d'Arena descartats. S'han netejat tots els arbres de treball.",
  'Arena is not supported in non-interactive mode. Use interactive mode to start an Arena session.':
    "Arena no s compatible amb el mode no interactiu. Utilitzeu el mode interactiu per iniciar una sessi d'Arena.",
  'Arena is not supported in non-interactive mode. Use interactive mode to stop an Arena session.':
    "Arena no s compatible amb el mode no interactiu. Utilitzeu el mode interactiu per aturar una sessi d'Arena.",
  'Arena is not supported in non-interactive mode.':
    'Arena no s compatible amb el mode no interactiu.',
  'An Arena session exists. Use /arena stop or /arena select to end it before starting a new one.':
    "Ja existeix una sessi d'Arena. Utilitzeu /arena stop o /arena select per finalitzar-la abans d'iniciar-ne una de nova.",
  'Usage: /arena start --models model1,model2 <task>':
    's: /arena start --models model1,model2 <tasca>',
  'Models to compete (required, at least 2)':
    'Models per competir (obligatori, almenys 2)',
  'Format: authType:modelId or just modelId':
    'Format: authType:modelId o noms modelId',
  'Arena requires at least 2 models. Use --models model1,model2 to specify.':
    'Arena requereix almenys 2 models. Utilitzeu --models model1,model2 per especificar-los.',
  'Arena started with {{count}} agents on task: "{{task}}"\nModels:\n{{modelList}}':
    'Arena iniciada amb {{count}} agents a la tasca: "{{task}}"\nModels:\n{{modelList}}',
  'Arena panes are running in tmux. Attach with: `{{command}}`':
    "Els panells d'Arena s'estan executant a tmux. Adjunteu-vos amb: `{{command}}`",
  '[{{label}}] failed: {{error}}': '[{{label}}] ha fallat: {{error}}',
  'Loading suggestions...': "S'estan carregant els suggeriments...",
  'Show per-item context usage breakdown.':
    "Mostrar el desglossament de l's del context per element.",
  'Lock release warning': "Avs d'alliberament del bloqueig",
  'Metadata write warning': "Avs d'escriptura de metadades",
  "Subsequent dreams may be skipped as locked until the next session's staleness sweep cleans the file.":
    'Els dreams posteriors es poden ometre com a bloquejats fins que la propera neteja de sessions obsoletes elimini el fitxer.',
  "The scheduler gate did not see this dream's timestamp; the next dream cycle may re-fire sooner than usual.":
    "La porta del planificador no ha vist la marca de temps d'aquest dream; el proper cicle de dream es pot tornar a executar abans del normal.",
  'Manage extension settings': 'Gestionar la configuraci de les extensions',
  'Desc:': 'Descripci:',
  'Ref:': 'Referncia:',
  ' (China)': 'Xina',
  ' (China) - ': 'Xina - ',
};
