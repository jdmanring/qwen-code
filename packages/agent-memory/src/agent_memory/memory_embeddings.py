import hashlib
import os
import sys
import time
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from typing import Any, cast

import requests
from sentence_transformers import SentenceTransformer

LOCAL_MODEL_NAME = "all-MiniLM-L6-v2"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        pass


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = LOCAL_MODEL_NAME) -> None:
        try:
            with redirect_stdout(sys.stderr):
                self.model = SentenceTransformer(model_name)
        except (OSError, ImportError, RuntimeError) as e:
            sys.stderr.write(f"[memory:embeddings] Failed to load local model: {e}\n")
            raise

    def embed(self, texts: list[str]) -> list[list[float]]:
        if isinstance(texts, str):
            texts = [texts]
        return cast(list[list[float]], self.model.encode(texts).tolist())


class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, retries: int = 5, batch_size: int = 16) -> None:
        if not api_key:
            raise RuntimeError("Gemini API Key is required")
        self.api_key = api_key
        self.retries = retries
        self.batch_size = batch_size
        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/gemini-embedding-2:embedContent?key={self.api_key}"
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        if isinstance(texts, str):
            texts = [texts]

        out = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            out.extend(self._call_api(batch))
        return out

    def _call_api(self, batch: list[str]) -> list[list[float]]:
        # Determine which endpoint to use based on batch size
        url: str
        payload: dict[str, Any]
        if len(batch) == 1:
            url = self.url.replace("batchEmbedContents", "embedContent")
            payload = {
                "content": {"parts": [{"text": batch[0]}]},
                "taskType": "RETRIEVAL_DOCUMENT",
            }
        else:
            url = self.url.replace("embedContent", "batchEmbedContents")
            payload = {
                "requests": [
                    {
                        "model": "models/gemini-embedding-2",
                        "content": {"parts": [{"text": t}]},
                        "taskType": "RETRIEVAL_DOCUMENT",
                    }
                    for t in batch
                ]
            }

        for attempt in range(self.retries):
            try:
                r = requests.post(url, json=payload, timeout=30)
                if r.status_code == 429:
                    wait = 2**attempt
                    sys.stderr.write(
                        f"[memory:embeddings] Gemini rate limit (429). Retrying in {wait}s...\n"
                    )
                    time.sleep(wait)
                    continue

                r.raise_for_status()
                data = r.json()

                # The response structure differs between single and batch
                if len(batch) == 1:
                    return [data["embedding"]["values"]]
                else:
                    return [e["values"] for e in data["embeddings"]]

            except requests.RequestException as e:
                if attempt == self.retries - 1:
                    sys.stderr.write(
                        f"[memory:embeddings] Gemini API call failed after "
                        f"{self.retries} attempts: {e}\n"
                    )
                    raise
                time.sleep(2**attempt)

        raise RuntimeError("Gemini embedding retries exhausted")


class CachedEmbeddingProvider(EmbeddingProvider):
    """A simple in-memory cache for embeddings."""

    def __init__(self, base_provider: EmbeddingProvider) -> None:
        self.provider = base_provider
        self.cache: dict[str, list[float]] = {}

    def embed(self, texts: list[str]) -> list[list[float]]:
        results = []
        missing_indices = []
        missing_texts = []

        for i, text in enumerate(texts):
            text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
            if text_hash in self.cache:
                results.append(self.cache[text_hash])
            else:
                missing_indices.append(i)
                missing_texts.append(text)

        if missing_texts:
            new_embeddings = self.provider.embed(missing_texts)
            for idx, embedding in zip(missing_indices, new_embeddings, strict=False):
                text_hash = hashlib.md5(texts[idx].encode("utf-8")).hexdigest()
                self.cache[text_hash] = embedding
                results.append(embedding)

            # Ensure results are in correct order if they were interleaved
            # (Wait, the loop above handles it correctly by appending to results)
            # But if we want to maintain original order, we should re-sort or
            # initialize a list of None. Let's do it properly.

            # Re-doing with proper indexing
            final_results: list[list[float] | None] = [None] * len(texts)
            for i, text in enumerate(texts):
                text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
                if text_hash in self.cache:
                    final_results[i] = self.cache[text_hash]

            # Now fill in the missing ones
            for idx, emb in zip(missing_indices, new_embeddings, strict=False):
                text_hash = hashlib.md5(texts[idx].encode("utf-8")).hexdigest()
                self.cache[text_hash] = emb
                final_results[idx] = emb

            return cast(list[list[float]], final_results)

        return results


# Global provider instances
_local_provider = LocalEmbeddingProvider()
_gemini_provider = GeminiEmbeddingProvider(GEMINI_API_KEY) if GEMINI_API_KEY else None
_cached_gemini = CachedEmbeddingProvider(_gemini_provider) if _gemini_provider else None


def embed(texts: str | list[str], tier: str) -> list[list[float]]:
    if isinstance(texts, str):
        texts = [texts]
    if tier == "local":
        return _local_provider.embed(texts)
    elif tier == "cloud":
        if not _cached_gemini:
            raise RuntimeError("Cloud embedding provider not initialized (check GEMINI_API_KEY)")
        return _cached_gemini.embed(texts)
    else:
        raise ValueError(f"Invalid embedding tier: {tier}")
