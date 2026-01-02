import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime


# Initialize Supabase Client using Streamlit Secrets
# We use @st.cache_resource to keep the connection open across reruns
@st.cache_resource
def init_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


supabase: Client = init_supabase()


def get_tasks():
    """Fetches all tasks from Supabase."""
    try:
        # Select all columns, order by ID descending (newest first)
        response = supabase.table("tasks").select("*").order("id", desc=True).execute()

        # Convert to Pandas DataFrame for compatibility with your existing Dashboard
        data = response.data
        if not data:
            return pd.DataFrame(columns=["id", "task", "status", "created_at"])

        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Error fetching tasks: {e}")
        return pd.DataFrame()


def get_tasks_as_string():
    """Returns a simplified string list for the AI Agent."""
    df = get_tasks()
    if df.empty:
        return "You have no pending tasks."

    # Filter for pending only
    pending_df = df[df["status"] == "Pending"]

    if pending_df.empty:
        return "No pending tasks."

    task_list = [f"{row['id']}. {row['task']}" for _, row in pending_df.iterrows()]
    return "\n".join(task_list)


def add_task(task_content):
    """Inserts a new task into Supabase."""
    try:
        data = {"task": task_content, "status": "Pending"}
        supabase.table("tasks").insert(data).execute()
    except Exception as e:
        st.error(f"Error adding task: {e}")


def delete_task(task_id):
    """Deletes a task by ID."""
    try:
        supabase.table("tasks").delete().eq("id", task_id).execute()
    except Exception as e:
        st.error(f"Error deleting task: {e}")


def update_task_status(task_id, new_status):
    """Updates the status (e.g., 'Completed')."""
    try:
        supabase.table("tasks").update({"status": new_status}).eq("id", task_id).execute()
    except Exception as e:
        st.error(f"Error updating task: {e}")