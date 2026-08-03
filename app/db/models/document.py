from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Enum as SQLEnum, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.db.models.mixins import TimestampMixin


class DocumentStatus(str, Enum):
    INDEXING = "INDEXING"
    READY = "READY"
    FAILED = "FAILED"


class Document(TimestampMixin, Base):
    """
    Represents an indexed knowledge base document.
    """

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    uploaded_by: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        SQLEnum(DocumentStatus),
        default=DocumentStatus.INDEXING,
        nullable=False,
    )

    total_chunks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )