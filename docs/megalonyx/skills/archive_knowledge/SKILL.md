# Skill: Archive Knowledge

## 1. Skill Identity
The **Archive Knowledge** skill is a utility for context management. It solves the problem of prompt saturation and "context drift" by moving specific pieces of information from the active `rag_context` to long-term `archive` storage, ensuring the prompt snapshot remains lean and efficient.

## 2. Trigger Logic
This skill is triggered when:
- The active context window is approaching its limit.
- Specific information is no longer needed for immediate reasoning but must be preserved for future reference.
- A `call_skill` request is made specifically for `archive_knowledge`.

## 3. Operational Workflow
The skill follows a direct execution path:
1. **Key Identification**: Receives a `key` argument identifying the target information in the `rag_context`.
2. **Context Extraction**: Locates the value associated with the key in the active context dictionary.
3. **Archival Transfer**: Moves the data to the long-term archive storage.
4. **Confirmation**: Returns a success or error status.

## 4. Output Contract
The skill adheres to the following JSON response schema:
- **Success**: `{"status": "success", "message": "Context archived successfully."}`
- **Error**: `{"error": "Key not found in rag_context."}`

## 5. Symmetry Link
Original Configuration: [`config/skills/archive_knowledge/SKILL.md`](../../../config/skills/archive_knowledge/SKILL.md)
