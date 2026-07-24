from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """Splits processed PDF pages into smaller chunks for embeddings."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        logger.info("Initializing TextChunker")

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk_document(
        self,
        processed_pages: list[dict],
        document_name: str,
    ) -> list[Document]:
        """
        Convert processed PDF pages into LangChain Documents.
        """

        documents: list[Document] = []

        for page in processed_pages:

            page_number = page["page"]
            page_text = page["text"]
            image_paths = page["images"]

            chunks = self.text_splitter.split_text(page_text)

            for chunk in chunks:

                metadata = {
                    "source": document_name,
                    "page": page_number,
                }

                # Only include images if the page has any
                if image_paths:
                    metadata["images"] = image_paths

                document = Document(
                    page_content=chunk,
                    metadata=metadata,
                )

                documents.append(document)

        return documents