import logging

from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Wrapper around the configured chat model.

    Responsibilities:
    - Initialize the configured LLM
    - Send messages to the model
    - Bind tools for LangGraph agents
    """

    def __init__(self):
        logger.info("Initializing LLMService...")

        self._llm = ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature,
            num_predict=256,
        )

    def invoke(self, messages: list[BaseMessage]):
        """
        Invoke the language model.

        Args:
            messages: LangChain message objects.

        Returns:
            AIMessage
        """
        return self._llm.invoke(messages)

    def bind_tools(self, tools: list):
        """
        Return an LLM instance with tools bound.

        Args:
            tools: LangChain tools.

        Returns:
            ChatOllama configured for tool calling.
        """
        return self._llm.bind_tools(tools)