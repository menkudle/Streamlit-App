import streamlit as st
from utils.auth import check_credentials

# Page Configuration
st.set_page_config(page_title="Streamlit App")

# Initialize Session State for Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.success("Logged in!")
            # st.rerun()
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Incorrect username or password")


def logout():
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()


# --- Main App Logic ---
if not st.session_state.logged_in:
    login()
else:
    # st.sidebar.title("Navigation")
    # logout()
    # st.write("### Welcome back, Admin!")
    # st.info("👈 Select a page from the sidebar to get started.")
    pg = st.navigation([
        st.Page("pages/dashboard.py", title="Business Overview", icon="📊"),
        st.Page("pages/ai_chatbot.py", title="Nemotron Assistant", icon="🤖"),
        st.Page("pages/task_manager.py", title="My Tasks", icon="✅"),
    ])

    # Show the sidebar logout button
    with st.sidebar:
        st.write("User: Admin")
        logout()

    # Run the selected page
    pg.run()