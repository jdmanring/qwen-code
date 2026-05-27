#  Cognitive Integrity Standard

This document defines the standard for "Technical Candor" within the Megalonyx. The goal is to maintain absolute honesty about the state of the system while ensuring that technical depth is never sacrificed for the sake of simplicity.

---

##  The Core Principle: Technical Candor

Technical Candor is the practice of describing a system's state with absolute precision, removing the gap between what a document *claims* and what the code *does*. 

We reject "Posturing"--the use of grandiose language to mask implementation gaps. We replace it with "Grounded Precision."

### 1. The "Implemented" Threshold
In this project, the word **"Implemented"** has a strict technical definition.

- ** NOT Implemented**: A service is written, a prompt is designed, and it works in a single test run or in-memory.
- ** Implemented**: There is a verified, end-to-end execution path from a user's natural language request to a persistent change in the system (e.g., a file written to disk, a record in a database, or a change in a system configuration).

If a feature only works in-memory or requires manual setup not covered by the installer, it must be labeled as a **"Prototype"** or **"Partial Implementation."**

### 2. Precision vs. Jargon (The Groundedness Rule)
We distinguish between **Technical Precision** (which we want) and **AI Jargon** (which we avoid).

| Type | Characteristic | Example | Status |
| :--- | :--- | :--- | :--- |
| **Technical Precision** | Uses the correct industry term to describe a specific mechanism. | "Using a vector database for semantic retrieval." |  **Keep** |
| **AI Jargon** | Uses abstract or grandiose terms to create an impression of intelligence. | "Leveraging high-dimensional cognitive synthesis." |  **Purge** |
| **Oversimplification** | Removes the technical mechanism to make it "relatable." | "The AI finds things in the memory." |  **Avoid** |

**The Standard**: Describe the mechanism precisely, but use plain language to explain the purpose.

### 3. The Gap Analysis Mandate
Every new feature or architectural change must be accompanied by a **Gap Analysis**. This is a candid assessment of the "Distance to Production."

**Required Gap Components**:
1. **The Current State**: What actually works today? (e.g., "The `AgentGenerator` produces a JSON prompt.")
2. **The Missing Link**: What is the exact break in the chain? (e.g., "There is no logic to write this JSON to `config/agents/`.")
3. **The Target State**: What does "Done" look like? (e.g., "The agent is automatically saved and available for the next turn.")

---

##  Operationalizing Honesty

To prevent cognitive debt, agents must apply the following checks during every task:

1. **The Evidence Check**: "Am I claiming this is implemented? If so, can I point to the exact line of code that persists the change?"
2. **The Jargon Check**: "Am I using a word because it is the most precise technical term, or because it sounds impressive?"
3. **The Gap Check**: "Have I been honest about what is still a prototype?"

---

##  Verification Matrix

| Claim | Verification Method | "Implemented" Criteria |
| :--- | :--- | :--- |
| "Feature X is implemented" | End-to-End Trace | User Prompt $\to$ Tool Call $\to$ Filesystem/DB Change $\to$ Verification. |
| "System is synchronized" | Symmetry Check | `symmetry-check.py` returns Exit 0. |
| "Documentation is current" | Blueprint Audit | Every `config/` file has a mirrored `docs/` file with matching intent. |
