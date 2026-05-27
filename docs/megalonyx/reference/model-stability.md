#  Model Stability & Repetition Control

This document tracks known model-level instabilities and the corresponding sampling configurations required to maintain deterministic, non-looping output.

---

## 1. The "Infinite Repetition" Bug (Gemma 4)

### **Affected Models**
- `google/gemma-4-31B-it`
- `google/gemma-4-26B-A4B-it`

### **Symptom**
The model enters a degenerate state where it repeats a phrase or a sequence of tokens with minor variations indefinitely. This is most prevalent during **structured output generation** (e.g., JSON schema enforcement), where the grammar constraints prevent the model from generating an EOS (End of Sequence) token, trapping it in a high-probability loop.

### **Recommended Mitigation (Sampling Parameters)**
To break the repetition bias without degrading the quality of naturally repetitive text (like tables or lists), the following parameters are recommended:

| Parameter | Value | Note |
| :--- | :--- | :--- |
| `repetition_penalty` | `1.15` $\rightarrow$ `1.20` | **Critical**. `1.18` is the observed sweet spot for Gemma 4. |
| `temperature` | `0.7` | Lowering temperature reduces the probability of entering a degenerate loop. |
| `top_p` | `0.95` | Maintains diversity while filtering out low-probability noise. |
| `max_tokens` | `16000` | Acts as a hard circuit-breaker for failed loops. |

---

## 2. Repetition Control Theory

### **Strategic vs. Stream Looping**

The system distinguishes between two types of repetition:

1.  **Strategic Looping (Livelock)**:
    - **Definition**: The agent repeats the same high-level action or tool call across multiple turns.
    - **Detection**: Handled by `SystemWatchdog` via response hashing.
    - **Remedy**: Reflection prompts and strategy pivots.

2.  **Stream Looping (Token Degeneration)**:
    - **Definition**: The model repeats tokens/phrases within a single response.
    - **Detection**: Requires real-time stream interception (n-gram analysis).
    - **Remedy**: `repetition_penalty` and immediate stream termination.

---

## 3. General Stability Guidelines

For any model exhibiting looping behavior:
1. **Increase `repetition_penalty`** in increments of `0.02`.
2. **Decrease `temperature`** to move the model toward more deterministic paths.
3. **Verify Stop Sequences**: Ensure the model is correctly configured to recognize the EOS token for the specific chat template being used.
