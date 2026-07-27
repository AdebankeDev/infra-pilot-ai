from __future__ import annotations

import fitz


class TextExtractor:
    """
    Extracts text from PDF pages.
    """

    def extract(self, page: fitz.Page) -> str:
        """
        Extract text from a single PDF page.

        Args:
            page: PyMuPDF page object.

        Returns:
            Extracted page text.
        """
        return page.get_text().strip()