from __future__ import annotations

from pathlib import Path

import pdfplumber


class TableExtractor:
    """
    Extracts and formats tables from PDF pages using pdfplumber.
    """

    def extract(self, pdf_path: Path, page_number: int) -> str:
        """
        Extract tables from a specific PDF page.

        Args:
            pdf_path: Path to the PDF.
            page_number: 1-based page number.

        Returns:
            Natural-language representation of the tables.
        """

        sections = []

        with pdfplumber.open(pdf_path) as pdf:

            page = pdf.pages[page_number - 1]

            tables = page.extract_tables()

            for table in tables:

                if not table or len(table) < 2:
                    continue

                headers = [
                    (header or "").replace("\n", " ").strip()
                    for header in table[0]
                ]

                for row in table[1:]:

                    if not row:
                        continue

                    row = [
                        (cell or "").replace("\n", " ").strip()
                        for cell in row
                    ]

                    entry = []

                    for header, value in zip(headers, row):

                        if not value:
                            continue

                        entry.append(f"{header}: {value}")

                    if entry:
                        sections.append("\n".join(entry))

        return "\n\n".join(sections)