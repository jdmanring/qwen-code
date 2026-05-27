# OOM  Replay 

****: 2026-05-19
****: `codex/memory-diagnostics-local-run`
****: yiliang114
****: v0.15.7 (#3735)  auto-compaction  `structuredClone`
 heap  OOM debug 

---

## 

 issue#4309, #4276, #4185, #4315, #4322, #2868 qwen-code  V8 heap OOM crash:

```
FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory
```

:
| Issue |  Heap |  |  |
|-------|------------|---------|------|
| #4276 | 4014 MB | ~110  | Linux x64 |
| #4315 | 2027 MB | ~19.6  | macOS ( 2GB limit) |
| #4322 | 4023 MB | ~7  | Windows |
| #2868 | 2035 MB | ~1.7  | Linux |
| #4309 | 7020 MB |  | Windows ( 8GB limit ) |

---

## 

:

1. ** heap **: `--max-old-space-size` 
   "history "
   4G/8G OOM 
2. ** heap  replay**: `NODE_OPTIONS` JSONL 
    review  process-tree RSS
   

 heap " OOM "
history  heap 

##  heap 

|                      |                                                            |
| ------------------------ | ------------------------------------------------------------ |
| CLI                  | 0.15.11 ( `codex/memory-diagnostics-local-run`  build) |
| Model                    | `qwen3.6-plus` (128K context window)                         |
| Heap limit               | `--max-old-space-size=512`                                   |
| Heap-pressure safety net | **** (HEAP_PRESSURE_COMPRESSION_RATIO  99.0)         |
|                  | YOLO +  Read                               |
|                  | qwen-code monorepo (3538 .ts files, 1.26M lines)             |

### 

`packages/core/src/core/geminiChat.ts`  heap-pressure compaction  0.7  99.0 #4186 

---

##  heap 

### 

```
[21:26:59] #1 RSS:193.6MB Ctx:0%   -> Read geminiChat.ts (1500 )
[21:27:46] #2 RSS:270.4MB Ctx:4.2% -> Read agent.ts
[21:28:32] #3 RSS:397.5MB Ctx:4.3% -> grep + Read 3 
[21:29:18] #4 RSS:452.7MB Ctx:5.7% -> Read slashCommandProcessor.ts
[21:30:04] #5 RSS:515.0MB Ctx:5.9% -> Read chatCompressionService.ts
[21:30:50] #6 RSS:649.1MB Ctx:4.0% <- TOKEN COMPACTION  (5.9%->4.0%)
                                       RSS  134MB (structuredClone )
[21:31:36] #7 RSS:666.7MB Ctx:3.2% <-  compaction, RSS 
[21:32:22] CRASH -- FATAL ERROR: Ineffective mark-compacts near heap limit
```

****: ~5.5 7 

 heap  history + compaction/history clone  V8 heap OOM
 heap  OOM 

###  heap  synthetic 

 512 MiB  heap  heap  synthetic runtime
pressure  review/subagent :

- root review turns: 10
- subagent calls: 30
- subagent transcript records: 780
- retained tool result bytes: 193,986,560
- serialized history bytes: 195,620,061
- pressure mode: retained `structuredClone(history)` copies

| Heap limit |     Clone pressure |                                      |  GC / stack                                              |
| ---------- | -----------------: | ---------------------------------------- | ------------------------------------------------------------ |
| 2 GiB      |  8 retained clones | RSS 2.42 GiBheap used 1.87 GiB |  heap limit                                              |
| 2 GiB      | 10 retained clones | OOM                                      | `Reached heap limit`, `ValueDeserializer`, `StructuredClone` |
| 4 GiB      | 20 retained clones | OOM                                      | `Reached heap limit`, `ValueDeserializer`, `StructuredClone` |

2 GiB  GC :

```
Mark-Compact 2042.9 (2081.9) -> 2042.9 (2081.1) MB
Mark-Compact 2048.9 (2087.2) -> 2048.9 (2087.2) MB
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
...
node::worker::(anonymous namespace)::StructuredClone
```

4 GiB  GC :

```
Mark-Compact 4082.5 (4126.8) -> 4082.5 (4126.3) MB
Mark-Compact 4095.1 (4139.0) -> 4095.1 (4139.0) MB
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
...
node::worker::(anonymous namespace)::StructuredClone
```

 512 MiB  2 GiB / 4 GiB heap OOM:
 history  tool result / subagent transcript history
 retained  clone  2-4 GiB heap  V8 OOM synthetic
 replay" heap "

###  GC 

```
[41381:0x130008000] 342468 ms: Mark-Compact 508.6 (526.7) -> 507.0 (526.9) MB,
  pooled: 1 MB, 86.42 / 0.00 ms  (average mu = 0.175, current mu = 0.150)
  task; scavenge might not succeed

[41381:0x130008000] 342568 ms: Mark-Compact 509.1 (526.9) -> 507.1 (528.2) MB,
  pooled: 0 MB, 93.79 / 0.12 ms  (average mu = 0.121, current mu = 0.068)
  allocation failure; scavenge might not succeed

FATAL ERROR: Ineffective mark-compacts near heap limit
Allocation failed - JavaScript heap out of memory
```

Mark-Compact  1-2 MB reachable

---

##  heap  replay

 heap  heap  JSONL replay:

-  `NODE_OPTIONS`
-  runtime profiler heap
-  CLI  rewound JSONL  fresh session
-  `QWEN_HOME` MCP  hooks
-  process-tree RSS

| CLI                  |  |    | Tree RSS  | Root RSS  | Worker RSS  |                                                         |
| -------------------- | ---- | -----: | ------------: | ------------: | --------------: | ----------------------------------------------------------- |
| installed `qwen`     |  | 167.3s |     838.0 MiB |     230.2 MiB |       566.3 MiB |  fresh run retry  |
| local rebuilt bundle |  | 106.3s |     527.5 MiB |     182.1 MiB |       345.4 MiB |  clone                                    |

 heap replay :

1.  review JSONL  MiB  0.8 GiB  process-tree RSS
    4G/8G OOM
2.  rebuilt bundle  replay  installed CLI
   history clone 
3.  OOM  4G/8G OOM 
   tool-result  MCP/tool schema  replay 

## 

### OOM 

```
+-----------------------------------------------------------+--
| Layer 3: V8 Heap Limit (512MB/2GB/4GB)                  | <- 
|-----------------------------------------------------------
| Layer 2: structuredClone()  ( ~2x)         | <- 
|-----------------------------------------------------------
| Layer 1: History  tool result  ()         | <- 
|-----------------------------------------------------------
| Layer 0: Token compaction                       | <- 
\_------------------------------------------------------------
```

### 

```
sendMessage()
  -> tryCompress()
    -> heapPressureRatio < threshold (safety net disabled)
    -> ChatCompressionService.compress()
      -> chat.getHistory(true)
        -> structuredClone(this._history)   <- 
          -> V8  ~N MB  clone
          ->  existing heap + N > limit -> OOM
```

### 

|                                     |                                            |
| --------------------------------------- | ---------------------------------------------- |
| Task #5->#6: Context 5.9%->4.0% ()    | Token compaction ****                |
| Task #5->#6: RSS 515->649 MB ( 134MB) | Compaction  `structuredClone`  |
| GC  1-2 MB                      |  livehistory + clone       |
| #4309  8GB limit                  | history clone  limit     |

: heap  issue  heap replay
"clone  RSS" 4G/8G OOM

###  128K context window 

- 128K * 70% = ~90K tokens  compaction
-  context window (1M)  70% = 700K tokens
- **compaction  -> structuredClone  -> OOM **
- DeepSeek  contextWindowSize  128K

---

## .5

 crash session  debug  session id


 session  `2026-05-19T13:26:35Z` ( 21:26:35)crash 
`2026-05-19T13:32:10Z` ( 21:32:10)

### Heap Pressure  Auto-Compaction 

```
13:29:43 [WARN]  Heap pressure at 74.9%; attempting auto-compaction before token threshold.
13:30:06 [DEBUG] [FILE_READ_CACHE] clear after auto tryCompress    <- compaction #1 
13:30:13 [WARN]  Heap pressure at 70.7%; attempting auto-compaction before token threshold.
                 <-  heap  74.9%  70.7%
13:30:52 [DEBUG] Heap pressure at 86.0%; skipping heap-pressure auto-compaction during cooldown.
                 <- 30s cooldown 
13:30:56 [WARN]  Heap pressure at 85.3%; attempting auto-compaction before token threshold.
                 <- cooldown heap  85.3%
13:31:21 [DEBUG] [FILE_READ_CACHE] clear after auto tryCompress    <- compaction #2 
13:31:37 [WARN]  Heap pressure at 88.8%; attempting auto-compaction before token threshold.
                 <-  heap  88.8%
13:32:09 [DEBUG] Heap pressure at 90.2%; skipping heap-pressure auto-compaction during cooldown.
                 <- heap  90.2%cooldown 
13:32:10 <-  OOM crash
```

### 

|                                                                               |                                                       |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 2.5  **4 ** heap-pressure auto-compaction  2  cooldown  | #3735  `tryCompress`                |
|  compaction  heap  >70%                                               | `structuredClone()`           |
| 74.9% -> 70.7% -> 86% -> 85.3% -> 88.8% -> 90.2% -> crash                                   | :->clone ->heap ->->         |
|  90.2%  1                                                             |  `getHistory(true)`  `structuredClone()`  |
| `[FILE_READ_CACHE] clear after auto tryCompress`  2                             |  compaction  compress -> setHistory  |

### 

```
heap  (>70%)
  ->  heap-pressure auto-compaction
    -> tryCompress()  getHistory(true)
      -> structuredClone(this._history)  <-  heap  +30~40%
        -> compaction  history
          ->  clone  heap 
            ->  send 
              -> heap  ->  -> crash
```

---

## .6: 0.15.7 ~ 0.15.11  OOM 

###  commit 

|          | PR                                                   |                                                                                 |  `structuredClone`  |
| ------------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------- |
| **v0.15.6**  | --                                                    | `getHistory(true)`  `sendMessage`  1                                  | : send 1  clone          |
| **v0.15.7**  | **#3735** `auto-compact subagent context`            |  `tryCompress()`  `GeminiChat`** send ** compaction   | **+1 **:send  compress     |
| **v0.15.10** | **#3879** `reactive compression on context overflow` |  provider  context overflow  `tryCompress()` + `getHistory(true)` | **+1~2 **:overflow retry     |
| **v0.15.10** | **#3985** `harden reactive compression`              |  reactive compression                                                   |                                 |

### v0.15.6 vs v0.15.11  `getHistory(true)` 

**v0.15.6** (2 ):

```
L367: const requestContents = this.getHistory(true);          <- send  request
L618: const recoveryContents = self.getHistory(true);         <- MAX_TOKENS escalation ()
```

**v0.15.11** (5 ):

```
L467: ChatCompressionService.compress()               <- #3735:  send  auto-compact
L574: requestContents = this.getHistory(true);                <- send  request
L724: reactive tryCompress()                          <- #3879: context overflow  retry
L739: requestContents = self.getHistory(true);                <- #3879: retry  request
L943: const recoveryContents = self.getHistory(true);         <- MAX_TOKENS escalation
```

### : send  4  `structuredClone`

```
sendMessage()
  -> tryCompress()              <- #3735: getHistory(true) [clone #1]
  -> getHistory(true)           <-  request [clone #2]
  -> API  context overflow
    -> reactive tryCompress()   <- #3879: getHistory(true) [clone #3]
    -> getHistory(true)         <- retry request [clone #4]
```

### 

**#3735 (v0.15.7)**  OOM ----
`sendMessage`  `tryCompress()` `tryCompress` 
`ChatCompressionService.compress()` -> `chat.getHistory(true)`  `structuredClone`
 history  " clone "  ~1.3x  ~2x+
:issue history  OOM  #3735  #3735  structuredClone
 OOM 

**#3879 (v0.15.10)** ---- heap  (provider  context overflow)
 clone session  crash

---

## #4186 

 heap-pressure safety net (HEAP_PRESSURE_COMPRESSION_RATIO = 0.7) :

|             |  safety net    |  safety net           |
| --------------- | ------------------ | ------------------------- |
| OOM         | 7  crash |  >10    |
| RSS         | 666 MB -> crash     | 555 MB -> GC  280 MB |
| Compaction  |  token threshold | heap 70%        |
| Context     | 5.9%->4.0%->crash    | 22.7%->17.0%   |

****: #4186  heap-pressure safety net  OOM****:

-  history  heap  60%+ compactclone 
-  #4309  8GB limit  crash

---

## 

 RSS :

|                          |    |                     |
| -------------------------------- | ------ | --------------------------- |
| `this._history[]` (tool results) | 40-50% |  +30-100MB    |
| `structuredClone()`      | 30-40% | compaction  |
| V8 runtime (GC metadata, code)   | ~15%   |                     |
| UI/logging/stream buffers        | ~5%    |                     |

---

## 

### 

```bash
#!/bin/bash
# /tmp/oom-simple-driver.sh <tmux-session-name>
SESSION="$1"

TASKS=(
  " Read  packages/core/src/core/geminiChat.ts"
  " Read  packages/core/src/tools/agent/agent.ts"
  " grep -rn structuredClone packages/core/src  Read  3 "
  " Read  packages/cli/src/ui/hooks/slashCommandProcessor.ts"
  " Read  packages/core/src/services/chatCompressionService.ts"
  " find packages/cli/src/ui/commands -name '*.ts'  Read"
  " Read  packages/core/src/core/turn.ts"
  # ... 
)

i=0
while true; do
  TASK="${TASKS[$((i % ${#TASKS[@]}))]}"
  i=$((i + 1))

  QWEN_PID=$(ps aux | grep "dist/index.js" | grep -v grep | awk '{print $2}' | sort -rn | head -1)
  RSS=$(ps -o rss= -p $QWEN_PID 2>/dev/null)
  [ -z "$RSS" ] && { echo "CRASH after $((i-1)) tasks!"; exit 0; }

  RSS_MB=$(echo "scale=1; $RSS/1024" | bc)
  CTX=$(tmux capture-pane -t "$SESSION:1" -p 2>/dev/null | grep -oE "[0-9]+\.[0-9]+% " | tail -1)
  echo "[$(date +%H:%M:%S)] #$i RSS:${RSS_MB}MB Ctx:$CTX | ${TASK:0:55}"

  tmux send-keys -t "$SESSION:1" C-u
  sleep 0.2
  tmux send-keys -t "$SESSION:1" "$TASK" Enter
  sleep 0.5
  tmux send-keys -t "$SESSION:1" Enter
  sleep 45
done
```

### 

```bash
# 1.  heap-pressure safety net
# geminiChat.ts: HEAP_PRESSURE_COMPRESSION_RATIO = 99.0

# 2. Build
npm run build --workspace=packages/core && npm run build --workspace=packages/cli

# 3.  qwen (128K context model, 512MB heap)
SESSION="oom-test"
tmux new-session -d -s "$SESSION" -c "$REPO_DIR"
tmux send-keys -t "$SESSION" \
  "NODE_OPTIONS='--max-old-space-size=512' node packages/cli/dist/index.js --model 'qwen3.6-plus'" Enter

# 4. 
sleep 10
bash /tmp/oom-simple-driver.sh "$SESSION"
```

---

## 

### 

- [x] #4186: heap-pressure auto-compaction safety net (0.7 threshold)
- [x] #4188: fileReadCache / crawlCache 

### 

- [ ]  `structuredClone()`  -- `nextSpeakerChecker`  clone 
- [ ] Compaction  slice +  deep clone
- [ ]  tool result (>100KB) history 

### 

- [ ] Tool result offload  + lazy load (#4184)
- [ ]  RSS  token count
- [ ] History 
