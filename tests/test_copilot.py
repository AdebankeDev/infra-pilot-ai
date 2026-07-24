from app.agent.copilot import CopilotService

copilot = CopilotService()

answer = copilot.ask(
    "What is Prism Central?"
)

print(answer)