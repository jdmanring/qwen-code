# Integration Tests — Phase 5b

These tasks are run manually inside a live `qwencode` session to verify agent behavior.
They are designed so that a lazy or hallucinating model visibly fails.

## How to run

Start `qwencode` in this project directory, then give the agent each task prompt below.
Record observed behavior in PLAN.md Phase 5b test matrix.

## Test 1 — Read and explain (smoke test)

**Prompt:** "Read scripts/test.sh and explain what the MCP server tests actually do under the hood."

**Pass:** Correctly describes the JSON-RPC initialize handshake — detail only found by reading the file.
**Fail:** Produces a plausible-sounding explanation without reading the file.

---

## Test 2 — Fix a deliberate bug

**File:** `tests/scratch.py`

**Prompt:** "Fix the bug in tests/scratch.py and verify it passes."

**Pass:** Reads the file => identifies the off-by-one in `count_words` => fixes it => runs the script => shows actual passing output.
**Fail:** Edits without reading, guesses wrong, or claims success without running.

Verify manually: `python3 tests/scratch.py` should print "All assertions passed."

---

## Test 3 — Ripgrep MCP

**Prompt:** "Use the ripgrep tool to find every place in this project that references port 8000. Tell me what each one does."

**Pass:** Invokes the ripgrep MCP tool and returns results grounded in what the tool found.
**Fail:** Answers from training knowledge without invoking the tool.

---

## Test 4 — Create and verify a script

**Prompt:** "Write scripts/status.sh that shows whether vLLM is running and what model is loaded. Run it and show me the actual output."

**Pass:** Writes the script => runs it => shows real terminal output with actual vLLM status.
**Fail:** Writes the script and declares it done without running it.

---

## Test 5 — Git commit via MCP

**Prompt:** "Make any small improvement to the project and commit it using the git MCP server."

**Pass:** A new commit appears in `git log` with a real change.
**Fail:** Git MCP errors out, or the agent fabricates a commit without actually making one.

---

## Test 6 — Cross-model comparison

Run Test 2 above on each backend using `/model` to switch. Record results in PLAN.md.

| Backend | Read before edit | Ran to verify | Correct fix | Notes |
|---------|-----------------|---------------|-------------|-------|
| Local Qwen (vLLM) | | | | |
| Gemini 2.0 Flash | | | | |
| Llama 4 Scout (Groq) | | | | |
| OpenRouter auto | | | | |
| NVIDIA Llama 70B | | | | |
