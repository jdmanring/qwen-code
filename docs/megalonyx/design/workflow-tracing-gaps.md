# Workflow  Span  (P1)

>  2026-05-13  qwen-code origin/main 

## 

qwen-code  tracing :

|           |                                              |                                                      |
| ------------- | ------------------------------------------------ | -------------------------------------------------------- |
| Span  | `packages/core/src/telemetry/session-tracing.ts` | `interaction``llm_request``tool``tool.execution`   |
| Tracer    | `packages/core/src/telemetry/tracer.ts`          | session root context`withSpan``startSpanWithContext` |
|       | `packages/core/src/core/client.ts`               |  `interaction` span                      |
|   | --                                                | AsyncLocalStorage + WeakRef + TTL cleanup                |

 runtime  generic spans:

- `api.generateContent` / `api.generateContentStream`
- `tool.<toolName>`

**:" tracing " agent workflow  trace **

### :claude-code  span 

 `claude-code/src/utils/telemetry/sessionTracing.ts` (line 49):

- `interaction`
- `llm_request`
- `tool`
- `tool.blocked_on_user`
- `tool.execution`
- `hook`

## 

|  span /                            |                                             |
| ------------------------------------------ | ----------------------------------------------- |
| `permission_wait` / `blocked_on_user` span |  vs                 |
| `hook` span                                | hook  tool span       |
| `subagent` root span                       | subagent  llm/tool  trace   |
| `tool.execution`                   | helper                      |
|  parent-child wiring                 | spans  session root  sibling  |

## 

### 1.  trace 

 `awaiting_approval` -> `scheduled` -> 

