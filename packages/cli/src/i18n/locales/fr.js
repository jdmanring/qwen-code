/**
 * @license
 * Copyright 2025 Qwen
 * SPDX-License-Identifier: Apache-2.0
 */

// Traductions franaises pour Qwen Code CLI

export default {
  // ============================================================================
  // Aide / Composants UI
  // ============================================================================
  ' to manage attachments': ' pour grer les pices jointes',
  '<- -> select, Delete to remove,  to exit':
    '<- -> slectionner, Delete pour retirer,  pour quitter',
  'Attachments: ': 'Pices jointes : ',
  'Basics:': 'Bases :',
  'Add context': 'Ajouter du contexte',
  'Use {{symbol}} to specify files for context (e.g., {{example}}) to target specific files or folders.':
    'Utilisez {{symbol}} pour spcifier des fichiers de contexte (ex. {{example}}) pour cibler des fichiers ou dossiers spcifiques.',
  '@': '@',
  '@src/myFile.ts': '@src/myFile.ts',
  'Shell mode': 'Mode shell',
  'YOLO mode': 'Mode YOLO',
  'plan mode': 'mode plan',
  'auto-accept edits': 'acceptation automatique des modifications',
  'Accepting edits': 'Acceptation des modifications',
  '(shift + tab to cycle)': '(Shift + Tab pour cycler)',
  '(tab to cycle)': '(Tab pour cycler)',
  'Execute shell commands via {{symbol}} (e.g., {{example1}}) or use natural language (e.g., {{example2}}).':
    'Excutez des commandes shell via {{symbol}} (ex. {{example1}}) ou utilisez le langage naturel (ex. {{example2}}).',
  '!': '!',
  '!npm run start': '!npm run start',
  'start server': 'dmarrer le serveur',
  'Commands:': 'Commandes :',
  'shell command': 'commande shell',
  'Model Context Protocol command (from external servers)':
    'Commande Model Context Protocol (depuis des serveurs externes)',
  'Keyboard Shortcuts:': 'Raccourcis clavier :',
  'Toggle this help display': 'Afficher/masquer cette aide',
  'Toggle shell mode': 'Basculer le mode shell',
  'Open command menu': 'Ouvrir le menu des commandes',
  'Add file context': 'Ajouter un contexte de fichier',
  'Accept suggestion / Autocomplete': 'Accepter la suggestion / Autocompltion',
  'Reverse search history': "Recherche inverse dans l'historique",
  'Press ? again to close': 'Appuyez  nouveau sur ? pour fermer',
  'for shell mode': 'pour le mode shell',
  'for commands': 'pour les commandes',
  'for file paths': 'pour les chemins de fichiers',
  'to clear input': "pour effacer l'entre",
  'to cycle approvals': 'pour cycler les approbations',
  'to quit': 'pour quitter',
  'for newline': 'pour une nouvelle ligne',
  'to clear screen': "pour effacer l'cran",
  'to search history': "pour rechercher dans l'historique",
  'to paste images': 'pour coller des images',
  'for external editor': 'pour un diteur externe',
  'Jump through words in the input': "Sauter de mot en mot dans l'entre",
  'Close dialogs, cancel requests, or quit application':
    "Fermer les botes de dialogue, annuler les requtes ou quitter l'application",
  'New line': 'Nouvelle ligne',
  'New line (Alt+Enter works for certain linux distros)':
    'Nouvelle ligne (Alt+Enter fonctionne sur certaines distributions Linux)',
  'Clear the screen': "Effacer l'cran",
  'Open input in external editor': "Ouvrir l'entre dans un diteur externe",
  'Send message': 'Envoyer le message',
  'Initializing...': 'Initialisation...',
  'Connecting to MCP servers... ({{connected}}/{{total}})':
    'Connexion aux MCP servers... ({{connected}}/{{total}})',
  'Type your message or @path/to/file':
    'Tapez votre message ou @chemin/vers/fichier',
  '? for shortcuts': '? pour les raccourcis',
  "Press 'i' for INSERT mode and 'Esc' for NORMAL mode.":
    "Appuyez sur 'i' pour le mode INSERTION et 'Esc' pour le mode NORMAL.",
  'Cancel operation / Clear input (double press)':
    "Annuler l'opration / Effacer l'entre (double appui)",
  'Cycle approval modes': "Cycler les modes d'approbation",
  'Cycle through your prompt history': "Parcourir l'historique des invites",
  'For a full list of shortcuts, see {{docPath}}':
    'Pour la liste complte des raccourcis, voir {{docPath}}',
  'docs/keyboard-shortcuts.md': 'docs/keyboard-shortcuts.md',
  'for help on Qwen Code': "pour l'aide de Qwen Code",
  'show version info': 'afficher les informations de version',
  'submit a bug report': 'soumettre un rapport de bogue',
  Status: 'Statut',

  // ============================================================================
  // Informations systme
  // ============================================================================
  'Qwen Code': 'Qwen Code',
  Runtime: 'Environnement',
  OS: 'OS',
  Model: 'Modle',
  'Fast Model': 'Modle rapide',
  Sandbox: 'Bac  sable',
  'Session ID': 'ID de session',
  'Base URL': 'Base URL',
  Proxy: 'Proxy',
  'Memory Usage': 'Utilisation mmoire',
  'IDE Client': 'Client IDE',

  // ============================================================================
  // Commandes - Gnral
  // ============================================================================
  'Analyzes the project and creates a tailored QWEN.md file.':
    'Analyse le projet et cre un fichier QWEN.md personnalis.',
  'List available Qwen Code tools. Usage: /tools [desc]':
    'Lister les outils Qwen Code disponibles. Utilisation : /tools [desc]',
  'List available skills.': 'Lister les comptences disponibles.',
  'Available Qwen Code CLI tools:': 'Outils Qwen Code CLI disponibles :',
  'No tools available': 'Aucun outil disponible',
  'View or change the approval mode for tool usage':
    "Voir ou modifier le mode d'approbation pour l'utilisation des outils",
  'Invalid approval mode "{{arg}}". Valid modes: {{modes}}':
    'Mode d\'approbation invalide "{{arg}}". Modes valides : {{modes}}',
  'Approval mode set to "{{mode}}"':
    'Mode d\'approbation dfini sur "{{mode}}"',
  'View or change the language setting':
    'Voir ou modifier le paramtre de langue',
  'List background tasks (text dump -- interactive dialog opens via the footer pill)':
    "Lister les tches d'arrire-plan (sortie texte ; la bote de dialogue interactive s'ouvre depuis la pastille du pied de page)",
  'Delete a previous session': 'Supprimer une session prcdente',
  'Run installation and environment diagnostics':
    "Excuter les diagnostics d'installation et d'environnement",
  'Browse dynamic model catalogs and choose which models stay enabled locally':
    'Parcourir les catalogues de modles dynamiques et choisir ceux qui restent activs localement',
  'Generate a one-line session recap now':
    'Gnrer maintenant un rcapitulatif de session en une ligne',
  'Rename the current conversation. --auto lets the fast model pick a title.':
    'Renommer la conversation en cours. --auto laisse le modle rapide choisir un titre.',
  'Rewind conversation to a previous turn':
    'Revenir  un tour prcdent de la conversation',
  'Rewind Conversation': 'Rembobiner la conversation',
  'No user turns to rewind to.':
    'Aucun tour utilisateur vers lequel rembobiner.',
  'Rewind to: ': 'Rembobiner vers : ',
  'Restore code and conversation': 'Restaurer le code et la conversation',
  'Restore conversation only': 'Restaurer la conversation uniquement',
  'Restore code only': 'Restaurer le code uniquement',
  'Never mind': 'Annuler',
  'Computing file changes...': 'Calcul des modifications de fichiers...',
  'Restoring...': 'Restauration en cours...',
  'Restored {{count}} file(s).': '{{count}} fichier(s) restaur(s).',
  'Failed to restore files: {{error}}':
    'chec de la restauration des fichiers : {{error}}',
  'Rewind failed: {{error}}': 'chec du retour en arrire : {{error}}',
  'Cannot rewind conversation: no active model client.':
    'Impossible de revenir en arrire sur la conversation : aucun client de modle actif.',
  'Code restored, but conversation could not be rewound (no active client).':
    'Code restaur, mais la conversation n'a pas pu tre ramene en arrire (aucun client actif).',
  'Conversation rewound. Edit your prompt and press Enter to continue.':
    'Conversation ramene en arrire. Modifiez votre invite et appuyez sur Entre pour continuer.',
  'Rewinding does not affect files edited manually or via shell commands.':
    'Le retour en arrire n'affecte pas les fichiers dits manuellement ou via des commandes shell.',
  'Cannot rewind to a turn that was compressed. Try a more recent turn.':
    'Impossible de revenir  un tour qui a t compress. Essayez un tour plus rcent.',
  'File restore is unavailable for this turn (no captured file changes, or this turn predates the current session).':
    'La restauration des fichiers est indisponible pour ce tour (aucune modification capture, ou ce tour est antrieur  la session actuelle).',
  '(+{{insertions}} -{{deletions}} in {{count}} file)':
    '(+{{insertions}} -{{deletions}} dans {{count}} fichier)',
  '(+{{insertions}} -{{deletions}} in {{count}} files)':
    '(+{{insertions}} -{{deletions}} dans {{count}} fichiers)',
  'Failed to restore {{count}} file(s): {{files}}':
    'chec de la restauration de {{count}} fichier(s) : {{files}}',
  'Cannot restore files: this turn was created before file checkpointing was enabled.':
    "Impossible de restaurer les fichiers : ce tour a t cr avant l'activation des points de contrle de fichiers.",
  'No files needed to be restored.':
    "Aucun fichier n'a eu besoin d'tre restaur.",
  ' to navigate  Enter to select  Esc to go back':
    ' naviguer  Enter slectionner  Esc retour',
  ' to navigate  Enter to select  Esc to cancel':
    ' naviguer  Enter slectionner  Esc annuler',
  'Enter/Y to confirm  Esc/N to go back': 'Enter/Y confirmer  Esc/N retour',
  'change the theme': 'changer le thme',
  'Select Theme': 'Slectionner un thme',
  Preview: 'Aperu',
  '(Use Enter to select, Tab to configure scope)':
    '(Utilisez Enter pour slectionner, Tab pour configurer la porte)',
  '(Use Enter to apply scope, Tab to go back)':
    '(Utilisez Enter pour appliquer la porte, Tab pour revenir)',
  'Theme configuration unavailable due to NO_COLOR env variable.':
    "Configuration du thme indisponible en raison de la variable d'environnement NO_COLOR.",
  'Theme "{{themeName}}" not found.': 'Thme "{{themeName}}" introuvable.',
  'Theme "{{themeName}}" not found in selected scope.':
    'Thme "{{themeName}}" introuvable dans la porte slectionne.',
  'Clear conversation history and free up context':
    "Effacer l'historique de conversation et librer le contexte",
  'Compresses the context by replacing it with a summary.':
    'Compresse le contexte en le remplaant par un rsum.',
  'open full Qwen Code documentation in your browser':
    'ouvrir la documentation complte de Qwen Code dans votre navigateur',
  'Configuration not available.': 'Configuration non disponible.',
  'Connect an LLM provider': 'Se connecter  un fournisseur LLM',
  'Copy the last result or code snippet to clipboard':
    'Copier le dernier rsultat ou extrait de code dans le presse-papiers',

  // ============================================================================
  // Commandes - Agents
  // ============================================================================
  'Manage subagents for specialized task delegation.':
    'Grer les sous-agents pour la dlgation de tches spcialises.',
  'Manage existing subagents (view, edit, delete).':
    'Grer les sous-agents existants (voir, modifier, supprimer).',
  'Create a new subagent with guided setup.':
    'Crer un nouveau sous-agent avec configuration guide.',

  // ============================================================================
  // Agents - Bote de dialogue de gestion
  // ============================================================================
  Agents: 'Agents',
  'Choose Action': 'Choisir une action',
  'Edit {{name}}': 'Modifier {{name}}',
  'Edit Tools: {{name}}': 'Modifier les outils : {{name}}',
  'Edit Color: {{name}}': 'Modifier la couleur : {{name}}',
  'Delete {{name}}': 'Supprimer {{name}}',
  'Unknown Step': 'tape inconnue',
  'Esc to close': 'Esc pour fermer',
  'Enter to select,  to navigate, Esc to close':
    'Enter pour slectionner,  pour naviguer, Esc pour fermer',
  'Esc to go back': 'Esc pour revenir',
  'Enter to confirm, Esc to cancel': 'Enter pour confirmer, Esc pour annuler',
  'Enter to select,  to navigate, Esc to go back':
    'Enter pour slectionner,  pour naviguer, Esc pour revenir',
  'Enter to submit, Esc to go back': 'Enter pour soumettre, Esc pour revenir',
  'Invalid step: {{step}}': 'tape invalide : {{step}}',
  'No subagents found.': 'Aucun sous-agent trouv.',
  "Use '/agents create' to create your first subagent.":
    "Utilisez '/agents create' pour crer votre premier sous-agent.",
  '(built-in)': '(intgr)',
  '(overridden by project level agent)':
    '(remplac par un agent au niveau du projet)',
  'Project Level ({{path}})': 'Niveau projet ({{path}})',
  'User Level ({{path}})': 'Niveau utilisateur ({{path}})',
  'Built-in Agents': 'Agents intgrs',
  'Extension Agents': "Agents d'extension",
  'Using: {{count}} agents': 'Utilisation : {{count}} agents',
  'View Agent': "Voir l'agent",
  'Edit Agent': "Modifier l'agent",
  'Delete Agent': "Supprimer l'agent",
  Back: 'Retour',
  'No agent selected': 'Aucun agent slectionn',
  'File Path: ': 'Chemin du fichier : ',
  'Tools: ': 'Outils : ',
  'Color: ': 'Couleur : ',
  'Description:': 'Description :',
  'System Prompt:': 'Invite systme :',
  'Open in editor': "Ouvrir dans l'diteur",
  'Edit tools': 'Modifier les outils',
  'Edit color': 'Modifier la couleur',
  ' Error:': ' Erreur :',
  'Are you sure you want to delete agent "{{name}}"?':
    'tes-vous sr de vouloir supprimer l\'agent "{{name}}" ?',

  // ============================================================================
  // Agents - Assistant de cration
  // ============================================================================
  'Project Level (.qwen/agents/)': 'Niveau projet (.qwen/agents/)',
  'User Level (~/.qwen/agents/)': 'Niveau utilisateur (~/.qwen/agents/)',
  ' Subagent Created Successfully!': ' Sous-agent cr avec succs !',
  'Subagent "{{name}}" has been saved to {{level}} level.':
    'Le sous-agent "{{name}}" a t enregistr au niveau {{level}}.',
  'Name: ': 'Nom : ',
  'Location: ': 'Emplacement : ',
  ' Error saving subagent:':
    ' Erreur lors de la sauvegarde du sous-agent :',
  'Warnings:': 'Avertissements :',
  'Name "{{name}}" already exists at {{level}} level - will overwrite existing subagent':
    'Le nom "{{name}}" existe dj au niveau {{level}} - le sous-agent existant sera cras',
  'Name "{{name}}" exists at user level - project level will take precedence':
    'Le nom "{{name}}" existe au niveau utilisateur - le niveau projet aura la priorit',
  'Name "{{name}}" exists at project level - existing subagent will take precedence':
    'Le nom "{{name}}" existe au niveau projet - le sous-agent existant aura la priorit',
  'Description is over {{length}} characters':
    'La description dpasse {{length}} caractres',
  'System prompt is over {{length}} characters':
    "L'invite systme dpasse {{length}} caractres",
  'Step {{n}}: Choose Location': "tape {{n}} : Choisir l'emplacement",
  'Step {{n}}: Choose Generation Method':
    'tape {{n}} : Choisir la mthode de gnration',
  'Generate with Qwen Code (Recommended)':
    'Gnrer avec Qwen Code (Recommand)',
  'Manual Creation': 'Cration manuelle',
  'Describe what this subagent should do and when it should be used. (Be comprehensive for best results)':
    'Dcrivez ce que ce sous-agent doit faire et quand il doit tre utilis. (Soyez complet pour de meilleurs rsultats)',
  'e.g., Expert code reviewer that reviews code based on best practices...':
    'ex. Rviseur de code expert qui rvise le code selon les meilleures pratiques...',
  'Generating subagent configuration...':
    'Gnration de la configuration du sous-agent...',
  'Failed to generate subagent: {{error}}':
    'chec de la gnration du sous-agent : {{error}}',
  'Step {{n}}: Describe Your Subagent':
    'tape {{n}} : Dcrire votre sous-agent',
  'Step {{n}}: Enter Subagent Name':
    'tape {{n}} : Entrer le nom du sous-agent',
  'Step {{n}}: Enter System Prompt': "tape {{n}} : Entrer l'invite systme",
  'Step {{n}}: Enter Description': 'tape {{n}} : Entrer la description',
  'Step {{n}}: Select Tools': 'tape {{n}} : Slectionner les outils',
  'All Tools (Default)': 'Tous les outils (par dfaut)',
  'All Tools': 'Tous les outils',
  'Read-only Tools': 'Outils en lecture seule',
  'Read & Edit Tools': 'Outils lecture et dition',
  'Read & Edit & Execution Tools': 'Outils lecture, dition et excution',
  'All tools selected, including MCP tools':
    'Tous les outils slectionns, y compris les MCP tools',
  'Selected tools:': 'Outils slectionns :',
  'Read-only tools:': 'Outils en lecture seule :',
  'Edit tools:': "Outils d'dition :",
  'Execution tools:': "Outils d'excution :",
  'Step {{n}}: Choose Background Color':
    "tape {{n}} : Choisir la couleur d'arrire-plan",
  'Step {{n}}: Confirm and Save': 'tape {{n}} : Confirmer et enregistrer',
  'Esc to cancel': 'Esc pour annuler',
  'Press Enter to save, e to save and edit, Esc to go back':
    'Appuyez sur Enter pour enregistrer, e pour enregistrer et modifier, Esc pour revenir',
  'Press Enter to continue, {{navigation}}Esc to {{action}}':
    'Appuyez sur Enter pour continuer, {{navigation}}Esc pour {{action}}',
  cancel: 'annuler',
  'go back': 'revenir',
  ' to navigate, ': ' pour naviguer, ',
  'Enter a clear, unique name for this subagent.':
    'Entrez un nom clair et unique pour ce sous-agent.',
  'e.g., Code Reviewer': 'ex. Rviseur de code',
  'Name cannot be empty.': 'Le nom ne peut pas tre vide.',
  "Write the system prompt that defines this subagent's behavior. Be comprehensive for best results.":
    "Rdigez l'invite systme qui dfinit le comportement de ce sous-agent. Soyez complet pour de meilleurs rsultats.",
  'e.g., You are an expert code reviewer...':
    'ex. Vous tes un rviseur de code expert...',
  'System prompt cannot be empty.': "L'invite systme ne peut pas tre vide.",
  'Describe when and how this subagent should be used.':
    'Dcrivez quand et comment ce sous-agent doit tre utilis.',
  'e.g., Reviews code for best practices and potential bugs.':
    'ex. Rvise le code pour les meilleures pratiques et les bogues potentiels.',
  'Description cannot be empty.': 'La description ne peut pas tre vide.',
  'Failed to launch editor: {{error}}':
    "chec du lancement de l'diteur : {{error}}",
  'Failed to save and edit subagent: {{error}}':
    'chec de la sauvegarde et modification du sous-agent : {{error}}',

  // ============================================================================
  // Extensions - Bote de dialogue de gestion
  // ============================================================================
  'Manage Extensions': 'Grer les extensions',
  'Extension Details': "Dtails de l'extension",
  'View Extension': "Voir l'extension",
  'Update Extension': "Mettre  jour l'extension",
  'Disable Extension': "Dsactiver l'extension",
  'Enable Extension': "Activer l'extension",
  'Uninstall Extension': "Dsinstaller l'extension",
  'Select Scope': 'Slectionner la porte',
  'User Scope': 'Porte utilisateur',
  'Workspace Scope': 'Porte espace de travail',
  'No extensions found.': 'Aucune extension trouve.',
  'Updating...': 'Mise  jour...',
  Unknown: 'Inconnu',
  Error: 'Erreur',
  'Stopped because': 'Arrt parce que',
  'Version:': 'Version :',
  'Status:': 'Statut :',
  'Are you sure you want to uninstall extension "{{name}}"?':
    'tes-vous sr de vouloir dsinstaller l\'extension "{{name}}" ?',
  'This action cannot be undone.': 'Cette action est irrversible.',
  'Extension "{{name}}" updated successfully.':
    'Extension "{{name}}" mise  jour avec succs.',
  'Name:': 'Nom :',
  'MCP Servers:': 'MCP Servers :',
  'Settings:': 'Paramtres :',
  active: 'actif',
  disabled: 'dsactiv',
  enabled: 'activ',
  'View Details': 'Voir les dtails',
  'Update failed:': 'chec de la mise  jour :',
  'Updating {{name}}...': 'Mise  jour de {{name}}...',
  'Update complete!': 'Mise  jour termine !',
  'User (global)': 'Utilisateur (global)',
  'Workspace (project-specific)': 'Espace de travail (spcifique au projet)',
  'Disable "{{name}}" - Select Scope':
    'Dsactiver "{{name}}" - Slectionner la porte',
  'Enable "{{name}}" - Select Scope':
    'Activer "{{name}}" - Slectionner la porte',
  'No extension selected': 'Aucune extension slectionne',
  '{{count}} extensions installed': '{{count}} extensions installes',
  "Use '/extensions install' to install your first extension.":
    "Utilisez '/extensions install' pour installer votre premire extension.",
  'up to date': ' jour',
  'update available': 'mise  jour disponible',
  'checking...': 'vrification...',
  'not updatable': 'non mise  jour possible',
  error: 'erreur',

  // ============================================================================
  // Commandes - Gnral (suite)
  // ============================================================================
  'View and edit Qwen Code settings':
    'Voir et modifier les paramtres de Qwen Code',
  Settings: 'Paramtres',
  'To see changes, Qwen Code must be restarted. Press r to exit and apply changes now.':
    'Pour voir les changements, Qwen Code doit tre redmarr. Appuyez sur r pour quitter et appliquer les changements maintenant.',
  // ============================================================================
  // tiquettes des paramtres
  // ============================================================================
  'Vim Mode': 'Mode Vim',
  'Attribution: commit': 'Attribution : commit',
  'Terminal Bell Notification': 'Notification sonore du terminal',
  'Enable Usage Statistics': "Activer les statistiques d'utilisation",
  Theme: 'Thme',
  'Preferred Editor': 'diteur prfr',
  'Auto-connect to IDE': "Connexion automatique  l'IDE",
  'Debug Keystroke Logging': 'Journalisation des frappes de dbogage',
  'Language: UI': 'Langue : Interface',
  'Language: Model': 'Langue : Modle',
  'Output Format': 'Format de sortie',
  'Hide Window Title': 'Masquer le titre de la fentre',
  'Show Status in Title': 'Afficher le statut dans le titre',
  'Hide Tips': 'Masquer les conseils',
  'Show Line Numbers in Code': 'Afficher les numros de ligne dans le code',
  'Show Citations': 'Afficher les citations',
  'Custom Witty Phrases': 'Phrases personnalises spirituelles',
  'Show Welcome Back Dialog': 'Afficher le dialogue de bienvenue',
  'Enable User Feedback': 'Activer les retours utilisateur',
  'How is Qwen doing this session? (optional)':
    'Comment se passe cette session avec Qwen ? (facultatif)',
  Bad: 'Mauvais',
  Fine: 'Correct',
  Good: 'Bien',
  Dismiss: 'Ignorer',
  'Screen Reader Mode': "Mode lecteur d'cran",
  'Max Session Turns': 'Nombre maximum de tours de session',
  'Skip Next Speaker Check':
    'Ignorer la vrification du prochain interlocuteur',
  'Skip Loop Detection': 'Ignorer la dtection de boucle',
  'Skip Startup Context': 'Ignorer le contexte de dmarrage',
  'Enable OpenAI Logging': 'Activer la journalisation OpenAI',
  'OpenAI Logging Directory': 'Rpertoire de journalisation OpenAI',
  Timeout: "Dlai d'attente",
  'Max Retries': 'Nombre maximum de tentatives',
  'Load Memory From Include Directories':
    'Charger la mmoire depuis les rpertoires inclus',
  'Respect .gitignore': 'Respecter .gitignore',
  'Respect .qwenignore': 'Respecter .qwenignore',
  'Enable Recursive File Search': 'Activer la recherche rcursive de fichiers',
  'Interactive Shell (PTY)': 'Shell interactif (PTY)',
  'Show Color': 'Afficher les couleurs',
  'Auto Accept': 'Acceptation automatique',
  'Use Ripgrep': 'Utiliser Ripgrep',
  'Use Builtin Ripgrep': 'Utiliser Ripgrep intgr',
  'Tool Output Truncation Threshold':
    'Seuil de troncature de sortie des outils',
  'Tool Output Truncation Lines': 'Lignes de troncature de sortie des outils',
  'Folder Trust': 'Confiance des dossiers',
  'Tool Schema Compliance': 'Conformit Tool Schema',
  'Auto (detect from system)': 'Auto (dtecter depuis le systme)',
  'Auto (detect terminal theme)': 'Auto (dtecter le thme du terminal)',
  Text: 'Texte',
  JSON: 'JSON',
  Plan: 'Plan',
  Default: 'Par dfaut',
  'Auto Edit': 'dition automatique',
  YOLO: 'YOLO',
  'toggle vim mode on/off': 'activer/dsactiver le mode Vim',
  'check session stats. Usage: /stats [model|tools]':
    'vrifier les stats de session. Utilisation : /stats [modle|outils]',
  'Show model-specific usage statistics.':
    "Afficher les statistiques d'utilisation spcifiques au modle.",
  'Show tool-specific usage statistics.':
    "Afficher les statistiques d'utilisation spcifiques aux outils.",
  'exit the cli': 'quitter le CLI',
  'Manage workspace directories':
    "Grer les rpertoires de l'espace de travail",
  'Add directories to the workspace. Use comma to separate multiple paths':
    "Ajouter des rpertoires  l'espace de travail. Utilisez une virgule pour sparer plusieurs chemins",
  'Show all directories in the workspace':
    "Afficher tous les rpertoires de l'espace de travail",
  'set external editor preference': "dfinir la prfrence d'diteur externe",
  'Select Editor': "Slectionner l'diteur",
  'Editor Preference': "Prfrence d'diteur",
  'These editors are currently supported. Please note that some editors cannot be used in sandbox mode.':
    'Ces diteurs sont actuellement pris en charge. Notez que certains diteurs ne peuvent pas tre utiliss en mode bac  sable.',
  'Your preferred editor is:': 'Votre diteur prfr est :',
  'Manage extensions': 'Grer les extensions',
  'Manage installed extensions': 'Grer les extensions installes',
  'Disable an extension': 'Dsactiver une extension',
  'Enable an extension': 'Activer une extension',
  'Install an extension from a git repo or local path':
    'Installer une extension depuis un dpt git ou un chemin local',
  'Uninstall an extension': 'Dsinstaller une extension',
  'No extensions installed.': 'Aucune extension installe.',
  'Extension "{{name}}" not found.': 'Extension "{{name}}" introuvable.',
  'No extensions to update.': 'Aucune extension  mettre  jour.',
  'Usage: /extensions install <source>':
    'Utilisation : /extensions install <source>',
  'Installing extension from "{{source}}"...':
    'Installation de l\'extension depuis "{{source}}"...',
  'Extension "{{name}}" installed successfully.':
    'Extension "{{name}}" installe avec succs.',
  'Failed to install extension from "{{source}}": {{error}}':
    'chec de l\'installation de l\'extension depuis "{{source}}" : {{error}}',
  'Do you want to continue? [Y/n]: ': 'Voulez-vous continuer ? [O/n] : ',
  'Do you want to continue?': 'Voulez-vous continuer ?',
  'Installing extension "{{name}}".':
    'Installation de l\'extension "{{name}}".',
  '**Extensions may introduce unexpected behavior. Ensure you have investigated the extension source and trust the author.**':
    "**Les extensions peuvent introduire des comportements inattendus. Assurez-vous d'avoir examin la source de l'extension et de faire confiance  l'auteur.**",
  'This extension will run the following MCP servers:':
    'Cette extension excutera les MCP servers suivants :',
  local: 'local',
  remote: 'distant',
  'This extension will add the following commands: {{commands}}.':
    'Cette extension ajoutera les commandes suivantes : {{commands}}.',
  'This extension will append info to your QWEN.md context using {{fileName}}':
    'Cette extension ajoutera des informations  votre contexte QWEN.md en utilisant {{fileName}}',
  'This extension will install the following skills:':
    'Cette extension installera les comptences suivantes :',
  'This extension will install the following subagents:':
    'Cette extension installera les sous-agents suivants :',
  'Installation cancelled for "{{name}}".':
    'Installation annule pour "{{name}}".',
  'You are installing an extension from {{originSource}}. Some features may not work perfectly with Qwen Code.':
    'Vous installez une extension depuis {{originSource}}. Certaines fonctionnalits peuvent ne pas fonctionner parfaitement avec Qwen Code.',
  '--ref and --auto-update are not applicable for marketplace extensions.':
    '--ref et --auto-update ne sont pas applicables aux extensions du marketplace.',
  'Extension "{{name}}" installed successfully and enabled.':
    'Extension "{{name}}" installe et active avec succs.',
  'The github URL, local path, or marketplace source (marketplace-url:plugin-name) of the extension to install.':
    "L'URL GitHub, le chemin local ou la source marketplace (marketplace-url:nom-plugin) de l'extension  installer.",
  'The git ref to install from.': 'La rfrence git depuis laquelle installer.',
  'Enable auto-update for this extension.':
    'Activer la mise  jour automatique pour cette extension.',
  'Enable pre-release versions for this extension.':
    'Activer les versions pr-release pour cette extension.',
  'Acknowledge the security risks of installing an extension and skip the confirmation prompt.':
    "Reconnatre les risques de scurit lis  l'installation d'une extension et ignorer la confirmation.",
  'The source argument must be provided.':
    "L'argument source doit tre fourni.",
  'Extension "{{name}}" successfully uninstalled.':
    'Extension "{{name}}" dsinstalle avec succs.',
  'Uninstalls an extension.': 'Dsinstalle une extension.',
  'The name or source path of the extension to uninstall.':
    "Le nom ou le chemin source de l'extension  dsinstaller.",
  'Please include the name of the extension to uninstall as a positional argument.':
    "Veuillez inclure le nom de l'extension  dsinstaller comme argument positionnel.",
  'Enables an extension.': 'Active une extension.',
  'The name of the extension to enable.': "Le nom de l'extension  activer.",
  'The scope to enable the extenison in. If not set, will be enabled in all scopes.':
    "La porte dans laquelle activer l'extension. Si non dfinie, sera active dans toutes les portes.",
  'Extension "{{name}}" successfully enabled for scope "{{scope}}".':
    'Extension "{{name}}" active avec succs pour la porte "{{scope}}".',
  'Extension "{{name}}" successfully enabled in all scopes.':
    'Extension "{{name}}" active avec succs dans toutes les portes.',
  'Invalid scope: {{scope}}. Please use one of {{scopes}}.':
    "Porte invalide : {{scope}}. Veuillez utiliser l'une de : {{scopes}}.",
  'Disables an extension.': 'Dsactive une extension.',
  'The name of the extension to disable.':
    "Le nom de l'extension  dsactiver.",
  'The scope to disable the extenison in.':
    "La porte dans laquelle dsactiver l'extension.",
  'Extension "{{name}}" successfully disabled for scope "{{scope}}".':
    'Extension "{{name}}" dsactive avec succs pour la porte "{{scope}}".',
  'Extension "{{name}}" successfully updated: {{oldVersion}} -> {{newVersion}}.':
    'Extension "{{name}}" mise  jour avec succs : {{oldVersion}} -> {{newVersion}}.',
  'Unable to install extension "{{name}}" due to missing install metadata':
    "Impossible d'installer l'extension \"{{name}}\" en raison de mtadonnes d'installation manquantes",
  'Extension "{{name}}" is already up to date.':
    'L\'extension "{{name}}" est dj  jour.',
  'Updates all extensions or a named extension to the latest version.':
    'Met  jour toutes les extensions ou une extension nomme vers la dernire version.',
  'Update all extensions.': 'Mettre  jour toutes les extensions.',
  'Either an extension name or --all must be provided':
    "Un nom d'extension ou --all doit tre fourni",
  'Lists installed extensions.': 'Liste les extensions installes.',
  'Path:': 'Chemin :',
  'Source:': 'Source :',
  'Type:': 'Type :',
  'Ref:': 'Rf :',
  'Release tag:': 'Tag de version :',
  'Enabled (User):': 'Activ (Utilisateur) :',
  'Enabled (Workspace):': 'Activ (Espace de travail) :',
  'Context files:': 'Fichiers de contexte :',
  'Skills:': 'Comptences :',
  'Agents:': 'Agents :',
  'MCP servers:': 'MCP servers :',
  'Link extension failed to install.':
    "chec de l'installation de l'extension lie.",
  'Extension "{{name}}" linked successfully and enabled.':
    'Extension "{{name}}" lie et active avec succs.',
  'Links an extension from a local path. Updates made to the local path will always be reflected.':
    'Lie une extension depuis un chemin local. Les modifications apportes au chemin local seront toujours refltes.',
  'The name of the extension to link.': "Le nom de l'extension  lier.",
  'Set a specific setting for an extension.':
    'Dfinir un paramtre spcifique pour une extension.',
  'Name of the extension to configure.': "Nom de l'extension  configurer.",
  'The setting to configure (name or env var).':
    "Le paramtre  configurer (nom ou variable d'environnement).",
  'The scope to set the setting in.':
    'La porte dans laquelle dfinir le paramtre.',
  'List all settings for an extension.':
    "Lister tous les paramtres d'une extension.",
  'Name of the extension.': "Nom de l'extension.",
  'Extension "{{name}}" has no settings to configure.':
    'L\'extension "{{name}}" n\'a aucun paramtre  configurer.',
  'Settings for "{{name}}":': 'Paramtres pour "{{name}}" :',
  '(workspace)': '(espace de travail)',
  '(user)': '(utilisateur)',
  '[not set]': '[non dfini]',
  '[value stored in keychain]': '[valeur stocke dans le trousseau]',
  'Value:': 'Valeur :',
  'Manage extension settings.': 'Grer les paramtres des extensions.',
  'You need to specify a command (set or list).':
    'Vous devez spcifier une commande (set ou list).',

  // ============================================================================
  // Choix de plugin / Marketplace
  // ============================================================================
  'No plugins available in this marketplace.':
    'Aucun plugin disponible dans ce marketplace.',
  'Select a plugin to install from marketplace "{{name}}":':
    'Slectionnez un plugin  installer depuis le marketplace "{{name}}" :',
  'Plugin selection cancelled.': 'Slection de plugin annule.',
  'Select a plugin from "{{name}}"': 'Slectionner un plugin depuis "{{name}}"',
  'Use  or j/k to navigate, Enter to select, Escape to cancel':
    'Utilisez  ou j/k pour naviguer, Enter pour slectionner, Escape pour annuler',
  '{{count}} more above': '{{count}} de plus au-dessus',
  '{{count}} more below': '{{count}} de plus en dessous',
  'manage IDE integration': "grer l'intgration IDE",
  'check status of IDE integration': "vrifier le statut de l'intgration IDE",
  'install required IDE companion for {{ideName}}':
    'installer le compagnon IDE requis pour {{ideName}}',
  'enable IDE integration': "activer l'intgration IDE",
  'disable IDE integration': "dsactiver l'intgration IDE",
  'IDE integration is not supported in your current environment. To use this feature, run Qwen Code in one of these supported IDEs: VS Code or VS Code forks.':
    "L'intgration IDE n'est pas prise en charge dans votre environnement actuel. Pour utiliser cette fonctionnalit, excutez Qwen Code dans l'un des IDEs pris en charge : VS Code ou ses drivs.",
  'Set up GitHub Actions': 'Configurer GitHub Actions',
  'Configure terminal keybindings for multiline input (VS Code, Cursor, Windsurf, Trae)':
    'Configurer les raccourcis du terminal pour la saisie multiligne (VS Code, Cursor, Windsurf, Trae)',
  'Please restart your terminal for the changes to take effect.':
    'Veuillez redmarrer votre terminal pour que les modifications prennent effet.',
  'Failed to configure terminal: {{error}}':
    'chec de la configuration du terminal : {{error}}',
  'Could not determine {{terminalName}} config path on Windows: APPDATA environment variable is not set.':
    "Impossible de dterminer le chemin de configuration de {{terminalName}} sur Windows : la variable d'environnement APPDATA n'est pas dfinie.",
  '{{terminalName}} keybindings.json exists but is not a valid JSON array. Please fix the file manually or delete it to allow automatic configuration.':
    "{{terminalName}} keybindings.json existe mais n'est pas un tableau JSON valide. Veuillez corriger le fichier manuellement ou le supprimer pour permettre la configuration automatique.",
  'File: {{file}}': 'Fichier : {{file}}',
  'Failed to parse {{terminalName}} keybindings.json. The file contains invalid JSON. Please fix the file manually or delete it to allow automatic configuration.':
    "chec de l'analyse de {{terminalName}} keybindings.json. Le fichier contient du JSON invalide. Veuillez corriger le fichier manuellement ou le supprimer pour permettre la configuration automatique.",
  'Error: {{error}}': 'Erreur : {{error}}',
  'Shift+Enter binding already exists': 'Le raccourci Shift+Enter existe dj',
  'Ctrl+Enter binding already exists': 'Le raccourci Ctrl+Enter existe dj',
  'Existing keybindings detected. Will not modify to avoid conflicts.':
    'Raccourcis existants dtects. Aucune modification pour viter les conflits.',
  'Please check and modify manually if needed: {{file}}':
    'Veuillez vrifier et modifier manuellement si ncessaire : {{file}}',
  'Added Shift+Enter and Ctrl+Enter keybindings to {{terminalName}}.':
    'Raccourcis Shift+Enter et Ctrl+Enter ajouts  {{terminalName}}.',
  'Modified: {{file}}': 'Modifi : {{file}}',
  '{{terminalName}} keybindings already configured.':
    'Raccourcis {{terminalName}} dj configurs.',
  'Failed to configure {{terminalName}}.':
    'chec de la configuration de {{terminalName}}.',
  'Your terminal is already configured for an optimal experience with multiline input (Shift+Enter and Ctrl+Enter).':
    'Votre terminal est dj configur pour une exprience optimale avec la saisie multiligne (Shift+Enter et Ctrl+Enter).',

  // ============================================================================
  // Commandes - Hooks
  // ============================================================================
  'Manage Qwen Code hooks': 'Grer les hooks Qwen Code',
  'List all configured hooks': 'Lister tous les hooks configurs',
  Hooks: 'Hooks',
  'Loading hooks...': 'Chargement des hooks...',
  'Error loading hooks:': 'Erreur lors du chargement des hooks :',
  'Press Escape to close': 'Appuyez sur Escape pour fermer',
  'Press Escape, Ctrl+C, or Ctrl+D to cancel':
    'Appuyez sur Escape, Ctrl+C ou Ctrl+D pour annuler',
  'Press Space, Enter, or Escape to dismiss':
    'Appuyez sur Space, Enter ou Escape pour ignorer',
  'No hook selected': 'Aucun hook slectionn',
  'No hook events found.': 'Aucun vnement de hook trouv.',
  '{{count}} hook configured': '{{count}} hook configur',
  '{{count}} hooks configured': '{{count}} hooks configurs',
  'This menu is read-only. To add or modify hooks, edit settings.json directly or ask Qwen Code.':
    'Ce menu est en lecture seule. Pour ajouter ou modifier des hooks, ditez settings.json directement ou demandez  Qwen Code.',
  'Enter to select  Esc to cancel':
    'Enter pour slectionner  Esc pour annuler',
  'Exit codes:': 'Codes de sortie :',
  'Configured hooks:': 'Hooks configurs :',
  'No hooks configured for this event.':
    'Aucun hook configur pour cet vnement.',
  'To add hooks, edit settings.json directly or ask Qwen.':
    'Pour ajouter des hooks, ditez settings.json directement ou demandez  Qwen.',
  'Enter to select  Esc to go back':
    'Enter pour slectionner  Esc pour revenir',
  'Hook details': 'Dtails du hook',
  'Event:': 'vnement :',
  'Extension:': 'Extension :',
  'Desc:': 'Description :',
  'No hook config selected': 'Aucune configuration de hook slectionne',
  'To modify or remove this hook, edit settings.json directly or ask Qwen to help.':
    'Pour modifier ou supprimer ce hook, ditez settings.json directement ou demandez  Qwen.',
  'Hook Configuration - Disabled': 'Configuration du hook - Dsactiv',
  'All hooks are currently disabled. You have {{count}} that are not running.':
    "Tous les hooks sont actuellement dsactivs. Vous en avez {{count}} qui ne s'excutent pas.",
  '{{count}} configured hook': '{{count}} hook configur',
  '{{count}} configured hooks': '{{count}} hooks configurs',
  'When hooks are disabled:': 'Quand les hooks sont dsactivs :',
  'No hook commands will execute': "Aucune commande de hook ne s'excutera",
  'StatusLine will not be displayed': 'La barre de statut ne sera pas affiche',
  'Tool operations will proceed without hook validation':
    "Les oprations d'outils se poursuivront sans validation des hooks",
  'To re-enable hooks, remove "disableAllHooks" from settings.json or ask Qwen Code.':
    'Pour ractiver les hooks, supprimez "disableAllHooks" de settings.json ou demandez  Qwen Code.',
  Project: 'Projet',
  User: 'Utilisateur',
  Skill: 'Comptence',
  System: 'Systme',
  Extension: 'Extension',
  'Local Settings': 'Paramtres locaux',
  'User Settings': 'Paramtres utilisateur',
  'System Settings': 'Paramtres systme',
  Extensions: 'Extensions',
  'Before tool execution': "Avant l'excution de l'outil",
  'After tool execution': "Aprs l'excution de l'outil",
  'After tool execution fails': "Aprs l'chec de l'excution de l'outil",
  'When notifications are sent': 'Quand des notifications sont envoyes',
  'When the user submits a prompt': "Quand l'utilisateur soumet une invite",
  'When a new session is started': 'Quand une nouvelle session est dmarre',
  'Right before Qwen Code concludes its response':
    'Juste avant que Qwen Code conclue sa rponse',
  'When a subagent (Agent tool call) is started':
    "Quand un sous-agent (appel d'outil Agent) est dmarr",
  'Right before a subagent concludes its response':
    "Juste avant qu'un sous-agent conclue sa rponse",
  'Before conversation compaction': 'Avant la compaction de la conversation',
  'When a session is ending': 'Quand une session se termine',
  'When a permission dialog is displayed':
    'Quand un dialogue de permission est affich',
  'When a new todo item is created': 'Quand un nouvel lment todo est cr',
  'When a todo item is marked as completed':
    'Quand un lment todo est marqu comme termin',
  'Input to command is JSON of tool call arguments.':
    "L'entre de la commande est du JSON des arguments d'appel d'outil.",
  'Input to command is JSON with fields "inputs" (tool call arguments) and "response" (tool call response).':
    "L'entre de la commande est du JSON avec les champs \"inputs\" (arguments d'appel d'outil) et \"response\" (rponse de l'appel d'outil).",
  'Input to command is JSON with tool_name, tool_input, tool_use_id, error, error_type, is_interrupt, and is_timeout.':
    "L'entre de la commande est du JSON avec tool_name, tool_input, tool_use_id, error, error_type, is_interrupt et is_timeout.",
  'Input to command is JSON with notification message and type.':
    "L'entre de la commande est du JSON avec le message et le type de notification.",
  'Input to command is JSON with original user prompt text.':
    "L'entre de la commande est du JSON avec le texte d'invite original de l'utilisateur.",
  'Input to command is JSON with session start source.':
    "L'entre de la commande est du JSON avec la source de dmarrage de session.",
  'Input to command is JSON with session end reason.':
    "L'entre de la commande est du JSON avec la raison de fin de session.",
  'Input to command is JSON with agent_id and agent_type.':
    "L'entre de la commande est du JSON avec agent_id et agent_type.",
  'Input to command is JSON with agent_id, agent_type, and agent_transcript_path.':
    "L'entre de la commande est du JSON avec agent_id, agent_type et agent_transcript_path.",
  'Input to command is JSON with compaction details.':
    "L'entre de la commande est du JSON avec les dtails de compaction.",
  'Input to command is JSON with tool_name, tool_input, and tool_use_id. Output JSON with hookSpecificOutput containing decision to allow or deny.':
    "L'entre de la commande est du JSON avec tool_name, tool_input et tool_use_id. Sortie JSON avec hookSpecificOutput contenant la dcision d'autoriser ou de refuser.",
  'Input to command is JSON with todo_id, todo_content, todo_status, all_todos, and phase. In validation, output JSON with decision (allow/block/deny) and reason. In postWrite, block/deny is ignored.':
    "L'entre de la commande est du JSON avec todo_id, todo_content, todo_status, all_todos et phase. Dans validation, sortie JSON avec decision (allow/block/deny) et reason. Dans postWrite, block/deny est ignor.",
  'Input to command is JSON with todo_id, todo_content, previous_status, all_todos, and phase. In validation, output JSON with decision (allow/block/deny) and reason. In postWrite, block/deny is ignored.':
    "L'entre de la commande est du JSON avec todo_id, todo_content, previous_status, all_todos et phase. Dans validation, sortie JSON avec decision (allow/block/deny) et reason. Dans postWrite, block/deny est ignor.",
  'stdout/stderr not shown': 'stdout/stderr non affich',
  'show stderr to model and continue conversation':
    'afficher stderr au modle et continuer la conversation',
  'show stderr to user only': "afficher stderr  l'utilisateur uniquement",
  'stdout shown in transcript mode (ctrl+o)':
    'stdout affich en mode transcription (ctrl+o)',
  'show stderr to model immediately': 'afficher stderr au modle immdiatement',
  'show stderr to user only but continue with tool call':
    "afficher stderr  l'utilisateur uniquement mais continuer l'appel d'outil",
  'block processing, erase original prompt, and show stderr to user only':
    "bloquer le traitement, effacer l'invite originale et afficher stderr  l'utilisateur uniquement",
  'stdout shown to Qwen': 'stdout affich  Qwen',
  'show stderr to user only (blocking errors ignored)':
    "afficher stderr  l'utilisateur uniquement (erreurs bloquantes ignores)",
  'command completes successfully': 'la commande se termine avec succs',
  'stdout shown to subagent': 'stdout affich au sous-agent',
  'show stderr to subagent and continue having it run':
    'afficher stderr au sous-agent et continuer son excution',
  'stdout appended as custom compact instructions':
    'stdout ajout comme instructions compactes personnalises',
  'block compaction': 'bloquer la compaction',
  'show stderr to user only but continue with compaction':
    "afficher stderr  l'utilisateur uniquement mais continuer la compaction",
  'use hook decision if provided': 'utiliser la dcision du hook si fournie',
  'allow todo creation': 'autoriser la cration de todo',
  'block todo creation and show reason to model':
    'bloquer la cration de todo et afficher la raison au modle',
  'allow todo completion': 'autoriser la compltion de todo',
  'block todo completion and show reason to model':
    'bloquer la compltion de todo et afficher la raison au modle',
  'Config not loaded.': 'Configuration non charge.',
  'Hooks are not enabled. Enable hooks in settings to use this feature.':
    'Les hooks ne sont pas activs. Activez les hooks dans les paramtres pour utiliser cette fonctionnalit.',
  // ============================================================================
  // Commandes - Export de session
  // ============================================================================
  'Export current session message history to a file':
    "Exporter l'historique des messages de la session actuelle vers un fichier",
  'Export session to HTML format': 'Exporter la session au format HTML',
  'Export session to JSON format': 'Exporter la session au format JSON',
  'Export session to JSONL format (one message per line)':
    'Exporter la session au format JSONL (un message par ligne)',
  'Export session to markdown format': 'Exporter la session au format markdown',

  // ============================================================================
  // Commandes - Insights
  // ============================================================================
  'generate personalized programming insights from your chat history':
    'gnrer des insights de programmation personnaliss depuis votre historique de chat',

  // ============================================================================
  // Commandes - Historique de session
  // ============================================================================
  'Resume a previous session': 'Reprendre une session prcdente',
  'Fork the current conversation into a new session':
    'Crer une branche de la conversation actuelle dans une nouvelle session',
  'Cannot branch while a response or tool call is in progress. Wait for it to finish or resolve the pending tool call.':
    "Impossible de crer une branche pendant qu'une rponse ou un appel d'outil est en cours. Attendez la fin ou traitez l'appel d'outil en attente.",
  'No conversation to branch.':
    'Aucune conversation  dupliquer dans une branche.',
  'Restore a tool call. This will reset the conversation and file history to the state it was in when the tool call was suggested':
    "Restaurer un appel d'outil. Cela rinitialisera la conversation et l'historique des fichiers  l'tat o il se trouvait lors de la suggestion de l'appel d'outil",
  'Could not detect terminal type. Supported terminals: VS Code, Cursor, Windsurf, and Trae.':
    'Impossible de dtecter le type de terminal. Terminaux pris en charge : VS Code, Cursor, Windsurf et Trae.',
  'Terminal "{{terminal}}" is not supported yet.':
    'Le terminal "{{terminal}}" n\'est pas encore pris en charge.',

  // ============================================================================
  // Commandes - Langue
  // ============================================================================
  'Invalid language. Available: {{options}}':
    'Langue invalide. Disponibles : {{options}}',
  'Language subcommands do not accept additional arguments.':
    "Les sous-commandes de langue n'acceptent pas d'arguments supplmentaires.",
  'Current UI language: {{lang}}': "Langue de l'interface actuelle : {{lang}}",
  'Current LLM output language: {{lang}}':
    'Langue de sortie LLM actuelle : {{lang}}',
  'Set UI language': "Dfinir la langue de l'interface",
  'Set LLM output language': 'Dfinir la langue de sortie LLM',
  'Usage: /language ui [{{options}}]':
    'Utilisation : /language ui [{{options}}]',
  'Usage: /language output <language>':
    'Utilisation : /language output <langue>',
  'Example: /language output ': 'Exemple : /language output ',
  'Example: /language output English': 'Exemple : /language output English',
  'Example: /language output ': 'Exemple : /language output ',
  'UI language changed to {{lang}}':
    "Langue de l'interface change en {{lang}}",
  'LLM output language set to {{lang}}':
    'Langue de sortie LLM dfinie sur {{lang}}',
  'Please restart the application for the changes to take effect.':
    "Veuillez redmarrer l'application pour que les modifications prennent effet.",
  'Failed to generate LLM output language rule file: {{error}}':
    'chec de la gnration du fichier de rgle de langue de sortie LLM : {{error}}',
  'Invalid command. Available subcommands:':
    'Commande invalide. Sous-commandes disponibles :',
  'Available subcommands:': 'Sous-commandes disponibles :',
  'To request additional UI language packs, please open an issue on GitHub.':
    "Pour demander des packs de langue d'interface supplmentaires, veuillez ouvrir un ticket sur GitHub.",
  'Available options:': 'Options disponibles :',
  'Set UI language to {{name}}':
    "Dfinir la langue de l'interface sur {{name}}",

  // ============================================================================
  // Commandes - Mode d'approbation
  // ============================================================================
  'Tool Approval Mode': "Mode d'approbation des outils",
  '{{mode}} mode': 'Mode {{mode}}',
  'Analyze only, do not modify files or execute commands':
    'Analyser uniquement, ne pas modifier les fichiers ni excuter des commandes',
  'Require approval for file edits or shell commands':
    "Demander l'approbation pour les modifications de fichiers ou les commandes shell",
  'Automatically approve file edits':
    'Approuver automatiquement les modifications de fichiers',
  'Automatically approve all tools':
    'Approuver automatiquement tous les outils',
  'Workspace approval mode exists and takes priority. User-level change will have no effect.':
    "Un mode d'approbation d'espace de travail existe et a la priorit. La modification au niveau utilisateur n'aura aucun effet.",
  'Apply To': 'Appliquer ',
  'Workspace Settings': "Paramtres de l'espace de travail",
  'Open MCP management dialog': 'Ouvrir le dialogue de gestion MCP',
  'Could not retrieve tool registry.':
    'Impossible de rcuprer le registre des outils.',
  "Successfully authenticated and refreshed tools for '{{name}}'.":
    "Authentification russie et outils actualiss pour '{{name}}'.",
  "Re-discovering tools from '{{name}}'...":
    "Redcouverte des outils depuis '{{name}}'...",
  "Discovered {{count}} tool(s) from '{{name}}'.":
    "{{count}} outil(s) dcouvert(s) depuis '{{name}}'.",
  'Authentication complete. Returning to server details...':
    'Authentification termine. Retour aux dtails du serveur...',
  'Authentication successful.': 'Authentification russie.',
  // ============================================================================
  // Bote de dialogue de gestion MCP
  // ============================================================================
  'Manage MCP servers': 'Grer les MCP servers',
  'Server Detail': 'Dtail du serveur',
  Tools: 'Outils',
  'Tool Detail': "Dtail de l'outil",
  'Loading...': 'Chargement...',
  'Unknown step': 'tape inconnue',
  'Esc to back': 'Esc pour revenir',
  ' to navigate  Enter to select  Esc to close':
    ' pour naviguer  Enter pour slectionner  Esc pour fermer',
  ' to navigate  Enter to select  Esc to back':
    ' pour naviguer  Enter pour slectionner  Esc pour revenir',
  ' to navigate  Enter to confirm  Esc to back':
    ' pour naviguer  Enter pour confirmer  Esc pour revenir',
  'User Settings (global)': 'Paramtres utilisateur (global)',
  'Workspace Settings (project-specific)':
    'Paramtres espace de travail (spcifique au projet)',
  'Disable server:': 'Dsactiver le serveur :',
  'Select where to add the server to the exclude list:':
    "Slectionnez o ajouter le serveur  la liste d'exclusion :",
  'Press Enter to confirm, Esc to cancel':
    'Appuyez sur Enter pour confirmer, Esc pour annuler',
  'View tools': 'Voir les outils',
  Reconnect: 'Reconnecter',
  Enable: 'Activer',
  Disable: 'Dsactiver',
  Authenticate: 'Authentifier',
  'Re-authenticate': 'Rauthentifier',
  'Clear Authentication': "Effacer l'authentification",
  'Server:': 'Serveur :',
  'Command:': 'Commande :',
  'Working Directory:': 'Rpertoire de travail :',
  'No server selected': 'Aucun serveur slectionn',
  prompts: 'invites',
  'Error:': 'Erreur :',
  tool: 'outil',
  tools: 'outils',
  connected: 'connect',
  connecting: 'connexion en cours',
  disconnected: 'dconnect',
  'User MCPs': 'MCPs utilisateur',
  'Project MCPs': 'MCPs projet',
  'Extension MCPs': "MCPs d'extension",
  server: 'serveur',
  servers: 'serveurs',
  'Add MCP servers to your settings to get started.':
    'Ajoutez des MCP servers  vos paramtres pour commencer.',
  'Run qwen --debug to see error logs':
    "Excutez qwen --debug pour voir les journaux d'erreurs",
  'OAuth Authentication': 'Authentification OAuth',
  'Authenticating... Please complete the login in your browser.':
    'Authentification... Veuillez complter la connexion dans votre navigateur.',
  'No tools available for this server.':
    'Aucun outil disponible pour ce serveur.',
  destructive: 'destructif',
  'read-only': 'lecture seule',
  'open-world': 'monde ouvert',
  idempotent: 'idempotent',
  'Tools for {{serverName}}': 'Outils pour {{serverName}}',
  '{{current}}/{{total}}': '{{current}}/{{total}}',
  required: 'requis',
  Parameters: 'Paramtres',
  'No tool selected': 'Aucun outil slectionn',
  Server: 'Serveur',
  '{{count}} invalid tools': '{{count}} outils invalides',
  invalid: 'invalide',
  'invalid: {{reason}}': 'invalide : {{reason}}',
  'missing name': 'nom manquant',
  'missing description': 'description manquante',
  '(unnamed)': '(sans nom)',
  'Warning: This tool cannot be called by the LLM':
    'Avertissement : Cet outil ne peut pas tre appel par le LLM',
  Reason: 'Raison',
  'Tools must have both name and description to be used by the LLM.':
    'Les outils doivent avoir un nom et une description pour tre utiliss par le LLM.',
  // ===========================================================
  // Commandes - Rsum
  // ============================================================================
  'Generate a project summary and save it to .qwen/PROJECT_SUMMARY.md':
    "Gnrer un rsum du projet et l'enregistrer dans .qwen/PROJECT_SUMMARY.md",
  'No chat client available to generate summary.':
    'Aucun client de chat disponible pour gnrer le rsum.',
  'Already generating summary, wait for previous request to complete':
    'Gnration de rsum dj en cours, attendez que la demande prcdente se termine',
  'No conversation found to summarize.':
    'Aucune conversation trouve  rsumer.',
  'Failed to generate project context summary: {{error}}':
    'chec de la gnration du rsum du contexte du projet : {{error}}',
  'Saved project summary to {{filePathForDisplay}}.':
    'Rsum du projet enregistr dans {{filePathForDisplay}}.',
  'Saving project summary...': 'Enregistrement du rsum du projet...',
  'Generating project summary...': 'Gnration du rsum du projet...',
  'Processing summary...': 'Traitement du rsum...',
  'Project summary generated and saved successfully!':
    'Le rsum du projet a t gnr et enregistr avec succs !',
  'Saved to: {{filePath}}': 'Enregistr dans : {{filePath}}',
  'Failed to generate summary - no text content received from LLM response':
    'chec de la gnration du rsum - aucun contenu texte reu de la rponse LLM',

  // ============================================================================
  // Commandes - Modle
  // ============================================================================
  'Switch the model for this session (--fast for suggestion model, [model-id] to switch immediately).':
    'Changer le modle pour cette session (--fast pour le modle de suggestion)',
  'Set a lighter model for prompt suggestions and speculative execution':
    "Dfinir un modle plus lger pour les suggestions d'invite et l'excution spculative",
  'Content generator configuration not available.':
    'Configuration du gnrateur de contenu non disponible.',
  'Authentication type not available.':
    "Type d'authentification non disponible.",
  'No models available for the current authentication type ({{authType}}).':
    "Aucun modle disponible pour le type d'authentification actuel ({{authType}}).",
  // Needs translation
  ' (not in model registry)': ' (not in model registry)',

  // ============================================================================
  // Commandes - Effacer
  // ============================================================================
  'Starting a new session, resetting chat, and clearing terminal.':
    "Dmarrage d'une nouvelle session, rinitialisation du chat et effacement du terminal.",
  'Starting a new session and clearing.':
    "Dmarrage d'une nouvelle session et effacement.",

  // ============================================================================
  // Commandes - Compresser
  // ============================================================================
  'Already compressing, wait for previous request to complete':
    'Compression dj en cours, attendez que la demande prcdente se termine',
  'Failed to compress chat history.':
    "chec de la compression de l'historique du chat.",
  'Failed to compress chat history: {{error}}':
    "chec de la compression de l'historique du chat : {{error}}",
  'Compressing chat history': "Compression de l'historique du chat",
  'Chat history compressed from {{originalTokens}} to {{newTokens}} tokens.':
    "L'historique du chat a t compress de {{originalTokens}}  {{newTokens}} tokens.",
  'Compression was not beneficial for this history size.':
    "La compression n'tait pas bnfique pour cette taille d'historique.",
  'Chat history compression did not reduce size. This may indicate issues with the compression prompt.':
    "La compression de l'historique du chat n'a pas rduit la taille. Cela peut indiquer des problmes avec l'invite de compression.",
  'Could not compress chat history due to a token counting error.':
    "Impossible de compresser l'historique du chat en raison d'une erreur de comptage de tokens.",
  // ============================================================================
  // Commandes - Rpertoire
  // ============================================================================
  'Configuration is not available.': 'Configuration non disponible.',
  'Please provide at least one path to add.':
    'Veuillez fournir au moins un chemin  ajouter.',
  'The /directory add command is not supported in restrictive sandbox profiles. Please use --include-directories when starting the session instead.':
    "La commande /directory add n'est pas prise en charge dans les profils de bac  sable restrictifs. Utilisez plutt --include-directories lors du dmarrage de la session.",
  "Error adding '{{path}}': {{error}}":
    "Erreur lors de l'ajout de '{{path}}' : {{error}}",
  'Successfully added QWEN.md files from the following directories if there are:\n- {{directories}}':
    "Fichiers QWEN.md ajouts avec succs depuis les rpertoires suivants s'ils existent :\n- {{directories}}",
  'Error refreshing memory: {{error}}':
    "Erreur lors de l'actualisation de la mmoire : {{error}}",
  'Successfully added directories:\n- {{directories}}':
    'Rpertoires ajouts avec succs :\n- {{directories}}',
  'Current workspace directories:\n{{directories}}':
    "Rpertoires actuels de l'espace de travail :\n{{directories}}",

  // ============================================================================
  // Commandes - Documentation
  // ============================================================================
  'Please open the following URL in your browser to view the documentation:\n{{url}}':
    "Veuillez ouvrir l'URL suivante dans votre navigateur pour voir la documentation :\n{{url}}",
  'Opening documentation in your browser: {{url}}':
    'Ouverture de la documentation dans votre navigateur : {{url}}',

  // ============================================================================
  // Botes de dialogue - Confirmation d'outil
  // ============================================================================
  'Do you want to proceed?': 'Voulez-vous continuer ?',
  'Yes, allow once': 'Oui, autoriser une fois',
  'Allow always': 'Toujours autoriser',
  Yes: 'Oui',
  No: 'Non',
  'No (esc)': 'Non (chap)',
  'Modify in progress:': 'Modification en cours :',
  'Save and close external editor to continue':
    "Enregistrez et fermez l'diteur externe pour continuer",
  'Apply this change?': 'Appliquer cette modification ?',
  'Yes, allow always': 'Oui, toujours autoriser',
  'Modify with external editor': "Modifier avec l'diteur externe",
  'No, suggest changes (esc)': 'Non, suggrer des modifications (chap)',
  "Allow execution of: '{{command}}'?":
    "Autoriser l'excution de : '{{command}}' ?",
  'Always allow in this project': 'Toujours autoriser dans ce projet',
  'Always allow {{action}} in this project':
    'Toujours autoriser {{action}} dans ce projet',
  'Always allow for this user': 'Toujours autoriser pour cet utilisateur',
  'Always allow {{action}} for this user':
    'Toujours autoriser {{action}} pour cet utilisateur',
  'Yes, restore previous mode ({{mode}})':
    'Oui, restaurer le mode prcdent ({{mode}})',
  'Yes, and auto-accept edits':
    'Oui, et accepter automatiquement les modifications',
  'Yes, and manually approve edits':
    'Oui, et approuver manuellement les modifications',
  'No, keep planning (esc)': 'Non, continuer la planification (chap)',
  'URLs to fetch:': 'URLs  rcuprer :',
  'MCP Server: {{server}}': 'MCP Server : {{server}}',
  'Tool: {{tool}}': 'Outil : {{tool}}',
  'Allow execution of MCP tool "{{tool}}" from server "{{server}}"?':
    'Autoriser l\'excution de MCP tool "{{tool}}" depuis MCP server "{{server}}" ?',
  // ============================================================================
  // Botes de dialogue - Confirmation shell
  // ============================================================================
  'Shell Command Execution': 'Excution de commande shell',
  'A custom command wants to run the following shell commands:':
    'Une commande personnalise veut excuter les commandes shell suivantes :',
  // ============================================================================
  // Botes de dialogue - Bienvenue
  // ============================================================================
  'Current Plan:': 'Plan actuel :',
  'Progress: {{done}}/{{total}} tasks completed':
    'Progression : {{done}}/{{total}} tches termines',
  ', {{inProgress}} in progress': ', {{inProgress}} en cours',
  'Pending Tasks:': 'Tches en attente :',
  'What would you like to do?': 'Que souhaitez-vous faire ?',
  'Choose how to proceed with your session:':
    'Choisissez comment poursuivre votre session :',
  'Start new chat session': 'Dmarrer une nouvelle session de chat',
  'Continue previous conversation': 'Continuer la conversation prcdente',
  ' Welcome back! (Last updated: {{timeAgo}})':
    ' Bon retour ! (Dernire mise  jour : {{timeAgo}})',
  ' Overall Goal:': ' Objectif global :',
  'Connect a Provider': 'Connecter un fournisseur',
  'You must connect a provider to proceed. Press Ctrl+C again to exit.':
    'Vous devez connecter un fournisseur pour continuer. Appuyez  nouveau sur Ctrl+C pour quitter.',
  'Terms of Services and Privacy Notice':
    "Conditions d'utilisation et avis de confidentialit",
  'Qwen OAuth': 'Qwen OAuth',
  'Discontinued -- switch to Coding Plan or API Key':
    'Abandonn -- passez  Coding Plan ou API Key',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Please select Coding Plan or API Key instead.':
    'Le niveau gratuit Qwen OAuth a t abandonn le 2026-04-15. Veuillez slectionner Coding Plan ou API Key.',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Please select a model from another provider or run /auth to switch.':
    "Le niveau gratuit de Qwen OAuth a t abandonn le 2026-04-15. Veuillez slectionner un modle d'un autre fournisseur ou excuter /auth pour changer.",
  '\n Qwen OAuth free tier was discontinued on 2026-04-15. Please select another option.\n':
    '\n Le niveau gratuit Qwen OAuth a t abandonn le 2026-04-15. Veuillez slectionner une autre option.\n',
  'Paid \u00B7 Up to 6,000 requests/5 hrs \u00B7 All Alibaba Cloud Coding Plan Models':
    "Payant  Jusqu' 6 000 requtes/5h  Tous les modles Alibaba Cloud Coding Plan",
  'Alibaba Cloud Coding Plan': 'Alibaba Cloud Coding Plan',
  'Bring your own API key': 'Apportez votre propre API Key',
  'Browser-based authentication with third-party providers (e.g. OpenRouter, ModelScope)':
    'Authentification base sur le navigateur avec des fournisseurs tiers (par exemple OpenRouter, ModelScope)',
  'Authentication is enforced to be {{enforcedType}}, but you are currently using {{currentType}}.':
    "L'authentification est impose  {{enforcedType}}, mais vous utilisez actuellement {{currentType}}.",
  'Qwen OAuth Authentication': 'Authentification Qwen OAuth',
  'Please visit this URL to authorize:':
    'Veuillez visiter cette URL pour autoriser :',
  'Waiting for authorization': "En attente d'autorisation",
  'Time remaining:': 'Temps restant :',
  'Qwen OAuth Authentication Timeout': "Dlai d'authentification Qwen OAuth",
  'OAuth token expired (over {{seconds}} seconds). Please select authentication method again.':
    "Token OAuth expir (plus de {{seconds}} secondes). Veuillez slectionner  nouveau la mthode d'authentification.",
  'Press any key to return to authentication type selection.':
    "Appuyez sur n'importe quelle touche pour revenir  la slection du type d'authentification.",
  'Waiting for Qwen OAuth authentication...':
    "En attente de l'authentification Qwen OAuth...",
  'Authentication timed out. Please try again.':
    "L'authentification a expir. Veuillez ressayer.",
  'Waiting for auth... (Press ESC or CTRL+C to cancel)':
    "En attente d'authentification... (Appuyez sur CHAP ou CTRL+C pour annuler)",
  'Missing API key for OpenAI-compatible auth. Set settings.security.auth.apiKey, or set the {{envKeyHint}} environment variable.':
    "API Key manquante pour l'authentification compatible OpenAI. Dfinissez settings.security.auth.apiKey ou la variable d'environnement {{envKeyHint}}.",
  '{{envKeyHint}} environment variable not found. Please set it in your .env file or environment variables.':
    "Variable d'environnement {{envKeyHint}} introuvable. Veuillez la dfinir dans votre fichier .env ou les variables d'environnement.",
  '{{envKeyHint}} environment variable not found (or set settings.security.auth.apiKey). Please set it in your .env file or environment variables.':
    "Variable d'environnement {{envKeyHint}} introuvable (ou dfinissez settings.security.auth.apiKey). Veuillez la dfinir dans votre fichier .env ou les variables d'environnement.",
  'Missing API key for OpenAI-compatible auth. Set the {{envKeyHint}} environment variable.':
    "API Key manquante pour l'authentification compatible OpenAI. Dfinissez la variable d'environnement {{envKeyHint}}.",
  'Anthropic provider missing required baseUrl in modelProviders[].baseUrl.':
    'Le fournisseur Anthropic manque le baseUrl requis dans modelProviders[].baseUrl.',
  'ANTHROPIC_BASE_URL environment variable not found.':
    "Variable d'environnement ANTHROPIC_BASE_URL introuvable.",
  'Invalid auth method selected.':
    "Mthode d'authentification invalide slectionne.",
  'Failed to authenticate. Message: {{message}}':
    "chec de l'authentification. Message : {{message}}",
  'Authenticated successfully with {{authType}} credentials.':
    'Authentification russie avec les identifiants {{authType}}.',
  'Invalid QWEN_DEFAULT_AUTH_TYPE value: "{{value}}". Valid values are: {{validValues}}':
    'Valeur QWEN_DEFAULT_AUTH_TYPE invalide : "{{value}}". Valeurs valides : {{validValues}}',
  // ============================================================================
  // Botes de dialogue - Modle
  // ============================================================================
  'Select Model': 'Slectionner un modle',
  'API Key': 'API Key',
  '(default)': '(par dfaut)',
  '(not set)': '(non dfini)',
  Modality: 'Modalit',
  'Context Window': 'Fentre de contexte',
  text: 'texte',
  'text-only': 'texte uniquement',
  image: 'image',
  pdf: 'pdf',
  audio: 'audio',
  video: 'vido',
  'not set': 'non dfini',
  none: 'aucun',
  unknown: 'inconnu',
  // ============================================================================
  // Botes de dialogue - Permissions
  // ============================================================================
  'Manage folder trust settings':
    'Grer les paramtres de confiance des dossiers',
  'Manage permission rules': 'Grer les permission rules',
  Allow: 'Autoriser',
  Ask: 'Demander',
  Deny: 'Refuser',
  Workspace: 'Espace de travail',
  "Qwen Code won't ask before using allowed tools.":
    "Qwen Code ne demandera pas avant d'utiliser les outils autoriss.",
  'Qwen Code will ask before using these tools.':
    "Qwen Code demandera avant d'utiliser ces outils.",
  'Qwen Code is not allowed to use denied tools.':
    "Qwen Code n'est pas autoris  utiliser les outils refuss.",
  'Manage trusted directories for this workspace.':
    'Grer les rpertoires de confiance pour cet espace de travail.',
  'Any use of the {{tool}} tool': "Toute utilisation de l'outil {{tool}}",
  "{{tool}} commands matching '{{pattern}}'":
    "Commandes {{tool}} correspondant  '{{pattern}}'",
  'From user settings': 'Depuis les paramtres utilisateur',
  'From project settings': 'Depuis les paramtres du projet',
  'From session': 'Depuis la session',
  'Project settings': 'Paramtres du projet',
  'Checked in at .qwen/settings.json': 'Valid dans .qwen/settings.json',
  'User settings': 'Paramtres utilisateur',
  'Saved in at ~/.qwen/settings.json': 'Enregistr dans ~/.qwen/settings.json',
  'Add a new rule...': 'Ajouter une nouvelle rgle...',
  'Add {{type}} permission rule': 'Ajouter {{type}} permission rule',
  'Permission rules are a tool name, optionally followed by a specifier in parentheses.':
    "Les permission rules sont un nom d'outil, suivi optionnellement d'un spcificateur entre parenthses.",
  'e.g.,': 'ex.,',
  or: 'ou',
  'Enter permission rule...': 'Entrer une permission rule...',
  'Enter to submit  Esc to cancel': 'Enter pour soumettre  Esc pour annuler',
  'Where should this rule be saved?':
    'O cette rgle doit-elle tre enregistre ?',
  'Enter to confirm  Esc to cancel': 'Enter pour confirmer  Esc pour annuler',
  'Delete {{type}} rule?': 'Supprimer la rgle {{type}} ?',
  'Are you sure you want to delete this permission rule?':
    'tes-vous sr de vouloir supprimer cette permission rule ?',
  'Permissions:': 'Permissions :',
  '(<-/-> or tab to cycle)': '(<-/-> ou Tab pour cycler)',
  'Press  to navigate  Enter to select  Type to search  Esc to cancel':
    'Appuyez sur  pour naviguer  Enter pour slectionner  Tapez pour rechercher  Esc pour annuler',
  'Search...': 'Rechercher...',
  'Add directory...': 'Ajouter un rpertoire...',
  'Add directory to workspace': "Ajouter un rpertoire  l'espace de travail",
  'Qwen Code can read files in the workspace, and make edits when auto-accept edits is on.':
    "Qwen Code peut lire les fichiers dans l'espace de travail et effectuer des modifications lorsque l'acceptation automatique est active.",
  'Qwen Code will be able to read files in this directory and make edits when auto-accept edits is on.':
    "Qwen Code pourra lire les fichiers dans ce rpertoire et effectuer des modifications lorsque l'acceptation automatique est active.",
  'Enter the path to the directory:': 'Entrez le chemin vers le rpertoire :',
  'Enter directory path...': 'Entrez le chemin du rpertoire...',
  'Tab to complete  Enter to add  Esc to cancel':
    'Tab pour complter  Enter pour ajouter  Esc pour annuler',
  'Remove directory?': 'Supprimer le rpertoire ?',
  'Are you sure you want to remove this directory from the workspace?':
    "tes-vous sr de vouloir supprimer ce rpertoire de l'espace de travail ?",
  '  (Original working directory)': "  (Rpertoire de travail d'origine)",
  '  (from settings)': '  (depuis les paramtres)',
  'Directory does not exist.': "Le rpertoire n'existe pas.",
  'Path is not a directory.': "Le chemin n'est pas un rpertoire.",
  'This directory is already in the workspace.':
    "Ce rpertoire est dj dans l'espace de travail.",
  'Already covered by existing directory: {{dir}}':
    'Dj couvert par le rpertoire existant : {{dir}}',

  // ============================================================================
  // Barre de statut
  // ============================================================================
  'Using:': 'Utilisation :',
  '{{count}} open file': '{{count}} fichier ouvert',
  '{{count}} open files': '{{count}} fichiers ouverts',
  '(ctrl+g to view)': '(ctrl+g pour afficher)',
  '{{count}} {{name}} file': '{{count}} fichier {{name}}',
  '{{count}} {{name}} files': '{{count}} fichiers {{name}}',
  '{{count}} MCP server': '{{count}} MCP server',
  '{{count}} MCP servers': '{{count}} MCP servers',
  '{{count}} Blocked': '{{count}} bloqu(s)',
  '(ctrl+t to view)': '(ctrl+t pour afficher)',
  '(ctrl+t to toggle)': '(ctrl+t pour basculer)',
  'Press Ctrl+C again to exit.': 'Appuyez  nouveau sur Ctrl+C pour quitter.',
  'Press Ctrl+D again to exit.': 'Appuyez  nouveau sur Ctrl+D pour quitter.',
  'Press Esc again to clear.': 'Appuyez  nouveau sur Esc pour effacer.',

  // ============================================================================
  // Statut MCP
  // ============================================================================
  'No MCP servers configured.': 'Aucun MCP servers configur.',
  ' MCP servers are starting up ({{count}} initializing)...':
    ' Les MCP servers dmarrent ({{count}} en initialisation)...',
  'Note: First startup may take longer. Tool availability will update automatically.':
    'Remarque : Le premier dmarrage peut prendre plus de temps. La disponibilit des outils se mettra  jour automatiquement.',
  'Configured MCP servers:': 'MCP servers configurs :',
  Ready: 'Prt',
  'Starting... (first startup may take longer)':
    'Dmarrage... (le premier dmarrage peut prendre plus de temps)',
  Disconnected: 'Dconnect',
  '{{count}} tool': '{{count}} outil',
  '{{count}} tools': '{{count}} outils',
  '{{count}} prompt': '{{count}} invite',
  '{{count}} prompts': '{{count}} invites',
  '(from {{extensionName}})': '(depuis {{extensionName}})',
  OAuth: 'OAuth',
  'OAuth expired': 'OAuth expir',
  'OAuth not authenticated': 'OAuth non authentifi',
  'tools and prompts will appear when ready':
    'les outils et invites apparatront quand prts',
  '{{count}} tools cached': '{{count}} outils mis en cache',
  'Tools:': 'Outils :',
  'Parameters:': 'Paramtres :',
  'Prompts:': 'Invites :',
  Blocked: 'Bloqu',
  ' Tips:': ' Conseils :',
  Use: 'Utilisez',
  'to show server and tool descriptions':
    'pour afficher les descriptions des serveurs et des outils',
  'to show tool parameter schemas': 'pour afficher les tool parameter schemas',
  'to hide descriptions': 'pour masquer les descriptions',
  'to authenticate with OAuth-enabled servers':
    'pour authentifier avec des serveurs compatibles OAuth',
  Press: 'Appuyez sur',
  'to toggle tool descriptions on/off':
    'pour activer/dsactiver les descriptions des outils',
  "Starting OAuth authentication for MCP server '{{name}}'...":
    "Dmarrage de l'authentification OAuth pour MCP server '{{name}}'...",
  // ============================================================================
  // Conseils de dmarrage
  // ============================================================================
  'Tips:': 'Conseils :',
  'Use /compress when the conversation gets long to summarize history and free up context.':
    "Utilisez /compress quand la conversation devient longue pour rsumer l'historique et librer le contexte.",
  'Start a fresh idea with /clear or /new; the previous session stays available in history.':
    "Commencez une nouvelle ide avec /clear ou /new ; la session prcdente reste disponible dans l'historique.",
  'Use /bug to submit issues to the maintainers when something goes off.':
    'Utilisez /bug pour soumettre des problmes aux mainteneurs quand quelque chose ne va pas.',
  'Switch auth type quickly with /auth.':
    "Changez rapidement le type d'authentification avec /auth.",
  'You can run any shell commands from Qwen Code using ! (e.g. !ls).':
    "Vous pouvez excuter n'importe quelle commande shell depuis Qwen Code en utilisant ! (ex. !ls).",
  'Type / to open the command popup; Tab autocompletes slash commands and saved prompts.':
    'Tapez / pour ouvrir le menu des commandes ; Tab autocomplte les commandes slash et les invites sauvegardes.',
  'You can resume a previous conversation by running qwen --continue or qwen --resume.':
    'Vous pouvez reprendre une conversation prcdente en excutant qwen --continue ou qwen --resume.',
  'You can switch permission mode quickly with Shift+Tab or /approval-mode.':
    'Vous pouvez changer rapidement le mode de permission avec Shift+Tab ou /approval-mode.',
  'You can switch permission mode quickly with Tab or /approval-mode.':
    'Vous pouvez changer rapidement le mode de permission avec Tab ou /approval-mode.',
  'Try /insight to generate personalized insights from your chat history.':
    'Essayez /insight pour gnrer des insights personnaliss depuis votre historique de chat.',

  // ============================================================================
  // cran de sortie / Stats
  // ============================================================================
  'Agent powering down. Goodbye!': "Agent en cours d'arrt. Au revoir !",
  'To continue this session, run': 'Pour continuer cette session, excutez',
  'Interaction Summary': "Rsum de l'interaction",
  'Session ID:': 'ID de session :',
  'Tool Calls:': "Appels d'outils :",
  'Success Rate:': 'Taux de succs :',
  'User Agreement:': "Accord de l'utilisateur :",
  reviewed: 'rvis',
  'Code Changes:': 'Modifications du code :',
  Performance: 'Performance',
  'Wall Time:': 'Temps rel :',
  'Agent Active:': 'Agent actif :',
  'API Time:': 'Temps API :',
  'Tool Time:': "Temps d'outil :",
  'Session Stats': 'Stats de session',
  'Model Usage': 'Utilisation du modle',
  Reqs: 'Req.',
  'Input Tokens': "Tokens d'entre",
  'Output Tokens': 'Tokens de sortie',
  'Savings Highlight:': 'conomies notables :',
  'of input tokens were served from the cache, reducing costs.':
    "des tokens d'entre ont t servis depuis le cache, rduisant les cots.",
  'Tip: For a full token breakdown, run `/stats model`.':
    'Conseil : Pour une dcomposition complte des tokens, excutez `/stats model`.',
  'Model Stats For Nerds': 'Stats du modle pour les geeks',
  'Tool Stats For Nerds': 'Stats des outils pour les geeks',
  Metric: 'Mtrique',
  API: 'API',
  Requests: 'Requtes',
  Errors: 'Erreurs',
  'Avg Latency': 'Latence moyenne',
  Total: 'Total',
  Prompt: 'Invite',
  Cached: 'En cache',
  Thoughts: 'Rflexions',
  Output: 'Sortie',
  'No API calls have been made in this session.':
    "Aucun appel API n'a t effectu dans cette session.",
  'Tool Name': "Nom de l'outil",
  Calls: 'Appels',
  'Success Rate': 'Taux de succs',
  'Avg Duration': 'Dure moyenne',
  'User Decision Summary': "Rsum des dcisions de l'utilisateur",
  'Total Reviewed Suggestions:': 'Total des suggestions rvises :',
  '  Accepted:': '  Acceptes :',
  '  Rejected:': '  Rejetes :',
  '  Modified:': '  Modifies :',
  ' Overall Agreement Rate:': " Taux d'accord global :",
  'No tool calls have been made in this session.':
    "Aucun appel d'outil n'a t effectu dans cette session.",
  'Session start time is unavailable, cannot calculate stats.':
    "L'heure de dbut de session est indisponible, impossible de calculer les stats.",

  // ============================================================================
  // Migration de format de commande
  // ============================================================================
  'Command Format Migration': 'Migration du format de commande',
  'Found {{count}} TOML command file:':
    'Trouv {{count}} fichier de commande TOML :',
  'Found {{count}} TOML command files:':
    'Trouv {{count}} fichiers de commande TOML :',
  'Current tasks': 'Tches actuelles',
  '... and {{count}} more': '... et {{count}} de plus',
  'The TOML format is deprecated. Would you like to migrate them to Markdown format?':
    'Le format TOML est obsolte. Souhaitez-vous les migrer vers le format Markdown ?',
  '(Backups will be created and original files will be preserved)':
    '(Des sauvegardes seront cres et les fichiers originaux seront conservs)',

  // ============================================================================
  // Phrases de chargement
  // ============================================================================
  'Waiting for user confirmation...':
    "En attente de la confirmation de l'utilisateur...",
  // ============================================================================
  // Phrases de chargement amusantes
  // ============================================================================
  WITTY_LOADING_PHRASES: [
    'Je me sens chanceux',
    "Livraison d'excellence...",
    'Repeignant les empattements...',
    'Navigation dans le moisissure numrique...',
    'Consultation des esprits numriques...',
    'Rticuler les splines...',
    'Rchauffement des hamsters IA...',
    'Consultation de la conque magique...',
    "Gnration d'une rplique spirituelle...",
    'Polissage des algorithmes...',
    'Ne prcipitez pas la perfection (ni mon code)...',
    'Brassage de nouveaux octets...',
    'Comptage des lectrons...',
    'Engagement des processeurs cognitifs...',
    "Vrification des erreurs de syntaxe dans l'univers...",
    "Un instant, optimisation de l'humour...",
    'Mlange des chutes de rpliques...',
    'Dmlage des rseaux de neurones...',
    'Compilation de la brillance...',
    'Chargement de wit.exe...',
    'Invocation du nuage de sagesse...',
    "Prparation d'une rponse spirituelle...",
    'Juste une seconde, je dbogue la ralit...',
    'Confusion des options...',
    'Accord des frquences cosmiques...',
    "Cration d'une rponse digne de votre patience...",
    'Compilation des 0 et des 1...',
    'Rsolution des dpendances... et des crises existentielles...',
    'Dfragmentation des mmoires... RAM et personnelles...',
    'Redmarrage du module humoristique...',
    "Mise en cache de l'essentiel (surtout les mmes de chats)...",
    'Optimisation pour une vitesse ludicrous',
    'change de bits... ne le dites pas aux octets...',
    'Nettoyage de la mmoire... je reviens...',
    'Assemblage des internets...',
    'Conversion de caf en code...',
    'Mise  jour de la syntaxe de la ralit...',
    'Recblage des synapses...',
    "Recherche d'un point-virgule gar...",
    'Graissage des rouages de la machine...',
    'Prchauffage des serveurs...',
    'Calibrage du condensateur de flux...',
    "Engagement de l'entranement de l'improbabilit...",
    'Canalisation de la Force...',
    'Alignement des toiles pour une rponse optimale...',
    "Qu'il en soit ainsi pour nous tous...",
    'Chargement de la prochaine grande ide...',
    'Juste un moment, je suis dans la zone...',
    'Prparation  vous blouir de brillance...',
    'Juste un instant, je peaufine mon esprit...',
    "Attendez, je cre un chef-d'uvre...",
    "Juste une seconde, je dbogue l'univers...",
    "Juste un moment, j'aligne les pixels...",
    "Juste un instant, j'optimise l'humour...",
    "Juste un moment, j'accorde les algorithmes...",
    'Vitesse warp enclenche...',
    'Extraction de plus de cristaux de Dilithium...',
    'Pas de panique...',
    'Suivre le lapin blanc...',
    'La vrit est l... quelque part...',
    'Souffler sur la cartouche...',
    'Chargement... Faites un tonneau !',
    'En attente du respawn...',
    'Finir la course de Kessel en moins de 12 parsecs...',
    "Le gteau n'est pas un mensonge, il charge juste encore...",
    "Bidouillage de l'cran de cration de personnage...",
    'Juste un moment, je cherche le bon mme...',
    "Appuyer sur 'A' pour continuer...",
    'Rassemblement de chats numriques...',
    'Polissage des pixels...',
    "Recherche d'un jeu de mots d'cran de chargement appropri...",
    'Vous distraire avec cette phrase spirituelle...',
    'Presque l... probablement...',
    "Nos hamsters travaillent aussi vite qu'ils peuvent...",
    'Donnant une tape dans le dos  Cloudy...',
    'Caressant le chat...',
    'Rickrolling mon patron...',
    'Je ne vais jamais vous abandonner, je ne vais jamais vous laisser tomber...',
    'Claquant la basse...',
    'Gotant les snozberries...',
    "Je vais jusqu'au bout, je vais  toute vitesse...",
    'Est-ce la vraie vie ? Est-ce juste une fantaisie ?...',
    "J'ai un bon pressentiment  ce sujet...",
    "Poking l'ours...",
    'Faire des recherches sur les derniers mmes...',
    'Trouver comment rendre a plus spirituel...',
    'Hmm... laissez-moi rflchir...',
    'Comment appelle-t-on un poisson sans yeux ? Un posson...',
    "Pourquoi l'ordinateur est-il all en thrapie ? Il avait trop d'octets...",
    "Pourquoi les programmeurs n'aiment pas la nature ? Elle a trop de bugs...",
    'Pourquoi les programmeurs prfrent le mode sombre ? Parce que la lumire attire les bugs...',
    "Pourquoi le dveloppeur est-il fauch ? Parce qu'il a utilis tout son cache...",
    "Que peut-on faire avec un crayon cass ? Rien, c'est inutile...",
    'Application de la maintenance percussive...',
    'Recherche de la bonne orientation USB...',
    "S'assurer que la fume magique reste  l'intrieur des cbles...",
    'Essai de quitter Vim...',
    'Mise en marche de la roue du hamster...',
    "Ce n'est pas un bug, c'est une fonctionnalit non documente...",
    'Engage.',
    'Je reviendrai... avec une rponse.',
    'Mon autre processus est un TARDIS...',
    "Communion avec l'esprit machine...",
    'Laisser les penses mariner...',
    "Je viens de me souvenir o j'ai mis mes cls...",
    "Contemplation de l'orbe...",
    "J'ai vu des choses que vous ne croiriez pas... comme un utilisateur qui lit les messages de chargement.",
    'Initiation du regard pensif...',
    "Quel est le goter prfr d'un ordinateur ? Les microchips.",
    "Pourquoi les dveloppeurs Java portent-ils des lunettes ? Parce qu'ils ne C# pas.",
    'Chargement du laser... pew pew !',
    'Division par zro... je plaisante !',
    "Recherche d'un superviseur... je veux dire, traitement.",
    'Faire du bip boop.',
    "Buffering... parce que mme les IAs ont besoin d'un moment.",
    'Enchevtrement de particules quantiques pour une rponse plus rapide...',
    'Polissage du chrome... sur les algorithmes.',
    "N'tes-vous pas diverti ? (On y travaille !)",
    'Invocation des lutins de code... pour aider, bien sr.',
    'En attente de la tonalit du modem...',
    "Recalibrage du sens de l'humour.",
    'Mon autre cran de chargement est encore plus drle.',
    "Je suis presque sr qu'il y a un chat qui marche sur le clavier quelque part...",
    'Amlioration... Amlioration... Toujours en chargement.',
    "Ce n'est pas un bug, c'est une caractristique... de cet cran de chargement.",
    "Avez-vous essay de l'teindre et de le rallumer ? (L'cran de chargement, pas moi.)",
    'Construction de pylnes supplmentaires...',
  ],

  // ============================================================================
  // Paramtres d'extension - Saisie
  // ============================================================================
  'Enter value...': 'Entrer une valeur...',
  'Enter sensitive value...': 'Entrer une valeur sensible...',
  'Press Enter to submit, Escape to cancel':
    'Appuyez sur Enter pour soumettre, Escape pour annuler',

  // ============================================================================
  // Outil de migration de commandes
  // ============================================================================
  'Markdown file already exists: {{filename}}':
    'Le fichier Markdown existe dj : {{filename}}',
  'TOML Command Format Deprecation Notice':
    "Avis d'obsolescence du format de commande TOML",
  'Found {{count}} command file(s) in TOML format:':
    'Trouv {{count}} fichier(s) de commande au format TOML :',
  'The TOML format for commands is being deprecated in favor of Markdown format.':
    "Le format TOML pour les commandes est en cours d'abandon au profit du format Markdown.",
  'Markdown format is more readable and easier to edit.':
    'Le format Markdown est plus lisible et plus facile  modifier.',
  'You can migrate these files automatically using:':
    'Vous pouvez migrer ces fichiers automatiquement en utilisant :',
  'Or manually convert each file:':
    'Ou convertir chaque fichier manuellement :',
  'TOML: prompt = "..." / description = "..."':
    'TOML : prompt = "..." / description = "..."',
  'Markdown: YAML frontmatter + content':
    'Markdown : YAML frontmatter + contenu',
  'The migration tool will:': "L'outil de migration va :",
  'Convert TOML files to Markdown': 'Convertir les fichiers TOML en Markdown',
  'Create backups of original files':
    'Crer des sauvegardes des fichiers originaux',
  'Preserve all command functionality':
    'Prserver toutes les fonctionnalits des commandes',
  'TOML format will continue to work for now, but migration is recommended.':
    "Le format TOML continuera  fonctionner pour l'instant, mais la migration est recommande.",

  // ============================================================================
  // Extensions - Commande Explore
  // ============================================================================
  'Open extensions page in your browser':
    'Ouvrir la page des extensions dans votre navigateur',
  'Unknown extensions source: {{source}}.':
    "Source d'extensions inconnue : {{source}}.",
  'Would open extensions page in your browser: {{url}} (skipped in test environment)':
    'Ouvrirait la page des extensions dans votre navigateur : {{url}} (ignor en environnement de test)',
  'View available extensions at {{url}}':
    'Voir les extensions disponibles sur {{url}}',
  'Opening extensions page in your browser: {{url}}':
    'Ouverture de la page des extensions dans votre navigateur : {{url}}',
  'Failed to open browser. Check out the extensions gallery at {{url}}':
    "chec de l'ouverture du navigateur. Consultez la galerie d'extensions sur {{url}}",
  'Retrying in {{seconds}} seconds... (attempt {{attempt}}/{{maxRetries}})':
    'Nouvelle tentative dans {{seconds}} secondes... (tentative {{attempt}}/{{maxRetries}})',
  'Press Ctrl+Y to retry': 'Appuyez sur Ctrl+Y pour ressayer',
  'No failed request to retry.': 'Aucune requte choue  ressayer.',
  'to retry last request': 'pour ressayer la dernire requte',

  // ============================================================================
  // Authentification du plan de codage
  // ============================================================================
  'API key cannot be empty.': "L'API Key ne peut pas tre vide.",
  'You can get your Coding Plan API key here':
    'Vous pouvez obtenir votre Coding Plan API Key ici',
  'Failed to update Coding Plan configuration: {{message}}':
    'chec de la mise  jour de la configuration Coding Plan : {{message}}',

  // ============================================================================
  // Configuration de cl API personnalise
  // ============================================================================
  'You can configure your API key and models in settings.json':
    'Vous pouvez configurer votre API Key et vos modles dans settings.json',
  'Refer to the documentation for setup instructions':
    'Consultez la documentation pour les instructions de configuration',

  // ============================================================================
  // Bote de dialogue Auth - Titres et tiquettes
  // ============================================================================
  'Coding Plan': 'Coding Plan',
  Custom: 'Personnalis',
  'Select Region for Coding Plan': 'Slectionner la rgion pour Coding Plan',
  'Choose based on where your account is registered':
    "Choisissez en fonction de l'endroit o votre compte est enregistr",
  'Enter Coding Plan API Key': 'Entrer la Coding Plan API Key',

  // ============================================================================
  // Mises  jour internationales Coding Plan
  // ============================================================================
  'New model configurations are available for {{region}}. Update now?':
    'De nouvelles configurations de modle sont disponibles pour {{region}}. Mettre  jour maintenant ?',
  '{{region}} configuration updated successfully. Model switched to "{{model}}".':
    'Configuration {{region}} mise  jour avec succs. Modle chang en "{{model}}".',
  // ============================================================================
  // Composant d'utilisation du contexte
  // ============================================================================
  'Context Usage': 'Utilisation du contexte',
  'No API response yet. Send a message to see actual usage.':
    "Pas encore de rponse API. Envoyez un message pour voir l'utilisation relle.",
  'Estimated pre-conversation overhead':
    'Surcharge estime avant la conversation',
  'Context window': 'Fentre de contexte',
  Used: 'Utilis',
  Free: 'Libre',
  'Autocompact buffer': 'Tampon de compaction automatique',
  'Usage by category': 'Utilisation par catgorie',
  'System prompt': 'Invite systme',
  'Built-in tools': 'Outils intgrs',
  'MCP tools': 'MCP tools',
  'Memory files': 'Fichiers mmoire',
  Skills: 'Comptences',
  Messages: 'Messages',
  'Run /context detail for per-item breakdown.':
    'Excutez /context detail pour une rpartition par lment.',
  'body loaded': 'corps charg',
  memory: 'mmoire',
  '{{region}} configuration updated successfully.':
    'Configuration {{region}} mise  jour avec succs.',
  'Authenticated successfully with {{region}}. API key and model configs saved to settings.json.':
    'Authentification russie avec {{region}}. API Key et configurations de modle enregistres dans settings.json.',
  'Tip: Use /model to switch between available Coding Plan models.':
    'Conseil : Utilisez /model pour basculer entre les modles Coding Plan disponibles.',
  'Type something...': 'Tapez quelque chose...',
  Submit: 'Soumettre',
  'Submit answers': 'Soumettre les rponses',
  Cancel: 'Annuler',
  'Your answers:': 'Vos rponses :',
  '(not answered)': '(sans rponse)',
  'Ready to submit your answers?': 'Prt  soumettre vos rponses ?',
  '/: Navigate | <-/->: Switch tabs | Enter: Select':
    "/ : Naviguer | <-/-> : Changer d'onglet | Enter : Slectionner",
  '/: Navigate | Enter: Select | Esc: Cancel':
    '/ : Naviguer | Enter : Slectionner | Esc : Annuler',
  'Authenticate using Qwen OAuth': 'Authentifier avec Qwen OAuth',
  'Authenticate using Alibaba Cloud Coding Plan':
    'Authentifier avec Alibaba Cloud Coding Plan',
  'Region for Coding Plan (china/global)':
    'Rgion pour Coding Plan (china/global)',
  'API key for Coding Plan': 'API Key pour Coding Plan',
  'Show current authentication status':
    "Afficher le statut d'authentification actuel",
  'Authentication completed successfully.':
    'Authentification termine avec succs.',
  'Starting Qwen OAuth authentication...':
    "Dmarrage de l'authentification Qwen OAuth...",
  'Successfully authenticated with Qwen OAuth.':
    'Authentification russie avec Qwen OAuth.',
  'Failed to authenticate with Qwen OAuth: {{error}}':
    "chec de l'authentification avec Qwen OAuth : {{error}}",
  'Processing Alibaba Cloud Coding Plan authentication...':
    "Traitement de l'authentification Alibaba Cloud Coding Plan...",
  'Successfully authenticated with Alibaba Cloud Coding Plan.':
    'Authentification russie avec Alibaba Cloud Coding Plan.',
  'Failed to authenticate with Coding Plan: {{error}}':
    "chec de l'authentification avec Coding Plan : {{error}}",
  ' (aliyun.com)': ' (aliyun.com)',
  Global: 'Global',
  'Alibaba Cloud (alibabacloud.com)': 'Alibaba Cloud (alibabacloud.com)',
  'Select region for Coding Plan:': 'Slectionner la rgion pour Coding Plan :',
  'Enter your Coding Plan API key: ': 'Entrez votre Coding Plan API Key : ',
  'Select authentication method:':
    "Slectionner la mthode d'authentification :",
  '\n=== Authentication Status ===\n': "\n=== Statut d'authentification ===\n",
  '  No authentication method configured.\n':
    "  Aucune mthode d'authentification configure.\n",
  'Run one of the following commands to get started:\n':
    "Excutez l'une des commandes suivantes pour commencer :\n",
  '  qwen auth qwen-oauth     - Authenticate with Qwen OAuth (discontinued)':
    '  qwen auth qwen-oauth     - Authentification avec Qwen OAuth (abandonn)',
  'Or simply run:': 'Ou simplement excutez :',
  '  qwen auth                - Interactive authentication setup\n':
    "  qwen auth                - Configuration d'authentification interactive\n",
  ' Authentication Method: Qwen OAuth':
    " Mthode d'authentification : Qwen OAuth",
  '  Type: Free tier (discontinued 2026-04-15)':
    '  Type : Niveau gratuit (abandonn 2026-04-15)',
  '  Limit: No longer available': '  Limite : Plus disponible',
  'Qwen OAuth free tier was discontinued on 2026-04-15. Run /auth to switch to Coding Plan, OpenRouter, Fireworks AI, or another provider.':
    'Le niveau gratuit Qwen OAuth a t abandonn le 2026-04-15. Excutez /auth pour passer  Coding Plan, OpenRouter, Fireworks AI ou un autre fournisseur.',
  ' Authentication Method: Alibaba Cloud Coding Plan':
    " Mthode d'authentification : Alibaba Cloud Coding Plan",
  ' (China) - ': ' (Chine) - ',
  'Global - Alibaba Cloud': 'Global - Alibaba Cloud',
  '  Region: {{region}}': '  Rgion : {{region}}',
  '  Current Model: {{model}}': '  Modle actuel : {{model}}',
  '  Config Version: {{version}}': '  Version de config : {{version}}',
  '  Status: API key configured\n': '  Statut : API Key configure\n',
  '  Authentication Method: Alibaba Cloud Coding Plan (Incomplete)':
    "  Mthode d'authentification : Alibaba Cloud Coding Plan (Incomplte)",
  '  Issue: API key not found in environment or settings\n':
    "  Problme : API Key introuvable dans l'environnement ou les paramtres\n",
  '  Run `qwen auth coding-plan` to re-configure.\n':
    '  Excutez `qwen auth coding-plan` pour reconfigurer.\n',
  ' Authentication Method: {{type}}':
    " Mthode d'authentification : {{type}}",
  '  Status: Configured\n': '  Statut : Configur\n',
  'Failed to check authentication status: {{error}}':
    "chec de la vrification du statut d'authentification : {{error}}",
  'Select an option:': 'Slectionner une option :',
  'Raw mode not available. Please run in an interactive terminal.':
    'Mode brut non disponible. Veuillez excuter dans un terminal interactif.',
  '(Use   arrows to navigate, Enter to select, Ctrl+C to exit)\n':
    '(Utilisez les flches   pour naviguer, Enter pour slectionner, Ctrl+C pour quitter)\n',
  'Hide tool output and thinking for a cleaner view (toggle with Ctrl+O).':
    'Masquer la sortie des outils et la rflexion pour une vue plus nette (basculer avec Ctrl+O).',
  'Press Ctrl+O to show full tool output':
    'Appuyez sur Ctrl+O pour afficher la sortie complte des outils',
  'Switch to plan mode or exit plan mode':
    'Passer en mode plan ou quitter le mode plan',
  'Exited plan mode. Previous approval mode restored.':
    "Mode plan quitt. Mode d'approbation prcdent restaur.",
  'Enabled plan mode. The agent will analyze and plan without executing tools.':
    "Mode plan activ. L'agent analysera et planifiera sans excuter d'outils.",
  'Already in plan mode. Use "/plan exit" to exit plan mode.':
    'Dj en mode plan. Utilisez "/plan exit" pour quitter le mode plan.',
  'Not in plan mode. Use "/plan" to enter plan mode first.':
    'Pas en mode plan. Utilisez "/plan" pour entrer en mode plan d\'abord.',
  "Set up Qwen Code's status line UI":
    "Configurer l'interface de la barre de statut de Qwen Code",
  'Press  to edit queued messages':
    'Appuyez sur  pour modifier les messages en file d'attente',
  'Add a QWEN.md file to give Qwen Code persistent project context.':
    'Ajoutez un fichier QWEN.md pour donner  Qwen Code un contexte de projet persistant.',
  'Use /btw to ask a quick side question without disrupting the conversation.':
    'Utilisez /btw pour poser une question secondaire rapide sans perturber la conversation.',
  'Context is almost full! Run /compress now or start /new to continue.':
    'Le contexte est presque plein ! Lancez /compress maintenant ou dmarrez /new pour continuer.',
  'Context is getting full. Use /compress to free up space.':
    'Le contexte se remplit. Utilisez /compress pour librer de l'espace.',
  'Long conversation? /compress summarizes history to free context.':
    'Conversation longue ? /compress rsume l'historique pour librer du contexte.',
  'Manage extension settings': 'Grer les paramtres de l'extension',
  'Ask a quick side question without affecting the main conversation':
    'Poser rapidement une question annexe sans affecter la conversation principale',
  'Manage Arena sessions': 'Grer les sessions Arena',
  'Start an Arena session with multiple models competing on the same task':
    "Dmarrer une session Arena o plusieurs modles s'affrontent sur la mme tche",
  'Stop the current Arena session': 'Arrter la session Arena en cours',
  'Show the current Arena session status':
    "Afficher l'tat de la session Arena en cours",
  'Select a model result and merge its diff into the current workspace':
    "Slectionner un rsultat de modle et fusionner son diff dans l'espace de travail actuel",
  'No running Arena session found.': 'Aucune session Arena en cours trouve.',
  'No Arena session found. Start one with /arena start.':
    'Aucune session Arena trouve. Lancez-en une avec /arena start.',
  'Arena session is still running. Wait for it to complete or use /arena stop first.':
    "La session Arena est encore en cours. Attendez qu'elle se termine ou utilisez d'abord /arena stop.",
  'No successful agent results to select from. All agents failed or were cancelled.':
    "Aucun rsultat d'agent russi  slectionner. Tous les agents ont chou ou ont t annuls.",
  'Use /arena stop to end the session.':
    'Utilisez /arena stop pour terminer la session.',
  'No idle agent found matching "{{name}}".':
    'Aucun agent inactif trouv correspondant  "{{name}}".',
  'Failed to apply changes from {{label}}: {{error}}':
    "chec de l'application des modifications de {{label}}: {{error}}",
  'Applied changes from {{label}} to workspace. Arena session complete.':
    "Modifications de {{label}} appliques  l'espace de travail. Session Arena termine.",
  'Discard all Arena results and clean up worktrees?':
    'Supprimer tous les rsultats Arena et nettoyer les arbres de travail?',
  'Arena results discarded. All worktrees cleaned up.':
    'Rsultats Arena supprims. Tous les arbres de travail ont t nettoys.',
  'Arena is not supported in non-interactive mode. Use interactive mode to start an Arena session.':
    "Arena n'est pas pris en charge en mode non interactif. Utilisez le mode interactif pour dmarrer une session Arena.",
  'Arena is not supported in non-interactive mode. Use interactive mode to stop an Arena session.':
    "Arena n'est pas pris en charge en mode non interactif. Utilisez le mode interactif pour arrter une session Arena.",
  'Arena is not supported in non-interactive mode.':
    "Arena n'est pas pris en charge en mode non interactif.",
  'An Arena session exists. Use /arena stop or /arena select to end it before starting a new one.':
    "Une session Arena existe. Utilisez /arena stop ou /arena select pour la terminer avant d'en dmarrer une nouvelle.",
  'Usage: /arena start --models model1,model2 <task>':
    'Utilisation: /arena start --models model1,model2 <tche>',
  'Models to compete (required, at least 2)':
    'Modles en comptition (obligatoire, au moins 2)',
  'Format: authType:modelId or just modelId':
    'Format: authType:modelId ou simplement modelId',
  'Arena requires at least 2 models. Use --models model1,model2 to specify.':
    'Arena ncessite au moins 2 modles. Utilisez --models model1,model2 pour les spcifier.',
  'Arena started with {{count}} agents on task: "{{task}}"\nModels:\n{{modelList}}':
    'Arena dmarre avec {{count}} agents sur la tche: "{{task}}"\nModles:\n{{modelList}}',
  'Arena panes are running in tmux. Attach with: `{{command}}`':
    "Les panneaux Arena sont en cours d'excution dans tmux. Attachez avec: `{{command}}`",
  '[{{label}}] failed: {{error}}': '[{{label}}] a chou: {{error}}',
  'Loading suggestions...': 'Chargement des suggestions...',
  'Open the memory manager.': 'Ouvrir le gestionnaire de mmoire.',
  'Save a durable memory to the memory system.':
    'Enregistrer une mmoire durable dans le systme de mmoire.',
  'Show context window usage breakdown. Use "/context detail" for per-item breakdown.':
    'Afficher le dtail de l'utilisation de la fentre de contexte. Utilisez "/context detail" pour le dtail par lment.',
  'Show per-item context usage breakdown.':
    'Afficher le dtail de l'utilisation du contexte par lment.',

  // === Missing key backfill ===
  'to toggle compact mode': 'basculer le mode compact',
  'The name of the extension to update.':
    "Le nom de l'extension  mettre  jour.",
  'Session (temporary)': 'Session (temporaire)',
  'Open auto-memory folder': 'Ouvrir le dossier de mmoire automatique',
  'Auto-memory: {{status}}': 'Mmoire automatique : {{status}}',
  'Auto-dream: {{status}}  {{lastDream}}  /dream to run':
    'Rve automatique : {{status}}  {{lastDream}}  /dream pour lancer',
  never: 'jamais',
  on: 'activ',
  off: 'dsactiv',
  'Remove matching entries from managed auto-memory.':
    'Supprimer les entres correspondantes de la mmoire automatique gre.',
  'Usage: /forget <memory text to remove>':
    'Utilisation : /forget <texte de mmoire  supprimer>',
  'No managed auto-memory entries matched: {{query}}':
    'Aucune entre de mmoire automatique gre ne correspond  : {{query}}',
  'Consolidate managed auto-memory topic files.':
    'Consolider les fichiers de sujets de mmoire automatique gre.',
  'Press c to copy the authorization URL to your clipboard.':
    "Appuyez sur c pour copier l'URL d'autorisation dans le presse-papiers.",
  'Copy request sent to your terminal. If paste is empty, copy the URL above manually.':
    "Demande de copie envoye au terminal. Si le collage est vide, copiez manuellement l'URL ci-dessus.",
  'Cannot write to terminal -- copy the URL above manually.':
    "Impossible d'crire dans le terminal -- copiez manuellement l'URL ci-dessus.",
  'Press Ctrl+O to toggle compact mode -- hide tool output and thinking for a cleaner view.':
    'Appuyez sur Ctrl+O pour basculer le mode compact -- masquer la sortie des outils et la rflexion pour une vue plus nette.',
  'Invalid API key. Coding Plan API keys start with "sk-sp-". Please check.':
    'API Key invalide. Les Coding Plan API Keys commencent par "sk-sp-". Veuillez vrifier.',
  'Lock release warning': 'Avertissement de libration du verrou',
  'Metadata write warning': "Avertissement d'criture des mtadonnes",
  "Subsequent dreams may be skipped as locked until the next session's staleness sweep cleans the file.":
    "Les dreams suivants peuvent tre ignors comme verrouills jusqu' ce que le prochain nettoyage des sessions obsoltes supprime le fichier.",
  "The scheduler gate did not see this dream's timestamp; the next dream cycle may re-fire sooner than usual.":
    "La porte du planificateur n'a pas vu l'horodatage de ce dream ; le prochain cycle de dream peut se relancer plus tt que d'habitude.",
  '% used': '% utilis',
  '% context used': '% de contexte utilis',
  'Context exceeds limit! Use /compress or /clear to reduce.':
    'Le contexte dpasse la limite ! Utilisez /compress ou /clear pour le rduire.',
  // === Same-as-English optimization ===
  Auth: 'Authentification',
  Auto: 'Automatique',
  Tokens: 'Jetons',
  tokens: 'jetons',
  ' (China)': 'Chine',
};
