from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import ChatRequest, ChatResponse
from app.db.database import get_db
from app.services.chat_service import ChatService

from uuid import UUID

from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService
from app.schemas.conversation import ConversationResponse
from app.schemas.message import MessageResponse


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



@router.get(
    "/conversations",
    response_model=list[ConversationResponse],
)
def list_conversations(
    db: Session = Depends(get_db),
):
    """
    Retrieve all conversations ordered by newest first.
    """

    conversation_service = ConversationService(
        conversation_repository=ConversationRepository(db),
        message_repository=MessageRepository(db),
    )

    return conversation_service.list_conversations()



@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve all messages for a conversation.
    """

    conversation_service = ConversationService(
        conversation_repository=ConversationRepository(db),
        message_repository=MessageRepository(db),
    )

    try:
        return conversation_service.get_conversation_messages(
            conversation_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )