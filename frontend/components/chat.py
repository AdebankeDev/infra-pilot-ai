import streamlit as st

from api import chat
from utils.sources import display_sources


def show_chat() -> None:
    """
    Render the main chat interface.
    """

    # -----------------------------
    # Header
    # -----------------------------
    st.title("🤖 InfraPilot AI")
    st.subheader("AI-Powered Infrastructure Copilot")
    st.caption("Enterprise Infrastructure Knowledge Assistant")

    st.divider()

    # -----------------------------
    # Session State
    # -----------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None

    # -----------------------------
    # Empty State
    # -----------------------------
    if not st.session_state.messages:

        st.info(
            """
            👋 Welcome to InfraPilot AI.

            Your AI assistant for enterprise infrastructure operations.

            You can ask about:

            • Nutanix troubleshooting
            • Server administration
            • Backup procedures
            • Infrastructure SOPs
            • Operational runbooks
            """
        )

    # -----------------------------
    # Display Chat History
    # -----------------------------
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                display_sources(
                    message.get("sources", [])
                )

    # -----------------------------
    # Chat Input
    # -----------------------------
    question = st.chat_input(
        "Ask an infrastructure question..."
    )

    if not question:
        return

    # -----------------------------
    # Display User Message
    # -----------------------------
    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # -----------------------------
    # Call Backend
    # -----------------------------
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chat(
                message=question,
                conversation_id=st.session_state.conversation_id,
            )

            st.session_state.conversation_id = (
                response["conversation_id"]
            )

        answer = response["answer"]
        sources = response["sources"]

        st.markdown(answer)

        display_sources(sources)

    # -----------------------------
    # Save Assistant Response
    # -----------------------------
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )