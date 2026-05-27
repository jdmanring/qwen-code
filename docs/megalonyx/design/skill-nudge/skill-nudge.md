# AutoSkill:

## 

 QwenCode  Memory-Dream  **AutoSkill** 

AutoSkill ****: agent  skill

###  Memory Extract 

|          | Memory Extract                   | AutoSkill                      |
| ------------ | -------------------------------- | ------------------------------ |
| **** |  |    |
| **** |                    |          |
| **** | `${projectRoot}/.qwen/memory/`   | `${projectRoot}/.qwen/skills/` |
| **** |    |      |
| **** | Dream /              |  review agent  |

---

## 

1. ****:skill review agent  `read_file``write_file``edit`  `.qwen/skills/` `skill_manage` ---- skill
2. ****: memory extract  `memory_tool`  `.qwen/skills/`  skillsession  skill review
3. **`auto-skill`  skill**:review agent  skill  YAML frontmatter  `source: auto-skill` skill review agent  skill skill
4. ****: >= 20 
5. ****:review agent  `write_file``edit`  `${projectRoot}/.qwen/skills/`  user / extension / bundled 
6. ** Hermes  prompt**:review agent  Hermes `_SKILL_REVIEW_PROMPT`

---

## 

### 1. :`toolCallCount` 

:

**** skill review:

```

  toolCallCount = 0


  toolCallCount += 1


  if (toolCallCount >= AUTO_SKILL_THRESHOLD):  //  20
     skillsModifiedInSession
    |--- true  -> skip skill review
    \_- false -> scheduleSkillReview()
```

**** `skill_manage` :

```

  if ( ${projectRoot}/.qwen/skills/ ):
    skillsModifiedInSession = true
```

: skills  `historyCallsSkillManage()` ---- `history`  tool result `write_file``edit` 

