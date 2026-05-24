# Memory Dreamer Service Configuration

## Component Identity
This configuration defines the operational persona, capabilities, and reporting standards for the **Memory Dreamer** agent. It transforms the conceptual "Dream" algorithm into an executable agentic persona.

## Technical Specification
The service is configured as a **Memory Synthesis Architect** with the following specifications:

### Persona & Logic
- **Role**: Memory Synthesis Architect.
- **System Prompt**: Mandates the merging of duplicates, synthesis of fragmented facts, and pruning of stale information while maintaining Dual-Tier (Local vs. Cloud) routing integrity.
- **Operational Flow**: Follows a strict sequence: `ORIENT` $\rightarrow$ `GATHER` $\rightarrow$ `CONSOLIDATE` $\rightarrow$ `PRUNE` $\rightarrow$ `INDEX`.

### Capabilities
- **Triggers**: Activated by keywords such as `"dream"`, `"consolidate memory"`, `"prune memories"`, and `"synthesize knowledge"`.
- **Toolset**: Equipped with a comprehensive suite for filesystem and memory management: `read_file`, `grep_search`, `glob`, `list_directory`, `write_file`, `edit`, `ingest`, `recall`, and `reflect`.
- **Model**: Inherits the current session model.

### Reporting Schema
The agent must report its output using a structured format:
1. **CONSOLIDATION SUMMARY**: Metrics on merged and pruned entries.
2. **TOUCHED TOPICS**: List of modified knowledge areas.
3. **RESOLVED CONTRADICTIONS**: Mapping of `[Old Fact]` $\rightarrow$ `[New Synthesized Fact]`.
4. **FINAL STATUS**: Qualitative assessment of memory state (`Lean` or `Redundant`).

## Interdependencies
- **Memory Bridge**: Relies on `ingest` and `recall` tools to interact with the Qdrant backend.
- **Orchestrator**: Triggered by the main orchestrator based on the defined keywords.

## Symmetry Link
[Original Config: `config/services/memory-dreamer/service.yaml`](../../config/services/memory-dreamer/service.yaml)
