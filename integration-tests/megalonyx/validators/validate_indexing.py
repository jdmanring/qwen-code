import json
import os

import requests
import tree_sitter_python as tspython
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from tree_sitter import Language, Node, Parser

# --- Configuration ---
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "agent_memory_local"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE_DIRS = {".git", ".venv", "__pycache__", ".qwen", "tests", "storage", "snapshots"}
SUPPORTED_EXTENSIONS = {".py"}

from typing import Any  # noqa: E402


class CodeIndexer:
    def __init__(self) -> None:
        self.client = QdrantClient(url=QDRANT_URL)
        self.parser = Parser(Language(tspython.language()))
        self._setup_collection()

    def _setup_collection(self) -> None:
        """Creates the Qdrant collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)

        if not exists:
            print(f"Creating collection {COLLECTION_NAME}...")
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=768, distance=Distance.COSINE
                ),  # nomic-embed-text is 768
            )

    def get_embedding(self, text: str) -> list[float]:
        """Fetches embedding from Ollama."""
        response = requests.post(
            OLLAMA_URL, json={"model": EMBEDDING_MODEL, "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def extract_symbols(self, file_path: str) -> list[dict[str, Any]]:
        """Uses Tree-sitter to extract functions and classes from a Python file."""
        with open(file_path, "rb") as f:
            code = f.read()

        tree = self.parser.parse(code)
        root_node = tree.root_node

        symbols = []

        def traverse(node: Node) -> None:
            # Check if this node is a function or class definition
            if node.type == "function_definition" or node.type == "class_definition":
                # Find the name identifier
                name = "unknown"
                for child in node.children:
                    if child.type == "identifier":
                        name = child.text.decode("utf8")
                        break

                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                content = code[node.start_byte : node.end_byte].decode("utf8")

                symbols.append(
                    {
                        "name": name,
                        "content": content,
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                )

            # Recurse into children
            for child in node.children:
                traverse(child)

        traverse(root_node)
        return symbols

    def index_project(self) -> None:
        """Walks the project and indexes all supported files."""
        print(f"Indexing project at {PROJECT_ROOT}...")
        points = []
        point_id = 0

        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1]
                if ext not in SUPPORTED_EXTENSIONS:
                    continue

                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")

                try:
                    symbols = self.extract_symbols(file_path)
                    for sym in symbols:
                        vector = self.get_embedding(sym["content"])

                        points.append(
                            PointStruct(
                                id=point_id,
                                vector=vector,
                                payload={
                                    "file_path": file_path,
                                    "symbol_name": sym["name"],
                                    "start_line": sym["start_line"],
                                    "end_line": sym["end_line"],
                                    "content": sym["content"],
                                },
                            )
                        )
                        point_id += 1
                except (
                    OSError,
                    requests.exceptions.RequestException,
                    json.JSONDecodeError,
                    UnicodeDecodeError,
                ) as e:
                    print(f"Error indexing {file_path}: {e}")

        if points:
            print(f"Upserting {len(points)} points to Qdrant...")
            self.client.upsert(collection_name=COLLECTION_NAME, points=points)
            print("Indexing complete!")
        else:
            print("No symbols found to index.")


if __name__ == "__main__":
    indexer = CodeIndexer()
    indexer.index_project()
