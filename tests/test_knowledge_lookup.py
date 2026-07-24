from app.tools.knowledge_lookup import KnowledgeLookupTool
from app.rag.retriever import Retriever
from app.services.embedding_service import EmbeddingService
from app.storage.vector_store import VectorStore


def test_knowledge_lookup():
    embedding_service = EmbeddingService()
    vector_store = VectorStore(embedding_service)
    retriever = Retriever(vector_store)

    tool = KnowledgeLookupTool(retriever)

    results = tool.search(
        "How do I restart the application service?"
    )

    assert len(results) > 0

    for result in results:
        print("=" * 60)
        print(result["metadata"])
        print(result["content"][:300])


if __name__ == "__main__":
    test_knowledge_lookup()