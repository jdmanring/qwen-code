# 🧠 Memory Taxonomy: The Three Layers of Cognition

In the Mega Code system, "Memory" is not a single feature but a hierarchy of three distinct cognitive layers. Confusing these layers leads to suboptimal agent behavior. This document formally defines the taxonomy to ensure clear communication between developers and the AI.

---

## 1. Instructional Memory (The "Law")
**Nature**: Static, Rule-Based, Behavioral.
**Primary Artifact**: `QWEN.md` (and system prompts).

Instructional Memory defines **HOW** the agent should behave. It is the "Behavioral Constitution" of the system. It does not store facts about the project, but rather the standards for operating within the project.

- **Scope**: Personas, coding standards, tool-use protocols, and safety constraints.
- **Mechanism**: Injected directly into the System Prompt at session start.
- **Update Cycle**: Updated via the `SYSTEM OPTIMIZER` skill or manual edits when a behavioral failure is identified.
- **Example**: *"Always use absolute paths when calling file tools."*

---

## 2. Semantic Memory (The "Library")
**Nature**: Dynamic, Fact-Based, Searchable.
**Primary Artifact**: `mega-memory-manager` (MCP Server $\rightarrow$ Qdrant).

Semantic Memory defines **WHAT** the project is. It is a durable record of architectural decisions, historical context, and technical facts.

- **Scope**: API specifications, design decisions, "lessons learned," and project history.
- **Mechanism**: Vector-based RAG (Retrieval Augmented Generation). The agent uses `search` and `reflect` tools to pull relevant facts into the context window.
- **Update Cycle**: Continuously updated via the `ingest` tool during the development process.
- **Example**: *"The decision to use Qdrant for the local tier was made on May 12th to ensure sub-10ms latency."*

---

## 3. Ephemeral Memory (The "Conversation")
**Nature**: Transient, Sequence-Based, Immediate.
**Primary Artifact**: The LLM Context Window.

Ephemeral Memory is the "Working Memory" of the current session. It tracks the immediate flow of the conversation.

- **Scope**: Current task state, recent tool outputs, and the immediate dialogue history.
- **Mechanism**: The sliding window of the LLM's context.
- **Update Cycle**: Updated with every turn of the conversation.
- **Example**: *"The user just asked me to fix the bug in `memory_daemon.py` that I found in the previous turn."*

---

## Summary Comparison Table

| Feature | Instructional Memory | Semantic Memory | Ephemeral Memory |
| :--- | :--- | :--- | :--- |
| **Question it Answers** | "How do I act?" | "What is the fact?" | "What just happened?" |
| **Storage** | `QWEN.md` / System Prompt | Qdrant Vector DB | LLM Context Window |
| **Access Method** | Automatic (Prompt) | Explicit (MCP Tools) | Automatic (History) |
| **Durability** | Permanent (until edited) | Permanent (until GC) | Transient (session-based) |
| **Update Trigger** | Behavioral Failure | New Knowledge | New Message |
