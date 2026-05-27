 
# Semantic Navigation: AST & Symbol Mapping

This document defines the technical specification for moving from probabilistic text search (grep) to structural semantic navigation using Abstract Syntax Trees (AST).

## 1. Objective
The goal is to provide AI agents with a high-fidelity map of the codebase that understands the *relationships* between symbols (functions, classes, variables) rather than just their textual occurrences.

## 2. Technical Implementation: Tree-sitter Integration

The system utilizes **Tree-sitter**, an incremental parsing library, to generate concrete syntax trees for all supported languages in the repository.

### 2.1 The Symbol Extraction Pipeline
1. **Parsing**: `Tree-sitter` parses the source file into an AST.
2. **Symbol Identification**: A set of language-specific queries identifies "Defining" and "Referencing" symbols.
3. **Mapping**: The system records the exact byte offset and line/column of every symbol definition.
4. **Indexing**: These symbols are stored in the `.codegraph` index, allowing for instantaneous "Jump to Definition" and "Find All References" queries.

### 2.2 Structural vs. Textual Discovery
| Discovery Method | Logic | Precision | Use Case |
| :--- | :--- | :--- | :--- |
| **Textual (Grep)** | Regex match on raw bytes. | Low (High Noise) | Finding a specific string or keyword. |
| **Structural (AST)** | Query against the syntax tree. | High (Zero Noise) | Finding a specific class method or variable definition. |

## 3. Integration with the Memory System

Semantic navigation is integrated into the **Recall** phase of the agentic loop:
- **Symbol-Aware Retrieval**: When an agent searches for a function, the system returns not just the line of code, but the entire function block and its call hierarchy.
- **Dependency Mapping**: The agent can query the "Call Graph" to understand the impact of a change before modifying a file.

## 4. Implementation Status
- **[Current]**: Basic `grep` and `glob` based discovery.
- **[Target]**: Full Tree-sitter integration for Python, TypeScript, and Rust, providing a complete symbol map for the entire project.
