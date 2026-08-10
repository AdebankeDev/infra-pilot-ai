def generate_conversation_title(
    text: str,
    max_length: int = 35,
) -> str:
    """
    Generate a short display title for conversations.
    """

    text = text.strip()

    if len(text) <= max_length:
        return text

    return text[:max_length].rstrip() + "..."