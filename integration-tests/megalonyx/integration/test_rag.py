import os
import sys
from typing import Any

# Add scripts directory to path to import CodeIndexer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

import pytest
import requests
from index_codebase import COLLECTION_NAME, EMBEDDING_MODEL, QDRANT_URL, CodeIndexer
from qdrant_client import QdrantClient


# Mock Qdrant setup to avoid needing a running server for unit tests
class MockQdrantClient:
    def __init__(self, **kwargs) -> None:
        pass

    def get_collections(self) -> Any:
        class Coll:
            def __init__(self, name: str) -> None:
                self.name = name

        class CollResp:
            def __init__(self, name: str) -> None:
                self.collections = [Coll(name)]

        return CollResp("agent_memory_local")

    def create_collection(self, **kwargs) -> None:
        pass

    def upsert(self, **kwargs) -> None:
        pass


# Patch CodeIndexer to use MockQdrantClient
import unittest.mock as mock  # noqa: E402


@pytest.fixture
def indexer() -> CodeIndexer:
    with mock.patch("index_codebase.QdrantClient", return_value=MockQdrantClient()):
        with mock.patch(
            "index_codebase.CodeIndexer.get_embedding", return_value=[0.1] * 768
        ):
            yield CodeIndexer()


def test_extract_symbols_basic() -> None:
    code = b"def hello():\n    print('hi')\n\nclass MyClass:\n    def method(self):\n        pass"
    temp_file = "tests/temp_test_basic.py"
    with open(temp_file, "wb") as f:
        f.write(code)

    indexer = CodeIndexer()
    symbols = indexer.extract_symbols(temp_file)

    assert len(symbols) == 3
    assert symbols[0]["name"] == "hello"
    assert symbols[1]["name"] == "MyClass"
    assert symbols[2]["name"] == "method"
    os.remove(temp_file)


def test_extract_symbols_complex() -> None:
    code = b"""
@decorator
async def async_func(a, b):
    return a + b

class Outer:
    class Inner:
        def inner_method(self):
            pass
    def outer_method(self):
        pass
"""
    temp_file = "tests/temp_test_complex.py"
    with open(temp_file, "wb") as f:
        f.write(code)

    indexer = CodeIndexer()
    symbols = indexer.extract_symbols(temp_file)

    names = [s["name"] for s in symbols]
    assert "async_func" in names
    assert "Outer" in names
    assert "Inner" in names
    assert "inner_method" in names
    assert "outer_method" in names
    os.remove(temp_file)


def test_extract_symbols_empty() -> None:
    code = b"x = 10\ny = 20"
    temp_file = "tests/temp_test_empty.py"
    with open(temp_file, "wb") as f:
        f.write(code)

    indexer = CodeIndexer()
    symbols = indexer.extract_symbols(temp_file)
    assert len(symbols) == 0
    os.remove(temp_file)


# --- Retrieval Accuracy Tests ---


def get_real_embedding(text: str) -> list[float]:
    """Helper to get embedding from Ollama for real tests."""
    url = "http://localhost:11434/api/embeddings"
    response = requests.post(url, json={"model": EMBEDDING_MODEL, "prompt": text})
    response.raise_for_status()
    return response.json()["embedding"]


def test_retrieval_accuracy() -> None:
    """Verifies that semantic queries return the correct top-1 symbol."""
    client = QdrantClient(url=QDRANT_URL)

    golden_set = [
        ("How are symbols extracted from Python files?", "extract_symbols"),
        ("Where is the Qdrant collection created?", "_setup_collection"),
        ("How does the system handle embeddings from Ollama?", "get_embedding"),
    ]

    for query, expected_symbol in golden_set:
        vector = get_real_embedding(query)
        search_result = client.query_points(
            collection_name=COLLECTION_NAME, query=vector, limit=1
        ).points

        assert len(search_result) > 0, f"No results found for query: {query}"
        actual_symbol = search_result[0].payload["symbol_name"]
        assert actual_symbol == expected_symbol, (
            f"Query '{query}' failed. Expected {expected_symbol}, got {actual_symbol}"
        )
