from app.core.config import settings
from app.rag.retriever import Retriever
from app.services.embedding_service import EmbeddingService
from app.storage.vector_store import VectorStore


def main():
    print("=" * 60)
    print("InfraPilot AI - Retriever Test")
    print("=" * 60)

    # Initialize services
    embedding_service = EmbeddingService()
    vector_store = VectorStore(embedding_service)
    retriever = Retriever(vector_store)

    # Test queries
    queries = [
        "How do I restart the application service?",
        "How do I troubleshoot a failed transaction?",
        "What should I do if a server is unreachable?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)

        results = retriever.search(query=query, k=3)

        if not results:
            print("No results found.")
            continue

        for index, result in enumerate(results, start=1):
            metadata = result["metadata"]

            print(f"\nResult {index}")
            print(f"Source : {metadata.get('source')}")
            print(f"Page   : {metadata.get('page')}")

            images = metadata.get("images", [])
            if images:
                print(f"Images : {images}")

            preview = result["content"][:300].replace("\n", " ")
            print(f"Content: {preview}...")


if __name__ == "__main__":
    main()