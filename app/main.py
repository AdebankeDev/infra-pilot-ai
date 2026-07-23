from app.core.config import settings
from fastapi import FastAPI
from app.services.llm import generate_response

app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Infrastructure Copilot for Enterprise IT Operations",
    version=settings.app_version,
)

@app.get("/")
def root():
    return {
        "message": "Welcome to InfraPilot AI API"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "InfraPilot AI API",
        "version": app.version
    }

@app.get("/test-llm")
def test_llm():
    response = generate_response("Introduce yourself in one sentence.")

    return {
        "status": "success",
        "response": response,
    }