# SKILL: archive_knowledge

## Description
Moves a specific piece of context from the active `rag_context` to the long-term `archive` to keep the prompt snapshot lean and efficient.

## Arguments
- `key` (string): The key in the `rag_context` dictionary that contains the information to be archived.

## Output
- `{"status": "success", "message": "Context archived successfully."}` if the key was found and moved.
- `{"error": "Key not found in rag_context."}` if the key does not exist.

## Usage Example
`{"tool": "call_skill", "args": {"skill_name": "archive_knowledge", "arguments": {"key": "file_structure_summary"}}}`
