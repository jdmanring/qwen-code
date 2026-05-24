# Failure Modes

## 1. Vector Dimension Mismatch

Symptom:
- Qdrant insert errors

Cause:
- wrong embedding used for collection

Fix:
- ensure routing correctness

---

## 2. Google Rate Limits

Symptom:
- 429 errors

Fix:
- exponential backoff (already implemented)
- fallback to local embeddings

---

## 3. MCP Misrouting

Symptom:
- wrong memory source queried

Fix:
- verify MCP server config
- ensure correct qdrant target

---

## 4. Silent Semantic Corruption

Symptom:
- retrieval returns irrelevant results

Cause:
- mixing embedding spaces

