from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.prompts import SYSTEM_PROMPT
from app.core.dependencies import get_knowledge_lookup_tool
from langchain_core.messages import SystemMessage
from app.core.dependencies import get_llm_service


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def knowledge_lookup(query: str) -> str:
    """
    Search the company's knowledge base.
    """

    results = get_knowledge_lookup_tool().search(query=query)

    if not results:
        return "No relevant information was found in the knowledge base."

    formatted_results = []

    for result in results:
        metadata = result["metadata"]

        formatted_results.append(
            f"""
Source: {metadata["source"]}
Page: {metadata["page"]}

{result["content"]}
""".strip()
        )

    return "\n\n" + ("\n" + "-" * 60 + "\n\n").join(formatted_results)


def assistant(state: AgentState):
    """
    Assistant node responsible for reasoning and deciding
    whether to call tools.
    """

    llm = get_llm_service().bind_tools([knowledge_lookup])

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"],
        ]
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