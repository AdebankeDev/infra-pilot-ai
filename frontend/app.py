import streamlit as st

from auth import is_authenticated
from components.auth import show_auth
from components.chat import show_chat
from components.knowledge_base import show_knowledge_base
from components.sidebar import show_sidebar


st.set_page_config(
    page_title="InfraPilot AI",
    page_icon="🤖",
    layout="wide",
)


if not is_authenticated():
    show_auth()
    st.stop()


selected_page = show_sidebar()

if selected_page == "Chat":
    show_chat()

elif selected_page == "Knowledge Base":
    show_knowledge_base()