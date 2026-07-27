from __future__ import annotations

from pathlib import Path

import fitz


class ImageExtractor:
    """
    Extracts embedded images from PDF pages.
    """

    def __init__(self, image_output_dir: Path):
        self.image_output_dir = image_output_dir

    def extract(
        self,
        document: fitz.Document,
        page: fitz.Page,
        page_number: int,
        document_name: str,
    ) -> list[str]:
        """
        Extract images from a page and save them to disk.
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