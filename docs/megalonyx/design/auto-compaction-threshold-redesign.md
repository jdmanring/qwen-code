# Auto-Compaction Threshold Redesign

**Status:** Draft  2026-05-14

## 

>  PR ****pre-redesign behavior `COMPRESSION_TOKEN_THRESHOLD``thinkingConfig.includeThoughts = true``hasFailedCompressionAttempt` file:line  PR #4345 ---- / 

 qwen-code  `COMPRESSION_TOKEN_THRESHOLD = 0.7``chatCompressionService.ts:33` claude-code  token autoCompact.ts:62-65qwen-code :

1. ****:1M  70%  700K  300K  +  ~33K
2. ** 1 **:`hasFailedCompressionAttempt = true`  session  auto-compactgeminiChat.ts:504 claude-code  3 
3. **tip  auto **:`tipRegistry.ts`  `context-*` tip  50/80/95  auto-compact 70%auto  80% / 95% tip auto  / 
4. ****:[chatCompressionService.ts:374-376](packages/core/src/services/chatCompressionService.ts:374)  `thinkingConfig.includeThoughts = true`:Compression quality drives every subsequent main turn sideQuery  `maxOutputTokens` [:436-437](packages/core/src/services/chatCompressionService.ts:436) `compressionOutputTokenCount may include non-persisted tokens (thoughts)` buffer <br/><br/> provider :Anthropic  thinking budget  max_tokens OpenAI  reasoning tokens  max_completion_tokens Gemini  maxOutputTokens  qwen-code  provider 

5. ** `lastPromptTokenCount` ** [geminiChat.ts:1217-1232](packages/core/src/core/geminiChat.ts:1217)  API response  `usageMetadata.totalTokenCount` gap:(a)  user message cheap-gate  prompt (b)  0`--continue`  session / sub-agent  send  claude-code  `tokenCountWithEstimation`[query.ts:638](src/query.ts:638) assistant API usage +  message  gap

## 

-  + 
-  warn / hard auto 
-  tip 
- 1 3  + 
- ** thinking  `maxOutputTokens` **: claude-code buffer 
- ** token **: `lastPromptTokenCount`  0 prompt 
-  settings  `contextPercentageThreshold`  PCT 
- **** env **** enabled 

## 

```
                       window  (raw context window)
                          |
                          |  <- SUMMARY_RESERVE = 20K
                          
                    effectiveWindow
                          |
                          |  <- HARD_BUFFER = 3K
                          
              hard_threshold = effectiveWindow - 3K
                          |
                          |  <- (AUTOCOMPACT_BUFFER - HARD_BUFFER) = 10K
                          
auto_threshold = max(PCT * window, effectiveWindow - AUTOCOMPACT_BUFFER)
                          |
                          |  <- WARN_BUFFER = 20K
                          
warn_threshold = max((PCT - WARN_OFFSET) * window, auto_threshold - WARN_BUFFER)
                          |
                          
                          0
```

### 

|        |                        |                                                      |
| -------- | ------------------------------ | -------------------------------------------------------- |
| **warn** | `tokenCount >= warn_threshold` | UI  X tokens send      |
| **auto** | `tokenCount >= auto_threshold` |  send  `tryCompress(force=false)`      |
| **hard** | `tokenCount >= hard_threshold` |  send  `tryCompress(force=true)` |

`hard`  reactive overflowgeminiChat.ts:711 send  oversized request round-trip

## 

```ts
// chatCompressionService.ts
const DEFAULT_PCT = 0.7; // auto 
const WARN_PCT_OFFSET = 0.1; // warn  = PCT - WARN_OFFSET = 0.6
const COMPACT_MAX_OUTPUT_TOKENS = 20_000; //  sideQuery thinking + summary 
const SUMMARY_RESERVE = 20_000; //  = maxOutput
const AUTOCOMPACT_BUFFER = 13_000; // auto  effectiveWindow 
const WARN_BUFFER = 20_000; // warn  auto 
const HARD_BUFFER = 3_000; // hard  effectiveWindow 
const MAX_CONSECUTIVE_FAILURES = 3; // 
```

: claude-code [autoCompact.ts:30,62-65](src/services/compact/autoCompact.ts:30)

`SUMMARY_RESERVE = COMPACT_MAX_OUTPUT_TOKENS` : `maxOutputTokens`  20K reserve  safety margin: thinking output budget  summary thinking`thinking + summary` Gemini SDK /  provider  `maxOutputTokens`  summary  20K 12 

