from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Provides the embedding model for the application."""

    def __init__(self):
        logger.info("Initializing EmbeddingService...")

        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """Return the configured embedding model."""

        return self.embeddings