import time

from qdrant_client import QdrantClient


def test():
    print("Attempting to connect to Qdrant...")
    client = QdrantClient(url="http://localhost:6333")
    try:
        start = time.time()
        collections = client.get_collections()
        end = time.time()
        print(f"SUCCESS: Connected in {end - start:.2f}s")
        print(f"Collections: {collections}")
    except (RuntimeError, ValueError, TypeError, AttributeError, OSError) as e:
        print(f"FAILURE: {e}")


if __name__ == "__main__":
    test()
