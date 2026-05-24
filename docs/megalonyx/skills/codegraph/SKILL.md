# Skill: CodeGraph

## 1. Skill Identity
**CodeGraph** is an advanced analysis skill that leverages a graph database (neug) and vector index (zvec) to provide deep structural and semantic insights into a codebase. It solves the limitations of grep and LSP by enabling complex queries regarding call chains, dead code, module coupling, and PR risk.

## 2. Trigger Logic
This skill is triggered by:
- Questions about call chains, callers/callees, or complex dependencies.
- Requests for architecture reports, dead code detection, or hotspot analysis.
- Semantic searches for similar functions across the codebase.
- Bug root cause analysis based on GitHub issues.
- PR risk assessment, conflict detection, or auto-merge candidate identification.
- Presence of a `.codegraph` index in the workspace.

## 3. Operational Workflow
CodeGraph operates through an indexing and querying pipeline:
1. **Indexing**: Initializes a knowledge graph using `codegraph init` (structural) and `codegraph ingest` (evolutionary/git history).
2. **Querying**: Utilizes either the CLI for reports or the Python API for raw Cypher queries and semantic searches.
3. **Analysis**: Executes specialized methods (e.g., `impact()`, `hotspots()`, `circular_deps()`).
4. **Synthesis**: Generates high-level reports or UML-style class diagrams (Mermaid).

### Specialized Sub-Capabilities
- **Bug Root Cause Analysis**: Fetches GitHub issues and maps them to the code graph using semantic search and call-chain tracing to rank root cause candidates.
- **PR Review & Analysis**: Analyzes open PRs to compute risk scores (Blast Radius, Interface Changes), detects cross-PR conflicts via connected-components, and identifies auto-merge candidates.

## 4. Output Contract
Depending on the query, CodeGraph produces:
- **Reports**: Markdown architecture reports including subsystem distribution and hotspots.
- **Visualizations**: Mermaid class diagrams (INHERITS, COMPOSES, AGGREGATES).
- **Data**: Lists of candidates for bug root causes or PR risk levels (CRITICAL, HIGH, MEDIUM, LOW).
- **Graph Data**: Raw Cypher query results.

## 5. Symmetry Link
Original Configuration: [`config/skills/codegraph/SKILL.md`](../../../config/skills/codegraph/SKILL.md)
