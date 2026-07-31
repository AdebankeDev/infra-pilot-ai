"""
Application configuration.
"""

API_BASE_URL = "http://127.0.0.1:8000"

# Authentication
LOGIN_ENDPOINT = f"{API_BASE_URL}/auth/login"
ME_ENDPOINT = f"{API_BASE_URL}/auth/me"
SIGNUP_ENDPOINT = f"{API_BASE_URL}/auth/signup"

# Chat
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
CONVERSATIONS_ENDPOINT = f"{CHAT_ENDPOINT}/conversations"

REQUEST_TIMEOUT = 300