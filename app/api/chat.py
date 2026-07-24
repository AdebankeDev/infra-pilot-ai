from fastapi import APIRouter

from app.agent.copilot import CopilotService
from app.api.schemas import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

copilot = CopilotService()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    """
    Chat with InfraPilot AI.
    """

    result = copilot.ask(request.message)

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
    )