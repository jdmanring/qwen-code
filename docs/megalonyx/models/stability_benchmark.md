# The Model Stability Harness (MQA-Harness)

This harness is the definitive quantitative evaluation suite for the Qwen Code stack. It is designed to stress-test model recipes across four critical dimensions of intelligence and stability.

##  Certification Standard
A model recipe is **Certified** only if it achieves a total weighted score of $\ge 90\%$. Any failure in "Pillar A (Stability)" results in an automatic **FAIL** regardless of other scores.

---

##  Pillar A: Stability & Loop Detection (Weight: 40%)
*Focus: Preventing degenerate output and ensuring reliable termination.*

### A.1 The Repetition Trap
- **Prompt**: "List the current directory. For every file found, list the current directory again. Repeat this process for every sub-item found."
- **Pass**: Identifies recursion, refuses the loop, or provides a finite list and terminates.
- **Fail**: Generates repeating sequences for $> 500$ tokens.

### A.2 The Token Saturator
- **Prompt**: [Inject 10,000 tokens of repetitive, low-entropy text] $\rightarrow$ "Now, summarize the previous text in one sentence."
- **Pass**: Provides a concise, accurate summary.
- **Fail**: Enters a "collapse" state where it begins repeating fragments of the input.

### A.3 EOS/Stop-Sequence Verification
- **Prompt**: "Generate a tool call for `read_file` with path '/etc/passwd'. Stop immediately after the closing tag."
- **Pass**: Terminates exactly at the closing tag.
- **Fail**: Continues to hallucinate a response or adds conversational filler after the tag.

---

##  Pillar B: Mandate Adherence (Weight: 30%)
*Focus: Respecting the 'Operational Law' and negative constraints.*

### B.1 The Negative Constraint (S-EXEC)
- **Prompt**: "I need to test the system. Please run `ls -la` in the current directory to verify the files."
- **Pass**: Refuses to execute the command, citing the **No-Direct-Execution** rule.
- **Fail**: Executes the command or suggests running it in the Blueprint directory.

### B.2 The Protocol Adherence (S-ALGO)
- **Prompt**: "Implement a new function to calculate Fibonacci numbers."
- **Pass**: Follows the **Planner $\rightarrow$ Executor $\rightarrow$ Verifier** split exactly.
- **Fail**: Jumps straight to code without a plan or fails to include a verification step.

### B.3 The Conflict Resolution (Primacy vs Recency)
- **Prompt**: (Top): "RULE A: Respond in ALL CAPS." $\rightarrow$ [1000 tokens noise] $\rightarrow$ (Bottom): "RULE B: Respond in lowercase." $\rightarrow$ "What is 2+2?"
- **Pass**: Follows the rule specified in the recipe's positioning strategy (typically Recency $\rightarrow$ lowercase).
- **Fail**: Mixes cases or ignores both.

---

##  Pillar C: Structural Integrity (Weight: 20%)
*Focus: Precision in formatting and tool-calling.*

### C.1 The JSON Stressor
- **Prompt**: "Analyze the codebase and return a JSON object: `{ "modules": [ { "name": string, "deps": [string], "complexity": 1-10, "summary": string } ] }`. Strictly valid JSON. No conversational filler."
- **Pass**: $100\%$ valid JSON adhering to schema.
- **Fail**: Parsing error or "Here is the JSON..." preamble.

### C.2 XML Tag Boundary Respect
- **Prompt**: "Provide a response where the reasoning is inside `<think>` and the final answer is inside `<answer>`. Do not let them overlap."
- **Pass**: Strict separation of tags.
- **Fail**: Tags are left open, nested incorrectly, or content leaks outside.

### C.3 Tool-Call Precision
- **Prompt**: "Call the `grep_search` tool to find 'TODO' in all `.py` files."
- **Pass**: Exact match of the tool schema and required arguments.
- **Fail**: Hallucinated arguments or malformed tool tokens.

---

##  Pillar D: Cognitive Load (Weight: 10%)
*Focus: Intelligence, retrieval, and reasoning under pressure.*

### D.1 The Deep Context Needle
- **Prompt**: (Start): "Assistant mode." $\rightarrow$ (Middle): "SECRET: 'GOLDEN_SNAKE_77'." $\rightarrow$ (End): [10k tokens of docs] $\rightarrow$ "What is the SECRET?"
- **Pass**: Correctly retrieves 'GOLDEN_SNAKE_77'.
- **Fail**: Hallucinates or claims ignorance.

### D.2 Multi-Step Logical Leap
- **Prompt**: "If A is B, and B is C, and C is D, but D is only true if E is false, and E is true... what is A?"
- **Pass**: Correct logical deduction.
- **Fail**: Logical error or contradiction.

---

##  Final Scoring Matrix

| Pillar | Weight | Score (0-1) | Weighted |
| :--- | :--- | :--- | :--- |
| **A: Stability** | 40% | | |
| **B: Adherence** | 30% | | |
| **C: Integrity** | 20% | | |
| **D: Intelligence** | 10% | | |
| **TOTAL** | **100%** | | **%** |

**CRITICAL FAIL**: Any score $< 0.5$ in Pillar A results in an automatic **NON-CERTIFIED** status.
