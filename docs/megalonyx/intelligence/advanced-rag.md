# Advanced RAG & Semantic Intelligence

This document defines the technical architecture for the evolution of the `qwen_code_stack` memory system, moving from basic vector retrieval to deep structural understanding.

## 1. The Dreaming Pipeline (Background Consolidation)

The "Dreaming" process is a background cognitive cycle that prevents memory bloat and improves recall precision.

### 1.1 The Consolidation Loop
Every hour, the `memory_daemon` executes the following sequence:
1. **Semantic Clustering**: Grouping related memory points using a density-based clustering algorithm.
2. **Deduplication**: Removing redundant information using content hashing and semantic similarity.
3. **Synthesis**: Using a lightweight LLM to consolidate multiple fragmented memories into a single, high-density "Architectural Anchor."
4. **Pruning**: Evicting low-utility or contradictory information based on a "Decay Score."

## 2. CRAG (Corrective Retrieval-Augmented Generation)

To eliminate hallucinations in retrieval, the system implements a **Self-Correcting Retrieval** loop.

### 2.1 The Verification Cycle
1. **Retrieve**: Fetch top-K documents from Qdrant.
2. **Evaluate**: A "Judge" agent assesses the relevance of each document to the query.
3. **Refine**: If relevance is low, the system automatically reformulates the query and performs a second, targeted search.
4. **Synthesize**: Only verified, high-relevance documents are passed to the final generation step.

## 3. GraphRAG: Structural Knowledge Mapping

The system moves beyond flat vector search to a **Graph-based** representation of the codebase.

### 3.1 The Knowledge Graph
- **Nodes**: Functions, Classes, Modules, and Axioms.
- **Edges**: Call relationships, Inheritance, and "Symmetry Links."
- **Querying**: Using Cypher-like queries to find "The ripple effect of changing function X" or "The architectural path from API $\to$ DB."

## 4. Race-to-Deadline Recall

To eliminate perceived latency, the system implements a strict **2.5s Deadline** for all memory retrievals.
- **Parallel Dispatch**: Queries are sent to Local and Cloud tiers simultaneously.
- **First-Hit Return**: The system returns the first high-confidence result, updating the context asynchronously if a better result arrives later.

## 5. Implementation Status
- **[Current]**: Basic hash-based deduplication in the Dreaming thread.
- **[Target]**: Full integration of CRAG and GraphRAG into the `MemoryAuthority` routing logic.
