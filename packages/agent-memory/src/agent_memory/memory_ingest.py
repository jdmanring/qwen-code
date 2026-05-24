import json
import os
import sys
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from .memory_embeddings import embed
from .memory_schema import MemoryRecord, deserialize, serialize

QDRANT_LOCAL_URL = os.getenv("QDRANT_LOCAL_URL", "http://localhost:6333")

QDRANT_CLOUD_URL = os.getenv("QDRANT_CLOUD_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

LOCAL_COLLECTION = "qwen_local_memory"
CLOUD_COLLECTION = "qwen_cloud_memory"

WAL_PATH = os.path.expanduser("~/.qwen/memory/wal.jsonl")

local_qdrant = QdrantClient(url=QDRANT_LOCAL_URL)

cloud_qdrant: QdrantClient | None = None

if QDRANT_CLOUD_URL and QDRANT_API_KEY:
    cloud_qdrant = QdrantClient(url=QDRANT_CLOUD_URL, api_key=QDRANT_API_KEY)


class WALManager:
    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def append(self, record_dict: dict[str, Any]) -> None:
        """Appends a record to the WAL."""
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record_dict) + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        """Reads all records from the WAL."""
        if not os.path.exists(self.path):
            return []

        records = []
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        return records

    def clear(self) -> None:
        """Clears the WAL."""
        if os.path.exists(self.path):
            os.remove(self.path)


wal = WALManager(WAL_PATH)


def ensure_collection(client: Any, collection: str, size: int) -> None:
    existing = [c.name for c in client.get_collections().collections]

    if collection not in existing:
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )


def ingest(text: str, tier: str) -> dict[str, Any]:
    record = MemoryRecord(text=text, tier=tier)

    # 1. Write to WAL first for crash recovery
    wal.append(serialize(record))

    try:
        _perform_ingest(record)
        # 2. If successful, we can clear the WAL or mark it done.
        # For simplicity in this prototype, we'll just let it exist and
        # rely on Qdrant's idempotent upsert during recovery.
        # In a production system, we would truncate the WAL here.
        return {"status": "stored", "tier": tier, "id": record.id}
    except (RuntimeError, UnexpectedResponse) as e:
        print(f"[memory:ingest] Error during ingestion: {e}", file=sys.stderr)
        raise


def _perform_ingest(record: MemoryRecord) -> None:
    """The actual heavy lifting of embedding and upserting."""
    vector = embed([record.text], record.tier)[0]

    client = local_qdrant
    collection = LOCAL_COLLECTION

    if record.tier == "cloud":
        if cloud_qdrant is None:
            raise RuntimeError("Cloud Qdrant not configured")

        client = cloud_qdrant
        collection = CLOUD_COLLECTION

    ensure_collection(client, collection, len(vector))

    client.upsert(
        collection_name=collection,
        points=[PointStruct(id=record.id, vector=vector, payload=serialize(record))],
    )


def recover() -> None:
    """Replays records from the WAL."""
    print("[memory:ingest] Starting recovery from WAL...", file=sys.stderr)
    records_data = wal.read_all()

    if not records_data:
        print("[memory:ingest] No records to recover.", file=sys.stderr)
        return

    print(
        f"[memory:ingest] Found {len(records_data)} records in WAL. Replaying...",
        file=sys.stderr,
    )

    for data in records_data:
        try:
            # Reconstruct record from serialized dict
            record = deserialize(data)
            _perform_ingest(record)
        except (ValueError, RuntimeError, UnexpectedResponse) as e:
            print(
                f"[memory:ingest] Failed to recover record {data.get('id')}: {e}",
                file=sys.stderr,
            )

    # Once all records are replayed (even if some failed), clear the WAL
    # to prevent infinite replay loops.
    wal.clear()
    print("[memory:ingest] Recovery complete. WAL cleared.", file=sys.stderr)
