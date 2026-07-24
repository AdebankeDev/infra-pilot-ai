from functools import lru_cache

from app.services.llm_service import LLMService
from app.tools.knowledge_lookup import KnowledgeLookupTool
from app.rag.retriever import Retriever
from app.services.embedding_service import EmbeddingService
from app.storage.vector_store import VectorStore


@lru_cache
def get_embedding_service() -> EmbeddingService:
    """Return the shared embedding service."""
    return EmbeddingService()


@lru_cache
def get_vector_store() -> VectorStore:
    """Return the shared vector store."""
    return VectorStore(
        embedding_service=get_embedding_service(),
    )


@lru_cache
def get_retriever() -> Retriever:
    """Return the shared retriever."""
    return Retriever(
        vector_store=get_vector_store(),
    )


@lru_cache
def get_knowledge_lookup_tool() -> KnowledgeLookupTool:
    """Return the shared knowledge lookup tool."""
    return KnowledgeLookupTool(
        retriever=get_retriever(),
    )


@lru_cache
def get_llm_service() -> LLMService:
    """Return the shared LLM service."""
    return LLMService()