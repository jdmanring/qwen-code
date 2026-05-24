# Memory Extractor Service Configuration

## Component Identity
This configuration defines the **Memory Extraction Specialist**, the agent responsible for the active capture and categorization of durable knowledge from the interaction stream.

## Technical Specification
The service is configured as a **Memory Extraction Specialist** with the following specifications:

### Persona & Logic
- **Role**: Memory Extraction Specialist.
- **System Prompt**: Focuses on the extraction of durable facts stated by the user or established as project truth, while strictly ignoring fillers and temporary state.
- **Operational Rules**:
  - **Read-First**: Must check existing memories before updating.
  - **Topic Classification**: Restricted to four specific topics: `user` (preferences/role), `feedback` (rules/style), `project` (goals/deadlines), and `reference` (docs/links).
  - **No Investigation**: Strictly prohibited from exploring the codebase to find memories.
  - **Batching**: Requires parallel execution of reads followed by parallel writes.

### Capabilities
- **Triggers**: Activated by keywords such as `"remember this"`, `"save to memory"`, `"update project goals"`, and `"extract facts"`.
- **Toolset**: Uses `read_file`, `grep_search`, `glob`, `list_directory`, `write_file`, `edit`, and `ingest`.
- **Model**: Inherits the current session model.

### Reporting Schema
The agent provides a structured report:
1. **TOUCHED TOPICS**: List of updated categories.
2. **EXTRACTED FACTS**: Mapping of `[Fact]` $\rightarrow$ `[Topic]`.
3. **JUSTIFICATION**: Explanation of why the fact was deemed "durable."

## Interdependencies
- **Memory Bridge**: Utilizes the `ingest` tool to write to the vector database.
- **Orchestrator**: Triggered by the main orchestrator upon detection of memory-related keywords.

## Symmetry Link
[Original Config: `config/services/memory-extractor/service.yaml`](../../config/services/memory-extractor/service.yaml)
