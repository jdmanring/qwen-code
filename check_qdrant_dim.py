from qdrant_client import QdrantClient

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "agent_memory_local"


def check_collection() -> None:
    client = QdrantClient(url=QDRANT_URL)
    try:
        collection_info = client.get_collection(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' found.")
        print(f"Vectors config: {collection_info.config.params.vectors}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_collection()
