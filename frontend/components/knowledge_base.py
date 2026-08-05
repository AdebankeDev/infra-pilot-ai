from datetime import datetime

import requests
import streamlit as st

from api import (
    delete_document,
    list_documents,
    upload_document,
)


def show_knowledge_base():
    """
    Render the Knowledge Base Management interface.
    """

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = None

    if "notification" not in st.session_state:
        st.session_state.notification = None

    st.title("📚 Knowledge Base")

    st.write(
        "Manage the infrastructure documents that power InfraPilot AI's knowledge retrieval."
    )

    # ==========================================================
    # Notifications
    # ==========================================================

    notification = st.session_state.notification

    if notification:
        getattr(
            st,
            notification["level"],
        )(notification["message"])

        st.session_state.notification = None

    st.divider()

    
    # ==========================================================
    # Upload Section
    # ==========================================================

    st.subheader("📤 Upload Document")

    st.caption(
        "Upload a PDF document to add new knowledge to InfraPilot AI's retrieval system."
    )

    upload_col, button_col = st.columns([5, 1])

    with upload_col:

        uploaded_file = st.file_uploader(
            "Choose a PDF document",
            type=["pdf"],
            label_visibility="collapsed",
        )


    with button_col:

        st.write("")
        st.write("")

        upload_clicked = st.button(
            "⬆ Upload",
            type="primary",
            use_container_width=True,
        )


    if uploaded_file:

        file_size_mb = uploaded_file.size / (1024 * 1024)

        st.caption(
            f"Selected: {uploaded_file.name} "
            f"({file_size_mb:.2f} MB)"
        )


    if upload_clicked:

        if uploaded_file is None:

            st.warning(
                "Please select a PDF document."
            )

        else:

            try:

                uploaded_file.seek(0)

                with st.spinner(
                    "Uploading and indexing document..."
                ):
                    upload_document(uploaded_file)

                st.session_state.notification = {
                    "level": "success",
                    "message": (
                        "Document uploaded successfully."
                    ),
                }

                st.rerun()

            except requests.HTTPError as e:

                st.session_state.notification = {
                    "level": "error",
                    "message": f"Upload failed: {e}",
                }

                st.rerun()

            except Exception as e:

                st.session_state.notification = {
                    "level": "error",
                    "message": str(e),
                }

                st.rerun()

    st.divider()

    # ==========================================================
    # Indexed Documents
    # ==========================================================

    st.subheader("📚 Indexed Documents")

    try:

        documents = list_documents()

        # ======================================================
        # Knowledge Base Metrics
        # ======================================================

        if documents:

            total_documents = len(documents)

            indexed_documents = sum(
                1
                for document in documents
                if document["status"].lower() == "indexed"
            )

            total_chunks = sum(
                document["total_chunks"]
                for document in documents
            )

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:

                st.metric(
                    label="Documents",
                    value=total_documents,
                )

            with metric_col2:

                st.metric(
                    label="Indexed",
                    value=indexed_documents,
                )

            with metric_col3:

                st.metric(
                    label="Total Chunks",
                    value=total_chunks,
                )

            st.divider()

        if not documents:

            st.info(
                "📂 No documents have been indexed yet."
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

                        status = document["status"].lower()

                        if status in ["ready", "indexed"]:

                            st.success(
                                "🟢 Ready"
                            )


                        elif status in ["indexing", "processing"]:

                            st.warning(
                                "🟡 Indexing"
                            )


                        elif status == "failed":

                            st.error(
                                "🔴 Failed"
                            )
                        st.write(
                            f"🧩 **Chunks:** {document['total_chunks']}"
                        )

                        st.write(
                            f"🕒 **Uploaded:** "
                            f"{uploaded_at.strftime('%d %b %Y, %I:%M %p')}"
                        )

                    with action_col:

                        st.write("")
                        st.write("")

                        if st.button(
                            "Delete",
                            key=f"delete_{document['id']}",
                            use_container_width=True,
                        ):

                            st.session_state.confirm_delete = (
                                document["id"]
                            )

                            st.rerun()

                    # ==================================================
                    # Delete Confirmation
                    # ==================================================

                    if (
                        st.session_state.confirm_delete
                        == document["id"]
                    ):

                        st.warning(
                            f"⚠️ Are you sure you want to delete "
                            f"**{document['filename']}**?"
                        )

                        confirm_col, cancel_col = st.columns(2)

                        with confirm_col:

                            if st.button(
                                "✅ Yes, Delete",
                                key=f"confirm_{document['id']}",
                                type="primary",
                                use_container_width=True,
                            ):

                                try:

                                    with st.spinner(
                                        "Deleting document..."
                                    ):

                                        delete_document(
                                            document["id"]
                                        )

                                    st.session_state.confirm_delete = None

                                    st.session_state.notification = {
                                        "level": "success",
                                        "message": (
                                            f"{document['filename']} deleted successfully."
                                        ),
                                    }

                                    st.rerun()

                                except requests.HTTPError as e:

                                    st.session_state.notification = {
                                        "level": "error",
                                        "message": (
                                            f"Delete failed: {e}"
                                        ),
                                    }

                                    st.rerun()

                                except Exception as e:

                                    st.session_state.notification = {
                                        "level": "error",
                                        "message": str(e),
                                    }

                                    st.rerun()

                        with cancel_col:

                            if st.button(
                                "Cancel",
                                key=f"cancel_{document['id']}",
                                use_container_width=True,
                            ):

                                st.session_state.confirm_delete = None

                                st.rerun()

    except requests.HTTPError as e:

        st.error(
            f"Failed to load documents: {e}"
        )

    except Exception as e:

        st.error(str(e))