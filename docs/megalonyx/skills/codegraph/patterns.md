# CodeScope Cypher Patterns Documentation

## Purpose
This file serves as a reference library of Neo4j Cypher queries used to extract structural and evolutionary insights from the CodeScope graph database.

## Logic & Structure
The patterns are categorized by the type of insight they provide:
- **Structural Queries**: Focus on the static call graph. Examples include finding callers/callees, transitive callers, module-based function lists, and calculating "risk" via fan-in/fan-out.
- **Evolution Queries**: Focus on git history. Examples include identifying functions modified by a specific commit, co-changed functions, and tracking backfill progress.
- **Composition Strategies**: High-level guidance on combining semantic search (vector) with structural queries (graph) to perform "Dependency Archaeology" or "Evolution Forensics."

## Usage
- **Developers**: Use these patterns when writing new `codegraph` features or performing manual database exploration via `cs.conn.execute()`.
- **AI Agents**: Use these as templates to construct complex graph queries when the standard API is insufficient for a specific analysis task.

## Original File
[config/skills/codegraph/patterns.md](../../config/skills/codegraph/patterns.md)
