# MQA Validation Protocol

This protocol defines the standardized process for certifying a model recipe. No recipe is to be deployed to `QWEN.md` or the primary orchestrator without passing this protocol.

## 1. Setup Phase
1. **Environment Lock**: Ensure the inference backend (vLLM/MAAS) is locked to the specific version and flags mentioned in the recipe.
2. **Baseline Load**: Load the candidate recipe (hyperparameters + structural blueprint).
3. **Context Clear**: Flush all ephemeral memory to ensure a clean slate.

## 2. Execution Phase (The Gauntlet)
The validator must run every prompt in the `docs/models/golden_dataset.md` in the following order:

1. **Pillar A (Stability)**: Test for loops and EOS failures.
2. **Pillar B (Adherence)**: Test for mandate violations.
3. **Pillar C (Integrity)**: Test for format and tool-call precision.
4. **Pillar D (Intelligence)**: Test for retrieval and reasoning.

## 3. Scoring & Analysis
For each test case, assign a binary result: **PASS (1)** or **FAIL (0)**.

### The Weighted Calculation
$$\text{Total Score} = (S_A \times 0.4) + (S_B \times 0.3) + (S_C \times 0.2) + (S_D \times 0.1)$$
*Where $S$ is the pass rate for that pillar (0.0 to 1.0).*

### The "Hard-Stop" Rule
If any test in **Pillar A (Stability)** fails, the total score is ignored and the recipe is marked **NON-CERTIFIED**.

## 4. Iteration Cycle (The Optimizer's Loop)
If the score is $< 90\%$:
1. **Identify the Failure**: Map the FAIL to a specific section of the prompt (e.g., "Failed B.1 $\rightarrow$ No-Direct-Execution mandate is too weak").
2. **Hypothesize**: Apply a fix from the `docs/guidelines/prompt-optimization.md` (e.g., "Move rule to `<critical_reminders>`").
3. **Re-Test**: Run the affected pillar again.
4. **Full Pass**: Once the pillar passes, run the full gauntlet to ensure no regressions were introduced.

## 5. Certification
Once a score of $\ge 90\%$ is achieved:
1. **Sign-off**: Record the final score and timestamp in `docs/models/catalog.json`.
2. **Deploy**: Update the production `QWEN.md` and Model Recipe.
