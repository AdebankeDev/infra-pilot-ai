from pathlib import Path

import fitz

class DocumentProcessor:
    """
    Processes PDF documents for the Visual RAG pipeline.

    Responsibilities:
    - Open PDF documents
    - Extract text from each page
    - Extract embedded images
    - Save extracted images
    - Return structured page data
    """

    def __init__(self, image_output_dir: Path):
        self.image_output_dir = image_output_dir
        self.image_output_dir.mkdir(parents=True, exist_ok=True)

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


    def extract_text(self, page: fitz.Page) -> str:
        """
        Extracts text from a single PDF page.

        Args:
            page: A PyMuPDF page object.

        Returns:
            The extracted text from the page.
        """

        return page.get_text().strip()

    
    def extract_images(self, document: fitz.Document, page: fitz.Page, page_number: int, document_name: str,) -> list[str]:
        """
        Extracts all embedded images from a page and saves them to disk.

        Args:
            document: The open PDF document.
            page: The current page.
            page_number: Human-readable page number.

        Returns:
            A list of saved image file paths.
        """

        image_paths = []

        document_image_dir = self.image_output_dir / document_name
        document_image_dir.mkdir(parents=True, exist_ok=True)

        for image_index, image_info in enumerate(page.get_images(), start=1):
            xref = image_info[0]

            image = document.extract_image(xref)

            image_bytes = image["image"]
            image_extension = image["ext"]

            image_filename = (
                f"page_{page_number}_img_{image_index}.{image_extension}"
            )

            image_path = document_image_dir / image_filename

            with open(image_path, "wb") as file:
                file.write(image_bytes)

            image_paths.append(str(image_path))

        return image_paths

    def process_document(self, pdf_path: Path) -> list[dict]:
        """
        Processes a PDF document and returns structured page data.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            A list containing the extracted text and images for each page.
        """
        document = self.open_document(pdf_path)
        document_name = pdf_path.stem

        processed_pages = []

        try:
            for page_number, page in enumerate(document, start=1):
                text = self.extract_text(page)

                images = self.extract_images(
                    document=document,
                    page=page,
                    page_number=page_number,
                    document_name=document_name,
                )

                processed_pages.append(
                    {
                        "page": page_number,
                        "text": text,
                        "images": images,
                    }
                )
        finally:
            document.close()

        return processed_pages