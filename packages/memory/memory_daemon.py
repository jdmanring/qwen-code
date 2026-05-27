import asyncio
import hashlib
import os
import queue
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from memory_compact import compact
from memory_embeddings import embed
from memory_ingest import cloud_qdrant, ingest, local_qdrant
from memory_ingest_filter import MemoryIngestFilter
from memory_search import (
    CLOUD_COLLECTION,
    LOCAL_COLLECTION,
    ensure_collections_exist,
)
from memory_transport import run_socket_server, run_stdio_server

# Define the socket path
SOCKET_PATH = os.path.join(
    os.path.expanduser("~"), ".local/share/megalonyx/tmp/megalonyx_memory.sock"
)


class MemoryDaemon:
    def __init__(self) -> None:

        self.queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.running = True

        self.authority = MemoryIngestFilter()
        self.dream_interval = 3600  # 1 hour
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._active_requests = 0
        self._request_lock = threading.Lock()

    def _inc_request(self) -> None:
        with self._request_lock:
            self._active_requests += 1

    def _dec_request(self) -> None:
        with self._request_lock:
            self._active_requests -= 1

    @property
    def active_requests(self) -> int:
        with self._request_lock:
            return self._active_requests

    # -------------------------
    # INGESTION
    # -------------------------

    async def ingest(self, text: str, tier: str = "auto") -> dict[str, Any]:
        self._inc_request()
        return await asyncio.shield(self._do_ingest(text, tier))

    async def _do_ingest(self, text: str, tier: str = "auto") -> dict[str, Any]:
        try:
            sys.stderr.write(f"[DEBUG] MemoryDaemon.ingest called with tier={tier}\n")
            sys.stderr.flush()

            if not self.authority.should_store(text):
                sys.stderr.write("[DEBUG] MemoryDaemon.ingest: rejected by authority\n")
                sys.stderr.flush()
                return {"status": "rejected"}

            if tier == "sync":
                sys.stderr.write("[DEBUG] MemoryDaemon.ingest: performing sync ingest\n")
                sys.stderr.flush()
                from memory_ingest import ingest as ingest_func

                loop = asyncio.get_running_loop()
                res = await loop.run_in_executor(self._executor, ingest_func, text, tier)
                sys.stderr.write(f"[DEBUG] MemoryDaemon.ingest: sync ingest complete: {res}\n")
                sys.stderr.flush()
                return res

            if tier == "auto":
                tier = self.authority.classify_tier(text)

            if len(text) > 1200:
                text = compact(text)

            sys.stderr.write(f"[DEBUG] MemoryDaemon.ingest: queuing text with tier={tier}\n")
            sys.stderr.flush()
            self.queue.put_nowait((text, tier))

            return {"status": "queued", "tier": tier}
        finally:
            self._dec_request()

    # -------------------------
    # SEARCH
    # -------------------------

    async def _search_collection(
        self, collection: str, query: str, tier: str, limit: int = 5
    ) -> list[dict[str, Any]]:

        loop = asyncio.get_running_loop()
        vector = (await loop.run_in_executor(self._executor, embed, [query], tier))[0]

        client_to_use = local_qdrant if tier == "local" else cloud_qdrant

        if client_to_use is None:
            raise RuntimeError(f"Client for tier {tier} is not available")

        resp = client_to_use.query_points(
            collection_name=collection,
            query=vector,
            limit=limit,
        )

        return [{"id": p.id, "score": p.score, "payload": p.payload} for p in resp.points]

    async def recall(
        self, query: str, tier: str = "auto"
    ) -> list[dict[str, Any]] | dict[str, list[dict[str, Any]]]:
        self._inc_request()
        return await asyncio.shield(self._do_recall(query, tier))

    async def _do_recall(
        self, query: str, tier: str = "auto"
    ) -> list[dict[str, Any]] | dict[str, list[dict[str, Any]]]:
        try:
            if tier == "local":
                return await self._search_collection(LOCAL_COLLECTION, query, "local")

            if tier == "cloud":
                return await self._search_collection(CLOUD_COLLECTION, query, "cloud")

            local = await self._search_collection(LOCAL_COLLECTION, query, "local")

            try:
                cloud = await self._search_collection(CLOUD_COLLECTION, query, "cloud")
            except (RuntimeError, ConnectionError):  # Broad catch for Qdrant errors
                cloud = []

            return {"local": local, "cloud": cloud}
        finally:
            self._dec_request()

    async def reflect(self, query: str) -> list[dict[str, Any]] | dict[str, list[dict[str, Any]]]:
        self._inc_request()
        return await asyncio.shield(self._do_reflect(query))

    async def _do_reflect(
        self, query: str
    ) -> list[dict[str, Any]] | dict[str, list[dict[str, Any]]]:
        try:
            return await self._do_recall(query, tier="auto")
        finally:
            self._dec_request()

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
                        f"[memory] Dreaming: Deleted {len(to_delete)} redundant"
                        f" points from {tier} tier.\n"
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

        from memory_ingest import recover

        recover()
        sys.stderr.write("[memory] Recovery performed.\n")
        sys.stderr.flush()

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
