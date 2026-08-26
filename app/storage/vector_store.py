import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Persistent ChromaDB vector store.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):
        logger.info("Initializing VectorStore...")

        self._embedding_service = embedding_service

        self._store = Chroma(
            collection_name=settings.chroma_collection_name,
            persist_directory=settings.chroma_persist_directory,
            embedding_function=self._embedding_service.get_embeddings(),
        )

    def add_documents(
        self,
        documents: list[Document],
    ) -> None:
        """
        Store documents in ChromaDB.
        """

        self._store.add_documents(documents)

    def similarity_search(
        self,
        query: str,
        k: int = 3,
    ) -> list[Document]:
        """
        Retrieve the most similar documents.
        """

        return self._store.similarity_search(
            query,
            k=k,
        )

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete all vector chunks belonging to a document.
        """

        self._store.delete(
            where={
                "document_id": document_id,
            }
        )

    def count(self) -> int:
        """
        Return the number of stored vectors.
        """

        return self._store._collection.count()

    def delete_collection(self) -> None:
        """
        Delete the entire ChromaDB collection.
        """

        self._store.delete_collection()