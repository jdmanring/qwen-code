# Memory Extractor Service

## Component Identity
The **Memory Extractor** is the primary ingestion engine for the system's semantic memory. Its role is to monitor transient conversation history and "distill" durable facts into the Dual-Tier Qdrant system, transforming ephemeral chat into permanent knowledge.

## Technical Specification
The extractor follows a rigorous extraction pipeline to ensure high signal-to-noise ratios:
1. **Orientation**: Scans existing memory structure to identify active topics (`user`, `feedback`, `project`, `reference`).
2. **Analysis**: Reviews history to identify "Durable Facts" (preferences, goals, architectural decisions) while filtering out speculative or transient state.
3. **De-duplication**: Cross-references identified facts with existing memories to avoid redundancy or flag contradictions.
4. **Persistence**: Ingests facts into the correct tier:
   - `Local`: Session-specific durable facts.
   - `Cloud`: Global project/user rules.
5. **Verification**: Uses `recall` to verify the accessibility and categorization of new entries.

**Hard Constraints**:
- **No-Snooping**: Forbidden from using source code or git logs for memory extraction; must rely solely on conversation history.
- **Conciseness**: Entries must be single-sentence bullet points.
- **Salience**: If no durable facts are found, the agent must explicitly state "No durable facts identified" and perform no writes.

## Interdependencies
- **Dual-Tier Qdrant Store**: Target for all ingested durable facts.
- **Conversation History**: The primary input stream for analysis.
- **Recall Tool**: Used for post-ingestion verification.

## Symmetry Link
[Original Config: `config/services/memory-extractor/README.md`](../../config/services/memory-extractor/README.md)
