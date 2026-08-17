from app.rag.retriever import Retriever


class KnowledgeLookupTool:
    """
    Tool for searching Xpress Payment Solutions' internal infrastructure
    knowledge base (SOPs, runbooks, internal procedures, FAQs).

    Call this ONLY when the user's message is a company-specific infrastructure
    question — e.g. asking about an internal procedure, runbook step, policy,
    or system that would be documented internally.

    Do NOT call this tool for:
    - Greetings, small talk, or thanks ("hi", "thanks", "how are you")
    - General infrastructure/IT questions answerable from general knowledge
      (e.g. "what is a load balancer?", "explain DNS caching")
    - Meta questions about the assistant itself ("what can you do?")
    - Follow-up conversational messages that don't introduce a new question
    """

    def __init__(self, retriever: Retriever):
        self._retriever = retriever

    def search(
        self,
        query: str,
        k: int = 5,
    ) -> list[dict]:
        """
        Search the internal knowledge base for company-specific infrastructure
        documentation relevant to the query.

        Only call this when the query is an actual company-specific infrastructure
        question (SOP, runbook, internal procedure, policy, or FAQ). Never call
        for greetings, small talk, or purely conceptual/general knowledge questions.

        Args:
            query: The user's company-specific infrastructure question, rephrased
                as a clear search query if needed.
            k: Number of relevant chunks to retrieve.

        Returns:
            Retrieved document chunks. May be empty if nothing relevant is found —
            in that case, tell the user the documentation wasn't found rather than
            fabricating an answer.
        """

        return self._retriever.search(
            query=query,
            k=k,
        )