# Changes From Upstream

> Master record of all deliberate divergence from upstream. Every file that the fork modifies differently from upstream should be listed here with the reason.

## Format

```
### path/to/file.ext
- **Why:** <reason>
- **What:** <brief description of the change>
- **Type:** protected | patch | fork-only
```

## Protected Files (restored after every sync)

These files are listed in PROTECTED_FILES in the pipeline source. The pipeline restores them automatically.

| File | Why |
|------|-----|
| `tooling/sync-upstreams/upstream_ingest_pipeline.py` | Fork-only pipeline script |
| `.github/workflows/sync-upstream.yml` | Fork-only CI workflow |
| `AI.md` | Fork-specific AI agent guidance |
| `docs/ai/RULES.md` | Fork-specific AI rules |
| `docs/ai/CONTEXT.md` | Fork-specific AI context |
| `docs/fork/` | Fork management documentation |

## Fork-Only Additions (not in upstream)

Files that exist only in this fork and should never be contributed upstream.

| File | Purpose |
|------|---------|
| `tooling/sync-upstreams/` | Entire pipeline directory |
| `docs/fork/` | Fork management documentation |
| `FORK_WORKBENCH_TEMPLATE.md` | Authoritative fork reference |
| `CHEAT_SHEET.md` | Daily operations cheat sheet |
| `docs/runbook.md` | Pipeline failure recovery |

## Patches (divergent from upstream)

Files that exist in both but are deliberately different in the fork.

| File | Reason | Type |
|------|--------|------|
| (No patches yet — add as needed) | | |
