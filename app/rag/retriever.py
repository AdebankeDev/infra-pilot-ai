from app.storage.vector_store import VectorStore


class Retriever:
    """
    Retrieves relevant document chunks from the vector store.

    Responsibilities:
    - Accept a user query.
    - Retrieve the most relevant document chunks.
    - Normalize retrieved documents into a consistent format.
    """

    def __init__(self, vector_store: VectorStore):
        self._vector_store = vector_store

    def search(
        self,
        query: str,
        k: int = 3,
    ) -> list[dict]:
        """
        Search the knowledge base for relevant document chunks.

        Args:
            query: User's natural language question.
            k: Number of document chunks to retrieve.

        Returns:
            A list of retrieved document chunks with metadata.
        """

        documents = self._vector_store.similarity_search(
            query=query,
            k=k,
        )

        results = []

        for document in documents:
            results.append(
                {
                    "content": document.page_content,
                    "metadata": {
                        "source": document.metadata.get("source"),
                        "page": document.metadata.get("page"),
                        "images": document.metadata.get("images", []),
                    },
                }
            )

        return results