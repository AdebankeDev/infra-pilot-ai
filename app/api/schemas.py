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


class ChatResponse(BaseModel):
    """
    Response model for chat.
    """

    answer: str
    sources: list[Source]