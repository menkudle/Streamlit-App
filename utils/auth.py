import streamlit as st
import time


def check_credentials(username, password):
    """
    Verifies username and password.
    In a real app, you would hash the password and check against a database.
    """
    # Hardcoded credentials for learning purposes
    VALID_USER = "admin"
    VALID_PASS = "password"

    if username == VALID_USER and password == VALID_PASS:
        return True
    return False


def require_auth():
    """
    Place this function at the very top of every page in the /pages/ folder.
    It checks if the user is logged in. If not, it stops the page and redirects.
    """
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("🔒 You must log in to view this page.")
        st.caption("Redirecting to login page in 2 seconds...")

        # Pause briefly so user sees the message
        time.sleep(2)

        # Force a switch back to the main login app
        st.switch_page("app.py")

        # Stop execution so the rest of the page code doesn't run
        st.stop()