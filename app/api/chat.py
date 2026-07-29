from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import ChatRequest, ChatResponse
from app.db.database import get_db
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Chat with InfraPilot AI.

    Handles:
    - Conversation lifecycle
    - Message persistence
    - AI response generation
    """

    chat_service = ChatService(db)

    result = chat_service.chat(
        message=request.message,
        conversation_id=request.conversation_id,
    )

    return ChatResponse(
        conversation_id=result["conversation_id"],
        answer=result["answer"],
        sources=result["sources"],
    )