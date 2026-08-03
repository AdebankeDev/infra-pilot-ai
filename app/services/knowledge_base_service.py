from pathlib import Path
import shutil
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.models.document import Document, DocumentStatus
from app.db.repositories.document_repository import DocumentRepository
from app.rag.text_chunker import TextChunker
from app.services.document_indexer import DocumentIndexer
from app.services.document_processing.document_processor import DocumentProcessor
from app.services.embedding_service import EmbeddingService
from app.storage.vector_store import VectorStore


class KnowledgeBaseService:
    """
    Service responsible for managing the knowledge base.
    """

    DOCUMENTS_DIR = Path("storage/documents")
    IMAGES_DIR = Path("storage/images")

    def __init__(self, db: Session):
        self.DOCUMENTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.repository = DocumentRepository(db)

        embedding_service = EmbeddingService()

        vector_store = VectorStore(
            embedding_service=embedding_service,
        )

        processor = DocumentProcessor(
            image_output_dir=self.IMAGES_DIR,
        )

        chunker = TextChunker()

        self.document_indexer = DocumentIndexer(
            processor=processor,
            chunker=chunker,
            vector_store=vector_store,
        )

    def list_documents(self) -> list[Document]:
        """
        Retrieve all indexed documents.
        """
        return self.repository.list_documents()

    def upload_document(
        self,
        file: UploadFile,
        uploaded_by: str,
    ) -> Document:
        """
        Upload and index a PDF document.
        """

        if (
            not file.filename
            or not file.filename.lower().endswith(".pdf")
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF documents are supported.",
            )

        existing = self.repository.get_by_filename(
            file.filename
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A document with this filename already exists.",
            )

        file_path = self.DOCUMENTS_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            filename=file.filename,
            file_path=str(file_path),
            uploaded_by=uploaded_by,
            status=DocumentStatus.INDEXING,
        )

        document = self.repository.create(document)

        try:
            result = self.document_indexer.index_document(
                pdf_path=file_path,
                document_id=str(document.id),
            )

            document.total_chunks = result["chunks"]
            document.status = DocumentStatus.READY

            return self.repository.update(document)

        except Exception:
            document.status = DocumentStatus.FAILED
            self.repository.update(document)

            if file_path.exists():
                file_path.unlink()

            raise

    def delete_document(
        self,
        document_id: UUID,
    ) -> None:
        """
        Delete an indexed document.

        This removes:
        - Vector embeddings from ChromaDB
        - Stored PDF
        - Extracted screenshots
        - Database record
        """

        document = self.repository.get_by_id(document_id)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        # Delete vectors from ChromaDB
        self.document_indexer.vector_store.delete_document(
            document_id=str(document.id),
        )

        # Delete stored PDF
        file_path = Path(document.file_path)

        if file_path.exists():
            file_path.unlink()

        # Delete extracted screenshots
        image_directory = self.IMAGES_DIR / Path(document.filename).stem

        if image_directory.exists():
            shutil.rmtree(image_directory)

        # Delete database record
        self.repository.delete(document)