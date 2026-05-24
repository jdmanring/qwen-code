# 🔍 Memory Gap Analysis: Native vs. Custom RAG

This document analyzes the differences between the native Qwen Code memory features and the custom Semantic Memory system implemented in the Mega Code stack.

## 1. Feature Mapping

The following table maps the "Native" features described in official documentation to our "Custom" high-fidelity implementation.

| Native Feature | Native Mechanism | Custom Implementation | Improvement |
| :--- | :--- | :--- | :--- |
| **Auto-Memory** | AI writes `.md` notes to disk. | `ingest` $\rightarrow$ Qdrant Vectors. | **Precision**: Vector search is far more accurate than keyword/file search. |
| **Dreaming** | `/dream` command deletes old files. | `memory_gc.py` (Age-based pruning). | **Automation**: Pruning is handled by a systematic GC cycle rather than manual triggers. |
| **Permanent Memory** | `QWEN.md` plain text file. | `QWEN.md` $\rightarrow$ System Prompt. | **Directness**: No change; we maintain this as the "Instructional Memory" layer. |
| **Context Recall** | File-based retrieval of notes. | `search` / `reflect` $\rightarrow$ RAG. | **Scale**: Handles thousands of facts without bloating the context window. |

---

## 2. The "Divergence Debt" Risk

A critical finding of this analysis is the risk of **Divergence Debt**. 

If both the native "Auto-memory" (flat files) and the custom "Semantic Memory" (vectors) are enabled, the agent will have two competing sources of truth. This leads to:
1. **Contradictions**: A fact updated in Qdrant might still exist in an old `.md` file.
2. **Context Bloat**: The model may retrieve the same fact twice (once from a file, once from a vector).
3. **Cognitive Load**: The model must decide which "memory" to trust.

**Decision**: To eliminate this risk, all native `managedAutoMemory` and `managedAutoDream` settings MUST be set to `false`.

---

## 3. Identified Gaps & Opportunities

While our system is technically superior, we identified a few "UX Gaps" from the native implementation:

### Gap 1: User-Facing "Dreaming" Concept
The native system uses the term "Dreaming" for cleanup. Our system uses "Garbage Collection."
- **Opportunity**: Rename our GC process to "Dreaming" in the documentation and `QWEN.md` to align with the Qwen Code mental model.

### Gap 2: Explicit "Best-Effort" vs "Guaranteed" Distinction
The native docs distinguish between `QWEN.md` (Guaranteed) and Auto-memory (Best-effort).
- **Opportunity**: Explicitly label our Semantic Memory as "Best-effort" (since RAG can occasionally miss a fragment) and `QWEN.md` as "Guaranteed" in the taxonomy.

---

## 4. Conclusion

The custom RAG system fully supersedes the native auto-memory features. By disabling the native plumbing and adopting the native terminology, we achieve a "World-Class" integration: the power of a vector database with the feel of a native Qwen Code feature.
