from pathlib import Path
import logging

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
)

from app.agent.graph import graph
from app.core.config import settings
from app.core.dependencies import get_retriever
from app.db.models.message import Message


logger = logging.getLogger(__name__)


class CopilotService:
    """
    Service for interacting with the Infrastructure Copilot.
    """

    MAX_HISTORY_MESSAGES = 6  # last 3 user+assistant exchanges

    # Messages that should never trigger the RAG/agent workflow.
    SMALL_TALK = {
        "hi",
        "hello",
        "hey",
        "thanks",
        "thank you",
        "good morning",
        "good afternoon",
        "good evening",
    }

    def ask(
        self,
        question: str,
        messages: list[Message],
    ) -> dict:
        """
        Send a question to InfraPilot AI.

        Args:
            question:
                The current user question.

            messages:
                Conversation history retrieved from the database.
        """

        # ==========================================================
        # Handle obvious small talk without invoking the AI agent
        # ==========================================================

        normalized = question.strip().lower()

        if normalized in self.SMALL_TALK:
            logger.info("Small-talk message detected. Skipping LangGraph.")

            return {
                "answer": "Hello! How can I help with your infrastructure question today?",
                "sources": [],
            }

        # ==========================================================
        # Limit conversation history
        # ==========================================================

        recent_messages = messages[-self.MAX_HISTORY_MESSAGES:]

        # Convert database messages into LangChain messages
        history: list[BaseMessage] = []

        for message in recent_messages:
            if message.role == "user":
                history.append(
                    HumanMessage(content=message.content)
                )
            else:
                history.append(
                    AIMessage(content=message.content)
                )

        logger.info("Routing request through LangGraph agent.")

        # ==========================================================
        # Generate AI response
        # ==========================================================

        response = graph.invoke(
            {
                "messages": history,
            }
        )

        answer = response["messages"][-1].content

        # ==========================================================
        # Retrieve source metadata
        # ==========================================================

        sources = self._get_sources(question)

        return {
            "answer": answer,
            "sources": sources,
        }

    def _get_sources(self, question: str) -> list:
        """
        Retrieve source metadata for the retrieved company documents.
        """

        retrieved_chunks = get_retriever().search(
            query=question,
            k=3,
        )

        sources = []
        seen = set()

        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]

            key = (
                metadata.get("source"),
                metadata.get("page"),
            )

            if key in seen:
                continue

            seen.add(key)

            document = Path(
                metadata.get("source", "Unknown")
            ).stem

            images = []

            for image in metadata.get("images", [])[:3]:
                relative_path = (
                    Path(image)
                    .relative_to("storage/images")
                    .as_posix()
                )

                images.append(
                    f"{settings.public_backend_url}/images/{relative_path}"
                )

            sources.append(
                {
                    "document": document,
                    "page": metadata.get("page"),
                    "images": images,
                }
            )

        return sources