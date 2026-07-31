from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ConversationResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }