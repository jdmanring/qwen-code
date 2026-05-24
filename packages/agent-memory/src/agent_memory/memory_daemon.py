import hashlib
import os
import queue
import sys
import threading
import time
from typing import Any

from .memory_compact import compact
from .memory_embeddings import embed
from .memory_ingest import cloud_qdrant, ingest, local_qdrant
from .memory_ingest_filter import MemoryIngestFilter
from .memory_search import (
    CLOUD_COLLECTION,
    LOCAL_COLLECTION,
    ensure_collections_exist,
)
from .memory_transport import run_socket_server, run_stdio_server

# Define the socket path
SOCKET_PATH = os.path.join(os.path.expanduser("~"), ".local/share/megalonyx/tmp/qwen_memory.sock")


class MemoryDaemon:
    def __init__(self) -> None:

        self.queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.running = True

        self.authority = MemoryIngestFilter()
        self.dream_interval = 3600  # 1 hour

    # -------------------------
    # INGESTION
    # -------------------------

    def ingest(self, text: str, tier: str = "auto") -> dict[str, Any]:

        if not self.authority.should_store(text):
            return {"status": "rejected"}

        if tier == "auto":
            tier = self.authority.classify_tier(text)

        if len(text) > 1200:
            text = compact(text)

        self.queue.put((text, tier))

        return {"status": "queued", "tier": tier}

    # -------------------------
    # SEARCH
    # -------------------------

    def _search_collection(
        self, collection: str, query: str, tier: str, limit: int = 5
    ) -> list[dict[str, Any]]:

        vector = embed([query], tier)[0]

        client_to_use = local_qdrant if tier == "local" else cloud_qdrant

        if client_to_use is None:
            raise RuntimeError(f"Client for tier {tier} is not available")

        resp = client_to_use.query_points(
            collection_name=collection,
            query=vector,
            limit=limit,
        )

        return [{"id": p.id, "score": p.score, "payload": p.payload} for p in resp.points]

    def recall(
        self, query: str, tier: str = "auto"
    ) -> list[dict[str, Any]] | dict[str, list[dict[str, Any]]]:

        if tier == "local":
            return self._search_collection(LOCAL_COLLECTION, query, "local")

        if tier == "cloud":
            return self._search_collection(CLOUD_COLLECTION, query, "cloud")

        local = self._search_collection(LOCAL_COLLECTION, query, "local")

        try:
            cloud = self._search_collection(CLOUD_COLLECTION, query, "cloud")
        except (RuntimeError, ConnectionError):  # Broad catch for Qdrant errors
            cloud = []

        return {"local": local, "cloud": cloud}

    def reflect(self, query: str) -> list[dict[str, Any]] | dict[str, list[dict[str, Any]]]:

        return self.recall(query, tier="auto")

    def dream(self) -> None:
        """
        The Dreaming Pipeline: Periodic consolidation and pruning of semantic memory.
        1. Consolidation: Merges similar memories into canonical forms.
        2. Deduplication: Removes redundant entries.
        3. Pruning: Cleans up transient local data.
        """
        sys.stderr.write("[memory] Starting Dreaming Pipeline...\n")
        try:
            # In a full implementation, this would use a clustering algorithm (e.g., DBSCAN)
            # on embeddings to find redundant memories.
            # For the prototype, we implement a basic deduplication based on content hashing.

            for tier in ["local", "cloud"]:
                collection = LOCAL_COLLECTION if tier == "local" else CLOUD_COLLECTION
                client = local_qdrant if tier == "local" else cloud_qdrant

                if client is None:
                    continue

                # 1. Fetch all points
                points = client.scroll(collection_name=collection, limit=1000)[0]
                if not points:
                    continue

                # 2. Simple deduplication by content hash
                seen_hashes = {}
                to_delete = []

                for p in points:
                    content = p.payload.get("text", "")
                    h = hashlib.sha256(content.encode()).hexdigest()
                    if h in seen_hashes:
                        to_delete.append(p.id)
                    else:
                        seen_hashes[h] = p.id

                if to_delete:
                    client.delete(collection_name=collection, points_selector=to_delete)
                    sys.stderr.write(
                        f"[memory] Dreaming: Deleted {len(to_delete)} redundant points"
                        f" from {tier} tier.\n"
                    )

            sys.stderr.write("[memory] Dreaming Pipeline completed successfully.\n")
        except (RuntimeError, ConnectionError, ValueError) as e:
            sys.stderr.write(f"[memory] Dreaming failure: {e}\n")

    def dream_worker(self) -> None:
        """Background thread that triggers the dreaming process periodically."""
        while self.running:
            time.sleep(self.dream_interval)
            self.dream()

    # -------------------------
    # WORKER
    # -------------------------

    def worker(self) -> None:
        while self.running:
            try:
                text, tier = self.queue.get(timeout=1)
                ingest(text, tier)
            except queue.Empty:
                continue
            except (RuntimeError, ConnectionError, ValueError) as e:
                sys.stderr.write(f"[memory] ingest failure: {e}\n")
                sys.stderr.flush()
                # PREVENT TIGHT LOOP ON ERROR
                time.sleep(2)

    # -------------------------
    # STARTUP
    # -------------------------

    def start(self) -> "MemoryDaemon":

        # from memory_ingest import recover
        # recover()
        # print("[DEBUG] Recovery skipped for testing.")

        # Retry connecting to Qdrant for up to 30 seconds
        retries = 30
        while retries > 0:
            try:
                ensure_collections_exist()
                sys.stderr.write("[memory] Qdrant collections verified.\n")
                break
            except (RuntimeError, ConnectionError) as e:
                sys.stderr.write(f"[memory] Waiting for Qdrant... ({retries}s remaining): {e}\n")
                sys.stderr.flush()
                retries -= 1
                time.sleep(1)

        if retries == 0:
            sys.stderr.write(
                "[memory] ERROR: Qdrant failed to become available after 30s. Exiting.\n"
            )
            sys.exit(1)

        # Start Ingestion Worker
        worker_thread = threading.Thread(target=self.worker, daemon=True)
        worker_thread.start()

        # Start Dreaming Worker
        dream_thread = threading.Thread(target=self.dream_worker, daemon=True)
        dream_thread.start()

        return self


# -------------------------
# BOOT
# -------------------------

if __name__ == "__main__":
    core = MemoryDaemon()

    # Start Qdrant initialization in a background thread so the MCP server
    # can start listening on the socket immediately.
    init_thread = threading.Thread(target=core.start, daemon=True)
    init_thread.start()

    transport = os.environ.get("MCP_TRANSPORT", "socket").lower()
    if transport == "stdio":
        run_stdio_server(core)
    else:
        run_socket_server(core, SOCKET_PATH)
