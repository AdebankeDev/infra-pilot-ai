from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.api.schemas import ChatRequest, ChatResponse
from app.db.database import get_db
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.message_repository import MessageRepository
from app.schemas.conversation import ConversationResponse
from app.schemas.message import MessageResponse
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService


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
    current_user=Depends(get_current_user),
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
        user_id=current_user.id,
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
    current_user=Depends(get_current_user),
):
    """
    Retrieve all conversations belonging to the authenticated user.
    """

    conversation_service = ConversationService(
        conversation_repository=ConversationRepository(db),
        message_repository=MessageRepository(db),
    )

    return conversation_service.list_conversations(
        user_id=current_user.id,
    )


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve all messages for one of the authenticated user's conversations.
    """

    conversation_service = ConversationService(
        conversation_repository=ConversationRepository(db),
        message_repository=MessageRepository(db),
    )

    try:
        return conversation_service.get_conversation_messages(
            conversation_id=conversation_id,
            user_id=current_user.id,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )