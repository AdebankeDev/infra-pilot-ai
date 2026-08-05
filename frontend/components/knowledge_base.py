from datetime import datetime

import requests
import streamlit as st
import time

from api import (
    delete_document,
    list_documents,
    upload_document,
)


def show_knowledge_base():
    """
    Render the Knowledge Base Management interface.
    """

    st.title("📚 Knowledge Base")

    st.write(
        "Upload, manage, and remove documents used by InfraPilot AI."
    )

    st.divider()

    # ==========================================================
    # Upload Section
    # ==========================================================

    st.subheader("Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"],
    )

    if st.button(
        "Upload",
        type="primary",
    ):
        if uploaded_file is None:
            st.warning("Please select a PDF document.")

        else:
            try:
                uploaded_file.seek(0)

                with st.spinner(
                    "Uploading and indexing document..."
                ):
                    upload_document(uploaded_file)

                st.success(
                    "Document uploaded successfully."
                )
                time.sleep(1)  # Wait for a moment before refreshing
                st.rerun()

            except requests.HTTPError as e:
                st.error(f"Upload failed: {e}")

            except Exception as e:
                st.error(str(e))

    st.divider()

    # ==========================================================
    # Indexed Documents
    # ==========================================================

    st.subheader("Indexed Documents")

    try:
        documents = list_documents()

        if not documents:

            st.info(
                "No documents have been indexed yet."
            )

        else:

            for document in documents:

                uploaded_at = datetime.fromisoformat(
                    document["created_at"]
                )

                with st.container(border=True):

                    info_col, action_col = st.columns([5, 1])

                    with info_col:

                        st.markdown(
                            f"#### 📄 {document['filename']}"
                        )

                        st.write(
                            f"**Status:** {document['status']}"
                        )

                        st.write(
                            f"**Chunks:** {document['total_chunks']}"
                        )

                        st.write(
                            f"**Uploaded:** "
                            f"{uploaded_at.strftime('%d %b %Y, %I:%M %p')}"
                        )

                    with action_col:

                        st.write("")
                        st.write("")

                        if st.button(
                            "🗑 Delete",
                            key=f"delete_{document['id']}",
                            use_container_width=True,
                        ):

                            try:

                                with st.spinner(
                                    "Deleting document..."
                                ):
                                    delete_document(
                                        document["id"]
                                    )

                                st.success(
                                    f"{document['filename']} deleted successfully."
                                )

                                st.rerun()

                            except requests.HTTPError as e:
                                st.error(
                                    f"Delete failed: {e}"
                                )

                            except Exception as e:
                                st.error(str(e))

    except requests.HTTPError as e:
        st.error(
            f"Failed to load documents: {e}"
        )

    except Exception as e:
        st.error(str(e))