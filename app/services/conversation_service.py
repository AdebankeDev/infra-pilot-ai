from uuid import UUID

from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.message_repository import MessageRepository


class ConversationService:
    """
    Service for conversation-related operations.
    """

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    def list_conversations(
        self,
        user_id: str,
    ) -> list[Conversation]:
        """
        Retrieve all conversations belonging to a user.
        """
        return self.conversation_repository.list_by_user(user_id)

    def get_conversation_messages(
        self,
        conversation_id: UUID,
        user_id: str,
    ) -> list[Message]:
        """
        Retrieve all messages for a user's conversation.
        """
        conversation = self.conversation_repository.get_by_id(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        if conversation is None:
            raise ValueError("Conversation not found.")

        return self.message_repository.get_by_conversation(
            conversation_id
        )