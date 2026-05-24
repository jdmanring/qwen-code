# Memory

Qwen Code stores long‑term data in the user‑area `~/.qwen`. The memory system is **automatic**:

| Directory | Purpose |
|-----------|---------|
| `~/.qwen/memory/` | Persistent JSON/markdown files written by the `memory` tool. |
| `~/.qwen/.gists/` | Cached Gist contents when using the `/gist` helper. |
| `settings.json.orig` | Automatic backup created whenever the settings schema is upgraded. |

**How it works**

- When a tool needs to remember something, it calls `memory.write`. The runtime writes a file under `~/.qwen/memory/`.
- On later sessions, the `memory.read` tool pulls that information back into the LLM’s context.
- The system automatically trims old entries to stay within token limits (see *Compact‑mode*).

**Our workflow**

1. Documentation overrides (e.g., `QWEN.md`) are **read‑only** and never written to `~/.qwen`.
2. Runtime state such as session recaps, dream fragments, or user‑provided notes is stored here.

*Reference:* `design/auto-memory/README.md` and `developers/memory.md`.
