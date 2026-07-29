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

    def create(self, title: str) -> Conversation:
        """
        Create a new conversation.
        """
        conversation = Conversation(title=title)

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        """
        Retrieve a conversation by its ID.
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id
        )

        return self.db.scalar(statement)

    def list_all(self) -> list[Conversation]:
        """
        Retrieve all conversations ordered by newest first.
        """
        statement = (
            select(Conversation)
            .order_by(Conversation.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def delete(self, conversation: Conversation) -> None:
        """
        Delete a conversation.
        """
        self.db.delete(conversation)
        self.db.commit()