## 

```ts
export interface CompactionThresholds {
  warn: number;
  auto: number;
  hard: number; //  hard < auto  auto
  effectiveWindow: number;
}

export function computeThresholds(window: number): CompactionThresholds {
  const effectiveWindow = window - SUMMARY_RESERVE;

  const absAuto = effectiveWindow - AUTOCOMPACT_BUFFER;
  const auto = Math.max(DEFAULT_PCT * window, absAuto);

  const absWarn = auto - WARN_BUFFER;
  const warn = Math.max((DEFAULT_PCT - WARN_PCT_OFFSET) * window, absWarn);

  const rawHard = effectiveWindow - HARD_BUFFER;
  const hard = Math.max(rawHard, auto); //  auto

  return { warn, auto, hard, effectiveWindow };
}
```

### 

|  | warn        | auto        | hard         |                             |
| ---- | ----------- | ----------- | ------------ | ------------------------------- |
| 32K  | 19.2K (pct) | 22.4K (pct) | 22.4K () |                         |
| 64K  | 38.4K (pct) | 44.8K (pct) | 44.8K () |                         |
| 128K | 76.8K (pct) | 95K (abs)   | 105K (abs)   | warn=pct, auto/hard=abs |
| 200K | 147K (abs)  | 167K (abs)  | 177K (abs)   |                         |
| 256K | 203K (abs)  | 223K (abs)  | 233K (abs)   |                         |
| 1M   | 947K (abs)  | 967K (abs)  | 977K (abs)   |                           |

`(pct)` `(abs)` 

## 

### ChatCompressionSettings 

```ts
// packages/core/src/config/config.ts:217
export interface ChatCompressionSettings {
  /**  compactionInputSlimming  */
  imageTokenEstimate?: number;
}
```

**:** `contextPercentageThreshold` :

1. >= 128K----
2. "" token 
3. claude-code 

### Breaking change 

**:**  `Config`  `chatCompression.contextPercentageThreshold` :

-  stderr :`"chatCompression.contextPercentageThreshold has been removed and is now controlled by built-in thresholds."`
- ********
- 

**SDK R5.4:** `CompressOptions`  `hasFailedCompressionAttempt: boolean`  `consecutiveFailures: number`:

|      |                          |                                                                |
| ---- | ------------------------------ | -------------------------------------------------------------------- |
|  | `hasFailedCompressionAttempt`  | `consecutiveFailures`                                                |
|  | `boolean`                      | `number`                                                             |
|  | `true` =  auto-compact | `>= MAX_CONSECUTIVE_FAILURES` 3=  force  |

 `GeminiChat.tryCompress`  migration  `@qwen-code/qwen-code-core`  published package`CompressOptions`  d.ts  SDK  `service.compress({ ..., hasFailedCompressionAttempt: true })`  TS **:**  `true`  `MAX_CONSECUTIVE_FAILURES` >= 3 `false`  `0`

## Token 

qwen-code  `lastPromptTokenCount`  API response  `usageMetadata.totalTokenCount`[geminiChat.ts:1217-1232](packages/core/src/core/geminiChat.ts:1217):

1. ****:cheap-gate  `lastPromptTokenCount`  send  prompt =  +  user message false-negative
2. ** 0**: 0 send  `--continue`  / sub-agent 

 `estimatePromptTokens` send  cheap-gate / hard :

```ts
// chatCompressionService.ts packages/core/src/services/tokenEstimation.ts

const BYTES_PER_TOKEN = 4; //  char/4 claude-code 
const BYTES_PER_TOKEN_JSON = 2; // JSON / tool_call input 

/**
 *  Content  token  API usage metadata 
 *  image / document  imageTokenEstimate 1600
 */
export function estimateContentTokens(
  contents: Content[],
  imageTokenEstimate = DEFAULT_IMAGE_TOKEN_ESTIMATE,
): number {
  //  estimateContentCharscompactionInputSlimming.ts bytesPerToken
  //  functionCall / functionResponse  BYTES_PER_TOKEN_JSON
  // ...
}

/**
 * cheap-gate  hard 
 * :lastPromptTokenCount  +  user message 
 * :full history 
 */
export function estimatePromptTokens(
  history: Content[],
  userMessage: Content,
  lastPromptTokenCount: number,
): number {
  if (lastPromptTokenCount > 0) {
    return lastPromptTokenCount + estimateContentTokens([userMessage]);
  }
  return estimateContentTokens([...history, userMessage]);
}
```

