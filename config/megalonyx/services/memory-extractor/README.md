# Memory Extractor Service

## Objective
Transform transient conversation history into durable, organized semantic memory in the Dual-Tier Qdrant system.

## Deterministic Algorithm
The Memory Extractor must follow these steps exactly:

1. **Orient**: 
   - Use `list_directory` and `read_file` to scan the existing memory structure.
   - Identify which topics (`user`, `feedback`, `project`, `reference`) already have content.
2. **Analyze**:
   - Review the provided conversation history.
   - Identify "Durable Facts": statements of preference, project goals, architectural decisions, or explicit "remember this" requests.
   - Filter out: questions, speculative thoughts, or session-specific transient state.
3. **De-duplicate**:
   - Compare identified facts against existing memories.
   - If a fact is already present, skip it.
   - If a fact contradicts an existing memory, mark it for update.
4. **Persist**:
   - Use the `ingest` tool to save the facts.
   - Assign the correct tier: `local` for session-specific durable facts, `cloud` for global project/user rules.
5. **Verify**:
   - Use `recall` to ensure the newly ingested facts are retrievable and correctly categorized.

## Hard Constraints
- **NO-SNOOPING**: Do not read source code or git logs to find memories. Work only from history and existing memory.
- **CONCISENESS**: Entries must be single-sentence bullet points. No prose.
- **SALIENCE**: If nothing durable is found, the agent MUST return "No durable facts identified" and make no changes.

## Output Contract
The final report must follow this format:
- **Status**: [Updated / No Changes]
- **Touched Topics**: [List of topics]
- **New/Updated Facts**:
  - `[Topic]`: [Fact]
- **Verification**: [Confirmed/Failed]
