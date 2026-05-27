from qdrant_client import QdrantClient

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "agent_memory_local"


def inspect_collection() -> None:
    client = QdrantClient(url=QDRANT_URL)
    try:
        collection_info = client.get_collection(collection_name=COLLECTION_NAME)
        print(f"Collection info: {collection_info}")
        print(f"Type of collection_info: {type(collection_info)}")
        # Try to see what attributes are available
        print(f"Attributes: {dir(collection_info)}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    inspect_collection()
