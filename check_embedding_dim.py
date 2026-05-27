import requests

# We need to make sure we can import EMBEDDING_MODEL if it's defined elsewhere,
# but for this quick check we'll just use the one from the test file.
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_URL = "http://localhost:11434/api/embeddings"


def get_real_embedding(text: str) -> list[float]:
    """Helper to get embedding from Ollama for real tests."""
    url = OLLAMA_URL
    response = requests.post(url, json={"model": EMBEDDING_MODEL, "prompt": text})
    response.raise_for_status()
    return response.json()["embedding"]


if __name__ == "__main__":
    try:
        embedding = get_real_embedding("test query")
        print(f"Embedding dimension: {len(embedding)}")
    except Exception as e:
        print(f"Error: {e}")
