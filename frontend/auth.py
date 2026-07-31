"""
Authentication utilities for the Streamlit frontend.
"""

import requests
import streamlit as st

from config import (
    LOGIN_ENDPOINT,
    SIGNUP_ENDPOINT,
    REQUEST_TIMEOUT,
)


def signup(
    email: str,
    password: str,
) -> bool:
    """
    Create a new user account.

    Returns:
        True if signup succeeds.
        False otherwise.
    """

    payload = {
        "email": email,
        "password": password,
    }

    try:
        response = requests.post(
            SIGNUP_ENDPOINT,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return True

    except requests.RequestException:
        return False


def login(
    email: str,
    password: str,
) -> bool:
    """
    Authenticate the user with the backend.

    Returns:
        True if login succeeds.
        False otherwise.
    """

    payload = {
        "email": email,
        "password": password,
    }

    try:
        response = requests.post(
            LOGIN_ENDPOINT,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        st.session_state["access_token"] = data["access_token"]

        return True

    except requests.RequestException:
        return False


def logout() -> None:
    """
    Log out the current user.
    """

    st.session_state.pop("access_token", None)
    st.session_state.pop("conversation_id", None)
    st.session_state.pop("messages", None)


def is_authenticated() -> bool:
    """
    Check whether the user is authenticated.
    """

    return "access_token" in st.session_state


def get_access_token() -> str | None:
    """
    Retrieve the stored access token.
    """

    return st.session_state.get("access_token")