:

- `chatCompressionService.compress()`  cheap-gate: `originalTokenCount`  `estimatePromptTokens(history, userMessage, lastPromptTokenCount)`
- `geminiChat.sendMessageStream`  hard 

****  char/4  false-positive  false-negative 

## 

### chatCompressionService.ts

1. ** `computeThresholds`** cheap-gate / UI / 
2. **`compress()` cheap-gate** (line 221-249):
   ```ts
   if (consecutiveFailures >= MAX_CONSECUTIVE_FAILURES && !force) {
     return NOOP;
   }
   const { auto } = computeThresholds(contextLimit);
   const effectiveTokens = estimatePromptTokens(
     curatedHistory,
     userMessage,
     originalTokenCount,
   );
   if (!force && effectiveTokens < auto) return NOOP;
   ```
3. **`compress()`  runSideQuery ** (line 356-380): thinking +  `maxOutputTokens`:

   ```ts
   const summaryResult = await runSideQuery(config, {
     // ...
     config: {
       thinkingConfig: { includeThoughts: false }, //  thinking claude-code 
       maxOutputTokens: COMPACT_MAX_OUTPUT_TOKENS, //  20K
     },
     // ...
   });
   ```

    `thinkingConfig`  `runSideQuery` [sideQuery.ts:118](packages/core/src/utils/sideQuery.ts:118)  `includeThoughts: false`

    thinking `maxOutputTokens`  thinking  budget `SUMMARY_RESERVE = maxOutput = 20K` 

    [chatCompressionService.ts:374-376](packages/core/src/services/chatCompressionService.ts:374) Compression quality drives every subsequent main turn -- keep reasoning on provider  claude-code 

   token math [:436-437](packages/core/src/services/chatCompressionService.ts:436) "may include non-persisted tokens (thoughts)" 

### geminiChat.ts: `sendMessageStream` line 562

```ts
// :tryCompress(force=false)
// : token  hard force 

const { hard } = computeThresholds(contextLimit);
const effectiveTokens = estimatePromptTokens(
  this.getHistory(true),
  createUserContent(params.message),
  this.lastPromptTokenCount,
);
const shouldForceFromHard = effectiveTokens >= hard;

if (shouldForceFromHard) {
  //  force compress
  this.consecutiveFailures = 0;
}

compressionInfo = await this.tryCompress(
  prompt_id,
  model,
  shouldForceFromHard,
  params.config?.abortSignal,
);
```

###  (`geminiChat.ts:504-510`)

```ts
// 
hasFailedCompressionAttempt: boolean;

// 
consecutiveFailures: number;  //  0

// 
} else if (isCompressionFailureStatus(info.compressionStatus)) {
  if (!force) {
    this.consecutiveFailures += 1;
  }
}

// 
this.consecutiveFailures = 0;
```

`force=true`  reactive / manual ""

## UI 

### tipRegistry.ts  context-\* tip

 tip  token :

| Tip ID             |                                       |                                                               |                                                           |
| ------------------ | --------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `compress-intro`   | `pct >= 50 && < 80 && sessionPromptCount > 5` | `tokenCount >= warn && tokenCount < auto && sessionPromptCount > 5` |                                                           |
| `context-high`     | `pct >= 80 && < 95`                           | `tokenCount >= auto && tokenCount < hard`                           |                                                           |
| `context-critical` | `pct >= 95`                                   | `tokenCount >= hard`                                                | Auto-compact will force on next send. hard  |

**:**

- auto :`tokenCount`  auto  tokenCount  `context-high` 
- auto  /  / reactive :`tokenCount`  warn -> auto -> hard  tip""
- `context-critical`  hard  send  force compressspec  tip post-rescue pre-rescue 

`TipContext` :

```ts
export interface TipContext {
  lastPromptTokenCount: number;
  contextWindowSize: number;
  sessionPromptCount: number;
  sessionCount: number;
  platform: string;
  // : isRelevant 
  // computeThresholds  tipRegistry  core
  thresholds?: CompactionThresholds;
}
```

`AppContainer.tsx:1150`  `TipContext` 

### /context  (`contextCommand.ts:177-183`)

