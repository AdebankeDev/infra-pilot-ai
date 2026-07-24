from app.rag.retriever import Retriever


class KnowledgeLookupTool:
    """
    Tool for searching the company's knowledge base.

    This tool is used by the LangGraph agent whenever
    company-specific knowledge is required.
    """

    def __init__(self, retriever: Retriever):
        self._retriever = retriever

    def search(
        self,
        query: str,
        k: int = 3,
    ) -> list[dict]:
        """
        Search the knowledge base.

        Args:
            query: User's question.
            k: Number of relevant chunks to retrieve.

        Returns:
            Retrieved document chunks.
        """

        return self._retriever.search(
            query=query,
            k=k,
        )