- "" trace 
- trace 
- """"

### 2. Hook  span

Pre/Post hook  `HookCallEvent` `logHookCall()` OTel span

- hook  tool span 
- hook  "tool "
- trace " hook  tool.execution "

### 3. Subagent  log/metric  trace subtree

subagent / `SubagentExecutionEvent`  log/metric span 

- " subagent "
-  trace " subagent  llm/tool "
-  subagent 

### 4. tool.execution helper 

`session-tracing.ts`  `startToolExecutionSpan()` / `endToolExecutionSpan()`

 trace :

```
session-root
  interaction
    api.generateContent
    tool.Bash
  subagent_execution        (log/metric)
  hook_call                 (event/QwenLogger)
```

 trace :

```
interaction
  llm_request
    tool
      tool.blocked_on_user
      hook(pre)
      tool.execution
      hook(post)
  subagent
    interaction
      llm_request
        tool
```

### 5. Parent-child wiring 

interaction span  spans  session root  sibling interaction 

- 
- 
-  llm/tool/hook/subagent 

## 

- traces  workflow 
- "hook tool "
-  subagent  trace 
- hook  tool span
-  Jaeger / Tempo / ARMS  claude-code 

---

## claude-code 

>  2026-05-13  claude-code 

### claude-code  tracing 

claude-code  `src/utils/telemetry/sessionTracing.ts` ** ALS  span **:

```
                    interactionContext (ALS)          toolContext (ALS)
                          |                                |
                                                          
              +-----------------------+--           +-----------------------+--
              |  interaction span   |           |    tool span        |
              |  (session root)     |           |  (child of intxn)   |
              \_------------------------           \_------------------------
                    parent of                        parent of
                   |                                 |
           +----------------+--              +-------------------------+--
           |               |              |          |          |
      llm_request      tool          blocked    execution    hook
                                     _on_user
```

**:**

|         |                                                                                                                                                                                       |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  ALS      | `interactionContext`  interaction span`toolContext`  tool span                                                                                                              |
| parent  |  span  ALS  parent:`llm_request`/`tool`  `interactionContext``blocked_on_user`/`execution`/`hook`  `toolContext``hook`  fallback  `interactionContext` |
|     | enterWith  -> span  -> enterWith(undefined)                                                                                                                                     |
|  span   |  ALS  span blocked_on_user `activeSpans` Map  `span.type`                                                                                                         |
|     | ALS  span  WeakRef ALS  span  strongRef  GCTTL 30min                                                                                                      |

**claude-code tool span ** (`toolExecution.ts`):

```
startToolSpan(name, attrs)                    // -> toolContext.enterWith(spanCtx)
  startToolBlockedOnUserSpan()                // -> parent = toolContext.getStore()
    [permission resolution / user prompt]
  endToolBlockedOnUserSpan(decision, source)
  startToolExecutionSpan()                    // -> parent = toolContext.getStore()
    [tool.call()]
  endToolExecutionSpan({ success })
endToolSpan(result)                           // -> toolContext.enterWith(undefined)
```

**claude-code hook span** (`hooks.ts`):

```
startHookSpan(event, name, count, defs)       // -> parent = toolContext ?? interactionContext
  [parallel hook execution]
endHookSpan(span, { success, blocking, ... })
```

### qwen-code  vs claude-code

#### : span 

 qwen-code :

|                  |                  |                                                                                         | parent                                                |
| ------------------ | -------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| session-tracing  | `session-tracing.ts` | `startInteractionSpan` / `startLLMRequestSpan` / `startToolSpan` / `startToolExecutionSpan` |  `interactionContext` ALS  parent                 |
| tracer           | `tracer.ts`          | `withSpan` / `startSpanWithContext`                                                         |  `context.active()`  parentfallback  session root |

**runtime :**

- `startInteractionSpan` -> **** (`client.ts` line 956) `interactionContext` ALS
- `startLLMRequestSpan` / `endLLMRequestSpan` -> ****runtime  `withSpan('api.generateContent', ...)` ( `loggingContentGenerator.ts`)
- `startToolSpan` / `endToolSpan` -> ****runtime  `withSpan('tool.${name}', ...)` ( `coreToolScheduler.ts`)
- `startToolExecutionSpan` / `endToolExecutionSpan` -> ****

**:**

`withSpan`  `getParentContext()`  `context.active()`OTel  context span  session root context** `interactionContext` ALS**

 interaction span  LLM/tool spans  session root ** sibling** parent-child :

```
session-root
  |---- interaction         ( session-tracing,  interactionContext ALS)
  |---- api.generateContent ( withSpan,  interactionContext ->  session root)
  |---- tool.Bash           ( withSpan, )
  \_-- tool.Read           ( withSpan, )
```

** claude-code  span sessionTracing.ts span  ALS -> OTel context **

#### 

##### 1.  ALS +  parent  -- 

|          | claude-code                                           | qwen-code                                    |
| ------------ | ----------------------------------------------------- | -------------------------------------------- |
| ALS      | 2 (`interactionContext` + `toolContext`)              | 1 (`interactionContext` `toolContext`)   |
| parent   |  span  ALS  parent            | `withSpan`  `context.active()`         |
| context  | `trace.setSpan(otelContext.active(), parentCtx.span)` | `withSpan`  `startActiveSpan`  |

**:**

qwen-code  `session-tracing.ts`  claude-code ** parent **:

```typescript
// qwen-code session-tracing.ts ()
export function startLLMRequestSpan(model, promptId): Span {
  const parentCtx = interactionContext.getStore();
  const ctx = parentCtx
    ? trace.setSpan(otelContext.active(), parentCtx.span)
    : otelContext.active();
  // ...
}
```

 claude-code  `startLLMRequestSpan` ****

**: runtime  `withSpan('api.*')` / `withSpan('tool.*')`  session-tracing  typed helpers**  session-tracing ---- API 

:

-  `toolContext` ALS claude-code
-  `blocked_on_user`  `hook` span  helper 

##### 2. tool.blocked_on_user -- 

|           | claude-code                                | qwen-code                                                                  |
| ------------- | ------------------------------------------ | -------------------------------------------------------------------------- |
|       |  `toolExecution.ts` tool span    |  `coreToolScheduler._schedule()` tool span                       |
|       |  `resolveHookPermissionDecision()` | :`validating` -> `awaiting_approval` -> `scheduled` -> `executing` |
| span  | tool span  blocked + execution         | tool span(`withSpan`)  execution `executeSingleToolCall`   |

**:** qwen-code  `executeSingleToolCall`  `toolCall.status !== 'scheduled'` ----Tool span  `withSpan` 

**:**

** A --  tool span :**

 `startToolSpan`  `executeSingleToolCall`  `_schedule`  tool span  `awaiting_approval`  `startToolBlockedOnUserSpan``scheduled` `endToolBlockedOnUserSpan`

```
_schedule():
  startToolSpan(name)                         // <- 
    startToolBlockedOnUserSpan()              // <-  awaiting_approval 
      []
    endToolBlockedOnUserSpan(decision)        // <-  scheduled 
executeSingleToolCall():
    startToolExecutionSpan()                  // <-  helper
      [hook + execute]
    endToolExecutionSpan()
  endToolSpan()                               // <-  finally 
```

** B --  tool span :**

 `_schedule`  `approval_wait` span tool  child interaction  claude-code trace 

** A**:

-  claude-code  trace 
- trace  tool " + "
-  span start/end  parent-child 

##### 3. hook span -- 

|           | claude-code                         | qwen-code                                                            |
| ------------- | ----------------------------------- | -------------------------------------------------------------------- |
| hook  | `executeHooks()` in `hooks.ts`      | `firePreToolUseHook`/`firePostToolUseHook` via `hookEventHandler.ts` |
|   | OTel span + Perfetto span           | `HookCallEvent` -> `QwenLogger` ( OTel)                             |
| parent        | `toolContext ?? interactionContext` | --                                                                    |

**:**

1.  `session-tracing.ts`  `startHookSpan` / `endHookSpan`parent = `toolContext ?? interactionContext` claude-code 
2.  `coreToolScheduler.ts`  `executeSingleToolCall` pre/post hook  start/end hook span
3.  `logHookCall` 

 hook 

##### 4. tool.execution --  helper

qwen-code  `startToolExecutionSpan(parentToolSpan)` / `endToolExecutionSpan(span, metadata)`  `executeSingleToolCall` :

```typescript
// coreToolScheduler.ts executeSingleToolCall 
const toolSpan = startToolSpan(toolName, attrs);
// ... hook pre ...
const execSpan = startToolExecutionSpan(toolSpan);
try {
  // ... invocation.execute() ...
  endToolExecutionSpan(execSpan, { success: true });
} catch (e) {
  endToolExecutionSpan(execSpan, { success: false, error: e.message });
}
// ... hook post ...
endToolSpan(toolSpan);
```

:qwen-code  `startToolExecutionSpan`  `parentToolSpan`  claude-code  `toolContext` ALS  `toolContext` ALS

##### 5. subagent trace tree -- 

|             | claude-code                                                             | qwen-code                                            |
| --------------- | ----------------------------------------------------------------------- | ---------------------------------------------------- |
| OTel trace  | **** -- subagent  interaction  root                              | **** -- subagent  trace                   |
|         | Perfetto metadataagent process/thread+ `teammateContextStorage` ALS | `subagentNameContext` ALS + `SubagentExecutionEvent` |
|         | OTel ALS `enterWith`  subagent      |                                            |

claude-code  subagent OTel tracing ****:

- `interactionContext.enterWith()`  subagent  ALS 
-  agent  Perfetto Anthropic  feature-flagged  OTel 

**:**

- : qwen-code  `subagentNameContext` + 
- : subagent  `subagent` spanparent =  toolContext `context.with()`  `enterWith()`  subagent  OTel context
-  claude-code

##### 6. LLM request span -- 

qwen-code  `loggingContentGenerator.ts`  `withSpan('api.generateContent', ...)`  `startSpanWithContext('api.generateContentStream', ...)`

 `startLLMRequestSpan` / `endLLMRequestSpan`session-tracing streaming :

- `startLLMRequestSpan`  `Span` 
-  `endLLMRequestSpan(span, metadata)` 
-  `startSpanWithContext` 

### 

|                                                                     |                             |                                         |  |
| ------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------- | ------ |
|  span  runtime `withSpan` session-tracing helpers | **** --  parent-child  | ~5                              | P0     |
|  `toolContext` ALS                                                    |  claude-code              | session-tracing.ts                  | P0     |
| tool.blocked_on_user span                                                 |  A                    | \_schedule + executeSingleToolCall  | P1     |
| tool.execution                                                        | helper                  | executeSingleToolCall  3            | P1     |
| hook span                                                                 |  helper +                   |                                             | P1     |
| LLM request span                                                      |  withSpan  typed helper         | 2                               | P1     |
| subagent trace tree                                                       | **** --        |                                             | P2     |

### 

```
Phase 1 --  trace  (P0)
|---- 1a. session-tracing.ts  toolContext ALS + blocked_on_user / hook span helpers
|---- 1b. loggingContentGenerator.ts: withSpan -> startLLMRequestSpan/endLLMRequestSpan
\_-- 1c. coreToolScheduler.ts: withSpan -> startToolSpan/endToolSpan

Phase 2 --  workflow span (P1)
|---- 2a. coreToolScheduler._schedule: blocked_on_user span 
|---- 2b. coreToolScheduler.executeSingleToolCall: tool.execution span 
\_-- 2c. hook pre/post : hook span 

Phase 3 -- Subagent trace tree (P2)
|---- 3a.  context.with()  enterWith
|---- 3b. subagent  subagent root span
\_-- 3c.  subagent 
```
