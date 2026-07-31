from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.conversation import Conversation


class ConversationRepository:
    """
    Repository for Conversation database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: str,
        title: str,
    ) -> Conversation:
        """
        Create a new conversation for a user.
        """
        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_by_id(
        self,
        conversation_id: UUID,
        user_id: str,
    ) -> Conversation | None:
        """
        Retrieve a conversation belonging to a specific user.
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )

        return self.db.scalar(statement)

    def list_by_user(
        self,
        user_id: str,
    ) -> list[Conversation]:
        """
        Retrieve all conversations for a user ordered by newest first.
        """
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def delete(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Delete a conversation.
        """
        self.db.delete(conversation)
        self.db.commit()