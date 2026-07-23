from pathlib import Path

from app.rag.document_processor import DocumentProcessor
from app.rag.text_chunker import TextChunker


def main():
    # Process the PDF
    processor = DocumentProcessor(
        image_output_dir=Path("data/images")
    )

    processed_pages = processor.process_document(
        Path("data/raw/infrastructure_sop.pdf")
    )

    # Chunk the processed pages
    chunker = TextChunker()

    documents = chunker.chunk_document(
        processed_pages=processed_pages,
        document_name="infrastructure_sop.pdf",
    )

    print(f"\nTotal Chunks: {len(documents)}\n")

    # Display the first 5 chunks
    for i, document in enumerate(documents[:5], start=1):
        print("=" * 80)
        print(f"Chunk {i}")
        print("=" * 80)

        print("Metadata:")
        print(document.metadata)

        print("\nContent:")
        print(document.page_content[:500])

        print("\n")


if __name__ == "__main__":
    main()