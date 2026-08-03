from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.document import Document


class DocumentRepository:
    """
    Repository for Document database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document: Document,
    ) -> Document:
        """
        Persist a new document.
        """
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def get_by_id(
        self,
        document_id: UUID,
    ) -> Document | None:
        """
        Retrieve a document by its ID.
        """
        statement = select(Document).where(
            Document.id == document_id,
        )

        return self.db.scalar(statement)

    def get_by_filename(
        self,
        filename: str,
    ) -> Document | None:
        """
        Retrieve a document by filename.
        """
        statement = select(Document).where(
            Document.filename == filename,
        )

        return self.db.scalar(statement)

    def list_documents(
        self,
    ) -> list[Document]:
        """
        Retrieve all indexed documents ordered by newest first.
        """
        statement = (
            select(Document)
            .order_by(Document.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def update(
        self,
        document: Document,
    ) -> Document:
        """
        Persist changes to an existing document.
        """
        self.db.commit()
        self.db.refresh(document)

        return document

    def delete(
        self,
        document: Document,
    ) -> None:
        """
        Delete a document.
        """
        self.db.delete(document)
        self.db.commit()