```ts
//  (1 - threshold) * contextWindowSize
const { warn, auto, hard, effectiveWindow } =
  computeThresholds(contextWindowSize);

// :
//   Effective window:   180K   (window  20K reserve)
//   Warn threshold:     147K   (...)
//   Auto threshold:     167K   <- 
//   Hard threshold:     177K
//  token count  tier
```

### Footer  follow-up

 spec  footer :

-  tip  history 
- Footer  ink 
-  spec  follow-up PR

 `tokenCount >= warn && tokenCount < auto` auto 

## 

### chatCompressionService.test.ts

- `computeThresholds(32K)` -> warn/auto  pcthard 
- `computeThresholds(128K)` -> warn=pctauto=abshard=abs
- `computeThresholds(200K)` -> warn/auto/hard  abs
- `computeThresholds(1M)` -> 
- `computeThresholds(window=10K)` -> 
-  `warn <= auto <= hard`
- max() pct \* window == abs

### tokenEstimation.test.ts

- `estimateContentTokens`  / json / functionCall / functionResponse / image / document  bytesPerToken
- `estimatePromptTokens`  `lastPromptTokenCount > 0`  0 
-  user message  cheap-gate  auto 
-  API usage  30% 

### geminiChat.test.ts / chatCompressionService.test.ts

- 3  cheap-gate NOOP force 
- 
-  token  hard  send  force compress
-  sideQuery  `maxOutputTokens = COMPACT_MAX_OUTPUT_TOKENS`  `runSideQuery``thinkingConfig.includeThoughts`  `false` sideQuery 
- ****: `lastPromptTokenCount = 0`  history  chat `--continue`  send  auto 

### 

-  `contextPercentageThreshold = 0.5`  -> stderr  +  PCT 

### Tip tipRegistry.test.ts

-  context-\* tip  warn/auto/hard 
-  auto  `context-high` 
-  + token  tip 
- TipContext  `thresholds` fallback

## 

| Phase |                                                                                          |              |
| ----- | -------------------------------------------------------------------------------------------- | ------------------ |
| 1     |  + `computeThresholds` + cheap-gate                              |          |
| 2     | 1 -> 3                                                                    |          |
| 3     | hard  force compress                                                                   |  P1 + P7       |
| 4     |  + breaking change                                                             |  P1            |
| 5     | UItip  + /context                                                                    |  P1            |
| 6     |  sideQuery  thinking +  `maxOutputTokens`                                        |  P1  |
| 7     | Token `estimateContentTokens` + `estimatePromptTokens` cheap-gate / hard |  P1    |

 Phase  PR **P6 -> P7 -> P1 -> P2 -> P4 -> P3 -> P5**: `maxOutputTokens`  buffer  token  hard  token  +  PR 

## 

1. ** thinking **  "Compression quality drives every subsequent main turn -- keep reasoning on"  spec  token  telemetry  `compression_input_token_count` / `compression_output_token_count` `COMPRESSION_FAILED_*`  thinking  + provider-specific thinkingBudget 

2. **`maxOutputTokens`  summary **  thinking 20K  summary claude-code  p99.99  17K ~3K  qwen-code  prompt  claude-code [chatCompressionService.ts:464-491](packages/core/src/services/chatCompressionService.ts:464) finish_reason = MAX_TOKENS NOOP  summary

3. ** provider  maxOutputTokens ** OpenAI compat (dashscope) -> `max_tokens`Anthropic -> `max_tokens`Gemini SDK -> `maxOutputTokens` qwen-code [contentGenerator.ts:94](packages/core/src/core/contentGenerator.ts:94)  P6  sideQuery  `maxOutputTokens`  provider 

4. **Token ""** `char/4`  provider  tokenizer  30% spec false-positive  token  /  `lastPromptTokenCount`API 

5. ** `estimateContentChars` ** [compactionInputSlimming.ts](packages/core/src/services/compactionInputSlimming.ts)  `estimateContentChars` split point  `estimateContentTokens`  bytesPerToken

##  spec 

- Env D :
- Footer : follow-up
-  prompt `MIN_COMPRESSION_FRACTION` :

##  review

1. **breaking change **: +  vs /

## 

2. **<= ~76.7K hard  auto ** -- ** `/context` **:
   -  32K `effectiveWindow - HARD_BUFFER <= 0.7 * window`  64K
   - : `currentTier`  `'auto'`  `'hard'``contextCommand.ts:43-44`  `>= hard``context-high` band`auto <= t < hard`----
   - "" UI  `context-high`  UI  spec  UI 
