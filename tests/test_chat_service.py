from app.db.database import SessionLocal
from app.services.chat_service import ChatService


def test_chat_service():

    db = SessionLocal()

    try:
        chat_service = ChatService(db)

        result = chat_service.chat(
            message="How do I restart the application service?"
        )

        print("RESULT:")
        print(result)

        print("\nConversation ID:")
        print(result["conversation_id"])

    finally:
        db.close()


if __name__ == "__main__":
    test_chat_service()