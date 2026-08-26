import logging
import time
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.prompts import SYSTEM_PROMPT
from app.core.dependencies import get_knowledge_lookup_tool
from app.core.dependencies import get_llm_service


logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def knowledge_lookup(query: str) -> str:
    """
    Search Xpress Payment Solutions' internal infrastructure knowledge base
    (SOPs, runbooks, internal procedures, policies, FAQs).

    Call this ONLY when the user asks a company-specific infrastructure
    question that would require internal documentation to answer accurately.

    Do NOT call this for:
    - Greetings, small talk, or thanks
    - General infrastructure/IT concepts
    - Meta questions about the assistant itself
    - Follow-up messages that don't introduce a new question
    """

    logger.info("Knowledge lookup started for query: %s", query)

    start_time = time.time()

    results = get_knowledge_lookup_tool().search(
        query=query,
        k=5,
    )

    logger.info(
        "Knowledge lookup completed in %.2f seconds. Results: %d",
        time.time() - start_time,
        len(results),
    )

    if not results:
        return (
            "No relevant information was found in the company knowledge base. "
            "Inform the user that the requested information could not be found "
            "in the available documentation. Do not generate an answer from "
            "general knowledge."
        )

    sections = []

    for index, result in enumerate(results, start=1):
        metadata = result["metadata"]

        sections.append(
            f"""
Document {index}
----------------
Source: {metadata["source"]}
Page: {metadata["page"]}

Content:
{result["content"]}
""".strip()
        )

    retrieved_context = "\n\n" + (
        "=" * 80 + "\n\n"
    ).join(sections)

    return f"""
The following is retrieved company documentation.

This documentation is the authoritative source for answering the user's question.

Instructions:

- Answer ONLY using the retrieved documentation below.
- Do NOT add information from your own knowledge.
- Do NOT suggest alternative procedures unless they are documented.
- Do NOT include PowerShell commands, Windows instructions, troubleshooting steps, or best practices unless they appear in the retrieved documentation.
- Preserve the documented order of procedural steps.
- Include the responsible role, estimated TAT, risks, controls, notes, and prerequisites whenever they are present.
- If the documentation does not completely answer the user's question, explicitly state that the information is not available in the retrieved documentation instead of guessing.

Retrieved Documentation
=======================

{retrieved_context}
"""


def assistant(state: AgentState):
    """
    Assistant node responsible for reasoning and deciding
    whether to call tools.
    """

    llm = get_llm_service().bind_tools([knowledge_lookup])

    logger.info("Starting LLM invocation...")

    start_time = time.time()

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"],
        ]
    )

    elapsed = time.time() - start_time

    logger.info(
        "LLM invocation completed in %.2f seconds. Tool calls: %d",
        elapsed,
        len(response.tool_calls),
    )

    if response.tool_calls:
        logger.info(
            "Tool selected: %s",
            [call["name"] for call in response.tool_calls],
        )

    return {
        "messages": [response],
    }


tool_node = ToolNode(
    tools=[knowledge_lookup]
)


graph_builder = StateGraph(AgentState)


graph_builder.add_node(
    "assistant",
    assistant,
)

graph_builder.add_node(
    "tools",
    tool_node,
)


graph_builder.add_edge(
    START,
    "assistant",
)


graph_builder.add_conditional_edges(
    "assistant",
    tools_condition,
)


graph_builder.add_edge(
    "tools",
    "assistant",
)


graph = graph_builder.compile()