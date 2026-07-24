from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Infrastructure Copilot for Enterprise IT Operations",
    version=settings.app_version,
)

app.include_router(chat_router)


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
        "version": app.version,
    }


app.mount(
    "/images",
    StaticFiles(directory="data/images"),
    name="images",
)