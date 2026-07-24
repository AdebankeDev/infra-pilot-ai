from langchain_core.messages import HumanMessage

from app.services.llm_service import LLMService


def test_llm():
    llm = LLMService()

    response = llm.invoke(
        [
            HumanMessage(
                content="Hello! Introduce yourself."
            )
        ]
    )

    print(response.content)


if __name__ == "__main__":
    test_llm()