# Skill: lsp

## Skill Identity
The `lsp` skill leverages the Language Server Protocol (LSP) to provide deep semantic analysis of the codebase. It allows the system to move beyond text-based search to understand symbols, definitions, references, and type-level errors.

## Trigger Logic
This skill is triggered by requests for:
- **Definitions**: "Where is this function defined?"
- **References**: "Where is this variable used?"
- **Diagnostics**: "Are there any type errors in this file?"
- **Hover Information**: "What is the type/documentation for this symbol?"

## Operational Workflow
1. **LSP Command Selection**: Map the request to the corresponding LSP command (`get_definitions`, `get_references`, `get_diagnostics`, or `hover`).
2. **Target Identification**: Resolve the symbol or request to an absolute file path and precise line/column number.
3. **LSP Execution**: Execute the command via the LSP server to retrieve semantic data.
4. **Information Synthesis**: Parse the raw LSP response into a human-readable and AI-friendly explanation.

## Output Contract
The output must include:
1. **LSP RESULTS**: The direct technical output from the LSP command.
2. **SEMANTIC ANALYSIS**: A brief interpretation of the findings in the context of the codebase.
3. **CONFIDENCE**: A numerical value (0.0 - 1.0).

## Symmetry Link
Original configuration: [`config/skills/lsp/SKILL.md`](../../../config/skills/lsp/SKILL.md)
