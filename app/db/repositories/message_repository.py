from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.message import Message


class MessageRepository:
    """
    Repository for Message database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        conversation_id: UUID,
        role: str,
        content: str,
    ) -> Message:
        """
        Create and persist a message.
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_by_conversation(
        self,
        conversation_id: UUID,
    ) -> list[Message]:
        """
        Retrieve all messages belonging to a conversation,
        ordered chronologically.
        """
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )

        return list(self.db.scalars(statement).all())

    def delete(
        self,
        message: Message,
    ) -> None:
        """
        Delete a message.
        """
        self.db.delete(message)
        self.db.commit()