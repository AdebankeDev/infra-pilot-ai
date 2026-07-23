import logging

from openai import APIError, OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)


def generate_response(prompt: str) -> str:
    """
    Generate a response from the configured LLM.

    Args:
        prompt: The user's prompt.

    Returns:
        The generated response text.

    Raises:
        APIError: If the request to the LLM provider fails.
    """
    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("The model returned an empty response.")

        return content

    except APIError as e:
        logger.exception("OpenRouter API request failed.")
        raise

    except Exception as e:
        logger.exception("Unexpected error while generating LLM response.")
        raise