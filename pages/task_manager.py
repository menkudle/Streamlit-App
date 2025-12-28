import streamlit as st
from utils.db_manager import init_db, add_task, get_tasks, delete_task
from utils.auth import require_auth

require_auth()

# Initialize DB on first load
init_db()

st.title("✅ Task Manager")

# Input for new task
new_task = st.text_input("New Task")
if st.button("Add Task"):
    if new_task:
        add_task(new_task)
        st.success("Task added!")
        st.rerun()

# Display Tasks
st.subheader("Your To-Do List")
df = get_tasks()

if not df.empty:
    for index, row in df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"• {row['task']}")
        with col2:
            if st.button("Delete", key=row['rowid']):
                delete_task(row['rowid'])
                st.rerun()
else:
    st.info("No tasks yet.")