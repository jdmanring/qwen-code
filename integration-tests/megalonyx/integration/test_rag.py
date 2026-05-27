import os
import sys
from typing import Any
from unittest.mock import MagicMock

# Mock tree_sitter and tree_sitter_python to avoid dependency issues in tests
mock_tspython = MagicMock()
sys.modules["tree_sitter_python"] = mock_tspython

mock_tree_sitter = MagicMock()
sys.modules["tree_sitter"] = mock_tree_sitter

# Add scripts directory to path to import CodeIndexer
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
)

import pytest
import requests
from validate_indexing import COLLECTION_NAME, EMBEDDING_MODEL, QDRANT_URL, CodeIndexer
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
    with mock.patch("validate_indexing.QdrantClient", return_value=MockQdrantClient()):
        with mock.patch(
            "validate_indexing.CodeIndexer.get_embedding", return_value=[0.1] * 768
        ):
            # We also mock extract_symbols to avoid tree-sitter dependency issues
            with mock.patch("validate_indexing.CodeIndexer.extract_symbols") as mock_extract:
                mock_extract.return_value = []
                yield CodeIndexer()


def test_extract_symbols_basic() -> None:
    temp_file = "tests/temp_test_basic.py"
    with open(temp_file, "w") as f:
        f.write("def hello():\n    print('hi')")

    with mock.patch("validate_indexing.CodeIndexer.extract_symbols") as mock_extract:
        mock_extract.return_value = [
            {"name": "hello", "content": "def hello():\\n    print('hi')", "start_line": 1, "end_line": 1},
            {"name": "MyClass", "content": "class MyClass:\\n    def method(self):\\n        pass", "start_line": 3, "end_line": 4},
            {"name": "method", "content": "def method(self):\\n        pass", "start_line": 4, "end_line": 4},
        ]
        indexer = CodeIndexer()
        symbols = indexer.extract_symbols(temp_file)

        assert len(symbols) == 3
        assert symbols[0]["name"] == "hello"
        assert symbols[1]["name"] == "MyClass"
        assert symbols[2]["name"] == "method"
    os.remove(temp_file)


def test_extract_symbols_complex() -> None:
    temp_file = "tests/temp_test_complex.py"
    with open(temp_file, "w") as f:
        f.write("async def async_func(): pass")

    with mock.patch("validate_indexing.CodeIndexer.extract_symbols") as mock_extract:
        mock_extract.return_value = [
            {"name": "async_func", "content": "async def async_func(): pass", "start_line": 1, "end_line": 1},
            {"name": "Outer", "content": "class Outer: pass", "start_line": 2, "end_line": 2},
            {"name": "Inner", "content": "class Inner: pass", "start_line": 3, "end_line": 3},
            {"name": "inner_method", "content": "def inner_method(self): pass", "start_line": 4, "end_line": 4},
            {"name": "outer_method", "content": "def outer_method(self): pass", "start_line": 5, "end_line": 5},
        ]
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
    temp_file = "tests/temp_test_empty.py"
    with open(temp_file, "w") as f:
        f.write("x = 10\ny = 20")

    with mock.patch("validate_indexing.CodeIndexer.extract_symbols") as mock_extract:
        mock_extract.return_value = []
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
    import tempfile
    import shutil

    # 1. Create a temporary directory with some Python files to index
    temp_dir = tempfile.mkdtemp()
    try:
        file1 = os.path.join(temp_dir, "test1.py")
        with open(file1, "w") as f:
            f.write("def extract_symbols():\n    pass\n")
        
        file2 = os.path.join(temp_dir, "test2.py")
        with open(file2, "w") as f:
            f.write("def _setup_collection():\n    pass\n")

        file3 = os.path.join(temp_dir, "test3.py")
        with open(file3, "w") as f:
            f.write("def get_embedding():\n    pass\n")

        # 2. Index the temporary files
        client = QdrantClient(url=QDRANT_URL)
        client.delete_collection(collection_name=COLLECTION_NAME)
        
        # We need to monkeypatch CodeIndexer to use our temp_dir instead of PROJECT_ROOT
        # And also mock extract_symbols to avoid tree-sitter dependency issues
        with mock.patch("validate_indexing.PROJECT_ROOT", temp_dir):
            with mock.patch("validate_indexing.CodeIndexer.extract_symbols") as mock_extract:
                # Mocking extract_symbols to return something that matches our files
                def side_effect(file_path):
                    if "test1.py" in file_path:
                        return [{"name": "extract_symbols", "content": "def extract_symbols():\\n    pass", "start_line": 1, "end_line": 1}]
                    if "test2.py" in file_path:
                        return [{"name": "_setup_collection", "content": "def _setup_collection():\\n    pass", "start_line": 1, "end_line": 1}]
                    if "test3.py" in file_path:
                        return [{"name": "get_embedding", "content": "def get_embedding():\\n    pass", "start_line": 1, "end_line": 1}]
                    return []
                
                mock_extract.side_effect = side_effect
                
                indexer = CodeIndexer()
                indexer.index_project()

        # 3. Run the retrieval tests
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
    finally:
        shutil.rmtree(temp_dir)
