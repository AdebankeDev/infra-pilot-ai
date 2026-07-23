from pathlib import Path
from pprint import pprint

from app.rag.document_processor import DocumentProcessor


def main():
    processor = DocumentProcessor(
        image_output_dir=Path("data/images")
    )

    raw_dir = Path("data/raw")
    pdf_files = list(raw_dir.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF files found in data/raw."
        )

    pdf_path = pdf_files[0]

    print(f"Processing: {pdf_path.name}")
    print("=" * 80)

    processed_pages = processor.process_document(pdf_path)

    print(f"Processed {len(processed_pages)} pages")
    print("=" * 80)

    pprint(processed_pages)


if __name__ == "__main__":
    main()