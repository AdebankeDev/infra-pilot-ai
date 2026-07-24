from pathlib import Path

from langchain_core.messages import HumanMessage

from app.agent.graph import graph
from app.core.dependencies import get_retriever


class CopilotService:
    """
    Service for interacting with the Infrastructure Copilot agent.
    """

    def ask(self, question: str) -> dict:
        """
        Send a question to the Infrastructure Copilot.

        Args:
            question: User's question.

        Returns:
            The assistant's answer together with source metadata.
        """

        # Invoke the LangGraph agent
        response = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=question),
                ]
            }
        )

        answer = response["messages"][-1].content

        # Retrieve relevant sources for metadata
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

            images = [
                image.replace("\\", "/").replace("data/images", "/images")
                for image in metadata.get("images", [])[:3]
            ]

            sources.append(
                {
                    "document": document,
                    "page": metadata.get("page"),
                    "images": images,
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }