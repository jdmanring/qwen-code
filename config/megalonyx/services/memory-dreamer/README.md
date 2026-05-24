# Memory Dreamer Service

## Objective
Perform a reflective consolidation of semantic memory to eliminate redundancy and synthesize fragmented facts into high-signal architectural anchors.

## Deterministic Algorithm
The Memory Dreamer must follow these steps exactly:

1. **Orient**:
   - Use `list_directory` and `read_file` to scan the current state of the memory tiers.
   - Read the semantic index to identify the current knowledge map.
2. **Gather Signal**:
   - Use `grep_search` on session transcripts to find recent facts that contradict or expand existing memories.
   - Use `reflect` to get a high-level summary of the current project state.
3. **Consolidate**:
   - Identify semantically duplicate entries (same fact, different wording).
   - Merge duplicates into a single canonical entry.
   - Resolve contradictions by prioritizing the most recent, verified signal.
4. **Prune**:
   - Delete redundant entries.
   - Convert relative dates (e.g., "yesterday") to absolute dates.
5. **Re-Index**:
   - Update the semantic index to reflect the new, consolidated state.
6. **Verify**:
   - Use `recall` to ensure the consolidated memories are still retrievable and the noise has decreased.

## Hard Constraints
- **NO DATA LOSS**: Never delete a fact unless it is a duplicate or explicitly contradicted by a newer, verified truth.
- **CANONICAL FORM**: Merged entries must be structured as high-signal architectural anchors, not just a list of combined bullets.
- **INDEX INTEGRITY**: The index must always be in sync with the actual files in the vector store.

## Output Contract
The final report must follow this format:
- **Consolidation Summary**: [X entries merged, Y entries pruned]
- **Touched Topics**: [List of topics]
- **Resolved Contradictions**:
  - `[Old Fact]` $\rightarrow$ `[New Synthesized Fact]`
- **Verification**: [Confirmed/Failed]
