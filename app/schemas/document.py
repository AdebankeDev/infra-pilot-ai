from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.db.models.document import DocumentStatus


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    uploaded_by: str
    status: DocumentStatus
    total_chunks: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }