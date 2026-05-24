# CodeScope Graph Schema Documentation

## Purpose
This file defines the formal data model (nodes and edges) of the CodeScope graph database, providing the necessary context for writing Cypher queries.

## Logic & Structure
The schema is documented as a set of tables:
- **Nodes**: Defines entities like `File`, `Function`, `Class`, `Module`, `Commit`, `Metadata`, `PR`, and `AUTHOR`, along with their key properties (e.g., `is_historical` for functions).
- **Edges**: Defines the relationships between nodes, such as `CALLS` (Function $\to$ Function), `MODIFIES` (Commit $\to$ Function), and `CHANGES` (PR $\to$ Function).
- **Backfill State**: Explains the `version_tag = 'bf'` property used to distinguish between basic file-level tracking and deep function-level modification tracking.
- **Cypher Reference**: A quick guide to the supported Neo4j syntax and known limitations within the CodeScope environment.

## Usage
- **Developers**: Essential reference for any developer implementing new graph-based features or writing queries.
- **AI Agents**: Use this schema to ensure that generated Cypher queries use the correct node labels and relationship types.

## Original File
[config/skills/codegraph/schema.md](../../config/skills/codegraph/schema.md)
