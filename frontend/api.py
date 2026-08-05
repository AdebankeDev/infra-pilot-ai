import requests

from auth import get_access_token
from config import (
    CHAT_ENDPOINT,
    CONVERSATIONS_ENDPOINT,
    DOCUMENTS_ENDPOINT,
    REQUEST_TIMEOUT,
)


def _get_headers() -> dict[str, str]:
    """
    Build the Authorization header for authenticated requests.
    """

    token = get_access_token()

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}",
    }


# ==========================================================
# Chat
# ==========================================================

def chat(
    message: str,
    conversation_id: str | None = None,
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


# ==========================================================
# Conversations
# ==========================================================

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


# ==========================================================
# Knowledge Base
# ==========================================================

def upload_document(file) -> dict:
    """
    Upload a PDF document to the knowledge base.
    """

    file.seek(0)

    files = {
        "file": (
            file.name,
            file,
            "application/pdf",
        )
    }

    response = requests.post(
        DOCUMENTS_ENDPOINT,
        headers=_get_headers(),
        files=files,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


def list_documents() -> list:
    """
    Retrieve all indexed documents.
    """

    response = requests.get(
        DOCUMENTS_ENDPOINT,
        headers=_get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


def delete_document(
    document_id: str,
) -> None:
    """
    Delete a document from the knowledge base.
    """

    response = requests.delete(
        f"{DOCUMENTS_ENDPOINT}/{document_id}",
        headers=_get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()