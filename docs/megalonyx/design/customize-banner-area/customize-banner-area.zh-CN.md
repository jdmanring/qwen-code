# Banner 

>  QWEN ASCII Logo Banner ----
> 
> 

## 

Qwen Code CLI  Banner QWEN ASCII
Logo :

- ** / **: Qwen Code 
   "Qwen Code"
- ****: Banner 
- ** / **:
  

:****
****
 / 

 issue:[#3005](https://github.com/QwenLM/qwen-code/issues/3005)

## Banner 

 Banner  `Header` `AppHeader` :

```
  marginX=2                                                           marginX=2
  |                                                                          |
                                                                            
+-------------------------------------------------------------------------------+--
|                                                                             |
|   +------ Logo  ---------+--  gap=2  +------  () --------------+--  |
|   |                      |         |                                     |  |
|   |   QWEN ASCII   |         |   :    >_ Qwen Code (vX.Y.Z)  |  |
|   |     ART ART    |         |   :   /  |  |
|   |   QWEN ASCII   |         |   :    Qwen OAuth | qwen-...    |  |
|   |                      |         |   :    ~/projects/example     |  |
|   \_-------- A --------------         \_---------------- B ---------------------  |
|                                                                             |
\_--------------------------------------------------------------------------------
                              :AppHeader
                          | Tips  ui.hideTips  |
```

:

- **A. Logo ** ----  ASCII art
  :`packages/cli/src/ui/components/AsciiArt.ts` 
  `shortAsciiLogo`
- **B. ** ---- 
  spacer:
  - **B** :`>_ Qwen Code (vX.Y.Z)` ----  + 
  - **B**  / spacer: `ui.customBannerSubtitle`
     fork 
    `Built-in DataWorks Official Skills`
  - **B** :`<> | <> ( /model )`
  - **B** : tildeify 

 `<AppHeader>`  `showBanner = !config.getScreenReader()`
 Banner 

##  ---- 

|                                |                              |               | /                                                                                                                                            |
| ---------------------------------- | ------------------------------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A. Logo **                     | `shortAsciiLogo` (`AsciiArt.ts`)     | ** + ** |  Logo                                                                      |
| **B. **`>_ Qwen Code` | `Header.tsx`                   | ****              |  `>_`  `customBannerTitle`                                                           |
| **B. **`(vX.Y.Z)`   | `version` prop                       | ****                |  `--version`                     |
| **B.  / spacer **         |                              | ****              |  /  fork  tag "Built-in DataWorks Official Skills" |
| **B. ** +       | `formattedAuthType``model` prop    | ****                |  token / footgun                             |
| **B. **         | `workingDirectory` prop              | ****                | Banner                                                                                     |
| ** Banner** (A + B)            | `AppHeader.tsx`  `<Header>`  | ****              |  `ui.hideBanner: true`  AB  ---- `<Tips>`  `ui.hideTips`                                 |

:

|                       |   |                                                                                                  |      |
| ------------------------- | ------- | ---------------------------------------------------------------------------------------------------- | ------------ |
| `ui.hideBanner`           | `false` |  Banner A + B                                                                      | A + B        |
| `ui.customBannerTitle`    |   |  B  trim =                              | B   |
| `ui.customBannerSubtitle` |   |  B  spacer 160  =  spacer | B spacer  |
| `ui.customAsciiArt`       |   |  A                                       | A            |

****:

- 
- /
- 
-  Logo  theme 
- 




##  ---- 

### 

 banner  art 


|                          |                                                                                                            |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| ****               | **80 ** `[BANNER]` warn                |
| ****             | **160 ** `[BANNER]` warn                           |
| **ASCII art **         | ** 200  * 200 ** `[BANNER]` warn                                                   |
| **ASCII art **       | **64 KB **                                                 |
| **ASCII art ** | ****Logo ----  |

ASCII art **** ---- /
 17 


### 

 `settings.json`  `ui` 
`~/.qwen/settings.json`
`.qwen/settings.json`workspace 
usersystem  workspace

`customAsciiArt` :
scope  tier  scope user 
 `{ small }`workspace  `{ large }` ----
`small`  user`large`  workspace:

1.  `{ path }` workspace `.qwen/`
   vs. user `~/.qwen/` merged  scope 
2.  `large` tier 
   `small`

 tier  scope system >
workspace > user scope  `customAsciiArt` 
 `{ path }`  scope  tier

###  Banner

```jsonc
{
  "ui": {
    "hideBanner": true,
  },
}
```

 Logo  `ui.hideTips`
Tips 

### 

```jsonc
{
  "ui": {
    "customBannerTitle": "Acme CLI",
  },
}
```

 `Acme CLI (vX.Y.Z)`
`>_` :
`"customBannerTitle": ">_ Acme CLI"`

### 

```jsonc
{
  "ui": {
    "customBannerSubtitle": "Built-in DataWorks Official Skills",
  },
}
```

**** spacer 
 / :

```
+-----------------------------------------------------------+--
| DataWorks DataAgent (vX.Y.Z)                            |  <- B 
| Built-in DataWorks Official Skills                      |  <- B 
| Qwen OAuth | qwen-coder ( /model )                  |  <- B 
| ~/projects/example                                      |  <- B 
\_------------------------------------------------------------
```

:

-  / 
  
-  160  ----  / "powered by" 
  
-  / =  spacer  ----
  
- 
  

###  ASCII art ---- 

```jsonc
{
  "ui": {
    "customAsciiArt": "  ___  _    _  ____ \n / _ \\| |  / |/ _\\\n| |_| | |__| | __/\n \\___/|____|_|___|",
  },
}
```

JSON  `\n`  ASCII art  Logo 


> ** ASCII art** 
>  `figlet`:
> `npx figlet -f "ANSI Shadow" "xxxCode" > brand.txt`
> `customAsciiArt: { "path": "./brand.txt" }` CLI ****
>  ASCII art ---- 

###  ASCII art ---- 

```jsonc
{
  "ui": {
    "customAsciiArt": { "path": "./brand.txt" },
  },
}
```

 JSON :

- ****: workspace  `.qwen/` 
- ****: `~/.qwen/`
- 
- ****
   ----  CLI

###  ASCII art ---- 

```jsonc
{
  "ui": {
    "customAsciiArt": {
      "small": "  ACME\n  ----",
      "large": { "path": "./brand-wide.txt" },
    },
  },
}
```

 `large` `small` Logo 
`small`  `large` 
 `{ path }`:

### Logo ---- 

 art ""****
:

|                                  |                                             |
| ---------------------------------- | ----------------------------------------------- |
|                      |                       |
|                          | 4  2 +  2                           |
| Logo         | 2                                           |
|                    | 44 40  +  +               |
| ** art **    | `  4  2  44 =   50`       |
|  art             | 200  * 200  `[BANNER]` warn |
| `customBannerTitle`  | 80  `[BANNER]` warn         |

 logo :

|  |  logo  |                                           |
| -------- | -------------------- | ------------------------------------------------------- |
| 80       | 30                   |  figlet "ANSI Shadow"  7-11  3  |
| 100      | 50                   | ANSI Shadow  6      |
| 120      | 70                   |  art                              |
| 200      | 150                  |  ANSI Shadow      |

 art :

1. ** ANSI Shadow **
   ANSI Shadow  7-9  `Custom Agent`  12 
    95  art ---- 100 
    figlet 
    ` Custom Agent `
2. **"""" `{ small, large }`
   ** `large`  >= 104 
    art`small`  16 
   logo 

```jsonc
{
  "ui": {
    "customBannerTitle": "Custom Agent",
    "customAsciiArt": {
      "small": " Custom Agent ",
      "large": { "path": "./banner-large.txt" },
    },
  },
}
```

`banner-large.txt`  ANSI Shadow  54  * 12 
:

```bash
( npx figlet -f "ANSI Shadow" CUSTOM
  npx figlet -f "ANSI Shadow" AGENT ) > banner-large.txt
```

### 

```jsonc
{
  "ui": {
    "hideBanner": false,
    "customBannerTitle": "Acme CLI",
    "customAsciiArt": {
      "small": "  ACME\n  ----",
      "large": { "path": "./brand-wide.txt" },
    },
  },
}
```

### 

1.  `settings.json` `qwen` ---- Banner 
   
2.  `small` / `large` 
    Logo 
3. 
   `~/.qwen/debug/<sessionId>.txt``latest.txt` 
   grep `[BANNER]` ----  warn
   

## 

```
   settings.json                              packages/cli/src/ui/components/
   -------------                              ------------------------------
   {                                          AppHeader.tsx
     "ui": {                                    |
       "hideBanner": false,                     |  showBanner =
       "customBannerTitle": "Acme",             |      !screenReader
       "customBannerSubtitle": "Built-in ...",    |   && !ui.hideBanner
       "customAsciiArt": ...                      |
     }                                          |
   }                                            
        |                              <Header
                                        customAsciiArt={resolved.asciiArt}
   loadSettings()                        customBannerTitle={resolved.title}
   merge user / workspace                customBannerSubtitle={resolved.subtitle}
        |                                version=... model=... authType=...
                                        workingDirectory=... />
   resolveCustomBanner(settings)                  |
   +---------------------------+--                    
   | 1.               |         packages/cli/src/ui/components/
   |    { small, large }     |         Header.tsx
   | 2. :          |           |
   |    string ->      |           |   availableTerminalWidth
   |    {path} -> fs.read     |           |  
   |      O_NOFOLLOW         |           
   |      <= 64 KB            |          Logo 
   | 3.  art:            |         :
   |    stripControlSeqs     |           Title    = customBannerTitle
   |    <= 200  * 200     |                   ?? '>_ Qwen Code'
   | 4.  title +          |           Subtitle = customBannerSubtitle
   |    subtitle      |                   ??  spacer 
   |    <= 80 / 160      |           Status   = 
   | 5.  memoize        |           Path     = 
   \_----------------------------
```


:

1. **** `string`  `{ path }` 
   `{ small: x, large: x }``{ small, large }` 
2. **** `AsciiArtSource`:
   - :
   - `{ path }`: `O_NOFOLLOW` 
     Windows  ---- 
      64 KB**:workspace
      workspace `.qwen/`user  `~/.qwen/`
      -> `[BANNER]` warn
3. ****Banner  stripper: OSC / CSI / SS2 / SS3 
    C0 / C1  DEL
   `\n`  ASCII art  trim  200 
   * 200  `[BANNER]` warn
4. **** `Header.tsx`  `small` 
   `large`
   `availableTerminalWidth >= logoWidth + logoGap + minInfoPanelWidth`:
   -  `large`  `large`
   -  `small`  `small`
   - ** custom art** Logo 
      `showLogo = false` ----  QWEN logo 
     
   -  custom art `shortAsciiLogo`
      logo 
5. ****
    `shortAsciiLogo`
   logo CLI **** Banner 

:

```ts
function pickTier(
  small: string | undefined,
  large: string | undefined,
  availableWidth: number,
  logoGap: number,
  minInfoPanelWidth: number,
): string | undefined {
  for (const candidate of [large, small]) {
    if (!candidate) continue;
    const w = getAsciiArtWidth(candidate);
    if (availableWidth >= w + logoGap + minInfoPanelWidth) {
      return candidate;
    }
  }
  return undefined; //  Logo 
}
```

## Settings schema 

 `packages/cli/src/config/settingsSchema.ts`  `ui` 
 `shellOutputMaxLines` :

```ts
hideBanner: {
  type: 'boolean',
  label: 'Hide Banner',
  category: 'UI',
  requiresRestart: false,
  default: false,
  description: 'Hide the startup ASCII banner and info panel.',
  showInDialog: true,
},
customBannerTitle: {
  type: 'string',
  label: 'Custom Banner Title',
  category: 'UI',
  requiresRestart: false,
  default: '' as string,
  description:
    'Replace the default ">_ Qwen Code" title shown in the banner info panel. The version suffix is always appended.',
  showInDialog: false,
},
customBannerSubtitle: {
  type: 'string',
  label: 'Custom Banner Subtitle',
  category: 'UI',
  requiresRestart: false,
  default: '' as string,
  description:
    'Optional subtitle line rendered between the banner title and the auth/model line. When unset, the info panel keeps its blank spacer row.',
  showInDialog: false,
},
customAsciiArt: {
  type: 'object',
  label: 'Custom ASCII Art',
  category: 'UI',
  requiresRestart: false,
  default: undefined,
  description:
    'Replace the default QWEN ASCII art. Accepts an inline string, {"path": "..."}, or {"small": ..., "large": ...} for width-aware selection.',
  showInDialog: false,
  //  SettingDefinition `type` 
  // override  JSON-schema  VS Code 
  // string{path}{small,large}
  // 
  jsonSchemaOverride: { /* string | {path} | {small,large} oneOf ... */ },
},
```

`hideBanner`  `hideTips` `showInDialog: true`
art ----
 TUI  ASCII 
`settings.json` 

## 

 `main` 

`packages/cli/src/ui/components/AppHeader.tsx:53` ---- 
`showBanner`:

```ts
const showBanner = !config.getScreenReader() && !settings.merged.ui?.hideBanner;
```

`packages/cli/src/ui/components/AppHeader.tsx` ---- 
Banner  `<Header>`:

```tsx
<Header
  version={version}
  authDisplayType={authDisplayType}
  model={model}
  workingDirectory={targetDir}
  customAsciiArt={resolvedBanner?.asciiArt /* { small?, large? } */}
  customBannerTitle={resolvedBanner?.title /* string | undefined */}
  customBannerSubtitle={resolvedBanner?.subtitle /* string | undefined */}
/>
```

`packages/cli/src/ui/components/Header.tsx` ----  `HeaderProps`:

```ts
interface HeaderProps {
  customAsciiArt?: { small?: string; large?: string };
  customBannerTitle?: string;
  customBannerSubtitle?: string;
  version: string;
  authDisplayType?: AuthDisplayType;
  model: string;
  workingDirectory: string;
}
```

`packages/cli/src/ui/components/Header.tsx:45-46` ---- 
`logoWidth` :

```ts
const tier = pickTier(
  customAsciiArt?.small,
  customAsciiArt?.large,
  availableTerminalWidth,
  logoGap,
  minInfoPanelWidth,
);
const displayLogo = tier ?? shortAsciiLogo;
```

`packages/cli/src/ui/components/Header.tsx` ----  prop 
 prop  spacer :

```tsx
<Text bold color={theme.text.accent}>
  {customBannerTitle ? customBannerTitle : '>_ Qwen Code'}
</Text>
...
{customBannerSubtitle ? (
  <Text color={theme.text.secondary}>{customBannerSubtitle}</Text>
) : (
  <Text> </Text>
)}
```

****:`packages/cli/src/ui/utils/customBanner.ts` ---- 
:

```ts
export interface ResolvedBanner {
  asciiArt: { small?: string; large?: string };
  title?: string;
  subtitle?: string;
}

export function resolveCustomBanner(settings: LoadedSettings): ResolvedBanner;
```


 CLI  scope 
 `settings.system.path` / `settings.workspace.path` /
`settings.user.path` `{ path }` 
 `settings.isTrusted`  false  workspace scope

## 

 5 


###  1 ----  issue 

```jsonc
{
  "ui": {
    "customAsciiArt": "...", // string | {path} | {small,large}
    "customBannerTitle": "Acme CLI",
    "hideBanner": false,
  },
}
```

- ****: issue 
- ****: `ui.*` 
  `hideTips``customWittyPhrases` 
- ****: `ui`  banner
   `ui` 
  

###  2 ----  `ui.banner` 

```jsonc
{
  "ui": {
    "banner": {
      "hide": false,
      "title": "Acme CLI",
      "asciiArt": { "path": "./brand.txt" },
    },
  },
}
```

- ****: 1
- ****: banner `/settings`
  
- ****: issue  UI 
   `ui.accessibility`  `ui.statusLine` 
  

###  3 ---- Banner profile  + slot override

```jsonc
{
  "ui": {
    "bannerProfile": "minimal" | "default" | "branded" | "hidden",
    "banner": { /* 'branded'  slot  */ }
  }
}
```

- ****: slot
- ****:onboarding  CLI 
- ****:issue 
  

###  4 ----  Banner 

```jsonc
{
  "ui": {
    "bannerTemplate": "{{logo}}\n>_ {{title}} ({{version}})\n{{auth}} | {{model}}\n{{path}}",
  },
}
```

- ****: freeform 
- ****:
- ****:Ink 
  

###  5 ----  /  API

 banner-renderer 

- ****:
- ****:
- ****:API  issue
  

### 

** 1** issue `ui.*` 
 banner 
 2  ---- `ui.banner.title` 
`ui.customBannerTitle` 

## 

 Banner **** path 
**** settings 
Session-title 

|                                                 |                                                                                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ASCII art /  /  ANSI / OSC-8 / CSI  | Banner  stripper`sanitizeArt` / `sanitizeSingleLine`: OSC / CSI / SS2 / SS3  C0 / C1  DEL |
|                                       |  64 KB                                                                                                                                                   |
|  ASCII art                                |  200  * 200  + `[BANNER]` warn                                                                                                           |
|  path                                     |  `O_NOFOLLOW`Windows                                                                                                           |
|                                       |  -> `[BANNER]` warn ->  UI                                                                                                                         |
|  /                            |  80/ 160                                                                                                                   |
|                         | `settings.isTrusted`  false  `settings.workspace` `settings.merged`                                                        |
|                                         | path  memoizereload                                                                      |

: `shortAsciiLogo`
+  warn


## 



|                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  ASCII art`{ text: "xxxCode" }`     | v1 **** `figlet`  2-3 MB unpacked vendor ~200  +  `.flf` : license  X  issueCJK /  /  ASCII art figlet  `npx figlet "xxxCode" > brand.txt` + `customAsciiArt: { "path": "./brand.txt" }` ----  Qwen Code : `AsciiArtSource`  `string \| {path} \| {text, font?}` |
| `/banner` slash                       |  UI  ASCII                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|  /                            |  theme Banner                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| URL  ASCII art                                | :`{path}`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|  Logo                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| VSCode / Web UI banner                        |  Ink Banner                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|  reload                             |  reload  art                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| version / auth / model / path |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

## 

 PR :

1. `~/.qwen/settings.json`  `customBannerTitle: "Acme CLI"`
    `customAsciiArt` -> `qwen` 
   ASCII art
2.  `customBannerSubtitle: "Built-in Acme Skills"` -> 
    / 
    spacer 
3.  `hideBanner: true` -> `qwen`  BannerTips 
   
4. workspace `settings.json` 
   `customAsciiArt: { "path": "./brand.txt" }``brand.txt` 
    `.qwen/`  -> 
5. `customAsciiArt: { "small": "...", "large": "..." }` ->
    /  /  large
   small Logo 
6. `customBannerTitle` **** `customBannerSubtitle` 
    `\x1b[31mhostile` -> 
   
7. `path`  -> CLI 
   `~/.qwen/debug/<sessionId>.txt`  `[BANNER]` warn
    art
8.  worktree -> workspace 
   `customAsciiArt` `{ path }` user scope
   
