import requests

from auth import get_access_token
from config import (
    CHAT_ENDPOINT,
    CONVERSATIONS_ENDPOINT,
    REQUEST_TIMEOUT,
)


def _get_headers() -> dict:
    """
    Build the Authorization header for authenticated requests.
    """

    token = get_access_token()

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}",
    }


def chat(
    message: str,
    conversation_id=None,
) -> dict:
    """
    Send a user message to the FastAPI backend.
    """

    payload = {
        "message": message,
        "conversation_id": conversation_id,
    }

    response = requests.post(
        CHAT_ENDPOINT,
        json=payload,
        headers=_get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


def list_conversations() -> list:
    """
    Retrieve all conversations for the authenticated user.
    """

    response = requests.get(
        CONVERSATIONS_ENDPOINT,
        headers=_get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


def get_messages(
    conversation_id: str,
) -> list:
    """
    Retrieve all messages for a conversation.
    """

    response = requests.get(
        f"{CONVERSATIONS_ENDPOINT}/{conversation_id}/messages",
        headers=_get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()