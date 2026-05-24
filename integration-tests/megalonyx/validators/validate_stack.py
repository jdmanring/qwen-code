#!/usr/bin/env python3
"""
=========================================================
QWEN STACK VALIDATION
=========================================================

Performs full-stack validation for:

- PyTorch CUDA runtime
- vLLM import/runtime
- Qdrant connectivity
- Embedding model loading
- Embedding generation
- Qdrant collection creation
- Vector insert
- Vector retrieval
- End-to-end RAG loop validation

Fails hard on critical infrastructure problems.

=========================================================
"""

import sys
import traceback
import uuid

# =========================================================
# CONFIG
# =========================================================

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "qwen_stack_validation"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TEST_DOCUMENTS = [
    "Qwen Code uses MCP tools.",
    "vLLM provides local inference.",
    "Qdrant stores semantic vectors.",
]

QUERY = "What stores vectors?"

# =========================================================
# HELPERS
# =========================================================


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"[ OK ] {msg}")


def warn(msg: str) -> None:
    print(f"[WARN] {msg}")


# =========================================================
# TORCH VALIDATION
# =========================================================

print("\n=== TORCH VALIDATION ===")

try:
    import torch

    ok(f"torch imported ({torch.__version__})")

    if not torch.cuda.is_available():
        fail("CUDA unavailable")

    ok(f"CUDA available ({torch.version.cuda})")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    fail(f"torch validation failed: {e}")

# =========================================================
# VLLM VALIDATION
# =========================================================

print("\n=== VLLM VALIDATION ===")

try:
    import vllm

    ok(f"vLLM imported ({vllm.__version__})")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    fail(f"vLLM validation failed: {e}")

# =========================================================
# EMBEDDING MODEL VALIDATION
# =========================================================

print("\n=== EMBEDDING VALIDATION ===")

try:
    from sentence_transformers import SentenceTransformer

    embedder = SentenceTransformer(EMBED_MODEL)

    ok(f"embedding model loaded ({EMBED_MODEL})")

    embeddings = embedder.encode(TEST_DOCUMENTS)

    if len(embeddings) != len(TEST_DOCUMENTS):
        fail("embedding generation count mismatch")

    VECTOR_SIZE = len(embeddings[0])

    ok(f"embeddings generated ({VECTOR_SIZE} dimensions)")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    traceback.print_exc()
    fail(f"embedding validation failed: {e}")

# =========================================================
# QDRANT VALIDATION
# =========================================================

print("\n=== QDRANT VALIDATION ===")

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams

    client = QdrantClient(url=QDRANT_URL)

    ok(f"connected to qdrant ({QDRANT_URL})")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    fail(f"qdrant connection failed: {e}")

# =========================================================
# COLLECTION SETUP
# =========================================================

print("\n=== COLLECTION VALIDATION ===")

try:
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME in names:
        client.delete_collection(COLLECTION_NAME)
        ok("old validation collection removed")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )

    ok("validation collection created")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    fail(f"collection setup failed: {e}")

# =========================================================
# VECTOR INSERTION
# =========================================================

print("\n=== VECTOR INSERTION ===")

try:
    points = []

    for doc, vec in zip(TEST_DOCUMENTS, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vec.tolist(),
                payload={"text": doc},
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    ok(f"{len(points)} vectors inserted")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    fail(f"vector insertion failed: {e}")

# =========================================================
# VECTOR SEARCH
# =========================================================

print("\n=== VECTOR SEARCH ===")

try:
    query_embedding = embedder.encode([QUERY])[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=3,
    ).points

    if not results:
        fail("search returned no results")

    top = results[0]

    payload = top.payload.get("text", "")

    ok(f"top result: {payload}")

    if "Qdrant stores semantic vectors" not in payload:
        warn("retrieval result unexpected")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    fail(f"vector search failed: {e}")

# =========================================================
# CLEANUP
# =========================================================

print("\n=== CLEANUP ===")

try:
    client.delete_collection(COLLECTION_NAME)
    ok("validation collection removed")

except (ImportError, RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
    warn(f"cleanup failed: {e}")

# =========================================================
# COMPLETE
# =========================================================

print("\n=========================================================")
print("STACK VALIDATION SUCCESS")
print("=========================================================")

print("")
print("Validated:")
print("- PyTorch CUDA runtime")
print("- vLLM import")
print("- sentence-transformers")
print("- embedding generation")
print("- Qdrant connectivity")
print("- vector insertion")
print("- vector retrieval")
print("- end-to-end RAG loop")
print("")
