# System Observability & Logging Reference

This document defines the logging architecture of the Mega Code stack, providing a guide for AI agents and developers to debug the system using structured logs.

## 1. Logging Architecture

Mega Code uses a **Dual-Stream Logging** strategy to separate high-level system events from high-volume raw data.

### Stream A: The System Log (JSONL)
- **Purpose**: Tracking system state, errors, and critical events.
- **Location**: Defined in `settings.json` $\rightarrow$ `logging.log_path` (Default: `~/.qwen/logs/qwen_system.log`).
- **Format**: Structured JSONL (JSON Lines).
- **Retention**: Persistent until manually cleared.

### Stream B: The Trace Log (Transient)
- **Purpose**: Debugging raw MCP I/O, LLM prompts, and tool responses.
- **Location**: `~/.qwen/tmp/trace_{YYYY-MM-DD}.log`.
- **Activation**: Enabled via `settings.json` $\rightarrow$ `logging.enable_trace = true`.
- **Retention**: Transient; rotated daily.

---

## 2. Log Level Hierarchy

The system respects the following verbosity levels:

| Level | Value | Description | Use Case |
| :--- | :--- | :--- | :--- |
| **DEBUG** | 10 | Fine-grained internal state. | Deep debugging of logic flows. |
| **INFO** | 20 | Normal operational events. | Tracking general progress and success. |
| **WARN** | 30 | Unexpected but non-fatal events. | Policy violations, retries, soft failures. |
| **ERROR** | 40 | Fatal for a specific job/request. | Tool failures, API timeouts, crashes. |
| **CRITICAL** | 50 | System-wide failure. | Memory daemon crash, disk full, auth failure. |

---

## 3. Event Catalog (System Log)

All system logs follow the schema: `{"timestamp": "...", "level": "...", "event": "...", "data": {...}}`.

### Core Events
| Event Type | Level | Description | Key Data Fields |
| :--- | :--- | :--- | :--- |
| `control_plane_activation` | INFO | Orchestrator started a new intent. | `intent`, `user_prompt` |
| `tool_call` | INFO | An MCP tool was invoked. | `tool`, `args` |
| `policy_violation` | WARN | Tool blocked by current intent policy. | `tool`, `reason` |
| `model_response` | INFO | Model returned a valid response. | `model`, `attempt`, `status` |
| `model_failure` | ERROR | Model failed to generate a response. | `model`, `error` |
| `tool_failure` | ERROR | MCP tool execution failed. | `tool`, `error` |
| `gc_start` | INFO | Memory Garbage Collection started. | `collection` |
| `gc_success` | INFO | GC completed successfully. | `collection`, `max_age_days` |
| `gc_failure` | ERROR | GC encountered an error. | `collection`, `error` |

---

## 4. Debugging Workflow

### Scenario: A Tool is Not Working
1. **Check System Log**: Search for `tool_failure` or `policy_violation` events.
2. **Enable Trace**: Set `enable_trace: true` in `settings.json`.
3. **Inspect Trace**: Open `~/.qwen/tmp/trace_{date}.log` and look for the raw MCP request/response pair for that tool.
4. **Verify Level**: If no logs appear, ensure `log_level` is set to `DEBUG`.

### Scenario: Memory is Not Retaining Facts
1. **Check GC Logs**: Search for `gc_success` to see if the target collection was pruned too aggressively.
2. **Verify Ingestion**: Search for `ingest` events in the system log to ensure the data was sent to the daemon.
