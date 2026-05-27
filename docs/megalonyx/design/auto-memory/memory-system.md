# Memory 

>  Qwen Code  **Managed Auto-Memory**

---

## 

1. [](#)
2. [](#)
3. [](#)
4. [](#)
5. [](#)
6. [Extract -- ](#extract--)
7. [Dream -- ](#dream--)
8. [Recall -- ](#recall--)
9. [Forget -- ](#forget--)
10. [](#)
11. [](#)

---

## 

Managed Auto-Memory  AI ****:

|  |     |                    |                                    |
| ---- | ------- | -------------------------- | -------------------------------------- |
|  | Extract |          |      |
|  | Dream   |      |          |
|  | Recall  |          |  |
|  | Forget  |  `/forget` |                  |

---

## 

### 

```
~/.qwen/                                      <- 
\_-- projects/
    \_-- <sanitized-git-root>/                 <-  Git 
        |---- meta.json                         <- /
        |---- extract-cursor.json               <- 
        |---- consolidation.lock                <- Dream 
        \_-- memory/                           <- 
            |---- MEMORY.md                     <- 
            |---- user.md                       <- 
            |---- feedback.md                   <- 
            |---- project/
            |   \_-- milestone.md              <- 
            \_-- reference/
                \_-- grafana.md                <- 
```

> ****:
>
> - `QWEN_CODE_MEMORY_BASE_DIR`:
> - `QWEN_CODE_MEMORY_LOCAL=1`: `.qwen/memory/`

### 

|                   |                                                                    |
| --------------------- | ---------------------------------------------------------------------- |
| `meta.json`           |  Extract / Dream  ID |
| `extract-cursor.json` |                  |
| `consolidation.lock`  | Dream  PID 1             |
| `MEMORY.md`           |  Extract/Dream  Markdown     |

---

## 

:

|         |                                               |                                  |                      |
| ----------- | ----------------------------------------------------- | ---------------------------------------- | ---------------------------- |
| `user`      |                         | //           |    |
| `feedback`  |  AI :              |  AI  |  AI            |
| `project`   | Bug               |      |  AI  |
| `reference` | DashboardSlack  |                |  |

****:/Git  QWEN.md/AGENTS.md 

---

## 

 **YAML frontmatter + Markdown body** :

```markdown
---
name: 
description: 
type: user|feedback|project|reference
---

summary 

Why:  AI 
How to apply: 
```

 `feedback`  `project`  `Why`  `How to apply`

---

## 

```mermaid
flowchart TD
    A([]) --> B

    subgraph " Recall"
        B[] --> C{\n?}
        C --  --> D[\nstrategy: none]
        C --  --> E{ Config?}
        E --  --> F[\nside query]
        F --> G{?}
        G --  --> H[strategy: model]
        G --  --> I[strategy: none]
        E --  --> J[]
        F --  --> J
        J --> K{ > 0 ?}
        K --  --> L[strategy: heuristic]
        K --  --> I
        H --> M[ Relevant Memory \n]
        L --> M
        I --> N[]
    end

    M --> O([AI ])
    N --> O
    D --> O

    O --> P([AI ])

    subgraph " Extract"
        P --> Q{ AI \n?}
        Q --  --> R[\nmemory_tool]
        Q --  --> S{\n?}
        S --  --> T[\nalready_running / queued]
        S --  --> U[\n extract cursor]
        U --> V[ Agent\nrunAutoMemoryExtractionByAgent]
        V --> W[ patches]
        W --> X{ touched topics?}
        X --  --> Y[ meta.json\n MEMORY.md ]
        X --  --> Z[ extract cursor]
        Y --> Z
    end

    subgraph "Dream "
        P --> AA{Dream }
        AA --> AB{?}
        AB --  --> AC[\nsame_session]
        AB --  --> AD{ Dream\n>= 24 ?}
        AD --  --> AE[\nmin_hours]
        AD --  --> AF{ Dream \n >= 5?}
        AF --  --> AG[\nmin_sessions]
        AF --  --> AH{consolidation.lock\n?}
        AH --  --> AI[\nlocked]
        AH --  --> AJ[\n PID]
        AJ --> AK{ Config?}
        AK --  --> AL[Agent \nplanManagedAutoMemoryDreamByAgent]
        AL --> AM{Agent ?}
        AM --  --> AN[ topics]
        AM -- "/" --> AO
        AK --  --> AO[\n++]
        AO --> AP[]
        AN --> AQ[ MEMORY.md \n meta.json]
        AP --> AQ
        AQ --> AR[]
    end
```

---

## Extract -- 

### 

 AI  `scheduleAutoMemoryExtract` 

### `extractScheduler.ts`

```mermaid
flowchart TD
    A[scheduleAutoMemoryExtract ] --> B{\n?}
    B --  --> C[ skipped \n: memory_tool]
    B --  --> D{isExtractRunning?}
    D --  --> E{ queued ?}
    E --  --> F[ queued \nhistory ]
    E --  --> G[ pending \n queue]
    D --  --> H[ running \n runTask]
    H --> I[markExtractRunning\nsetCurrentTaskId]
    I --> J[runAutoMemoryExtract]
    J --> K[]
    K --> L[clearExtractRunning\n queue -> startQueuedIfNeeded]
    F --> M[ skipped: queued]
    G --> M
    C --> N[ skipped: memory_tool]
```

****:

|               |                                             |
| ----------------- | ----------------------------------------------- |
| `memory_tool`     |  Agent  |
| `already_running` |                           |
| `queued`          |                   |

### `extract.ts`

```mermaid
flowchart TD
    A[runAutoMemoryExtract] --> B[ensureAutoMemoryScaffold\n]
    B --> C[buildTranscriptMessages\n Content[]  offset ]
    C --> D[readExtractCursor\n]
    D --> E[loadUnprocessedTranscriptSlice\n]
    E --> F{slice ?}
    F --  --> G[ patches ]
    F --  --> H[runAutoMemoryExtractionByAgent\n forked agent  patches]
    H --> I[dedupeExtractPatches\n+]
    I --> J{ touched topics?}
    J --  --> K[bumpMetadata\n meta.json]
    K --> L[rebuildManagedAutoMemoryIndex\n MEMORY.md]
    L --> M[writeExtractCursor\n offset]
    J --  --> M
    M --> N[ AutoMemoryExtractResult]
```

**Cursor**:

- :`{ sessionId, processedOffset, updatedAt }`
-  `processedOffset` 
-  `offset >= processedOffset` 
- `sessionId`  0 

**Patch **:

-  < 12  -> 
-  `?`  -> 
- today/now/currently/temporary -> 
-  `topic:summary`  -> 

---

## Dream -- 

### 

 AI  `scheduleManagedAutoMemoryDream` 

### `dreamScheduler.ts`

```mermaid
flowchart TD
    A[scheduleManagedAutoMemoryDream ] --> B{Dream ?}
    B --  --> C[: disabled]
    B --  --> D[ensureAutoMemoryScaffold\n lastDreamSessionId]
    D --> E{ sessionId\n== lastDreamSessionId?}
    E --  --> F[: same_session]
    E --  --> G{elapsedHours >= 24h\n dream?}
    G --  --> H[: min_hours]
    G --  --> I{ session scan\n< 10 ?}
    I --  --> J[: min_sessions\n]
    I --  --> K[ chats/*.jsonl mtime\n Dream ]
    K --> L{ >= 5?}
    L --  --> M[: min_sessions]
    L --  --> N{lockExists?\nPID  + }
    N --  --> O[: locked]
    N --  --> P{dedupeKey \n Dream ?}
    P --  --> Q[: running\n taskId]
    P --  --> R[\nBgTaskScheduler]
    R --> S[acquireDreamLock\n PID  consolidation.lock]
    S --> T[runManagedAutoMemoryDream]
    T --> U[ meta.json\n]
```

****:

|                        |    |                           |
| -------------------------- | -------- | ----------------------------- |
| `minHoursBetweenDreams`    | 24   |  Dream  |
| `minSessionsBetweenDreams` | 5  |  Dream  |
| `SESSION_SCAN_INTERVAL_MS` | 10   |         |
| `DREAM_LOCK_STALE_MS`      | 1    | lock  |

****:

- lock  `<project-state-dir>/consolidation.lock`
-  PID
- : PID `kill(pid, 0)`  lock  1  -> 

### `dream.ts`

```mermaid
flowchart TD
    A[runManagedAutoMemoryDream] --> B{ Config?}
    B --  --> C[Agent \nplanManagedAutoMemoryDreamByAgent]
    C --> D{Agent ?}
    D --  --> E[ touched topics]
    E --> F[bumpMetadata\n MEMORY.md ]
    F --> G[updateDreamMetadataResult]
    G --> H[]
    H --> I[]
    B --  --> J[]
    C --  --> J
    D --  --> J

    J --> K[scanAutoMemoryTopicDocuments\n]
    K --> L[ buildDreamedBody]
    L --> M[ entries ->  summary \n -> ]
    M --> N{body ?}
    N --  --> O[]
    O --> P[ touched topic]
    N --> Q[\ndedupeKey = type:summary]
    Q --> R{?}
    R --  --> S[ entries  canonical \n]
    S --> P
    R --  --> T{ touched topics?}
    P --> T
    T --  --> U[bumpMetadata\n MEMORY.md ]
    U --> V[updateDreamMetadataResult\n -> ]
    T --  --> V
```

****:

1. : `summary.toLowerCase()`  `why`/`howToApply` 
2.  summary 
3. : `type:summary` 

---

## Recall -- 

### 

 AI  `resolveRelevantAutoMemoryPromptForQuery` 

### `recall.ts`

```mermaid
flowchart TD
    A[resolveRelevantAutoMemoryPromptForQuery] --> B[scanAutoMemoryTopicDocuments\n]
    B --> C[filterExcludedAutoMemoryDocuments\n]
    C --> D{query \n docs \n limit <= 0?}
    D --  --> E[ prompt\nstrategy: none]
    D --  --> F{ Config?}
    F --  --> G[selectRelevantAutoMemoryDocumentsByModel\n side query ]
    G --> H{?}
    H --  --> I[strategy: model]
    H --  --> J[strategy: none\n]
    G -- "/" --> K[]
    F --  --> K
    K --> L[tokenize query\n >=3  token]
    L --> M[scoreDocument \n +2 /  +1 /  +1]
    M --> N[ score=0 \n Top 5]
    N --> O{?}
    O --  --> P[strategy: heuristic]
    O --  --> J
    I --> Q[buildRelevantAutoMemoryPrompt\n Relevant Memory ]
    P --> Q
    Q --> R[ prompt ]
```

****:

|                              |              |
| -------------------------------- | ---------------- |
| query token      | +2 token |
| query token  | +1 token |
|  body                    | +1               |

****:

- `user`:user, preference, background, role, terse
- `feedback`:feedback, rule, avoid, style, summary
- `project`:project, goal, incident, deadline, release
- `reference`:reference, dashboard, ticket, docs, link

**Prompt **:

-  5 `MAX_RELEVANT_DOCS`
-  body  1200 `MAX_DOC_BODY_CHARS`
- :"NOTE: Relevant memory truncated for prompt budget."
-  mtime

---

## Forget -- 

### 

 `/forget <query>` 

### `forget.ts`

```mermaid
flowchart TD
    A[forgetManagedAutoMemoryEntries\nquery + config] --> B[ensureAutoMemoryScaffold]
    B --> C[listIndexedForgetCandidates\n entry]
    C --> D[ entry  ID\n entry : relativePath\n entry : relativePath:index]
    D --> E{ Config?}
    E --  --> F[selectByModel\n selection prompt\n side query temperature=0]
    F --> G{?}
    G --  --> H[strategy: model]
    G --  --> I[selectByHeuristic\n]
    E --  --> I
    I --> J[strategy: heuristic]
    H --> K[ candidates]
    J --> K
    K --> L{entries.length == 1?}
    L --  --> M[\nfs.unlink]
    L --  --> N[ entries\n entry\n]
    M --> O[ removedEntries]
    N --> O
    O --> P{ touched topics?}
    P --  --> Q[bumpMetadata\n MEMORY.md ]
    P --> R[ AutoMemoryForgetResult]
    Q --> R
```

**Entry ID **:

- :`relativePath` `feedback/no-summary.md`
- :`relativePath:index` `feedback/style.md:2`
-  ID 

---

## 

`MEMORY.md`  Extract  Dream  `rebuildManagedAutoMemoryIndex` :

```
- [](user/preferences.md) --  Go  React
- [](feedback/style.md) -- 
- [](project/milestone.md) -- 
```

****:

-  150  `...` 
-  200 
-  25,000 

---

## 

:

### Extract 

|              |                         |                     |
| ---------------- | --------------------------- | ----------------------- |
| `trigger`        | `'auto'`                    |   |
| `status`         | `'completed'` \| `'failed'` |                 |
| `patches_count`  | number                      |  patch  |
| `touched_topics` | string[]                    |     |
| `duration_ms`    | number                      |           |

### Dream 

|               |                                   |                    |
| ----------------- | ------------------------------------- | ---------------------- |
| `trigger`         | `'auto'`                              |                |
| `status`          | `'updated'` \| `'noop'` \| `'failed'` |                |
| `deduped_entries` | number                                |  |
| `touched_topics`  | string[]                              |    |
| `duration_ms`     | number                                |          |

### Recall 

|             |                                    |              |
| --------------- | -------------------------------------- | ---------------- |
| `query_length`  | number                                 |    |
| `docs_scanned`  | number                                 |    |
| `docs_selected` | number                                 |  |
| `strategy`      | `'none'` \| `'heuristic'` \| `'model'` |          |
| `duration_ms`   | number                                 |    |

---

## 

|                                                  |                                                                           |
| ---------------------------------------------------- | ----------------------------------------------------------------------------- |
| `packages/core/src/memory/types.ts`                  | :`AutoMemoryType``AutoMemoryMetadata``AutoMemoryExtractCursor`   |
| `packages/core/src/memory/paths.ts`                  | :`getAutoMemoryRoot``isAutoMemPath` helpers          |
| `packages/core/src/memory/store.ts`                  | :`ensureAutoMemoryScaffold`/                     |
| `packages/core/src/memory/scan.ts`                   | :`scanAutoMemoryTopicDocuments` frontmatter                |
| `packages/core/src/memory/entries.ts`                | :`parseAutoMemoryEntries``renderAutoMemoryBody`              |
| `packages/core/src/memory/extract.ts`                | :`runAutoMemoryExtract`patch                     |
| `packages/core/src/memory/extractScheduler.ts`       | :`ManagedAutoMemoryExtractRuntime`/                |
| `packages/core/src/memory/extractionAgentPlanner.ts` |  Agent:`runAutoMemoryExtractionByAgent`                                  |
| `packages/core/src/memory/dream.ts`                  | :`runManagedAutoMemoryDream`Agent  +               |
| `packages/core/src/memory/dreamScheduler.ts`         | :`ManagedAutoMemoryDreamRuntime`                 |
| `packages/core/src/memory/dreamAgentPlanner.ts`      |  Agent:`planManagedAutoMemoryDreamByAgent`                               |
| `packages/core/src/memory/recall.ts`                 | :`resolveRelevantAutoMemoryPromptForQuery`+        |
| `packages/core/src/memory/forget.ts`                 | :`forgetManagedAutoMemoryEntries`+                 |
| `packages/core/src/memory/indexer.ts`                | :`rebuildManagedAutoMemoryIndex``buildManagedAutoMemoryIndex`      |
| `packages/core/src/memory/prompt.ts`                 | :                                |
| `packages/core/src/memory/governance.ts`             | :`AutoMemoryGovernanceSuggestionType`                            |
| `packages/core/src/memory/state.ts`                  | :`isExtractRunning``markExtractRunning``clearExtractRunning` |
| `packages/core/src/memory/memoryAge.ts`              | :`memoryAge``memoryFreshnessText`                                |
