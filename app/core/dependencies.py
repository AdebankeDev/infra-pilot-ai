from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.message_repository import MessageRepository
from app.rag.retriever import Retriever
from app.services.conversation_service import ConversationService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.storage.vector_store import VectorStore
from app.tools.knowledge_lookup import KnowledgeLookupTool


# ==========================================================
# AI Dependencies (Singletons)
# ==========================================================

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


# ==========================================================
# Request-scoped Dependencies
# ==========================================================

def get_conversation_service(
    db: Session = Depends(get_db),
) -> ConversationService:
    """
    Return a ConversationService for the current request.
    """
    conversation_repository = ConversationRepository(db)
    message_repository = MessageRepository(db)

    return ConversationService(
        conversation_repository=conversation_repository,
        message_repository=message_repository,
    )