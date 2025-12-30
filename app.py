import streamlit as st
from utils.auth import check_credentials

# Page Configuration
st.set_page_config(page_title="Streamlit App", layout="wide")


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
            st.rerun()
        else:
            st.error("Incorrect username or password")


def logout():
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()


# --- DEFINE ALL PAGES ---
# 1. Wrap the login function as a Page
login_page = st.Page(login, title="Log In", icon="🔐")

# 2. Define your application pages
dashboard = st.Page("pages/basic_dashboard.py", title="Business Overview", icon="📊")
plotly_dash = st.Page("pages/plotly_dashboard.py", title="Detailed Analysis", icon="🤓")
chatbot = st.Page("pages/ai_chatbot.py", title="Agentic Assistant", icon="🤖")
tasks = st.Page("pages/task_manager.py", title="My Tasks", icon="✅")

# --- NAVIGATION LOGIC ---
if not st.session_state.logged_in:
    # SHOW ONLY LOGIN PAGE
    # position="hidden" hides the sidebar entirely on the login screen
    pg = st.navigation([login_page], position="hidden")
else:
    # SHOW APP PAGES
    pg = st.navigation({
        "Dashboards": [dashboard, plotly_dash],
        "Tools": [chatbot, tasks]
    })

    # Show user profile in sidebar
    with st.sidebar:
        st.write("User: Admin")
        logout()

# Run the selected page
pg.run()