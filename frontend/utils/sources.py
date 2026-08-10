import streamlit as st


def display_sources(sources: list) -> None:

    if not sources:
        return

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