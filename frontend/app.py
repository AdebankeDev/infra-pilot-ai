import streamlit as st

from api import chat


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="InfraPilot AI",
    page_icon="🤖",
    layout="wide",
)

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


# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                with st.expander("📄 View Sources"):

                    for source in sources:

                        st.markdown(
                            f"**Document:** {source['document']}"
                        )

                        st.markdown(
                            f"**Page:** {source['page']}"
                        )

                        images = source.get("images", [])

                        if images:

                            st.markdown("**Associated Screenshots**")

                            for image in images:
                                st.image(
                                    image,
                                    use_container_width=True,
                                )

                        st.divider()


# -----------------------------
# Chat Input
# -----------------------------
question = st.chat_input(
    "Ask an infrastructure question..."
)

if question:

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Call backend
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching company documentation..."
        ):

            response = chat(question)

        answer = response["answer"]
        sources = response["sources"]

        st.markdown(answer)

        if sources:

            with st.expander("📄 View Sources"):

                for source in sources:

                    st.markdown(
                        f"**Document:** {source['document']}"
                    )

                    st.markdown(
                        f"**Page:** {source['page']}"
                    )

                    images = source.get("images", [])

                    if images:

                        st.markdown(
                            "**Associated Screenshots**"
                        )

                        for image in images:
                            st.image(
                                image,
                                use_container_width=True,
                            )

                    st.divider()

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )