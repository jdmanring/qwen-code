# Optimal Orchestrator Structure (Gemma 4)

This document defines the structural blueprint for the Primary Agent's system prompt. It leverages XML-style semantic tagging mapped to native chat roles to maximize instruction adherence and minimize token waste.

## 1. Structural Hierarchy

The prompt should be constructed as a single **System Role** block with the following internal hierarchy:

```xml
<system_instructions>
  <!-- 1. IDENTITY & ROLE -->
  <identity>
    [Clear, concise definition of the agent's persona, expertise, and primary objective.]
  </identity>

  <!-- 2. OPERATIONAL LAW (The "Law") -->
  <operational_law>
    <core_mandates>
      [Fundamental behavioral rules. Use imperatives: "ALWAYS", "NEVER", "MUST".]
    </core_mandates>
    <critical_constraints>
      [Non-negotiable safety and operational boundaries. e.g., "No-Direct-Execution Rule".]
    </critical_constraints>
  </operational_law>

  <!-- 3. CAPABILITIES & TOOLS -->
  <capabilities>
    <tools>
      [Tool definitions and schemas. Map to native <|tool|> tokens where possible.]
    </tools>
    <skills>
      [High-level workflow macros and protocol references.]
    </skills>
  </capabilities>

  <!-- 4. OUTPUT PROTOCOL -->
  <output_protocol>
    <format_requirements>
      [Strict formatting rules, JSON schemas, or structured output mandates.]
    </format_requirements>
    <stop_sequences>
      [Definition of when to terminate the response.]
    </stop_sequences>
  </output_protocol>

  <!-- 5. RECENCY REINFORCEMENT -->
  <critical_reminders>
    [A condensed list of the top 3 most frequently violated constraints. 
     Placed here to leverage the recency effect.]
  </critical_reminders>
</system_instructions>
```

## 2. Implementation Guidelines

### A. Semantic Mapping
- **System Role**: The entire block above resides in the `system` role of the chat template.
- **User Role**: Contains the current request and ephemeral context.
- **Model Role**: The agent's response, starting with `<|think|>` if reasoning is enabled.

### B. Token Efficiency Rules
- **Imperative Language**: Replace "The agent should try to avoid..." with "AVOID...".
- **Attribute-Based tags**: For repetitive lists, use attributes: `<rule id="1" priority="high">...</rule>`.
- **No Conversational Filler**: Remove all preambles and "politeness" markers.

### C. Positioning Strategy
- **Primacy**: Core identity and the "Law" are placed first.
- **Recency**: The `<critical_reminders>` block is placed last to ensure the model doesn't "forget" the most important rules during long prompts.
