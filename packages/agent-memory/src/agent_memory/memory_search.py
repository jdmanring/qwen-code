import os
import sys
import time
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, VectorParams

# === CONFIG ===
QDRANT_LOCAL_URL = os.getenv("QDRANT_LOCAL_URL", "http://localhost:6333")
QDRANT_CLOUD_URL = os.getenv("QDRANT_CLOUD_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

LOCAL_COLLECTION = "qwen_local_memory"
CLOUD_COLLECTION = "qwen_cloud_memory"

LOCAL_DIM = 384
CLOUD_DIM = 3072

# === CLIENTS ===
local_client = QdrantClient(url=QDRANT_LOCAL_URL, timeout=10)
cloud_client: QdrantClient | None = None

if QDRANT_CLOUD_URL and QDRANT_API_KEY:
    cloud_client = QdrantClient(url=QDRANT_CLOUD_URL, api_key=QDRANT_API_KEY, timeout=10)

# Alias for backward compatibility
client = local_client


def check_connection(client_obj: QdrantClient, retries: int = 3, delay: int = 2) -> bool:
    """Verifies connection to Qdrant with exponential backoff."""
    for i in range(retries):
        try:
            client_obj.get_collections()
            return True
        except (UnexpectedResponse, OSError) as e:
            print(
                f"[memory:search] Connection attempt {i + 1}/{retries} failed: {e}",
                file=sys.stderr,
            )
            if i < retries - 1:
                time.sleep(delay * (2**i))
    return False


def ensure_collection(client_obj: QdrantClient, name: str, size: int) -> None:
    """Ensures collection exists and has correct vector dimensions."""
    try:
        collections = client_obj.get_collections().collections
        existing = {c.name for c in collections}

        if name in existing:
            info = client_obj.get_collection(collection_name=name)
            current_dim = info.config.params.vectors.size
            if current_dim != size:
                raise ValueError(
                    f"Dimension mismatch for '{name}': expected {size}, found {current_dim}"
                )
            return

        print(f"[memory:search] Creating collection: {name}", file=sys.stderr)
        client_obj.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )
    except (UnexpectedResponse, OSError) as e:
        print(f"[memory:search] Error ensuring collection '{name}': {e}", file=sys.stderr)
        raise


def ensure_collections_exist() -> None:
    """Bootstraps all required collections with safety checks."""
    if not check_connection(local_client):
        raise ConnectionError("Could not connect to local Qdrant server.")

    ensure_collection(local_client, LOCAL_COLLECTION, LOCAL_DIM)

    if cloud_client:
        if not check_connection(cloud_client):
            print(
                "[memory:search] WARNING: Cloud Qdrant connection failed.",
                file=sys.stderr,
            )
        else:
            ensure_collection(cloud_client, CLOUD_COLLECTION, CLOUD_DIM)
    else:
        print(
            "[memory:search] Cloud Qdrant not configured, skipping cloud collection.",
            file=sys.stderr,
        )

    print(
        "[memory:search] All collections verified/created successfully.",
        file=sys.stderr,
    )


def search(
    client_obj: QdrantClient,
    collection: str,
    query_vector: list[float],
    limit: int = 5,
    min_score: float = 0.0,
) -> list[dict[str, Any]]:
    """Performs a similarity search with relevance thresholding and diagnostics."""
    start_time = time.perf_counter()
    try:
        results = client_obj.query_points(
            collection_name=collection,
            query=query_vector,
            limit=limit,
        )

        duration = time.perf_counter() - start_time
        filtered_results = [
            {"id": p.id, "score": p.score, "payload": p.payload}
            for p in results.points
            if p.score >= min_score
        ]

        print(
            f"[memory:search] Query in '{collection}': {len(results.points)} found, "
            f"{len(filtered_results)} passed threshold ({min_score}), "
            f"latency={duration:.4f}s",
            file=sys.stderr,
        )
        return filtered_results

    except (UnexpectedResponse, OSError) as e:
        duration = time.perf_counter() - start_time
        print(
            f"[memory:search] Search failed in '{collection}' after {duration:.4f}s: {e}",
            file=sys.stderr,
        )
        raise
