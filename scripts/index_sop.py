from pathlib import Path

from app.rag.document_processor import DocumentProcessor
from app.services.document_indexer import DocumentIndexer
from app.services.embedding_service import EmbeddingService
from app.rag.text_chunker import TextChunker
from app.storage.vector_store import VectorStore


def main():
    print("=" * 60)
    print("InfraPilot AI - Document Indexing")
    print("=" * 60)

    # Path for extracted images
    image_output_dir = Path("data/images")

    # Path to SOP document
    pdf_path = Path("data/raw/infrastructure_sop.pdf")

    # Initialize services
    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        embedding_service=embedding_service
    )

    processor = DocumentProcessor(
        image_output_dir=image_output_dir
    )

    chunker = TextChunker()

    indexer = DocumentIndexer(
        processor=processor,
        chunker=chunker,
        vector_store=vector_store,
    )

    # Index document
    result = indexer.index_document(pdf_path)

    print("\nIndexing Complete")
    print("-" * 60)

    print(f"Document : {result['document']}")
    print(f"Pages    : {result['pages']}")
    print(f"Chunks   : {result['chunks']}")

    print("\nChromaDB Statistics")
    print("-" * 60)

    print(f"Stored Documents: {vector_store.count()}")

    print("=" * 60)


if __name__ == "__main__":
    main()