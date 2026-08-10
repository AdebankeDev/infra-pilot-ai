import streamlit as st

from api import (
    get_messages,
    list_conversations,
)
from auth import logout
from utils.text import generate_conversation_title


# Number of recent conversations to display
MAX_CONVERSATIONS = 10


def show_sidebar() -> str:
    """
    Render the application sidebar.

    Returns:
        The currently selected page.
    """

    with st.sidebar:

        st.title("🤖 InfraPilot AI")

        st.divider()

        # -----------------------------
        # Navigation
        # -----------------------------
        selected_page = st.segmented_control(
            "Navigation",
            ["Chat", "Knowledge Base"],
            default="Chat",
        )

        st.divider()

        # -----------------------------
        # Chat Sidebar
        # -----------------------------
        if selected_page == "Chat":

            if st.button(
                "🆕 New Chat",
                use_container_width=True,
            ):

                st.session_state.messages = []
                st.session_state.conversation_id = None

                st.rerun()

            st.divider()

            st.subheader("Conversations")

            conversations = list_conversations()

            # Show only the most recent conversations
            conversations = conversations[:MAX_CONVERSATIONS]

            if not conversations:

                st.caption("No conversations yet.")

            else:

                for conversation in conversations:

                    conversation_title = generate_conversation_title(
                        conversation["title"]
                    )

                    if st.button(
                        conversation_title,
                        key=str(conversation["id"]),
                        use_container_width=True,
                    ):

                        messages = get_messages(
                            str(conversation["id"])
                        )

                        st.session_state.conversation_id = (
                            conversation["id"]
                        )

                        st.session_state.messages = [
                            {
                                "role": message["role"],
                                "content": message["content"],
                            }
                            for message in messages
                        ]

                        st.rerun()

        st.divider()

        # -----------------------------
        # Logout
        # -----------------------------
        if st.button(
            "Logout",
            use_container_width=True,
        ):

            logout()

            st.rerun()

    return selected_page
