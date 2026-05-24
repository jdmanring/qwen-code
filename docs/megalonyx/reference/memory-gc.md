# 🧹 Memory Maintenance & "Dreaming" (Garbage Collection)

This document describes the data retention policies and maintenance procedures for the Mega Code memory system. In alignment with Qwen Code terminology, the periodic cleanup of semantic memory is referred to as **Dreaming**.

## 1. Retention Policy

To prevent the vector database from growing indefinitely and to ensure that retrieved context remains relevant, the system implements an age-based pruning strategy.

### The 90-Day Dreaming Rule
By default, the memory system retains records for **90 days**.

- **Logic**: Any record with a `created_at` timestamp older than 90 days is considered stale and is automatically deleted during a Dreaming (GC) cycle.
- **Purpose**: This ensures that transient project context from months ago does not pollute current search results, while still maintaining a significant long-term history.

---

## 2. The Dreaming Process

The Dreaming process is handled by the `memory_gc.py` module.

### How Dreaming Works:
1. **Targeting**: The GC identifies the `qwen_local_memory` and `qwen_cloud_memory` collections.
2. **Filtering**: It creates a Qdrant range filter: `created_at < (current_time - 90 days)`.
3. **Deletion**: All points matching this filter are permanently removed from the database.

### Triggering a Dreaming Cycle
Dreaming can be triggered in two ways:
1. **Automated**: Integrated into the system's maintenance schedule (TBD).
2. **Manual**: By running the GC script directly via the CLI:
   ```bash
   mega-run-py packages/memory_gc.py
   ```

---

## 3. Storage Considerations

### Capacity
The system does not enforce a hard limit on the number of vectors. Storage is bounded by:
- **Local Tier**: Available disk space on the host machine.
- **Cloud Tier**: The quota provided by the Qdrant Cloud instance.

### Performance Impact
As the number of vectors increases, search latency may increase slightly. Regular Dreaming cycles are recommended to keep the index lean and the retrieval speed high.
