"""
Application configuration.
"""
import os

API_BASE_URL = os.getenv(
    "BACKEND_BASE_URL",
    "http://localhost:8000"
)

# ==========================================================
# Authentication
# ==========================================================

LOGIN_ENDPOINT = f"{API_BASE_URL}/auth/login"
SIGNUP_ENDPOINT = f"{API_BASE_URL}/auth/signup"
ME_ENDPOINT = f"{API_BASE_URL}/auth/me"

# ==========================================================
# Chat
# ==========================================================

CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
CONVERSATIONS_ENDPOINT = f"{CHAT_ENDPOINT}/conversations"

# ==========================================================
# Knowledge Base
# ==========================================================

DOCUMENTS_ENDPOINT = f"{API_BASE_URL}/knowledge-base/documents"

# ==========================================================
# General
# ==========================================================

REQUEST_TIMEOUT = 600
