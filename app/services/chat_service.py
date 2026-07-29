from uuid import UUID

from sqlalchemy.orm import Session

from app.agent.copilot import CopilotService
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.message_repository import MessageRepository


class ChatService:
    """
    Handles chat workflow and conversation persistence.

    Responsibilities:
    - Manage conversation lifecycle
    - Persist user and assistant messages
    - Coordinate with the AI Copilot service
    """

    def __init__(self, db: Session):
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)
        self.copilot = CopilotService()

    def chat(
        self,
        message: str,
        conversation_id: UUID | None = None,
    ) -> dict:
        """
        Process a chat request.

        Flow:
        1. Create or retrieve conversation
        2. Save user message
        3. Generate AI response
        4. Save assistant response
        5. Return response with conversation ID
        """

        # Create a new conversation if this is the first message
        if conversation_id is None:
            conversation = self.conversation_repo.create(
                title=message[:50]
            )

            conversation_id = conversation.id

        else:
            # Verify that the conversation exists
            conversation = self.conversation_repo.get_by_id(
                conversation_id
            )

            if conversation is None:
                raise ValueError(
                    "Conversation not found"
                )

        # Persist user message
        self.message_repo.create(
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

        # Generate AI response
        result = self.copilot.ask(message)

        # Persist assistant message
        self.message_repo.create(
            conversation_id=conversation_id,
            role="assistant",
            content=result["answer"],
        )

        return {
            "conversation_id": conversation_id,
            "answer": result["answer"],
            "sources": result["sources"],
        }