# Prompt Optimization Master Guide

This guide defines the professional standards for crafting, optimizing, and validating system prompts within the Qwen Code stack. It is designed to maximize instruction adherence and token efficiency, specifically for the Gemma 4 model family.

## 1. Structural Theory: The XML-Hybrid Approach

To maximize adherence, we move away from plain-text instructions and adopt an **XML-Hybrid Structure**. This leverages the model's ability to recognize semantic boundaries and hierarchy.

### The Hierarchy
Prompts should be wrapped in a high-level `<system_instructions>` tag and divided into the following functional blocks:

- `<identity>`: Defines the persona, expertise, and core objective.
- `<operational_law>`: Contains non-negotiable behavioral rules.
    - `<core_mandates>`: Fundamental laws of operation.
    - `<critical_constraints>`: Safety and operational boundaries (e.g., No-Direct-Execution).
- `<capabilities>`: Defines what the agent *can* do.
    - `<tools>`: MCP tool definitions.
    - `<skills>`: Workflow macro references.
- `<output_protocol>`: Defines how the agent *must* respond.
    - `<format_requirements>`: JSON schemas or structural mandates.
- `<critical_reminders>`: A condensed summary of the most important rules.

### Why this works
XML tags act as "anchor points" for the model's attention. By categorizing instructions, we prevent "prompt drift" where the model confuses a capability with a constraint.

---

## 2. The Positioning Law: Primacy & Recency

LLMs suffer from the "Lost-in-the-Middle" phenomenon. To combat this, we use a **Primacy-Recency** layout.

### The Layout Strategy
1. **Primacy (Top)**: Place the `<identity>` and `<operational_law>` first. This establishes the "mental frame" for the entire session.
2. **The Middle**: Place `<capabilities>` and `<output_protocol>`. These are reference materials the model accesses as needed.
3. **Recency (Bottom)**: Place `<critical_reminders>` last. This ensures that the most critical constraints are the last things the model "sees" before generating a response.

---

## 3. The Compression Protocol: Lean Mandates

Token efficiency is not just about saving money; it's about reducing noise. Noise leads to "prompt dilution," where the model ignores rules because there is too much fluff.

### Conversion Rules
| Verbose Pattern (AVOID) | Lean Pattern (USE) | Example |
| :--- | :--- | :--- |
| "It is very important that you..." | **MANDATE:** | `MANDATE: Always paginate files.` |
| "The agent should try to avoid..." | **AVOID:** | `AVOID: Direct execution in Blueprint.` |
| "Please ensure that you always..." | **MUST:** | `MUST: Verify context before editing.` |
| "In the event that X happens, do Y." | **IF X $\rightarrow$ Y** | `IF truncated $\rightarrow$ use offset/limit.` |

**The Goal**: Every token must provide semantic value. If a word can be removed without changing the meaning of the rule, it MUST be removed.

---

## 4. Hyperparameter Alignment

A prompt is only as good as the sampling parameters that run it.

| Parameter | Purpose | Gemma 4 Optimal Range |
| :--- | :--- | :--- |
| **Temperature** | Creativity vs. Precision | `0.6 - 0.8` (Lower for coding/logic) |
| **Top_P** | Nucleus Sampling | `0.9 - 0.95` |
| **Repetition Penalty**| Loop Prevention | `1.15 - 1.20` (Crucial for MoE models) |
| **Stop Sequences** | Hard Termination | `["<|end_of_turn|>", "User:"]` |

---

## 5. The Iteration Loop (The Optimizer's Path)

Optimization is an empirical process, not a guessing game.

1. **DETECTION**: Identify a behavioral failure (e.g., the agent ignores the No-Direct-Execution rule).
2. **ANALYSIS**: Determine if the failure is due to:
    - **Missing Rule**: The rule isn't in the prompt.
    - **Dilution**: The rule is buried in too much text.
    - **Conflict**: Another rule is contradicting it.
3. **HYPOTHESIS**: Propose a fix (e.g., "Move rule to `<critical_reminders>`" or "Convert to Lean Mandate").
4. **VALIDATION**: Run the new version against the **Stability Harness** (see `docs/models/stability_benchmark.md`).
5. **INSTITUTIONALIZATION**: Update the Model Recipe and `QWEN.md`.
