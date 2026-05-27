# Telemetry: Custom Resource Attributes + Metric Cardinality Controls

>  issue: [#4365](https://github.com/QwenLM/qwen-code/issues/4365)
>  issue: [#3731](https://github.com/QwenLM/qwen-code/issues/3731)
>  2026-05-21  qwen-code main 

## 1. 

qwen-code  OpenTelemetry SDK Resource :

1. ****: telemetry  `team` / `env` / `cost_center` / `user_id`  `OTEL_RESOURCE_ATTRIBUTES` ****
2. **cardinality**:`session.id`  Resource  metric  CLI session Prometheus /  ARMS Metric / VictoriaMetrics time-series 

:****

## 2. 

### 2.1 Resource 

`packages/core/src/telemetry/sdk.ts:156-161`:

```ts
const resource = resourceFromAttributes({
  [SemanticResourceAttributes.SERVICE_NAME]: SERVICE_NAME,
  [SemanticResourceAttributes.SERVICE_VERSION]:
    config.getCliVersion() || 'unknown',
  'session.id': config.getSessionId(),
});
```

`sdk.ts:274-278`:

```ts
sdk = new NodeSDK({
  resource,
  // Disable async host/process/env resource detectors: they leave attributes
  // pending and trigger an OTel diag.error on any resource attribute read
  // before the detectors settle (e.g. during HttpInstrumentation span creation).
  autoDetectResources: false,
  ...
});
```

`autoDetectResources: false`  OTel  `envDetector`---- `OTEL_RESOURCE_ATTRIBUTES`  `OTEL_SERVICE_NAME` detector  settle  `diag.error` qwen-code ****

### 2.2 `session.id` 

|                         |                      |                                   |
| --------------------------- | ------------------------ | ------------------------------------- |
| Resource                    | `sdk.ts:160`             |  signalspans / logs / metrics |
| Per-span                    | `session-tracing.ts:169` | spans                                 |
| Per-log                     | `loggers.ts:128`         | logs                                  |
| **`getCommonAttributes()`** | `metrics.ts:57`          | ** metric record **       |

** `session.id`  Resource **----`metrics.ts:57`  `baseMetricDefinition.getCommonAttributes()`  30+  metric  `...spread`  `session.id`

```ts
// metrics.ts:55-59
const baseMetricDefinition = {
  getCommonAttributes: (config: Config): Attributes => ({
    'session.id': config.getSessionId(),
  }),
};
```

: metric 30+  chokepoint

### 2.3 config resolver 

`packages/core/src/telemetry/config.ts:resolveTelemetrySettings()` :

```
argv (highest)  >  QWEN_* env  >  OTEL_* env  >  settings.json (lowest)
```

 pattern

### 2.4 settings schema 

`packages/cli/src/config/settingsSchema.ts:998-1018`  `telemetry`  JSON schema:

```ts
telemetry: {
  type: 'object',
  // ...
  jsonSchemaOverride: {
    type: 'object',
    properties: {
      includeSensitiveSpanAttributes: { ... },
    },
    additionalProperties: true,  // <-  telemetry.* key 
  },
}
```

`additionalProperties: true`  schema  `otlpEndpoint` / `otlpProtocol` / `resourceAttributes`  `resourceAttributes` / `metrics`  schema IDE  settings UI 

### 2.5 

`packages/core/src/telemetry/qwen-logger/qwen-logger.ts`  qwen-code **** RUM  `RumResourceEvent` OTel SDK  endpointproxy **** 3 

### 2.6  /  `OTEL_*` 

|                                             |                               |
| --------------------------------------------------- | --------------------------------- |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       |  `config.ts:79`         |
| `OTEL_EXPORTER_OTLP_{TRACES,LOGS,METRICS}_ENDPOINT` |                             |
| `OTEL_EXPORTER_OTLP_HEADERS`                        |   exporter          |
| `OTEL_TRACES_SAMPLER`                               |  `tracer.ts:247`        |
| **`OTEL_RESOURCE_ATTRIBUTES`**                      |                       |
| **`OTEL_SERVICE_NAME`**                             |                       |
| **`OTEL_METRICS_INCLUDE_*`**                        |  claude-code  |

## 3.  / 

### 3.1 

-  `OTEL_RESOURCE_ATTRIBUTES`  `settings.json`  OTLP  span / log / metric  resource attributes
-  `OTEL_SERVICE_NAME`  OTel  `OTEL_RESOURCE_ATTRIBUTES`  `service.name` 
- metric **** `session.id`
-  metric-level session correlation 
-  spans  logs  `session.id`trace correlation 
-  `autoDetectResources: false` `diag.error`  bug
-  `settingsSchema.ts`  settings UI  IDE 

### 3.2 

- **`qwen-logger` **: RUM device iduser agent  RUM  resource attribute  `qwen-logger` 
- **Per-span  attribute hook**: / hook  span  attributeclaude-code 
- **`service.version` cardinality **:time series  v2 OTel View API
- **Agent SDK  per-query resource attrs**:qwen-code  SDK 
- **OTLP auth headers**: issue #3731 P1
- **CLI flag  resource attribute**:env var + settings.json CLI flag 

## 4. 

### 4.1 

```
+--- Resourcesdk.ts:156----------------------------------------+--
|   service.name        <- OTEL_SERVICE_NAME                      |
|                          > OTEL_RESOURCE_ATTRIBUTES.service.name|
|                          > 'qwen-code'                         |
|   service.version     <- config.getCliVersion()  [reserved]     |
|   ...user attrs       <- OTEL_RESOURCE_ATTRIBUTES               |
|                          + settings.resourceAttributes         |
|    session.id                                             |
\_-------------------------------------------------------------------
       |
       |-----> Spans      session.idsession-tracing.ts:169
       |-----> Logs       session.idloggers.ts:128
       \_---> Metrics    getCommonAttributes() --  {}
                          toggle ON: { session.id }
```

### 4.2  / merge 

####  attribute

 -> :

1. `OTEL_RESOURCE_ATTRIBUTES` OTel env var
2. `settings.telemetry.resourceAttributes`
3. 

****: ops-time CI /  debugsettings.json  fleet-baked ----

#### `service.name` 

`service.name`  [OTel ](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/):

> **`OTEL_SERVICE_NAME` takes precedence over `service.name` defined with the `OTEL_RESOURCE_ATTRIBUTES` variable.**

 `service.name`  -> :

1. `OTEL_SERVICE_NAME` OTel 
2. `settings.resourceAttributes.service.name`settings  env
3. `OTEL_RESOURCE_ATTRIBUTES.service.name`
4.  `'qwen-code'`

`service.name`  settings ---- service  fleet  settings.json  service.name  GitOps `OTEL_SERVICE_NAME`  OTel "" CI /  settings

:

|                                                     |  `service.name`            |
| ------------------------------------------------------- | -------------------------------------- |
| `OTEL_SERVICE_NAME=foo`                                 |        |
| `settings.resourceAttributes={ "service.name": "foo" }` |   `OTEL_SERVICE_NAME`  |
| `OTEL_RESOURCE_ATTRIBUTES=service.name=foo`             |              |

### 4.3 

|                 |                                                             |                                                                                                   |
| ----------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `service.name`    |  env var + settings  4.2                           | service  ops                                                                          |
| `service.version` |   + warn                                                | ----                                                                        |
| `session.id`      |   + warn metric  toggle  runtime  | runtime-only Resource  metric cardinality toggleResource attr  signal |
| `qwen.*`      |   docs                                  |  attr  attr                                                                     |

****:

```ts
// telemetry/resource-attributes.ts (new file)
/** Keys that cannot be overridden from any source (env or settings). */
export const RESERVED_RESOURCE_ATTRIBUTE_KEYS = new Set<string>([
  'service.version',
  'session.id',
]);
```

`service.name` **** RESERVED ----4.2""RESERVED "" env  settings 

### 4.4 `OTEL_RESOURCE_ATTRIBUTES` 

 OTel  envDetector:

```ts
function parseOtelResourceAttributes(
  raw: string | undefined,
): Record<string, string> {
  if (!raw) return {};
  const out: Record<string, string> = {};
  for (const pair of raw.split(',')) {
    const trimmed = pair.trim();
    if (!trimmed) continue;
    const idx = trimmed.indexOf('=');
    if (idx <= 0) {
      diag.warn(
        `Skipping malformed OTEL_RESOURCE_ATTRIBUTES entry: ${trimmed}`,
      );
      continue;
    }
    const key = trimmed.slice(0, idx).trim();
    const valueRaw = trimmed.slice(idx + 1).trim();
    if (!key) continue;
    let value: string;
    try {
      value = decodeURIComponent(valueRaw);
    } catch {
      diag.warn(
        `Invalid percent-encoding in OTEL_RESOURCE_ATTRIBUTES for key "${key}", using raw value`,
      );
      value = valueRaw;
    }
    out[key] = value; // duplicate keys: last wins (matches OTel reference impls)
  }
  return out;
}
```

 OTel :`key1=val1,key2=val2` percent-encoded

### 4.5 Metric attribute filter

 `metrics.ts:55-59`:

```ts
const baseMetricDefinition = {
  getCommonAttributes: (config: Config): Attributes => {
    const out: Attributes = {};
    if (config.getTelemetryMetricsIncludeSessionId()) {
      out['session.id'] = config.getSessionId();
    }
    return out;
  },
};
```

30+ ----`...spread` 

### 4.6 

|                                                              |                                                                     |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `OTEL_RESOURCE_ATTRIBUTES=""` ()                         |  `{}`                                                     |
| `OTEL_RESOURCE_ATTRIBUTES="a"` ( `=`)                          |  + `diag.warn`                                    |
| `OTEL_RESOURCE_ATTRIBUTES="=val"` ( key)                       |                                                   |
| `OTEL_RESOURCE_ATTRIBUTES="a=,b=2"` ( value)                   | `a=''`, `b='2'`OTel  value                                |
| `OTEL_RESOURCE_ATTRIBUTES="a=val%ZZbad"` ( percent-encoding) |  `val%ZZbad` + `diag.warn`                                      |
| `OTEL_RESOURCE_ATTRIBUTES="a=1,a=2"` (duplicate key)             |  `a=2` OTel SDK                               |
| `OTEL_RESOURCE_ATTRIBUTES="a=1, b=2 "` ()                  |  trim                                                               |
| `OTEL_RESOURCE_ATTRIBUTES=service.version=x`                     |  `service.version` + `diag.warn`                    |
| `settings.resourceAttributes={ "service.name": "x" }`            | settings  service.name 4.2                             |
| `settings.resourceAttributes={ "service.version": "x" }`         |  + `diag.warn`                                                  |
| `settings.resourceAttributes={ "team": 123 }` ( string)        | TypeScript runtime  settings JSON schema validator  |
| Resource  > OTel  (4KB?)                               |  OTel SDK                                       |

** attribute key ** OTel  `[a-z][a-z0-9_.]*` :OTel SDK  export  SDK 

**RESERVED **:

```ts
//  env-parsed attrs
for (const k of RESERVED_RESOURCE_ATTRIBUTE_KEYS) {
  if (k in envAttrs) {
    diag.warn(`OTEL_RESOURCE_ATTRIBUTES cannot override "${k}"; ignoring`);
    delete envAttrs[k];
  }
}

//  settings attrs
for (const k of RESERVED_RESOURCE_ATTRIBUTE_KEYS) {
  if (k in settingsAttrs) {
    diag.warn(
      `settings.telemetry.resourceAttributes cannot override "${k}"; ignoring`,
    );
    delete settingsAttrs[k];
  }
}
```

### 4.7 

- **SDK init **:Resource  `initializeTelemetry()` **** OTel SDK 
- **Subagent fork**:qwen-code  subagent  (`subagent-runtime.ts`) Resource subagent** init SDK** env var  settings---- env 
- **Hot reload**:settings ** Resource** CLI 
- **`refreshSessionContext()`** (`sdk.ts:306`): session ALS context** Resource**---- Resource  `session.id` 

## 5. Config schema 

### 5.1 `TelemetrySettings` `packages/core/src/config/config.ts:293`

```ts
export interface TelemetrySettings {
  // ... existing fields
  /** Static resource attributes attached to every span/log/metric. */
  resourceAttributes?: Record<string, string>;
  /** Per-signal cardinality controls. */
  metrics?: {
    /** Include session.id on metric data points (default: false). */
    includeSessionId?: boolean;
  };
}
```

### 5.2 `Config` getter

```ts
class Config {
  getTelemetryResourceAttributes(): Record<string, string> {
    return this.telemetrySettings.resourceAttributes ?? {};
  }
  getTelemetryMetricsIncludeSessionId(): boolean {
    return this.telemetrySettings.metrics?.includeSessionId ?? false;
  }
}
```

### 5.3 `resolveTelemetrySettings()` 

```ts
const envResourceAttrs = parseOtelResourceAttributes(
  env['OTEL_RESOURCE_ATTRIBUTES'],
);
const settingsResourceAttrs = { ...(settings.resourceAttributes ?? {}) };

// Strip RESERVED keys from both sources (warn if user tried to set them).
for (const k of RESERVED_RESOURCE_ATTRIBUTE_KEYS) {
  if (k in envResourceAttrs) {
    diag.warn(`OTEL_RESOURCE_ATTRIBUTES cannot override "${k}"; ignoring`);
    delete envResourceAttrs[k];
  }
  if (k in settingsResourceAttrs) {
    diag.warn(
      `settings.telemetry.resourceAttributes cannot override "${k}"; ignoring`,
    );
    delete settingsResourceAttrs[k];
  }
}

// Merge: env < settings (settings wins on conflict).
const merged: Record<string, string> = {
  ...envResourceAttrs,
  ...settingsResourceAttrs,
};

// service.name precedence: OTEL_SERVICE_NAME (env-only escape) wins over
// everything else. settings already overwrote env in the spread above.
if (env['OTEL_SERVICE_NAME']) {
  merged['service.name'] = env['OTEL_SERVICE_NAME'];
}

const resourceAttributes = merged;

const metricsIncludeSessionId =
  parseBooleanEnvFlag(env['QWEN_TELEMETRY_METRICS_INCLUDE_SESSION_ID']) ??
  settings.metrics?.includeSessionId ??
  false;

return {
  // ... existing fields
  resourceAttributes,
  metrics: { includeSessionId: metricsIncludeSessionId },
};
```

### 5.4 `sdk.ts` Resource 

```ts
const userAttrs = config.getTelemetryResourceAttributes();
// service.version is always built-in; service.name flows through userAttrs
// (it was already resolved with OTEL_SERVICE_NAME precedence in resolver).
const builtinServiceName = userAttrs['service.name'] ?? SERVICE_NAME;
const { 'service.name': _, 'service.version': __, ...nonReserved } = userAttrs;

const resource = resourceFromAttributes({
  ...nonReserved,
  [SemanticResourceAttributes.SERVICE_NAME]: builtinServiceName,
  [SemanticResourceAttributes.SERVICE_VERSION]:
    config.getCliVersion() || 'unknown',
  // session.id deliberately NOT placed on Resource -- see design doc 4.1
});
```

### 5.5 `settingsSchema.ts` 

`packages/cli/src/config/settingsSchema.ts:998-1018`  `telemetry.jsonSchemaOverride.properties` :

```ts
{
  // ... existing includeSensitiveSpanAttributes
  resourceAttributes: {
    type: 'object',
    additionalProperties: { type: 'string' },
    description:
      'Static resource attributes attached to all telemetry data. ' +
      'Keys must be strings; values must be strings. ' +
      'Reserved keys (service.name, service.version) are silently dropped.',
    default: {},
  },
  metrics: {
    type: 'object',
    additionalProperties: false,
    properties: {
      includeSessionId: {
        type: 'boolean',
        default: false,
        description:
          'Include session.id on every metric data point. ' +
          'WARNING: each CLI session creates a new value, causing unbounded ' +
          'metric time-series fan-out. Only enable for short-term debugging.',
      },
    },
  },
}
```

 `additionalProperties: true` ---- permissive strict permissive schema  `telemetry.*`  docs ""

## 6. 

|                                                            |                                                                        |
| -------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `packages/core/src/telemetry/sdk.ts`                           |  Resource  user attrs `session.id`                       |
| `packages/core/src/telemetry/resource-attributes.ts` ()  | `parseOtelResourceAttributes()` + `RESERVED_RESOURCE_ATTRIBUTE_KEYS`   |
| `packages/core/src/telemetry/config.ts`                        | resolver  `resourceAttributes` + `metrics.includeSessionId`  merge |
| `packages/core/src/telemetry/metrics.ts`                       | `getCommonAttributes()`  toggle gate                                     |
| `packages/core/src/config/config.ts`                           | `TelemetrySettings` schema +  getter                                   |
| `packages/cli/src/config/settingsSchema.ts`                    | `jsonSchemaOverride`  `resourceAttributes` + `metrics`                   |
| `docs/developers/development/telemetry.md`                     |  "Resource attributes" + "Cardinality controls"  +  +    |
| `packages/core/src/telemetry/resource-attributes.test.ts` () |  4.6                                        |
| `packages/core/src/telemetry/sdk.test.ts`                      | merge  /  / `OTEL_SERVICE_NAME`                                |
| `packages/core/src/telemetry/metrics.test.ts`                  | toggle off/on  `session.id`                                      |
| `packages/core/src/telemetry/config.test.ts`                   | env / settings                                                         |
| `CHANGELOG.md`  release notes                                | PR 2  breaking change                                                |

## 7.  PR 

 review  blast radius  PR:

### PR 1 -- Custom resource attributesadditive

-  `resource-attributes.ts`:`parseOtelResourceAttributes()` + `RESERVED_RESOURCE_ATTRIBUTE_KEYS`
- `TelemetrySettings.resourceAttributes`  + resolver merge 
- `OTEL_SERVICE_NAME` / `OTEL_RESOURCE_ATTRIBUTES`  4.2 
-  Resource`sdk.ts`
- `settingsSchema.ts`  `resourceAttributes` JSON schema
- **** `session.id`  Resource 
- Docs  "Resource attributes" 

****: additive settings

### PR 2 -- Cardinality controlssemantic break

-  Resource  `session.id` (`sdk.ts:160` )
-  `metrics.includeSessionId` togglesettings + env+ `getCommonAttributes()` gate
- `settingsSchema.ts`  `metrics` JSON schema
- CHANGELOG / 
-  metric attribute 
- Docs  "Cardinality controls"  + 

****: metric  `session.id`  Prometheus query / Grafana dashboard /  release note  1-2 

**Opt-in ******:

> PR 2 "opt-out"---- `session.id`  metric warn log "this default will flip in v0.X" release 

:1 qwen-code 2 cardinality bug3 issue owner 

### PR 3 -- Docs polish + samplescleanup

- `docs/developers/development/telemetry.md`  10
-  ARMS / Prometheus / Grafana 
-  use case  settings.json 

## 8. 

### 8.1 `parseOtelResourceAttributes()` 

 4.6  vitest `it.each`:

```ts
it.each([
  ['', {}],
  ['a=1', { a: '1' }],
  ['a=1,b=2', { a: '1', b: '2' }],
  ['a=hello%20world', { a: 'hello world' }],
  ['a=val%ZZbad', { a: 'val%ZZbad' }], // invalid percent
  ['malformed', {}],
  ['=val', {}],
  ['a=', { a: '' }],
  ['a=1,a=2', { a: '2' }],
  [' a = 1 , b = 2 ', { a: '1', b: '2' }],
])('parses %j -> %j', (input, expected) => {
  expect(parseOtelResourceAttributes(input)).toEqual(expected);
});
```

### 8.2 Resolver merge 

|                                                                     |  `service.name`                                   |  user attr                       |
| ----------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------ |
|                                                                     | `'qwen-code'`                                         |                                |
|  env `OTEL_SERVICE_NAME=A`                                            | `'A'`                                                 | --                                    |
|  env `OTEL_RESOURCE_ATTRIBUTES=service.name=B`                        | `'B'`                                                 | --                                    |
| `OTEL_SERVICE_NAME=A` + `OTEL_RESOURCE_ATTRIBUTES=service.name=B`       | `'A'`OTEL_SERVICE_NAME                        | --                                    |
| `OTEL_SERVICE_NAME=A` + `settings={service.name:C}`                     | `'A'`OTEL_SERVICE_NAME                        | --                                    |
| `OTEL_RESOURCE_ATTRIBUTES=service.name=B` + `settings={service.name:C}` | `'C'`settings  env OTEL_SERVICE_NAME  | --                                    |
| `OTEL_RESOURCE_ATTRIBUTES=team=x` + `settings={team:y}`                 | `'qwen-code'`                                         | `team='y'`settings           |
| `OTEL_RESOURCE_ATTRIBUTES=service.version=fake`                         | `'qwen-code'` + warn                                  | service.version  cli version |
| `settings={service.version:fake}`                                       | `'qwen-code'` + warn                                  | service.version  cli version |

### 8.3 Resource 

 `InMemorySpanExporter`  span:

```ts
expect(span.resource.attributes['service.name']).toBe('qwen-code');
expect(span.resource.attributes['service.version']).toBe(EXPECTED_VERSION);
expect(span.resource.attributes['session.id']).toBeUndefined(); // 
expect(span.resource.attributes['team']).toBe('platform'); // 
```

### 8.4 Metric attribute toggle 

```ts
it('does not emit session.id on metrics by default', async () => {
  // emit one tool call counter
  recordToolCallMetrics(...);
  const data = await metricReader.collect();
  const dp = data.resourceMetrics.scopeMetrics[0].metrics[0].dataPoints[0];
  expect(dp.attributes['session.id']).toBeUndefined();
});

it('emits session.id when toggle is true', async () => {
  config.telemetrySettings.metrics = { includeSessionId: true };
  recordToolCallMetrics(...);
  const data = await metricReader.collect();
  const dp = data.resourceMetrics.scopeMetrics[0].metrics[0].dataPoints[0];
  expect(dp.attributes['session.id']).toBe(KNOWN_SESSION_ID);
});
```

### 8.5 Spans / Logs 

- spans  `session.id` metric toggle 
- logs  `session.id` metric toggle 

### 8.6 

- `autoDetectResources: false` assertion on config
-  `diag.error` OTel diag  assertion
-  telemetry CI

### 8.7 Diag warn 

 `diag.warn` :

- `settings.resourceAttributes = { 'service.version': 'x' }`reserved
- `OTEL_RESOURCE_ATTRIBUTES=service.version=x`reservedenv  warn
- `OTEL_RESOURCE_ATTRIBUTES=malformed` `=`
- `OTEL_RESOURCE_ATTRIBUTES=a=val%ZZ` percent-encoding

**** warn:

- `settings.resourceAttributes = { 'service.name': 'x' }`settings  service.name
- `OTEL_SERVICE_NAME=foo` + `settings.resourceAttributes = { 'service.name': 'bar' }`OTEL_SERVICE_NAME  warn

## 9.  / 

### 9.1 PR 2

** `session.id` **:

- Prometheus query  `by (session_id)` / `group_left(session_id)` 
- Grafana dashboard  session 
-  session.id 

:spans  logs  `session.id` ****

### 9.2 

:

** A**: debug 

```bash
export QWEN_TELEMETRY_METRICS_INCLUDE_SESSION_ID=true
```

 `settings.json`:

```json
{
  "telemetry": {
    "metrics": { "includeSessionId": true }
  }
}
```

 ****: metric time-series  =  session  debug 

** B**: spans / logs  session 

- spans / logs  `session.id` trace backend Jaeger / Aliyun ARMS Tracing/ log backend Loki / SLS session 
-  per-event cardinality 
-  session-level drill-down 

### 9.3 Release note 

```
**Breaking change (metric attribute):**

The `session.id` attribute is no longer attached to metric data
points by default. This protects metric backends from unbounded
time-series fan-out.

- Spans and logs are unaffected -- `session.id` is still present.
- To restore the previous behavior (short-term debugging only), set
  `QWEN_TELEMETRY_METRICS_INCLUDE_SESSION_ID=true` or in settings.json:
  `telemetry.metrics.includeSessionId: true`.
- For long-term session correlation, query against trace / log
  backends instead of metric backends.

See docs/developers/development/telemetry.md "Migration" for details.
```

## 10. 

### 10.1  team / env  telemetry

```bash
export OTEL_RESOURCE_ATTRIBUTES="team=platform,env=prod,cost_center=eng-123"
```

: span / log / metric  `team=platform` `env=prod` `cost_center=eng-123`

### 10.2  `OTEL_SERVICE_NAME`  collector 

```bash
export OTEL_SERVICE_NAME=qwen-code-ci
```

:`service.name=qwen-code-ci` OTel collector  service.name 

### 10.3 Fleet baseline +  override

 fleet  `~/.qwen/settings.json`GitOps :

```json
{
  "telemetry": {
    "resourceAttributes": {
      "deployment.environment": "production",
      "service.namespace": "engineering-tooling"
    }
  }
}
```

 ops  settings:

```bash
export OTEL_RESOURCE_ATTRIBUTES="debug_run=true"
# settings  deployment.environment / service.namespace 
#  debug_run=true
```

### 10.4  debug  metric session.id

```bash
#  debug run
QWEN_TELEMETRY_METRICS_INCLUDE_SESSION_ID=true qwen ""
```

 settings

### 10.5  ARMS Metric 

```json
{
  "telemetry": {
    "enabled": true,
    "otlpEndpoint": "http://<arms-endpoint>/api/v1/...",
    "otlpProtocol": "http",
    "resourceAttributes": {
      "team": "platform",
      "deployment.environment": "production"
    },
    "metrics": {
      "includeSessionId": false
    }
  }
}
```

## 11.  claude-code 

|                        | claude-code                                      | qwen-code                                  |                                            |
| -------------------------- | ------------------------------------------------ | ------------------------------------------------ | -------------------------------------------------- |
|  OTel env var          | `OTEL_RESOURCE_ATTRIBUTES` / `OTEL_SERVICE_NAME` |                                            |                                            |
| `OTEL_SERVICE_NAME`  |  OTel                                    |                                            | spec                                       |
| Cardinality        | `OTEL_METRICS_INCLUDE_*`                         | `QWEN_TELEMETRY_METRICS_INCLUDE_*`               |  OTel                            |
|                  |  metric                                        |   metric                                     | spans / logs  per-event cardinality  |
|                      |  attribute  false                      |   false                                    |                                            |
| Per-attribute granularity  |  attribute  toggle                         |                                            |                              |
| settings.json        |                                              |   `telemetry.resourceAttributes` + `metrics` |  fleet  base config                        |
| Per-span  hook         |                                              |                                              | claude-code              |
|  `account_uuid`      |                                                |                                              | qwen-code metric  attr                     |
| Agent SDK `options.env`    |                                                |                                              | qwen-code                              |
|                  |  built-in id                           |                                            |                                          |
|              | claude-code  OTel    |  qwen-logger                           |                          |

****:

1. ****:`*_INCLUDE_*` `*_EXCLUDE_*` / `*_DROP_*`
2. ****: gate metric gate span/log----claude-code 

**qwen-code **:

- settings.json :claude-code  env var fleet 
- `service.version` :
- :qwen-logger  OTLP 

## 12. v2 + 

- **`service.version` cardinality **: OTel View API  metric  drop attribute
- ** cardinality toggle**: metric  `user.account_uuid` / `model`  toggle
- **Per-span  attribute hook**: qwen-code  hooks  `OnSpanStart(span, context) => attrs` 
- **Resource attribute schema **: key  `service.*`  attr
- **Hot reload Resource**: settings.json  qwen-serve daemon  Resource daemon  reload 
- ** subagent context **:subagent  parent  trace context resource OTel context propagation  header 
