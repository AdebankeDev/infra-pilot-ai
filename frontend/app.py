import streamlit as st

from auth import is_authenticated
from components.auth import show_auth
from components.chat import show_chat
from components.sidebar import show_sidebar


st.set_page_config(
    page_title="InfraPilot AI",
    page_icon="🤖",
    layout="wide",
)


if not is_authenticated():
    show_auth()
    st.stop()


show_sidebar()

show_chat()