# Memory Dreamer Service

## Component Identity
The **Memory Dreamer** is a reflective consolidation service designed to maintain the health and signal-to-noise ratio of the system's semantic memory. It acts as a "garbage collector" and "synthesizer" for long-term knowledge, ensuring that the memory store does not become bloated with redundant or contradictory information.

## Technical Specification
The service operates on a deterministic algorithm focused on the lifecycle of a "Dream" cycle:
- **Orientation**: Scans memory tiers and the semantic index to establish a knowledge baseline.
- **Signal Gathering**: Searches session transcripts for new facts that expand or contradict existing knowledge.
- **Consolidation**: Merges semantically identical entries into a single canonical form.
- **Pruning**: Removes redundant entries and normalizes relative timestamps (e.g., "yesterday" $\rightarrow$ absolute date).
- **Re-Indexing**: Synchronizes the semantic index with the modified vector store.
- **Verification**: Uses recall tests to ensure knowledge retrieval remains intact while noise is reduced.

**Hard Constraints**:
- **Zero Data Loss**: Facts are only removed if they are duplicates or explicitly superseded by verified newer truths.
- **Canonical Form**: Synthesis must result in high-signal architectural anchors rather than simple lists.
- **Index Integrity**: Strict 1:1 mapping between the index and the physical store.

## Interdependencies
- **Semantic Memory Store**: Primary target for reads, merges, and deletions.
- **Session Transcripts**: Source of truth for recent signals and contradiction resolution.
- **Semantic Index**: Updated at the end of every cycle to reflect the new state.

## Symmetry Link
[Original Config: `config/services/memory-dreamer/README.md`](../../config/services/memory-dreamer/README.md)
