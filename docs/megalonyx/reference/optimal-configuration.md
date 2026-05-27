#  Optimal Configuration Guide: Memory & RAG

This guide provides the recommended `settings.json` configuration for the Mega Code stack. These settings are designed to maximize the performance of the Semantic Memory system while eliminating "Divergence Debt" caused by native Qwen Code features.

## 1. The "Gold Standard" Configuration

Add or update the following sections in your `~/.qwen/settings.json`:

```json
{
  "memory": {
    "enableManagedAutoMemory": false,
    "enableManagedAutoDream": false,
    "policy": {
      "cloud_signals": [
        "architecture", "preference", "always", "never",
        "standard", "policy", "remember", "long-term", "project",
        "decision", "convention", "constraint"
      ],
      "noise_words": [
        "ok", "okay", "yes", "no", "thanks", "cool", "nice", 
        "understood", "got it", "sure", "perfect", "right"
      ],
      "dedup_window_size": 1000
    }
  }
}
```

---

## 2. Technical Justification

### Why disable `enableManagedAutoMemory`?
Native "Auto-memory" writes plain-text markdown files to your disk. Our custom system uses a **Vector Database (Qdrant)**. Enabling both creates two competing sources of truth. By disabling the native feature, we ensure that the agent relies solely on the high-fidelity RAG system, preventing contradictions and context bloat.

### Why disable `enableManagedAutoDream`?
The native "Dreaming" process deletes markdown files. Our system implements a more robust, age-based pruning cycle in `packages/memory_gc.py`. We maintain the "Dreaming" concept (periodic cleanup) but execute it via a systematic Garbage Collection process.

### Routing Logic (`cloud_signals`)
We have expanded the signals to include `decision`, `convention`, and `constraint`. This ensures that any "Law of the Project" is automatically routed to the **Cloud Tier**, which is designed for long-term, high-importance architectural knowledge.

### Noise Filtering (`noise_words`)
To prevent the vector database from being polluted with conversational filler, we use a strict noise filter. Any input consisting solely of these words is rejected before it ever reaches the embedding model.

---

## 3. Maintenance Checklist

To keep your memory system in peak condition, follow these guidelines:

1.  **Trigger a "Dreaming" Cycle**: Periodically run the GC script to prune stale memories (default 90 days).
    ```bash
    mega-run-py packages/memory_gc.py
    ```
2.  **Audit your `QWEN.md`**: If you find the agent is consistently making a behavioral mistake, do not "remember" it in the RAG system--update the **Instructional Memory** in `QWEN.md`.
3.  **Verify Connectivity**: If recall feels slow, check the status of your local Qdrant instance.
    ```bash
    mega-status
    ```
