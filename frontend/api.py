import requests

from config import CHAT_ENDPOINT, REQUEST_TIMEOUT


def chat(message: str) -> dict:
    """
    Send a user message to the FastAPI backend.

    Returns:
        Parsed JSON response.
    Raises:
        requests.RequestException:
            If communication with the backend fails.
    """

    response = requests.post(
        CHAT_ENDPOINT,
        json={"message": message},
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()