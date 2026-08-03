from pathlib import Path

from app.services.document_processing.document_processor import DocumentProcessor
from app.rag.text_chunker import TextChunker
from app.storage.vector_store import VectorStore


class DocumentIndexer:
    """
    Orchestrates the document indexing pipeline.

    Workflow:
    PDF -> DocumentProcessor -> TextChunker -> VectorStore -> ChromaDB
    """

    def __init__(
        self,
        processor: DocumentProcessor,
        chunker: TextChunker,
        vector_store: VectorStore,
    ):
        self.processor = processor
        self.chunker = chunker
        self.vector_store = vector_store

    def index_document(
        self,
        pdf_path: Path,
        document_id: str | None = None,
    ) -> dict:
        """
        Process a PDF and index it into the vector database.

        Args:
            pdf_path:
                Path to the PDF document.

            document_id:
                Database ID of the document.
                Stored in each chunk's metadata to support
                document management operations such as deletion.

        Returns:
            Dictionary containing indexing statistics.
        """

        # Step 1: Extract text and images from the PDF
        processed_pages = self.processor.process_document(pdf_path)

        # Step 2: Convert pages into LangChain Documents
        documents = self.chunker.chunk_document(
            processed_pages=processed_pages,
            document_name=pdf_path.name,
        )

        # Step 3: Attach database document ID to every chunk
        if document_id:
            for document in documents:
                document.metadata["document_id"] = document_id

        # Step 4: Store document chunks in ChromaDB
        self.vector_store.add_documents(documents)

        # Step 5: Return indexing summary
        return {
            "document": pdf_path.name,
            "pages": len(processed_pages),
            "chunks": len(documents),
        }