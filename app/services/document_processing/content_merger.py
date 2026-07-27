from __future__ import annotations


class ContentMerger:
    """
    Combines extracted page content into a unified structure.
    """

    def merge(
        self,
        *,
        document_name: str,
        page_number: int,
        text: str,
        tables: str,
        images: list[str],
    ) -> dict:
        return {
            "document_name": document_name,
            "page": page_number,
            "text": text,
            "tables": tables,
            "images": images,
        }