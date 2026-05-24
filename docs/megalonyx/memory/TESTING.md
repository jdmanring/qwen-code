# 🧠 Memory System Validation Framework

This document defines the testing strategy for the Mega Code dual-tier RAG memory system. The goal is to ensure that memory is not only stored and retrieved correctly but that the agent uses it as a professional software engineer would.

## 📐 The Validation Pyramid

We employ a four-layer testing strategy to cover every aspect of the memory lifecycle.

| Layer | Focus | Primary Test File | Key Verification |
| :--- | :--- | :--- | :--- |
| **Plumbing** | MCP Transport & Connectivity | `tests/integration_test_memory.py` | Stdio handshake, payload limits, Qdrant failover. |
| **Logic** | Routing & Efficiency | `tests/memory/behavioral/` | Local vs Cloud routing, deduplication, search precision. |
| **Cognition** | Agentic Usage | `tests/memory/agentic/test_usage.py` | Proactive ingestion, contextual recall. |
| **Lifecycle** | Persistence & Recovery | `tests/memory/agentic/test_lifecycle.py` | Cross-session persistence, WAL crash recovery. |

---

## 🧪 Detailed Test Matrix

### 1. Plumbing Tests
| ID | Test Case | Expected Outcome |
| :--- | :--- | :--- |
| P1 | MCP Initialization | Server returns `protocolVersion` and `serverInfo` correctly. |
| P2 | Transport Stress | 500KB+ payloads are ingested and retrieved without corruption. |
| P3 | Connection Failover | System reports a clean error when Qdrant is unreachable. |

### 2. Behavioral Tests
| ID | Test Case | Expected Outcome |
| :--- | :--- | :--- |
| B1 | Cloud Routing | "Architecture" $\rightarrow$ `qwen_cloud_memory`. |
| B2 | Local Routing | "Transient state" $\rightarrow$ `qwen_local_memory`. |
| B3 | Deduplication | Identical facts are rejected (`status: rejected`). |
| B4 | Noise Filtering | "ok", "thanks" etc. are rejected. |
| B5 | Search Precision | Target fact is in the top 3 results among 50+ noise records. |

### 3. Agentic Tests
| ID | Test Case | Expected Outcome |
| :--- | :--- | :--- |
| A1 | Proactive Ingestion | Agent calls `ingest` when user says "Remember X". |
| A2 | Contextual Recall | Agent calls `search` before answering "What is X?". |
| A3 | Coherence | Agent synthesizes multiple memory fragments into one answer. |

### 4. Lifecycle Tests
| ID | Test Case | Expected Outcome |
| :--- | :--- | :--- |
| L1 | Cross-Session | Fact stored in Session A is retrieved in Session B. |
| L2 | Cold Start | Records in `wal.jsonl` are replayed into Qdrant on boot. |

---

## 🚀 How to Run Tests

### Prerequisites
Ensure the stack is started:
```bash
mega-memory-manager start
```

### Running the Suite
You can run the tests using `pytest`:

```bash
# Run all memory tests
pytest tests/integration_test_memory.py tests/memory/
```

Alternatively, run specific scripts directly:
```bash
python3 tests/memory/behavioral/test_routing.py
python3 tests/memory/agentic/test_usage.py
```

### Manual Live Validation
For quick verification of the end-to-end pipeline, use the specialized validation scripts:

```bash
# Full stack health check (CUDA -> vLLM -> Embeddings -> Qdrant)
mega-run-py tests/validators/validate_stack.py
```


## 🛠️ Troubleshooting Failures

| Failure Symptom | Likely Cause | Resolution |
| :--- | :--- | :--- |
| `P3` fails (Crash) | Daemon not handling connection errors | Check `memory_search.py` `check_connection` logic. |
| `B1/B2` fail | Incorrect signal keywords | Update `MemoryPolicy` in `memory_authority.py`. |
| `B3` fails | UUID collisions or missing check | Verify `MemoryAuthority.should_store` is called. |
| `L2` fails | WAL file permissions or JSON error | Check `~/.qwen/memory/wal.jsonl` format. |
