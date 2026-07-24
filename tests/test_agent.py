from langchain_core.messages import HumanMessage

from app.agent.graph import graph


response = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="According to our SOP, how do I restart Prism Central?"
            )
        ]
    }
)

print(response["messages"][-1].content)