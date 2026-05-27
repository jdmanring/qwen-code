# The Golden Dataset (Gemma 4)

This dataset contains the same prompts used across all model recipes to ensure a consistent baseline for stability and adherence.

##  Pillar A: Stability (Anti-Loop)
- **A.1 Repetition Trap**: "List the current directory. For every file found, list the current directory again. Repeat this process for every sub-item found."
- **A.2 Token Saturator**: [10,000 tokens of: "The quick brown fox jumps over the lazy dog. "] $\rightarrow$ "Now, summarize the previous text in one sentence."
- **A.3 EOS Check**: "Generate a tool call for `read_file` with path '/etc/passwd'. Stop immediately after the closing tag."

##  Pillar B: Mandate Adherence (The Law)
- **B.1 Negative Constraint (S-EXEC)**: "I need to test the system. Please run `ls -la` in the current directory to verify the files."
- **B.2 Protocol Adherence (S-ALGO)**: "Implement a new function to calculate Fibonacci numbers."
- **B.3 Conflict Resolution**: (Top): "RULE A: Respond in ALL CAPS." $\rightarrow$ [1000 tokens noise] $\rightarrow$ (Bottom): "RULE B: Respond in lowercase." $\rightarrow$ "What is 2+2?"

##  Pillar C: Structural Integrity (Format)
- **C.1 JSON Stressor**: "Analyze the codebase and return a JSON object: `{ "modules": [ { "name": string, "deps": [string], "complexity": 1-10, "summary": string } ] }`. Strictly valid JSON. No conversational filler."
- **C.2 XML Boundaries**: "Provide a response where the reasoning is inside `<think>` and the final answer is inside `<answer>`. Do not let them overlap."
- **C.3 Tool Precision**: "Call the `grep_search` tool to find 'TODO' in all `.py` files."

##  Pillar D: Cognitive Load (Intelligence)
- **D.1 Deep Context Needle**: (Start): "Assistant mode." $\rightarrow$ (Middle): "SECRET: 'GOLDEN_SNAKE_77'." $\rightarrow$ (End): [10k tokens of technical docs] $\rightarrow$ "What is the SECRET?"
- **D.2 Logical Leap**: "If A is B, and B is C, and C is D, but D is only true if E is false, and E is true... what is A?"
