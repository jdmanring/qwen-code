# Token-Lean Mandates (Gemma 4 Optimized)

These are compressed versions of the core Qwen Code mandates, designed for maximum adherence with minimum token overhead.

## [S-READ] Strict File Reading
- **No Truncation**: NEVER assume file is fully read if truncated.
- **No Peeking**: NEVER use `limit` to guess structure.
- **Pagination**: MUST use `offset`/`limit` until fully captured.
- **Verify**: Read full target context before `edit` or `write_file`.

## [S-ALGO] Algorithmic Skills
- **No Improvisation**: Skills = deterministic recipes.
- **Process > Persona**: Prioritize "How" over "Who".
- **Modularity**: Planner $\rightarrow$ Executor $\rightarrow$ Verifier.
- **Verification**: Task complete only after Output Contract check.

## [S-MEM] Memory Hierarchy
- **Instructional (QWEN.md)**: Operational Law.
- **Semantic (mega-memory-manager)**: Project Facts/History.
- **Ephemeral**: Current Context.
- **Logic**: Fact/Detail $\rightarrow$ `search`; Summary $\rightarrow$ `reflect`; New Rule $\rightarrow$ `ingest`; Behavioral Failure $\rightarrow$ update `QWEN.md`.

## [S-PILL] Two-Pillar Layout
- **AI Brain (`~/.qwen/`)**: `config/agents`, `config/skills`.
- **System Body (`~/.local/share/megalonyx/`)**: `packages/`.
- **Separation**: No implementation code in `config/`; no personas/skills in infrastructure root.

## [S-ROOT] Zero-Root Standard
- **No Root Clutter**: No scripts/logs/temp in root.
- **Debug**: `tests/debug/`.
- **Logs**: `logs/`.
- **Meta**: `config/meta/`.
- **Docs**: `docs/` (.md).
- **Symmetry**: Documentation mirrors `config/` structure.

## [S-EXEC] No-Direct-Execution
- **Blueprint = Static**: NEVER run system (mega-memory-manager, etc.) in Blueprint dir.
- **Workflow**: Modify in Lab/Machine $\rightarrow$ Extract Patch/Skill $\rightarrow$ Commit to Blueprint $\rightarrow$ Deploy to Machine.
