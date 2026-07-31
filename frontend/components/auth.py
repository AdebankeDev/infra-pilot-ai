import streamlit as st

from auth import login, signup


def show_auth() -> None:
    """
    Render the authentication page.
    """

    st.title("🤖 InfraPilot AI")

    st.subheader("AI-Powered Infrastructure Copilot")

    st.caption(
        "Enterprise Infrastructure Knowledge Assistant"
    )

    st.divider()

    login_tab, signup_tab = st.tabs(
        ["Login", "Sign Up"]
    )

    # -------------------------
    # Login
    # -------------------------
    with login_tab:

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                key="login_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )

            submitted = st.form_submit_button(
                "Login"
            )

            if submitted:

                success = login(
                    email=email,
                    password=password,
                )

                if success:
                    st.success(
                        "Login successful."
                    )
                    st.rerun()

                st.error(
                    "Invalid email or password."
                )

    # -------------------------
    # Sign Up
    # -------------------------
    with signup_tab:

        with st.form("signup_form"):

            email = st.text_input(
                "Email",
                key="signup_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password",
            )

            submitted = st.form_submit_button(
                "Create Account"
            )

            if submitted:

                success = signup(
                    email=email,
                    password=password,
                )

                if success:

                    st.success(
                        "Account created successfully."
                    )

                    st.info(
                        "You can now log in."
                    )

                else:

                    st.error(
                        "Unable to create account."
                    )