> ****
>  `skill_manage`  review agent  `write_file`/`edit`""" `.qwen/skills/` ": skill  review

> ****
> ---- 1  30  20  Hermes  10  QwenCode  edit

### 2. 

 `MemoryManager`  skill review

```

  |--- scheduleExtract(params)           // 
  \_- scheduleSkillReview(params)       // 
       :toolCallCount >= AUTO_SKILL_THRESHOLD
             && !skillsModifiedInSession
```

extract  skill review  `MemoryManager.track()` 

### 3. Skill Review Agent 

skill review agent **** `skill_manage` :

|          |                                   |                                                                     |
| ------------ | ------------------------------------- | --------------------------------------------------------------------------- |
| `read_file`  |  skill  frontmatter |                                                                       |
| `ls`         |  `.qwen/skills/`          |                                                                       |
| `write_file` |  skill                      |  `${projectRoot}/.qwen/skills/`                                       |
| `edit`       |  skill                    |  `${projectRoot}/.qwen/skills/`  `source: auto-skill` |
| `shell`      |  `cat``find`          | Shell AST                                         |

** `edit` `auto-skill` **:

skill review agent  `edit`  `write_file` YAML frontmatter `source: auto-skill` :

```
skill_review_agent: edit is only allowed on skills with 'source: auto-skill' in frontmatter.
This skill appears to be user-created. Modify it manually or ask the user.
```

 `createSkillScopedAgentConfig`  system prompt skill

****: agent  `.qwen/skills/` ---- `write_file`/`edit`  skill `skillsModifiedInSession = true` session  skill review

### 4. :`SkillScopedPermissionManager`

 `extractionAgentPlanner.ts`  `createMemoryScopedAgentConfig` skill review agent :

```typescript
// skill review agent 
read_file:    
ls:           
shell:        Shell AST  isShellCommandReadOnlyAST
write_file:    ${projectRoot}/.qwen/skills/  skill
edit:          ${projectRoot}/.qwen/skills/  source: auto-skill
```

**`auto-skill` **:

1. ****:`edit`  frontmatter `source: auto-skill` 
2. **System prompt **: agent  `source: auto-skill`  skill
3. ****: system prompt 

---

## Skill Review Agent 

###  prompt Hermes

```
Review the conversation above and consider saving or updating a skill if appropriate.

Focus on: was a non-trivial approach used to complete a task that required trial
and error, or changing course due to experiential findings along the way, or did
the user expect or desire a different method or outcome? If a relevant skill
already exists and has 'source: auto-skill' in its frontmatter, update it with
what you learned. Otherwise, create a new skill if the approach is reusable.

IMPORTANT constraints:
- You may ONLY modify skill files that contain 'source: auto-skill' in their
  YAML frontmatter. Always read a skill file before editing it.
- Do NOT touch skills that lack this marker -- they were created by the user.
- When creating a new skill, you MUST include 'source: auto-skill' in the
  frontmatter so future review agents can safely update it.
- Do NOT delete any skill. Only create or update.

If nothing is worth saving, just say 'Nothing to save.' and stop.

Skills are saved to the current project (.qwen/skills/).
Use write_file to create a new skill, edit to update an existing auto-skill.
Each skill lives at .qwen/skills/<name>/SKILL.md with YAML frontmatter:

---
name: <skill-name>
description: <one-line description>
metadata:
  source: auto-skill
  extracted_at: '<ISO-8601 timestamp>'
---

<markdown body with the procedure/approach>
```

### Agent 

```typescript
{
  name: "managed-skill-extractor",
  tools: [
    "read_file",   //  skill  source: auto-skill
    "ls",          //  .qwen/skills/ 
    "write_file",  //  skill 
    "edit",        //  auto-skill frontmatter
    "shell",       //  findcat
  ],
  permissionManager: createSkillScopedAgentConfig(config, projectRoot),
  history: sessionHistory,  // 
}
```

---

##  MemoryManager 

### `ScheduleSkillReviewParams`

```typescript
export interface ScheduleSkillReviewParams {
  projectRoot: string;
  sessionId: string;
  history: Content[]; // 
  toolCallCount: number; // 
  skillsModified: boolean; //  .qwen/skills/
  config?: Config;
  enabled?: boolean;
  threshold?: number;
  maxTurns?: number;
  timeoutMs?: number;
}

export interface SkillReviewScheduleResult {
  status: 'scheduled' | 'skipped';
  taskId?: string;
  skippedReason?: 'below_threshold' | 'skills_modified_in_session' | 'disabled';
}
```

### `MemoryManager.scheduleSkillReview()`

```typescript
scheduleSkillReview(params: ScheduleSkillReviewParams): SkillReviewScheduleResult {
  // 1. 
  if (params.enabled === false) {
    return { status: 'skipped', skippedReason: 'disabled' };
  }

  // 2. 
  const threshold = params.threshold ?? AUTO_SKILL_THRESHOLD;
  if (params.toolCallCount < threshold) {
    return { status: 'skipped', skippedReason: 'below_threshold' };
  }

  // 3.  skill review
  if (params.skillsModified) {
    return { status: 'skipped', skippedReason: 'skills_modified_in_session' };
  }

  // 4. 
  const record = makeTaskRecord('skill-review', params.projectRoot, params.sessionId);
  const promise = this.track(record.id, this.runSkillReview(record, params));
  return { status: 'scheduled', taskId: record.id, promise };
}
```

### 

```typescript
//  MemoryTaskRecord.taskType
export type MemoryTaskType = 'extract' | 'dream' | 'skill-review';

// 
export const AUTO_SKILL_THRESHOLD = 20; // 
```

---

## 

```

  agent 
    |---  -> toolCallCount += 1
    \_-  ${projectRoot}/.qwen/skills/ 
         -> skillsModifiedInSession = true

sessionEnd 
  |--- scheduleExtract(params)
  |     \_- [:fork extraction agent ->  .qwen/memory/]
  |
  \_- toolCallCount >= 20 && !skillsModifiedInSession ?
       |---  -> skip   skill
       \_-  -> scheduleSkillReview(params)
                 \_-  fork skill review agent
                        
                 skill review agentmax 8 2 min
                 :read_file, ls, write_file, edit, shell
                  sessionHistory
                        
                 
                 |---  ->  skill source: auto-skill
                 |         -> write_file  skill source: auto-skill
                 |         -> edit  auto-skill
                 |         -> SkillManager notifyChangeListeners
                 \_-  -> "Nothing to save." 


  SkillManager.listSkills({ level: 'project' })
  ->  .qwen/skills/  skill
  ->  system prompt  <available_skills> Tier 1
```

---

## SKILL.md project-level

 skill  `${projectRoot}/.qwen/skills/<name>/SKILL.md` SkillManager :

```yaml
---
name: <skill-name> #  + 
description: <description> # <= 1024 
version: 1.0.0
metadata:
  source: auto-skill # review agent 
  extracted_at: '2026-04-24T12:00:00Z'
---
# <>

< /  / >
```

**`source: auto-skill` **:

|        |        | skill review agent  |  |
| ------------ | ------------ | --------------------------- | ------------ |
| `auto-skill` | review agent |                         |          |
|      |  |       |          |

 skill  `source: auto-skill` review agent 

---

## 

|                                  |                                                                                                          |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
|  skill     |  frontmatter `source: auto-skill`  `edit`system prompt  auto-skill     |
| skill                        | review prompt " skill" skill                                               |
|                        | `write_file`/`edit`  `${projectRoot}/.qwen/skills/` `assertRealProjectSkillPath`  symlink  |
|                |                                                                                          |
| review agent  skill              | review agent  `rm` `shell` system prompt                         |
|  skill  review | `skillsModifiedInSession` : `.qwen/skills/`  review                                 |
| symlink  skills  | `assertRealProjectSkillPath`async: `fs.realpath()`  skills root       |

---

## 

 QwenCode config :

```typescript
// config schema  memory 
memory?: {
  enableAutoSkill?: boolean;   //  true
}
```

 QWEN.md / `~/.qwen/config.json` :

```json
{
  "memory": {
    "enableAutoSkill": true
  }
}
```

---

## E2E 

 `.qwen/skills/e2e-testing/SKILL.md`  `npm run build && npm run bundle` `node dist/cli.js` 

### 1. 

-  headless 
-  `memory.enableAutoSkill: true`
- 
-  `.qwen/skills/`  `source: auto-skill` skillJSON  `.qwen/skills/` 

### 2.  skill review

-  headless `AUTO_SKILL_THRESHOLD`  20
- 
-  skill review`.qwen/skills/<name>/SKILL.md`  frontmatter  `source: auto-skill`
-  `Nothing to save.`

### 3.  skill  review

-  `write_file`  `edit`  `.qwen/skills/`  skill
-  session  `skillsModifiedInSession = true``scheduleSkillReview`  `skippedReason: 'skills_modified_in_session'`
-  review agent

### 4.  project-level skills

-  skill review agent user-level skill  bundled skill 
-  `${projectRoot}/.qwen/skills/`
-  `${projectRoot}/.qwen/skills/<name>/SKILL.md`

### 5. `auto-skill`  skill

-  `.qwen/skills/`  `source: auto-skill`  skill
-  skill review agent  skill
-  skill  auto-skill
-  `source: auto-skill`  skill 

### 6. symlink 

-  `.qwen/skills/`  symlink
-  skill review agent  symlink 
-  `assertRealProjectSkillPath`  `symlink traversal detected` 

### 7. 

-  `memory.enableAutoSkill: false`
- `enableAutoSkill`  `true`

### 8. 

-  e2e-testing skill  headless JSON :
  `node dist/cli.js "<prompt>" --approval-mode yolo --output-format json 2>/dev/null`
-  `--openai-logging --openai-logging-dir <tmp-dir>`  schemaprompt 
-  TUI  sessionEnd  tmux interactive 

## 

```
 MemoryManager
  |--- scheduleExtract()       <- 
  |--- scheduleDream()         <- 
  |--- recall()                <- 
  |--- forget()                <- 
  \_- scheduleSkillReview()   <- 

 SkillManager
  |--- listSkills()            <-  .qwen/skills/ 
  \_- loadSkill()             <- 

read_file / write_file / edit
  |--- : skill
  |   \_-  .qwen/skills/ -> skillsModifiedInSession = true
  \_- skill review agent :/ auto-skill
      \_-  +  source: auto-skill

 sessionEnd hook
  \_-  scheduleExtract + scheduleSkillReview
```

SkillManager `listSkills``loadSkill`----review agent  `${projectRoot}/.qwen/skills/` `SkillManager`  `chokidar`  `notifyChangeListeners()`  system prompt  skill
