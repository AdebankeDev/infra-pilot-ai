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

    image_output_dir = Path("data/images")

    raw_dir = Path("data/raw")

    pdf_files = list(raw_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF documents found.")
        return

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

    total_chunks = 0

    for pdf_path in pdf_files:
        print(f"\nIndexing: {pdf_path.name}")

        result = indexer.index_document(pdf_path)

        print(f"Pages  : {result['pages']}")
        print(f"Chunks : {result['chunks']}")

        total_chunks += result["chunks"]

    print("\nIndexing Complete")
    print("-" * 60)

    print(f"Documents Indexed: {len(pdf_files)}")
    print(f"Total Chunks     : {total_chunks}")

    print("\nChromaDB Statistics")
    print("-" * 60)

    print(f"Stored Documents: {vector_store.count()}")

    print("=" * 60)


if __name__ == "__main__":
    main()