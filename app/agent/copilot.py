from pathlib import Path
import logging

from langchain_core.messages import HumanMessage

from app.agent.graph import graph
from app.core.config import settings
from app.core.dependencies import get_retriever


logger = logging.getLogger(__name__)


class CopilotService:
    """
    Service for interacting with the Infrastructure Copilot.
    """

    def ask(self, question: str) -> dict:
        """
        Send a question to InfraPilot AI.

        Every request is routed through the LangGraph agent.
        The agent determines whether to answer directly using the LLM
        or retrieve company documentation through the knowledge_lookup tool.

        Args:
            question:
                User input.

        Returns:
            A dictionary containing the generated answer and
            any associated source metadata.
        """

        logger.info("Routing request through LangGraph agent.")

        response = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            }
        )

        answer = response["messages"][-1].content

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
            k=1,
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
                    .relative_to("data/images")
                    .as_posix()
                )

                images.append(
                    f"{settings.backend_base_url}/images/{relative_path}"
                )

            sources.append(
                {
                    "document": document,
                    "page": metadata.get("page"),
                    "images": images,
                }
            )

        return sources