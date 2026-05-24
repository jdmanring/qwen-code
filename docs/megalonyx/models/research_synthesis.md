# MORL: Research Synthesis - Gemma 4 Optimization

This document synthesizes findings from external research and community intelligence regarding the optimization of Google Gemma 4 models (`gemma-4-31B-it` and `gemma-4-26B-A4B-it`) within the Qwen Code orchestrator role.

## 1. Prompt Structuring & XML Tagging
### Findings
- **Native Templates > Raw XML**: Gemma 4 relies heavily on its native chat template and control tokens (e.g., `<|think|>`, `<|channel|>`, `<|tool_call|>`).
- **Hybrid Approach**: The most effective structure is a hybrid:
    - Use **Native Roles** (System, User, Model) for top-level separation.
    - Use **XML-style tags** (e.g., `<constraints>`, `<context>`, `<rules>`) *inside* the system role to create semantic hierarchies.
    - Map conceptual "tool" sections to the model's native `<|tool>` control tokens.
- **Instruction Positioning**: "Lost-in-the-Middle" is a factor. Critical mandates should be placed in the **System Role** (Primacy) and repeated/summarized at the **end of the prompt** (Recency) just before the user input.

## 2. Token Compression & Efficiency
### Strategies
- **Semantic Paraphrasing**: Replace verbose phrases ("It is absolutely critical that you always...") with direct imperatives ("MANDATE: ...").
- **Compact Schemas**: Use minimal XML attributes or YAML for tool descriptions.
- **Token-Lean Mandates**: Strip conversational fillers and "politeness" from the system prompt.

## 3. Stability & Anti-Looping
### Findings
- **Repetition Collapse**: Looping often occurs when the model fails to generate the EOS (End of Sequence) token or gets stuck in a degenerate pattern.
- **Mitigation**:
    - **Sampling**: `repetition_penalty` (1.15 - 1.20), `temperature` (~0.7), `top_p` (~0.95).
    - **Stop Sequences**: Use closing control tokens (e.g., closing tool tags) as hard stop markers.
    - **Structured Output**: Enforce strict JSON/Schema parsing; treat malformed output as a trigger for a "correction" loop rather than allowing it to continue.

## 4. Model Comparison: 31B vs 26B-A4B
| Feature | gemma-4-31B-it (Dense) | gemma-4-26B-A4B-it (MoE) |
| :--- | :--- | :--- |
| **Quality** | Higher raw reasoning/coding quality | High, but slightly lower in complex benchmarks |
| **Speed** | Slower (all parameters active) | Much faster (partial activation) |
| **Memory** | Higher VRAM requirement | Lower active memory footprint |
| **Best Use Case** | Complex architectural design, deep debugging | High-frequency orchestration, multi-turn tool loops |

## 5. Evidence Gaps (Areas for Internal Validation)
The following require empirical testing within the Qwen Code environment:
- **Quantitative Tagging Gain**: Does `<constraints>` actually increase adherence vs a bulleted list?
- **Stop Sequence Ranking**: Which specific sentinel tokens most effectively kill loops?
- **Positioning Curve**: Exactly where is the "sweet spot" for repeated instructions?
