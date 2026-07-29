import requests

from config import CHAT_ENDPOINT, REQUEST_TIMEOUT


def chat(
    message: str,
    conversation_id=None,
) -> dict:
    """
    Send a user message to the FastAPI backend.

    Args:
        message:
            User's message.

        conversation_id:
            Existing conversation ID.
            None creates a new conversation.

    Returns:
        Parsed JSON response.

    Raises:
        requests.RequestException:
            If communication with the backend fails.
    """

    payload = {
        "message": message,
        "conversation_id": conversation_id,
    }

    response = requests.post(
        CHAT_ENDPOINT,
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()