# 🏗️ Prompt Architecture: The Cognitive Sandwich

This document describes how the Sovereign stack constructs prompts to ensure strict operational control and consistent AI behavior.

## 🥪 The Prompt Hierarchy

The system does not send raw user queries to the LLM. Instead, it constructs a "Cognitive Sandwich"—a layered prompt that wraps the user's intent in strict operational constraints.

### Construction Sequence (Top to Bottom)

1. **Identity Layer (The Persona)**
   - **Source**: `config/agents/[agent].md`
   - **Purpose**: Establishes the expert identity, goals, and behavioral boundaries of the agent.

2. **Operational Law Layer (The Constitution)**
   - **Source**: `QWEN.md`
   - **Purpose**: Injects the global axioms (`S-READ`, `S-SNAP`, `P-AUTH`, etc.) that the AI must follow regardless of its persona.

3. **State Context Layer (The Situation)**
   - **Source**: `skill_bridge.py` (Dynamic)
   - **Purpose**: Provides the AI with its current operational state:
     - **Current Phase**: (e.g., `PLANNING`, `EXECUTION`, `VERIFICATION`).
     - **Todo List**: A real-time snapshot of completed and pending tasks.
     - **Runtime Variables**: Current CWD, OS, and active toolset.

4. **Conversation History Layer (The Memory)**
   - **Source**: Session History / Memory Bridge
   - **Purpose**: Provides the necessary context from previous turns, pruned for token efficiency.

5. **Query Layer (The Intent)**
   - **Source**: User Input
   - **Purpose**: The specific task or question the user wants the AI to address.

---

## 🛡️ Programmatic Enforcement

To prevent "Prompt Leakage" or "Instruction Drift," the system employs two enforcement mechanisms:

### 1. Instructional Enforcement
The `AgentGeneratorService` uses `QWEN.md` as a template when creating or refining agent personas, ensuring that the "Law" is baked into the identity.

### 2. Structural Enforcement (The Policy Engine)
The `PolicyEngine` (`packages/core/src/policy_engine.py`) acts as a hard guardrail. It does not rely on the LLM's "willingness" to follow instructions. Instead, it:
- Intercepts every tool call.
- Checks the `intent` and `agent_name` against a permission matrix.
- Blocks unauthorized actions (e.g., preventing a `Developer` agent from modifying `QWEN.md` without `Architect` approval).

## 🔄 Feedback Loop
The output of the LLM is parsed for tool calls. If a tool call is made, the result is fed back into the **State Context Layer**, updating the "Situation" before the next turn.
