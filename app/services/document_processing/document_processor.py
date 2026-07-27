from pathlib import Path

import fitz

from app.services.document_processing.content_merger import ContentMerger
from app.services.document_processing.image_extractor import ImageExtractor
from app.services.document_processing.table_extractor import TableExtractor
from app.services.document_processing.text_extractor import TextExtractor


class DocumentProcessor:
    """
    Orchestrates the document processing pipeline.

    Responsibilities:
    - Open PDF documents
    - Coordinate text extraction
    - Coordinate table extraction
    - Coordinate image extraction
    - Merge extracted content into a unified page structure
    """

    def __init__(self, image_output_dir: Path):
        self.image_output_dir = image_output_dir
        self.image_output_dir.mkdir(parents=True, exist_ok=True)

        self.text_extractor = TextExtractor()
        self.table_extractor = TableExtractor()
        self.image_extractor = ImageExtractor(image_output_dir)
        self.content_merger = ContentMerger()

    def open_document(self, pdf_path: Path) -> fitz.Document:
        """
        Opens a PDF document after validating the file.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            An open PyMuPDF Document object.

        Raises:
            FileNotFoundError: If the PDF does not exist.
            ValueError: If the file is not a PDF.
            RuntimeError: If the PDF cannot be opened.
        """

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file, got: {pdf_path.suffix}")

        try:
            return fitz.open(pdf_path)

        except Exception as exc:
            raise RuntimeError(
                f"Failed to open PDF: {pdf_path}"
            ) from exc

    def process_document(self, pdf_path: Path) -> list[dict]:
        """
        Processes a PDF document and returns structured page data.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            A list containing the extracted content for each page.
        """

        document = self.open_document(pdf_path)
        document_name = pdf_path.stem

        processed_pages = []

        try:
            for page_number, page in enumerate(document, start=1):

                # Extract page text
                text = self.text_extractor.extract(page)

                # Placeholder for table extraction
                tables = self.table_extractor.extract(page)

                # Extract embedded images
                images = self.image_extractor.extract(
                    document=document,
                    page=page,
                    page_number=page_number,
                    document_name=document_name,
                )

                # Merge extracted content
                page_data = self.content_merger.merge(
                    document_name=document_name,
                    page_number=page_number,
                    text=text,
                    tables=tables,
                    images=images,
                )

                processed_pages.append(page_data)

        finally:
            document.close()

        return processed_pages