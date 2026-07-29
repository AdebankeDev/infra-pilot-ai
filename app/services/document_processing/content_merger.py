import re


class ContentMerger:
    """
    Combines extracted text and tables into a unified page representation.
    """

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text for duplicate comparison.
        """
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def merge(
        self,
        *,
        document_name: str,
        page_number: int,
        text: str,
        tables: str,
        images: list[str],
    ) -> dict:

        sections = []

        text = text.strip()
        tables = tables.strip()

        if text:
            sections.append(text)

        if tables:

            normalized_text = self.normalize(text)
            normalized_tables = self.normalize(tables)

            if normalized_tables not in normalized_text:
                sections.append(tables)

        combined_content = "\n\n".join(sections)

        return {
            "document_name": document_name,
            "page": page_number,
            "content": combined_content,
            "images": images,
        }