Recommended Prompt Engineering Loop

Use this exact process.

STEP 1
------
Feed original QWEN.md into Gemini 2.5 Flash.

Ask:
- identify duplicated rules
- identify conflicting instructions
- identify token-heavy sections
- preserve all behavioral constraints

STEP 2
------
Feed Gemini analysis + original prompt into
Qwen3 Coder 480B.

Ask:
- rewrite for token efficiency
- preserve semantic behavior exactly
- improve hierarchy
- reduce ambiguity
- optimize for agent orchestration

STEP 3
------
Feed compressed version into GPT-OSS 120B.

Ask:
- identify lost constraints
- identify instruction collisions
- identify underspecified behaviors
- adversarially critique the prompt

STEP 4
------
Feed audited prompt into Gemma 4 31B.

Ask:
- improve conversational stability
- improve orchestration clarity
- improve routing behavior
- maintain compactness

STEP 5
------
Freeze prompt version.
Track revisions in git.
Best Prompt Compression Prompt

Use this with Qwen3 Coder 480B:

You are optimizing a production orchestration prompt for an autonomous
multi-agent coding system.

GOALS
-----
1. Preserve ALL behavioral fidelity.
2. Preserve ALL constraints.
3. Preserve ALL routing logic.
4. Reduce token count aggressively.
5. Eliminate redundancy.
6. Improve hierarchical clarity.
7. Improve deterministic interpretation.
8. Reduce ambiguity.
9. Improve tool-routing consistency.
10. Preserve orchestration stability.

RULES
-----
- DO NOT summarize.
- DO NOT simplify behavior.
- DO NOT remove safety-critical instructions.
- DO NOT collapse distinct behaviors together.
- Preserve operational semantics exactly.
- Prefer compact structural wording.
- Remove duplicate wording.
- Normalize repeated rules into unified directives.
- Convert prose into concise operational language.
- Prefer deterministic wording over conversational wording.

OUTPUT
------
1. Optimized prompt
2. Token reduction analysis
3. List of merged redundancies
4. List of preserved critical constraints
5. Risk assessment for behavioral drift
Best Free Stack You Currently Have

You already possess an unusually strong free prompt-engineering stack:

Role	Model
Ingestion	gemini-2.5-flash
Compression	qwen/qwen3-coder-480b-a35b-instruct:free
Audit	openai/gpt-oss-120b:free
Polish	gemma-4-31b-it
Tool prompts	codestral-latest

That is honestly a very capable orchestration lab already.
