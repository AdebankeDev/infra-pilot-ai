from uuid import UUID

from pydantic import BaseModel, Field


class Source(BaseModel):
    """
    Source document used to answer the question.
    """

    document: str
    page: int
    images: list[str]


class ChatRequest(BaseModel):
    """
    Request model for chat messages.
    """

    message: str = Field(
        ...,
        min_length=1,
        description="User's message to InfraPilot AI.",
    )

    conversation_id: UUID | None = Field(
        default=None,
        description="Existing conversation ID. Creates a new conversation if omitted.",
    )


class ChatResponse(BaseModel):
    """
    Response model for chat.
    """

    conversation_id: UUID

    answer: str

    sources: list[Source]