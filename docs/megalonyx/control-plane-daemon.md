# Control Plane Daemon

The control-plane-daemon is a Python service that receives tasks, figures out what kind of
task each one is, breaks it down into jobs, and routes each job to the right model and tool
configuration.

Location: `apps/control-plane-daemon/`  
Entry point: `apps/control-plane-daemon/src/control_plane_daemon/main.py`  
Package name: `control-plane-daemon` (installed as `control_plane_daemon`)

---

## What it does

When a task arrives, the daemon runs it through a pipeline:

1. **Intent classification** — categorizes the task into one of six types (see below)
2. **Task decomposition** — breaks it into a sequence of atomic jobs with dependency ordering
3. **Profile selection** — picks an execution profile from `.qwen/agents/` that matches the task context
4. **Model routing** — assigns a specific model to each job based on its profile
5. **Tool execution** — calls the model with the resolved prompt and context; handles retries

---

## Modules

### `intent_classifier.py`

Classifies a raw task prompt into one of six intent types using an LLM call:

| Intent | What it means |
|---|---|
| Exploratory | User wants to understand something — read-only, low risk |
| Surgical Fix | Narrow, targeted change to a specific known location |
| Feature Synthesis | New capability that spans multiple files or systems |
| Structural Evolution | Refactoring, architecture changes, large-scale reorganization |
| Adversarial Review | Security audit, code review, finding problems |
| Knowledge Sync | Documentation, test writing, bringing docs/tests in line with code |

The intent type determines the risk profile and which decomposition strategy to apply.

### `task_decomposer.py`

Takes an intent-classified task and produces a list of atomic jobs with:
- Specific instructions for each job
- Dependencies between jobs (job 2 cannot start until job 1 completes)
- Skill assignments (which `.qwen/agents/` profile to use for each job)

Uses an LLM call to do the decomposition. Reads available skill profiles from `.qwen/agents/` to know what tools are available when building the job list.

### `job_state_manager.py`

Tracks the lifecycle of every job: `pending` → `in_progress` → `completed` or `failed` or `retrying`.

Maintains dependency awareness — a job only becomes eligible when all jobs it depends on are complete. Provides the next executable job when polled.

### `execution_context.py`

A container for the ephemeral state of one job execution: file cache, config overrides, any data passed from a prior job. Uses the Prototype pattern so each job starts with a clean copy — state from one job cannot accidentally affect the next.

### `execution_profile_selector.py`

Loads execution profiles from `.qwen/agents/` and selects the best match for a given job. Matching is based on file patterns (what files the job touches) and task keywords.

Each profile is a YAML+Markdown file specifying which model to use, which skills to activate, and what the system prompt should emphasize. See `docs/megalonyx/execution-profiles.md`.

### `model_router.py`

Reads the selected execution profile and maps it to a concrete model from `settings.json`. Handles cases where the preferred model is unavailable by falling back to the next best option.

Output: a model ID, system prompt template, and generation parameters for the job.

### `tool_executor.py`

The core execution engine. Given a model assignment and execution context, it:
1. Resolves the final system prompt from the profile template and context
2. Calls the model via the appropriate provider API
3. Handles tool call responses (routes them to MCP or local tool handlers)
4. Retries on transient failures; falls back to an alternate model on hard failures
5. Returns the result to the job state manager

### `command_manager.py`

Loads slash-command definitions from Markdown frontmatter files. Slash commands are shortcuts
that expand to multi-step job sequences — `/deploy` might expand to lint + test + build + push.

### `agent_generator.py`

An LLM-based factory that synthesizes new execution profiles. Given a description of what kind
of agent is needed, it generates a YAML+Markdown file in `.qwen/agents/` format, including
the system prompt, skill list, and "when to use" examples.

---

## Startup sequence

```python
ControlPlane.__init__()
  → load settings.json
  → IntentClassifier(settings)
  → TaskDecomposer(settings, skill_dir=".qwen/agents/")
  → JobStateManager()
  → CommandManager(command_dir=".qwen/commands/")
  → ExecutionProfileSelector(profile_dir=".qwen/agents/")
  → VerificationEngine()
  → PolicyEngine()
  → ready
```

---

## Tests

Unit tests: `apps/control-plane-daemon/tests/unit/`  
Control plane integration tests: `apps/control-plane-daemon/tests/control_plane/`

Run: `uv run pytest apps/control-plane-daemon/tests/`
