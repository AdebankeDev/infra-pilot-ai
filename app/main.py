from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.core.config import settings
from app.api.admin import router as admin_router


app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Infrastructure Copilot for Enterprise IT Operations",
    version=settings.app_version,
)


app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(admin_router)

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
    StaticFiles(directory="storage/images"),
    name="images",
)