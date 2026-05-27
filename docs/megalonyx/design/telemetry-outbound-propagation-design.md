# Telemetry: Outbound Trace Context & Session ID Header Propagation

>  issue: [#4384](https://github.com/QwenLM/qwen-code/issues/4384)
>  issue: [#3731](https://github.com/QwenLM/qwen-code/issues/3731) (P3 deeper observability)
>  PR: #4367 (resource attributes -- merged 2026-05-21, commit `64401e1`)
>  2026-05-21  qwen-code main  +  claude-code 

## 

|  |        |                                           |                                                                                                                                                                                                                                                                               |
| ---- | ---------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1   | 2026-05-21 |                                           | : LLM  `X-Qwen-Code-Session-Id` + `traceparent`                                                                                                                                                                                                            |
| R2   | 2026-05-22 | wenshao R2/R3 review                          | :URL normalizeport matchingquote staticCorrelationHeaders try/catchhost:port fallback strip                                                                                                                                                                  |
| R3   | 2026-05-23 | LaZzyMan REQUEST_CHANGES                      | ****:`X-Qwen-Code-Session-Id`  first-partyAlibaba/DashScopehost  11                                                                                                                                                                 |
| R4   | 2026-05-25 | LaZzyMan round-8 follow-up (scope conflation) | **PR scope **: PR  client HTTP span + OTLP loop guard`traceparent`  offNoopTextMapPropagator `outboundCorrelation.*`  namespace  toggleR3  `X-Qwen-Code-Session-Id` ** PR** follow-up PR 12 |

****: 3.1/ 3.2/ 4.3Part B / 4.4 schema / 5/ 9 claude-code / 10/ 11R3 host-allowlist scoping 12 ---- **R4  R1-R3 " PR  traceparent + session id header"**: PR  telemetry observability +  outbound trace-context toggle outbound correlation header  R3  host allowlist follow-up PRR3  follow-up PR 

## 1. 

#4367 **emitted telemetry  attribute  cardinality** span/log/metric  `user.id`/`tenant.id` :**outbound LLM  HTTP header** qwen-code  DashScope / OpenAI / Gemini / Anthropic ** cross-process correlation header**---- W3C `traceparent` session id

:

1. trace context  qwen-code  ARMS Tracing  DashScope OTel instrumentation span  qwen-code  trace  trace tree 
2.  session id  wire  qwen-code  metric/log  trace id  header 
3.  trace  client-side HTTP span `api.generateContent`  TTFB /  / 

## 2. 

### 2.1  `HttpInstrumentation`

`packages/core/src/telemetry/sdk.ts:330`:

```ts
instrumentations: [new HttpInstrumentation()],
```

`HttpInstrumentation`  hook Node  `http`/`https` **** `globalThis.fetch` / undici 

### 2.2  LLM SDK  fetch / undici

| SDK                                              | HTTP                                                                                                                           | `HttpInstrumentation`  |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `openai@5.11.0`                                  | `globalThis.fetch`Node 18+  undici:`node_modules/openai/internal/shims.mjs`  `'fetch' is not defined as a global` |                              |
| `@google/genai@1.30.0`                           | `globalThis.fetch` + `new Headers()`:`dist/node/index.mjs`  `new Headers()`                                         |                              |
| `@anthropic-ai/sdk`anthropicContentGenerator |  fetch                                                                                                                     |                              |

### 2.3  manual propagation

```
grep -rn "propagation\.\|setGlobalPropagator\|W3CTraceContext\|traceparent" packages/core/src --include="*.ts" | grep -v "\.test\."
```

->  `propagation.inject()`  traceparent 

### 2.4  provider  `defaultHeaders` 

OpenAI  `openai` SDK:

 OpenAI  provider  `extends DefaultOpenAICompatibleProvider`**buildHeaders override ** grep audit :

| Provider   |                    | `buildHeaders()`                                                                    |                                            |
| ---------- | ---------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------- |
|        | `default.ts:63-74`     |  `{ 'User-Agent' }` + customHeaders                                                 |                                          |
| DashScope  | `dashscope.ts:110-124` | **`override`  call `super`**---- `User-Agent` + `X-DashScope-*`           | **** correlation header  |
| OpenRouter | `openrouter.ts:20-30`  | `override` ** `const baseHeaders = super.buildHeaders()`**                          |                                |
| DeepSeek   | `deepseek.ts`          |  override `buildHeaders` override `buildRequest` / `getDefaultGenerationConfig` |                                |
| Minimax    | `minimax.ts`           |  deepseek                                                                             |                                      |
| Mistral    | `mistral.ts`           |  deepseek                                                                             |                                      |
| ModelScope | `modelscope.ts`        |  deepseek                                                                             |                                      |

-> **OpenAI  2 **:`default.ts`  `dashscope.ts` 5 

Google Gemini:

| Provider |                            |                                                      |
| -------- | ------------------------------ | -------------------------------------------------------------- |
| Gemini   | `geminiContentGenerator.ts:59` | `new GoogleGenAI({ httpOptions: { headers } })` -- SDK  |

Anthropic:

| Provider  |                                                                                                    |        |
| --------- | ------------------------------------------------------------------------------------------------------ | ---------------- |
| Anthropic | `anthropicContentGenerator.ts:177` (`buildHeaders`) + `:212` (`defaultHeaders` arg to `new Anthropic`) | `defaultHeaders` |

** 4  SDK ** session id header SDK  `defaultHeaders` / `httpOptions.headers` fetch wrapper

### 2.5  proxy  fetch 

`provider/default.ts:87-89`:

```ts
const runtimeOptions = buildRuntimeFetchOptions(
  'openai',
  this.cliConfig.getProxy(),
);
```

`buildRuntimeFetchOptions`  proxy  `{ fetch: customFetch }`  `setGlobalDispatcher(new ProxyAgent(...))` `config.ts:1126-1128`**undici  dispatcher  `UndiciInstrumentation` **---- monkey-patch `globalThis.fetch`  undici  channel diagnostics  dispatcher

## 3.  / 

### 3.1 

-  outbound LLM  W3C `traceparent` headerOTel SDK  `W3CTraceContextPropagator`
- ~~~~  LLM  `X-Qwen-Code-Session-Id` headerclaude-code  -- **R3 **: first-party (Alibaba/DashScope) host  provider  11
-  OTLP exporter endpoint  tracefeedback loop
-  LLM  client span vs 
-  4  provider :OpenAI DashScope overrideGeminiAnthropic
- streaming  / proxy  / 
-  #4367 : `defaultHeaders`  SDK-native  -- **R1 **: staleness  fetch wrapper**R3 **:fetch wrapper  host gate

### 3.2 

- **`baggage` header**: SDK  qwen-code  `propagation.setBaggage()`
- **subprocess `TRACEPARENT` env var **:claude-code  Bash/PowerShell  `TRACEPARENT`qwen-code  `BashTool`  follow-up sub-issue
- **inbound `TRACEPARENT` / `TRACESTATE` **:claude-code  `-p`  Agent SDK  env  traceparent  traceqwen-code  follow-up
- **`X-Qwen-Code-Request-Id`**:claude-code  `x-client-request-id` correlation  sub-issue
- ** propagatorB3 / Jaeger / X-Ray**: W3C  99%  future config option
- ~~**per-endpoint **:claude-code  endpoint (Bedrock / Vertex)  traceparentqwen-code ~~ -- **R3 **:LaZzyMan review  qwen-code  CLI  providerOpenAI / Anthropic / OpenRouter / claude-code  first-party->first-party session id header  host  11`traceparent`  R1 OTel  header trace id  `sha256(sessionId)`  follow-up  per-destination toggle`telemetry.propagateTraceContext`

## 4. 

### 4.1 

```
+--- qwen-code process --------------------------------------------+--
|                                                                |
|  +--- session-tracing.ts -+--                                     |
|  | active span ctx      |                                     |
|  \_------------------------                                     |
|         |                                                      |
|                                                               |
|  +--- propagation.inject() (called by undici instrumentation) -+--|
|  | writes `traceparent: 00-<traceId>-<spanId>-01` to headers ||
|  \_----------------------------------------------------------------|
|         |                                                      |
|  +----------------------------------------------------------+--  |
|  |   fetch() -- undici, instrumented                        |  |
|  |   creates HTTP client span                              |  |
|  |   injects traceparent into request headers              |  |
|  |   (skipped via ignoreRequestHook if endpoint is OTLP)   |  |
|  \_------------------------------------------------------------  |
|         |                                                      |
|         |   +--- defaultHeaders (per SDK constructor) -------+--  |
|         |   | { 'X-Qwen-Code-Session-Id': sessionId, ... } |  |
|         \_------------------------------------------------------ |
|             |                                                  |
\_---------------------------------------------------------------------
              |
               outbound HTTP
   POST /v1/chat/completions
   traceparent: 00-...
   X-Qwen-Code-Session-Id: ...
   ... (existing User-Agent, X-DashScope-*, etc.)
```

:

| Layer                    |                               |                                                       |
| ------------------------ | ------------------------------------- | ------------------------------------------------------------- |
| `traceparent`            |  fetch                      | `UndiciInstrumentation`  OTel SDK  propagator |
| `X-Qwen-Code-Session-Id` | SDK  `defaultHeaders` |                                                       |

### 4.2 Part A -- `traceparent` via undici instrumentation

****:`packages/core/src/telemetry/sdk.ts`

```ts
import { UndiciInstrumentation } from '@opentelemetry/instrumentation-undici';

// ...
const otlpUrls = [
  config.getTelemetryOtlpEndpoint(),
  config.getTelemetryOtlpTracesEndpoint(),
  config.getTelemetryOtlpLogsEndpoint(),
  config.getTelemetryOtlpMetricsEndpoint(),
]
  .filter((u): u is string => !!u)
  .map((u) => u.replace(/\/$/, ''));

instrumentations: [
  new HttpInstrumentation(),
  new UndiciInstrumentation({
    ignoreRequestHook: (request) => {
      // request.origin = "https://collector:4318", request.path = "/v1/traces"
      const url = `${request.origin}${request.path}`;
      return otlpUrls.some((e) => url.startsWith(e));
    },
  }),
],
```

####  `ignoreRequestHook` 

OTel SDK  fetch  POST  OTLP collectorUndiciInstrumentation "" span ->  span  ->  /  OTel OTel  hook

####  propagator

OTel SDK `NodeSDK`  `textMapPropagator`  `CompositePropagator([W3CTraceContextPropagator, W3CBaggagePropagator])`

#### `traceparent` 

```
traceparent: 00-<32hex traceId>-<16hex spanId>-<01 sampled | 00 not sampled>
              --                                          --
               version ( 00)                            flags
```

 55 bytes padding

#### `tracestate`  `baggage`

- `tracestate`:  inject OTel SDK 
- `baggage`:  `propagation.setBaggage(ctx, ...)` qwen-code 

### 4.3 Part B -- `X-Qwen-Code-Session-Id` via fetch wrapperOpenAI / Anthropic+ static headersGemini

> **R3 **: fetch wrapper  staleness  4  provider  --  wrapper  host allowlist gate`staticCorrelationHeaders`  `destinationUrl`  host gate  default allowlist  11

#### Critical:staleness 

`defaultHeaders`  bake-in `getSessionId()`** bug**:

1. `pipeline.ts:60`  contentGenerator  `this.client = this.config.provider.buildClient()`SDK client  `defaultHeaders`  capture  session id
2. `config.ts:1850`  session reset `/clear`  `this.sessionId`  `refreshSessionContext()`** contentGenerator**
3.  LLM  client -> wire header  session id ->  correlation 

->  session id **per-request** bake at

#### 

```
                   +--- fetch  -+--  
OpenAI SDK          |            |  fetch wrapper (per-request  sessionId) 
Anthropic SDK       |            |  fetch wrapper 
@google/genai SDK   |            |  static httpOptions.headers +  staleness
                   \_-----------------
```

`@google/genai`'s `HttpOptions` interface  `fetch` grep `node_modules/@google/genai/dist/genai.d.ts` : `baseUrl`/`apiVersion`/`headers`/`timeout`/`extraParams` Gemini  static headers OpenAI/Anthropic ---- **known limitation** 8.6

#### per-request fetch wrapper

 `packages/core/src/telemetry/llm-correlation-fetch.ts`:

```ts
import type { Config } from '../config/config.js';

/**
 * Wrap a fetch implementation so every outbound request gets correlation
 * headers (`X-Qwen-Code-Session-Id`) populated from the **current** session
 * id, not the value captured when the SDK client was constructed.
 *
 * Matches claude-code's pattern (src/services/api/client.ts:370-390 --
 * `buildFetch()`). Per-request injection is necessary because `/clear`
 * resets the session id mid-process; SDK clients (and their static
 * `defaultHeaders`) are NOT recreated on reset.
 *
 * Caller responsible for choosing the base fetch -- usually
 * `runtimeOptions?.fetch ?? globalThis.fetch` so proxy-aware fetch is
 * preserved when ProxyAgent is in use.
 *
 * If telemetry is disabled, returns baseFetch unchanged (no correlation
 * header is added, matching the privacy stance of 3.1).
 */
export function wrapFetchWithCorrelation(
  baseFetch: typeof fetch,
  config: Config,
): typeof fetch {
  return async function correlationFetch(input, init) {
    if (!config.getTelemetryEnabled()) {
      return baseFetch(input, init);
    }
    const sid = config.getSessionId();
    if (!sid) {
      // Defensive: empty header value is rejected by some HTTP middleware.
      // Skip injection rather than send `X-Qwen-Code-Session-Id: `.
      return baseFetch(input, init);
    }
    const headers = new Headers(init?.headers);
    headers.set('X-Qwen-Code-Session-Id', sid);
    return baseFetch(input, { ...init, headers });
  };
}
```

Companion helper for the SDKs that can only take static headers (Gemini):

```ts
/**
 * Static correlation headers. Captures the session id at call time --
 * **subject to staleness** if the host SDK keeps these headers in a
 * captured-at-construction slot (e.g. `@google/genai`'s `httpOptions.headers`).
 * Prefer `wrapFetchWithCorrelation` whenever the SDK exposes a `fetch` hook.
 */
export function staticCorrelationHeaders(
  config: Config,
): Record<string, string> {
  if (!config.getTelemetryEnabled()) return {};
  return { 'X-Qwen-Code-Session-Id': config.getSessionId() };
}
```

####  1: `provider/default.ts` (OpenAI )

`buildClient()` ----compose  `runtimeOptions.fetch`proxy wrapper:

```ts
buildClient(): OpenAI {
  // ... existing ...
  const runtimeOptions = buildRuntimeFetchOptions('openai', this.cliConfig.getProxy());
  const baseFetch =
    (runtimeOptions as { fetch?: typeof fetch } | undefined)?.fetch
    ?? globalThis.fetch;
  return new OpenAI({
    apiKey,
    baseURL: baseUrl,
    timeout,
    maxRetries,
    defaultHeaders,
    ...(runtimeOptions || {}),
    // After spread, override `fetch` so our correlation wrapper wraps the
    // proxy-aware fetch (or globalThis.fetch when no proxy).
    fetch: wrapFetchWithCorrelation(baseFetch, this.cliConfig),
  });
}
```

`buildHeaders()` itself unchanged.

####  2: `provider/dashscope.ts` (override)

`buildClient()`  compose  override buildClient`buildHeaders()` 

####  3: `geminiContentGenerator/index.ts` (factory, NOT )

****:`geminiContentGenerator.ts` ****`index.ts:48`  factory  `gcConfig: Config`line 33  `gcConfig?.getUsageStatisticsEnabled()` factory  correlation  headers merge  `httpOptions.headers`:

```ts
// geminiContentGenerator/index.ts
let headers: Record<string, string> = { ...baseHeaders };
if (gcConfig?.getUsageStatisticsEnabled()) {
  // ... existing x-gemini-api-privileged-user-id ...
}
headers = { ...headers, ...staticCorrelationHeaders(gcConfig) }; // <- 
const httpOptions = config.baseUrl
  ? { headers, baseUrl: config.baseUrl }
  : { headers };
// new GeminiContentGenerator(...) unchanged
```

 signature 

####  4: `anthropicContentGenerator.ts`

Anthropic SDK  custom `fetch` `buildRuntimeFetchOptions` `buildClient`  fetch wrap  OpenAI default.ts`buildHeaders` 

#### 

: `customHeaders`  `defaultHeaders` merge  8.2 spoofing fetch wrapper  `X-Qwen-Code-Session-Id`  SDK  headers list **** `Headers` ---- Node `Headers.set()`  user  customHeaders  header

** OpenAI/Anthropicfetch wrapper **:correlation > customHeaders > SDK defaults
** Geministatic headers **:customHeaders > correlation > SDK defaults spread 

 fetch wrapper  spoofing fetch wrapper  SDK headers  **bug **---- 8.2 

### 4.4  schema 

~~**** setting~~ -- **R3 **: setting `telemetry.sessionIdHeaderHosts: string[]` first-party host schema  `packages/cli/src/config/settingsSchema.ts` override `["*"]`  / `[]`  /  11 R3 :

- `traceparent`  telemetry enabled  toggle
- `X-Qwen-Code-Session-Id`  telemetry enabled 
- `ignoreRequestHook`  OTLP url  config 

 setting**out of scope**:

- `telemetry.outboundCorrelationHeader`:  header name `X-Qwen-Code-Session-Id`
- `telemetry.outboundPropagationDisabled`:  LLM  header 
- ~~per-destination header scope toggle~~ -- **R3 ** 11

## 5. 

|                                                                             |  |                                                                                                                                                             |
| ------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `packages/core/package.json`                                                    |    | `@opentelemetry/instrumentation-undici`                                                                                                                         |
| `packages/core/src/telemetry/sdk.ts`                                            |      | +`UndiciInstrumentation` + `ignoreRequestHook`                                                                                                                  |
| `packages/core/src/telemetry/llm-correlation-fetch.ts`                          |    | `wrapFetchWithCorrelation()` (OpenAI/Anthropic) + `staticCorrelationHeaders()` (Gemini fallback)                                                                |
| `packages/core/src/core/openaiContentGenerator/provider/default.ts`             |      | `buildClient()`  `new OpenAI({...})`  `fetch: wrapFetchWithCorrelation(baseFetch, cliConfig)`                                                             |
| `packages/core/src/core/openaiContentGenerator/provider/dashscope.ts`           |      | override `buildClient`                                                                                                                                  |
| `packages/core/src/core/geminiContentGenerator/index.ts`                        |      | factory  merge `staticCorrelationHeaders(gcConfig)`  `httpOptions.headers`**caller  Config signature ** --  over-specification |
| `packages/core/src/core/anthropicContentGenerator/anthropicContentGenerator.ts` |      | `buildClient`  `wrapFetchWithCorrelation`  SDK  `fetch` option                                                                                      |

** audited ** reviewer :

- `packages/core/src/qwen/qwenContentGenerator.ts` -- `extends OpenAIContentGenerator` `DashScopeOpenAICompatibleProvider`** dashscope.ts  buildClient ** Qwen OAuth 
- `packages/core/src/core/loggingContentGenerator/loggingContentGenerator.ts` -- wrapper  SDK client contentGenerator  telemetry logging
- `packages/core/src/core/contentGenerator.ts` -- factory  client
  | `packages/core/src/telemetry/sdk.test.ts` |  |  undici instrumentation  + ignoreRequestHook  |
  | `packages/core/src/telemetry/llm-correlation-fetch.test.ts` |  | telemetry-on/off  + per-request  sessionId critical:session reset  wrapped fetch  id |
  |  provider  `*.test.ts` |  |  SDK  `fetch` option  wrapped OpenAI/Anthropic Gemini  `httpOptions.headers`  `X-Qwen-Code-Session-Id` |
  | `docs/developers/development/telemetry.md` |  |  "Trace context & session correlation propagation"  |
  | `docs/design/telemetry-outbound-propagation-design.md` |  |  |

## 6.  PR 

 review  PR:

### PR 1 -- `traceparent` structural

-  `@opentelemetry/instrumentation-undici` 
- `sdk.ts`  `UndiciInstrumentation` + `ignoreRequestHook`
- :SDK OTLP endpoint  trace
- 

****:Additive client span  net  span 

### PR 2 -- `X-Qwen-Code-Session-Id` header helper 

-  `llm-correlation-headers.ts`
- 4  provider 
- : provider  header telemetry-off 
- 

****:- `geminiContentGenerator` 

### PR 3 -- Docs + E2E verify

-  `telemetry.md` 
-  E2E verify script `/tmp/verify-telemetry-pr-4367.mjs` : fetch +  header

 PR 2 

### 

PR 1  PR 2 ****----** PR 1 **:

- `traceparent`  OTel **** header OTel-aware collector /  -> 
- `X-Qwen-Code-Session-Id` **** header -> 
-  PR 2 review PR 1  cross-process trace 
- PR 1  additive structural

## 7. 

### 7.1 `sdk.ts` 

-  `UndiciInstrumentation`  `NodeSDK`  `instrumentations` 
-  `ignoreRequestHook`  `https://collector:4318/v1/traces`  true
-  `ignoreRequestHook`  `https://dashscope.aliyuncs.com/...`  false
-  trailing slash  trailing slash 

### 7.2 `llm-correlation-fetch.ts` 

**`wrapFetchWithCorrelation`**:

|                                                     |                                                                    |
| ------------------------------------------------------- | ---------------------------------------------------------------------- |
| `getTelemetryEnabled() === false`                       | wrapped fetch = baseFetch header                           |
| `getTelemetryEnabled() === true`, sessionId = "abc-123" | wrapped fetch  init.headers  `X-Qwen-Code-Session-Id: abc-123` |
| `init.headers`  `X-Qwen-Code-Session-Id: spoof`     | wrapper  sessionIdfetch wrapper  spoof8.1   |
| **session reset  wrapped fetch **           | ** sessionId**regression guard for staleness fix             |
| baseFetch reject                                        | wrapper  reject                                                |

**`staticCorrelationHeaders`**Gemini path:

|                                                     |                                                          |
| ------------------------------------------------------- | ---------------------------------------------------------------- |
| `getTelemetryEnabled() === false`                       | `{}`                                                             |
| `getTelemetryEnabled() === true`, sessionId = "abc-123" | `{ 'X-Qwen-Code-Session-Id': 'abc-123' }`                        |
| sessionId  unicode`-1`                      | ----HTTP header value  SDK                       |
| sessionId                                     | `{ 'X-Qwen-Code-Session-Id': '' }`---- invariant |

### 7.3 Per-provider 

 provider  `buildHeaders()` / :

```ts
it('includes X-Qwen-Code-Session-Id when telemetry enabled', () => {
  const config = makeFakeConfig({
    sessionId: 'sess-xyz',
    telemetry: { enabled: true },
  });
  const provider = new DefaultProvider(genConfig, config);
  expect(provider.buildHeaders()['X-Qwen-Code-Session-Id']).toBe('sess-xyz');
});

it('omits X-Qwen-Code-Session-Id when telemetry disabled', () => {
  const config = makeFakeConfig({ telemetry: { enabled: false } });
  const provider = new DefaultProvider(genConfig, config);
  expect(provider.buildHeaders()).not.toHaveProperty('X-Qwen-Code-Session-Id');
});
```

### 7.4 E2E verificationtmux + local HTTP server

 **** mock `globalThis.fetch`  header:`UndiciInstrumentation`  undici  diagnostics channel hookmonkey-patching globalThis.fetch  bypass instrumentation patch  `traceparent` ** local HTTP server** SDK server  headers

 `/tmp/verify-telemetry-pr-4367.mjs` :

1. `http.createServer((req, res) => { capturedHeaders.push(req.headers); res.end('{}') })`  server
2.  telemetry + outfile +  OpenAI SDK  `baseURL`  `http://127.0.0.1:<port>` mock provider  SDK  fetch
3.  `client.chat.completions.create(...)` mock  SDK ---- server  OpenAI 
4.  `capturedHeaders[0]`  `traceparent: 00-...`  `X-Qwen-Code-Session-Id: <sessionId>`
5.  OTLP collector mock  different port OTLP **** `traceparent`  `ignoreRequestHook`
6. **:staleness ** -- emit request 1 -> call `config.resetSession(...)` -> emit request 2 ->  request 2  `X-Qwen-Code-Session-Id`  session id** #1 fix **

### 7.5 

- streaming chat completion  fetch `stream: true`----`UndiciInstrumentation`  streaming response  span lifecycle  bug** streaming completion  client span  end +  leaked span + **
- proxy mode (`ProxyAgent`)  instrumentation ----`ignoreRequestHook`  endpoint proxy 
- `maxRetries` client span `traceparent` parent retry  span  child span --  SDK 

## 8.  / 

### 8.1 customHeaders override  spoofing 

 provider  spoofing ****:

| Provider                            | spoofing ? |                                                                                                                 |
| --------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------- |
| OpenAI / Anthropic (fetch wrapper ) |   spoof  | fetch wrapper  SDK headers list  `headers.set('X-Qwen-Code-Session-Id', ...)` user customHeaders  |
| Gemini (static headers )            |   spoof    | merge  `{ ...baseHeaders, ...correlationHeaders, ...customHeaders }`----customHeaders                       |

claude-code  fetch wrapper  OpenAI/Anthropic spoofing  staleness bug 

**""**----Gemini  SDK  `fetch` hook OpenAI  static 

Session id spoofing  source code reviewer  fetch wrapper  spoof  customHeaders 

### 8.2 OTLP collector URL  edge case

#### (a) Auth token in URL

 OTLP endpoint  `https://collector/path?token=secret``ignoreRequestHook`  `url.startsWith(e)`  query string undici  `request.path`  path query `e`  path  query:

```ts
const otlpUrls = [...]
  .map((u) => u.replace(/\?.*$/, '').replace(/\/$/, ''));
```

#### (b) startsWith  hostname  false positive

 `e = "http://collector"` port url = `http://collector-fake/v1/traces`  startsWith 

****:

- OTLP endpoint  port4317 gRPC / 4318 HTTP`http://collector:4318`  `-fake` port  `/`
-  endpoint  port  SDK  fallback

** harden**: URL origin + path  startsWith:

```ts
const parsed = otlpUrls.map((u) => new URL(u));
return parsed.some(
  (e) =>
    `${request.origin}` === e.origin && request.path.startsWith(e.pathname),
);
```

----false positive 

### 8.3 Vertex AI  Gemini

`@google/genai`  `vertexai: true`  GCP  Vertex  generative ai endpoint fetch instrumentation `httpOptions.headers` 

### 8.4 Anthropic SDK  `defaultHeaders` 

`anthropicContentGenerator.ts:177`  `buildHeaders()`  `new Anthropic({ defaultHeaders })` staleness ---- `fetch` wrapper  OpenAI 

### 8.5 SDK  fetch  trailer header

`openai` SDK  streaming  `Transfer-Encoding: chunked`  trailer headers request-time  `traceparent` / `X-Qwen-Code-Session-Id` ----

### 8.6  Known limitation: Gemini  session id  `/clear`  stale

 `@google/genai` SDK  `fetch` hook`HttpOptions`  `baseUrl`/`apiVersion`/`headers`/`timeout`/`extraParams`Gemini provider  static `httpOptions.headers` ----session id  SDK  capture**`/clear`  session reset **

****:

-  qwen-code -> `/clear` ->  Gemini  -> wire  `X-Qwen-Code-Session-Id`  session id
-  correlation trace id  log  session wire header 

****:

- OpenAI / Anthropic ** bug**fetch wrapper  per-request  session id
- Gemini fix path  scope

**Future fix path **:

|                                           |                                                                                  |                                                                                       |
| --------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **A. Lazy invalidate**                   | session reset  mark contentGenerator dirty LLM  lazy recreate        | :~10  `resetSession` + LLM  API                            |
| B. Eager recreate                             | session reset  `await createContentGenerator(...)` async  `resetSession` | :API                                                                       |
| C. Proxy headers object                       |  `httpOptions.headers`  Proxy  getter                                        | :`@google/genai`  per-request  headers  silently break |
| D.  `@google/genai`  `fetch` option |  PR  google-deepmind/generative-ai-js                                            |                                                                               |

****: Gemini provider  `/clear`  LLM wire  session id  trace correlation spans/logs  session.id 

 follow-up sub-issue  A

## 9.  claude-code 

|                          | claude-code                                                                                                                                          | qwen-code                                                                                                                                                               |                                                                                                                            |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Session id header        | `X-Claude-Code-Session-Id`                                                                                                               | `X-Qwen-Code-Session-Id`                                                                                                                                          |                                                                                                                  |
| Session id           | SDK `defaultHeaders``client.ts:108`+  `buildFetch()` wrapper`client.ts:370-390`per-request `randomUUID()`  `x-client-request-id` | OpenAI/Anthropic  fetch wrapperper-request  session id `/clear` stalenessGemini  static `httpOptions.headers`SDK                                    |  claude-code  fetch wrapper claude-code  fetch wrapper  per-request  `x-client-request-id`                 |
| Session id             | claude-code  `/clear`- session resetsession = process                                                                                        |  `/clear` reset -> fetch wrapper static headers  stale8.6                                                                                           | qwen-code                                                                                                              |
| Session id               | HTTP header baggage                                                                                                                          | HTTP header                                                                                                                                                                   |  ----backend                                                                                                                 |
| `traceparent`            |  docs  repo  `propagation.inject` / `UndiciInstrumentation`                                                            | `@opentelemetry/instrumentation-undici`                                                                                                                                   | claude-code  OTel                                                                        |
| `traceparent`        |  Anthropic API Bedrock/Vertex/Foundry                                                                                                  |  fetch (W3C trace id  `sha256(sessionId)` )**R3 **:session id header  first-party (Alibaba/DashScope)  11 | R3  qwen-code  session header  claude-code  first-party-only `traceparent`  per-destination toggle follow-up |
| `x-client-request-id` () |                                                                                                                                              |  follow-up sub-issue                                                                                                                                    |                                                                                                                            |
|  `TRACEPARENT` env     |                                                                                                                              |  follow-up                                                                                                                                                        |                                                                                                                            |
|  `TRACEPARENT`       | `-p` / Agent SDK                                                                                                                 |  follow-up                                                                                                                                                        |                                                                                                                            |

**verified vs documented **:

| claim                                           |                                                                                                                                           |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `X-Claude-Code-Session-Id` via `defaultHeaders` |  Open source `src/services/api/client.ts:108`                                                                                               |
| `x-client-request-id` via fetch wrapper         |  Open source `src/services/api/client.ts:370-390`                                                                                           |
| `traceparent`                               |   docs.claude.com/docs/en/monitoring-usage.md  repo `grep -rn "propagation\.inject\|UndiciInstrumentation\|traceparent" src`  |

## 10. 

 #3731 P3 ****:

- **`X-Qwen-Code-Request-Id`**  UUID per requestclaude-code :`x-client-request-id`/timeout error correlation ---- assign request id id R3 :per-request UUID """ LLM provider / header"
- **`traceparent`  per-destination scope toggle** -- R3  session id header `traceparent`  fetch  `telemetry.propagateTraceContext: 'trusted-hosts' | 'all' | 'none'` 11  allowlist 
- **Gemini  session id staleness lazy-invalidate fix**8.6  A:`/clear`  mark contentGenerator dirty LLM  lazy recreate Gemini  fetch wrapper 
- ** `TRACEPARENT` env**: `BashTool`  env trace tool execution lifecycle
- ** `TRACEPARENT`**:`--prompt`  env CI /  orchestrator  qwen-code  trace
- ** `correlationHeader` name**: ops  header `X-Qwen-Code-Session-Id`
- **`baggage` propagation **: set baggage  `user.id` / `tenant.id`  baggage 

## 11. R3  -- Host-Allowlist Scoping for `X-Qwen-Code-Session-Id`

> :[LaZzyMan  PR #4390  REQUEST_CHANGES review](https://github.com/QwenLM/qwen-code/pull/4390)
>  commit:`1c8528a56` () + `cb162e716` (Vertex baseUrl fail-closed + `["*"]` trim )

### 11.1 

R1  `X-Qwen-Code-Session-Id` **** LLM  `telemetry.enabled` LaZzyMan review :

1. ****:`feat(telemetry):` + `telemetry/`  + `getTelemetryEnabled()` gate " collector" `X-Qwen-Code-Session-Id`  OTLP  LLM API  DashScope / OpenAI / Anthropic / Gemini / OpenRouter / MiniMax / ModelScope / Mistral

2. **claude-code **:R1  9  fetch wrapper "" claude-code claude-code  Anthropic  -> Anthropic single vendor, single directionqwen-code  CLI ->  provider" cross-request UUID " R1 

3. **traceparent **:trace id = `sha256(sessionId).slice(0, 32)` per-session  session 

LaZzyMan  severity:session id `high` / traceparent `medium`

### 11.2 

** first-party hosts** setting:

```jsonc
"telemetry": {
  "sessionIdHeaderHosts": ["*"]                          //  R1 
  "sessionIdHeaderHosts": []                              //  header
  "sessionIdHeaderHosts": ["api.mycompany.com",
                           "*.gateway.mycompany.internal"]
}
```

 `packages/core/src/telemetry/trusted-llm-hosts.ts:DEFAULT_SESSION_ID_HEADER_HOSTS`:

```
dashscope.aliyuncs.com
dashscope-intl.aliyuncs.com
*.dashscope.aliyuncs.com
*.dashscope-intl.aliyuncs.com
*.alibaba-inc.com
*.aliyun-inc.com
```

"LLM providerARMS Tracing qwen-code distribution "---- claude-code  single-vendor / single-direction  qwen-code  providerOpenAI / Anthropic / OpenRouter / **** header

### 11.3 Pattern intentionally tiny

`matchesTrustedHost(hostname, patterns)`  `DashScopeOpenAICompatibleProvider.isDashScopeProvider` :

- bare hostname -> case-insensitive
- `*.suffix` ->  `suffix`  **AND** dot-anchored  `evil-alibaba-inc.com` / `alibaba-inc.com.attacker.tld`  typo-suffix 

 regex/scheme  globbing ----  settings 

### 11.4  vs R1

#### `wrapFetchWithCorrelation` (OpenAI / Anthropic)

R1  wrapper  telemetry-enabled + sessionId  gateR3  gate:

```ts
const trustedHosts =
  config.getTelemetrySessionIdHeaderHosts?.() ??
  DEFAULT_SESSION_ID_HEADER_HOSTS;
const broadcastAll = trustedHosts.some((p) => p.trim() === '*');

return async function correlationFetch(input, init) {
  if (!config.getTelemetryEnabled()) return baseFetch(input, init);
  if (!broadcastAll) {
    const host = extractRequestHost(input);
    if (!host || !matchesTrustedHost(host, trustedHosts)) {
      return baseFetch(input, init); // host gate
    }
  }
  const sid = config.getSessionId();
  if (!sid) return baseFetch(input, init);
  // ... header injection
};
```

`trustedHosts`  wrap  snapshot session id "" `telemetry.sessionIdHeaderHosts`  contentGenerator `[" * "]`  `.trim()`  broadcast settings.json 

#### `staticCorrelationHeaders` (Gemini)

 `destinationUrl?: string` :

```ts
export function staticCorrelationHeaders(
  config: Config,
  destinationUrl?: string,
): Record<string, string> {
  if (!config.getTelemetryEnabled()) return {};
  if (!destinationUrl) return {}; // fail-closed: 
  if (!matchesTrustedHost(new URL(destinationUrl).hostname, trustedHosts)) {
    return {};
  }
  return { [SESSION_ID_HEADER]: config.getSessionId() };
}
```

#### Gemini factory 

Gemini SDK  default endpoint`generativelanguage.googleapis.com`  `{region}-aiplatform.googleapis.com` `vertexai` factory R3 "`config.baseUrl`  `undefined`" helper fail-closed ->  header `baseUrl` SDK  destination  Vertex destination 

### 11.5  / 

|                                                                  |                                                                                               |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `packages/core/src/telemetry/trusted-llm-hosts.ts` (NEW)             | `DEFAULT_SESSION_ID_HEADER_HOSTS` + `matchesTrustedHost` + `extractRequestHost`                   |
| `packages/core/src/telemetry/trusted-llm-hosts.test.ts` (NEW)        |  TLD-suffix IPv6 fail-closedport/userinfo/query                           |
| `packages/core/src/telemetry/llm-correlation-fetch.ts`               |  host gate`staticCorrelationHeaders`  `destinationUrl`                                  |
| `packages/core/src/telemetry/llm-correlation-fetch.test.ts`          |  host-gate 8  case`mockConfig`  `'hosts' in opts`  "default allowlist" vs "broadcast" |
| `packages/core/src/telemetry/config.ts` (`resolveTelemetrySettings`) |  `sessionIdHeaderHosts`                                                                       |
| `packages/core/src/config/config.ts`                                 | `TelemetrySettings.sessionIdHeaderHosts` + `getTelemetrySessionIdHeaderHosts()` getter            |
| `packages/core/src/core/geminiContentGenerator/index.ts`             |  `config.baseUrl`  helperfail-closed when undefined                                         |
| `packages/core/src/core/geminiContentGenerator/index.test.ts`        |  telemetry-on Gemini  fail-closed                                             |
| `packages/cli/src/config/settingsSchema.ts`                          | `sessionIdHeaderHosts` JSON schema                                                            |
| `packages/vscode-ide-companion/schemas/settings.schema.json`         |  `npm run generate:settings-schema`                                                     |
| `docs/developers/development/telemetry.md`                           | "Session correlation header"  +  scope + override                                 |

### 11.6  LazzyMan 

| LazzyMan                          | R3                                                                                                                                                                              |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  telemetry                   | ****: DashScope session id header  ARMS Tracing `telemetry.enabled`                                                        |
|  cross-vendor stable identifier  | ****: allowlist  first-party host opt-in (`["*"]`)                                                                                                   |
|  traceparent     | ****:traceparent  R1 :W3C trace id  sha256 in-vendor trace  W3C per-destination traceparent toggle  10 future work |

### 11.7  + 

- **traceparent scope** --    10
- **Per-request random UUID** (`X-Qwen-Code-Request-Id`) -- LazzyMan  10
- **Gemini staleness lazy-invalidate** (8.6  A) --  R3  sub-issue
- **`matchesTrustedHost` IPv6 ** --  IPv6 destination  allowlist `URL.hostname`  `[::1]` pattern " first-party endpoint" raw IP allowlist 

## 12. R4  -- Scope Conflation Split

> :[LaZzyMan round-8 follow-up review on PR #4390](https://github.com/QwenLM/qwen-code/pull/4390)
> : PR R3  session-id  follow-up PR

### 12.1 

R3  LaZzyMan  review  providerseverity: high round-8 follow-up :

> "Telemetry is not a container for adjacent features. The `traceparent` cross-process propagation and the `X-Qwen-Code-Session-Id` header injection are **not telemetry**. They are outbound-identity / outbound-correlation work that uses some OTel APIs internally as an implementation detail."

:

- **"telemetry" namespace  recipient =  OTLP collector**
-  `traceparent`  `X-Qwen-Code-Session-Id`  recipient = ** LLM provider**
-  recipient 
- R3  wire-level  `telemetry.*` ****: telemetry PR  wire 
- "If we accept that principle, the split is mechanical. If we don't, this PR is the wrong place to debate it because the technical fixes are already in."

### 12.2 " C" hybrid split

 yiliang  customHeader  customHeader  runtime-dynamic  ** C**:

** PR **:

- `UndiciInstrumentation`  client HTTP span ->  OTLP collector
- OTLP feedback-loop guard
- **`NoopTextMapPropagator` ** -> `propagation.inject()`  no-op -> outbound `fetch` ** `traceparent`**
- ** `outboundCorrelation.propagateTraceContext: bool` ( false)**  namespace  true  W3C composite propagator
-  `R3 session-id` `llm-correlation-fetch.ts` / `trusted-llm-hosts.ts` / `telemetry.sessionIdHeaderHosts` setting / 4  provider  / ****

** follow-up PR**:

- `X-Qwen-Code-Session-Id` header R3 
-  `outboundCorrelation.*` namespace setting key TBD**** `telemetry.*`
- Follow-up PR :threat model section reviewsecurity-relevant  docs
- `X-Qwen-Code-Request-Id` per-request UUIDLazzyMan  R3 round  follow-up 

### 12.3  R3 R1 

| R1/R3                                           | R4                                                                                                            |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 3.1 " LLM  traceparent"              |  **R4  off** `outboundCorrelation.propagateTraceContext: true`                                        |
| 3.1 " LLM  `X-Qwen-Code-Session-Id`" |  **R4  PR** follow-up PR                                                                          |
| 4.3 fetch wrapper  session id                  |   PR follow-up PR                                                                           |
| 11 host allowlist (R3 )                        |   follow-up PR                                                                                      |
| 4.4  setting                               |  ** PR  `outboundCorrelation.propagateTraceContext`**  booleansession id  setting  follow-up PR |
| 10 future work "`X-Qwen-Code-Request-Id`"          |   future work session-id follow-up                                                                |

### 12.4  namespace 

`outboundCorrelation.*`  namespace  PR  boolean (`propagateTraceContext`)****:

- ****: session-id / request-id / etc.  namespace
- ** security-relevant**:`settingsSchema.ts` description  "SECURITY-RELEVANT""""observability "
- **defaults  off**: LazzyMan "open-source  id"
- ** telemetry.\* **: settings.json  `outboundCorrelation.*`  wire  observability

#### :`telemetry.enabled`

 namespace  `telemetry.*` ** `telemetry.enabled: true`** ---- OTel SDK  telemetry  SDK  propagator  `propagation.inject()` flag  no-op footgun: `propagateTraceContext: true`  telemetrytrap server  `traceparent` error /  warning

:

- `telemetry.md`  `propagateTraceContext`  flag JSON 
- `settingsSchema.ts`  description string **** "Requires `telemetry.enabled: true`" VS Code  UI 

 session-id header  `outboundCorrelation.*` setting**** ----  telemetry  OTel instrumentation/SDK Follow-up PR  footgun 

### 12.5 

|                                                                             |                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `packages/core/src/telemetry/llm-correlation-fetch.ts`                          | ****                                                                                                                                                                                                                          |
| `packages/core/src/telemetry/llm-correlation-fetch.test.ts`                     | ****                                                                                                                                                                                                                          |
| `packages/core/src/telemetry/trusted-llm-hosts.ts`                              | ****                                                                                                                                                                                                                          |
| `packages/core/src/telemetry/trusted-llm-hosts.test.ts`                         | ****                                                                                                                                                                                                                          |
| `packages/core/src/telemetry/sdk.ts`                                            | + `NoopTextMapPropagator` `getOutboundCorrelationPropagateTraceContext()`  SDK textMapPropagator                                                                                                                          |
| `packages/core/src/core/openaiContentGenerator/provider/default.ts`             |  `wrapFetchWithCorrelation`                                                                                                                                                                                               |
| `packages/core/src/core/openaiContentGenerator/provider/dashscope.ts`           |                                                                                                                                                                                                                               |
| `packages/core/src/core/anthropicContentGenerator/anthropicContentGenerator.ts` |                                                                                                                                                                                                                               |
| `packages/core/src/core/geminiContentGenerator/index.ts`                        |  `staticCorrelationHeaders`                                                                                                                                                                                               |
|  4  provider  `*.test.ts`                                               |  session-id  case                                                                                                                                                                                                       |
| `packages/core/src/config/config.ts`                                            |  `TelemetrySettings.sessionIdHeaderHosts``getTelemetrySessionIdHeaderHosts`** `OutboundCorrelationSettings`  + `outboundCorrelationSettings`  + `getOutboundCorrelationPropagateTraceContext()` getter**        |
| `packages/core/src/telemetry/config.ts`                                         |  `resolveTelemetrySettings`  sessionIdHeaderHosts                                                                                                                                                                         |
| `packages/cli/src/config/settingsSchema.ts`                                     |  `sessionIdHeaderHosts` schema** `outboundCorrelation`  schema **                                                                                                                                                   |
| `packages/cli/src/config/config.ts`                                             |  `outboundCorrelation: settings.outboundCorrelation`  `ConfigParameters`                                                                                                                                                    |
| `packages/vscode-ide-companion/schemas/settings.schema.json`                    | `npm run generate:settings-schema` description                                                                                                                                                      |
| `docs/developers/development/telemetry.md`                                      |  "Trace context propagation" -> "Client-side HTTP span on outbound fetch" "Session correlation header"  "Outbound correlation (SECURITY-RELEVANT)"  section `telemetry.enabled`  + JSON  |
| `docs/design/telemetry-outbound-propagation-design.md`                          |  + R4  +                                                                                                                                                                                                          |
| `packages/core/src/config/config.test.ts`                                       | ** `OutboundCorrelation Configuration` describe block**`it.each` 4  case  `getOutboundCorrelationPropagateTraceContext`  default-false omitted / `{}` / explicit true / explicit false                |

### 12.6  LazzyMan 

|                                             | R4                                                                                              |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| "Telemetry namespace  collector " |  wire  `telemetry.*` `outboundCorrelation.*` namespace ""       |
| ""      |  `propagateTraceContext`  falsesession-id  follow-up PR  off                      |
| "telemetry PR  wire-level "         |   PR "telemetry  wire "wire  `outboundCorrelation.*`  |
| "split is mechanical, work isn't wasted"        |  R3  branch git history  follow-up PR  cherry-pick          |

### 12.7 follow-up PR  PR 

 follow-up PR :

- `outboundCorrelation.sessionIdHeader: { enabled, trustedHosts }`  setting
-  R3  `wrapFetchWithCorrelation` / `matchesTrustedHost` / `DEFAULT_SESSION_ID_HEADER_HOSTS` 
- threat model :recipient  id  per-request UUID 
- ** off** default allowlist ----  R3  LazzyMan  CLI 
- security-relevant  + docs/users/configuration/settings.md 
