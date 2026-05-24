# 📋 Memory Record Schema

This document defines the structure of the data stored within the Mega Code memory system. Adherence to this schema ensures consistency across local and cloud tiers and enables safe schema evolution.

## 1. The `MemoryRecord` Object

All memory entries are encapsulated in a `MemoryRecord` dataclass (defined in `packages/memory_schema.py`).

### Field Specifications

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `string` (UUID) | `uuid4()` | Unique identifier for the record. Used as the Point ID in Qdrant. |
| `text` | `string` | **Required** | The actual semantic content being stored. |
| `tier` | `string` | **Required** | The storage tier: `local` or `cloud`. |
| `source` | `string` | `"qwen-code"` | The system or agent that created the record. |
| `importance` | `int` | `5` | Priority level (1-10). Used for future relevance weighting. |
| `metadata` | `object` | `{}` | Extensible dictionary for storing task IDs, file paths, or tags. |
| `created_at` | `float` | `time.time()` | Unix timestamp of creation. Used by the GC for pruning. |
| `updated_at` | `float` | `time.time()` | Unix timestamp of the last modification. |
| `schema_version` | `string` | `"1.0"` | Version of the schema used for this record. |

---

## 2. Serialization & Storage

To maintain compatibility between the Python daemon and the Qdrant JSON payload, records undergo a serialization process.

### Serialization Flow
`MemoryRecord (Dataclass)` $\rightarrow$ `serialize()` $\rightarrow$ `JSON Dictionary` $\rightarrow$ `Qdrant Payload`.

### Deserialization & Evolution
When retrieving a record, the `deserialize()` function reconstructs the `MemoryRecord` object. It provides defaults for missing fields, allowing the system to load records created with older versions of the schema without crashing.

---

## 3. Validation Rules

Every `MemoryRecord` must pass the `validate()` method before ingestion:
- **Non-Empty**: `text` cannot be empty.
- **Valid Tier**: `tier` must be either `local` or `cloud`.
- **Importance Range**: `importance` must be between 1 and 10.
- **ID Presence**: A valid `id` must be present.
