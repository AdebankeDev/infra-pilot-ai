"""
Application configuration.
"""

API_BASE_URL = "http://127.0.0.1:8000"

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

REQUEST_TIMEOUT = 300