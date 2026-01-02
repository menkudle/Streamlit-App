import streamlit as st
import requests
import re
from utils.auth import require_auth
from utils.db_manager import add_task, get_tasks_as_string

# 1. Security Check
require_auth()

st.title("🤖 Agentic Assistant")

# 2. CONFIGURATION: Check for Cloud API Key
# If found in secrets, use Groq. If not, default to Localhost (Ollama).
if "GROQ_API_KEY" in st.secrets:
    IS_CLOUD = True
    API_KEY = st.secrets["GROQ_API_KEY"]
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL_NAME = "llama-3.3-70b-versatile" # Highly capable, fast model
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    st.caption("⚡ Powered by Groq Cloud API")
else:
    IS_CLOUD = False
    API_URL = "http://localhost:11434/api/chat"
    MODEL_NAME = "llama3.2"
    HEADERS = {}
    st.caption("🏠 Running Locally on Ollama")


# 2. System Prompt
SYSTEM_PROMPT = """
You are a AI Assistant who can answer simple queries and also manage Tasks.
AVAILABLE TOOLS:
1. To add a task to list, output: COMMAND: ADD_TASK | [Task Content]
2. To list tasks, output: COMMAND: LIST_TASKS

RULES:
- Check for user query and if it matches available tools above, respond in specified out. If it does matches the above tools, respond normally without using above commands.
- Only use the commands listed above.
- Dont memorise the task list. Use available tools for tasks
"""

# 3. Initialize History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input Handling
if prompt := st.chat_input("What can I do for you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

        # Prepare Messages for API
        # We always insert the System Prompt at the start
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 Thinking...")

        try:
            # 5. SEND REQUEST
            payload = {
                "model": MODEL_NAME,
                "messages": api_messages,
                "temperature": 0.0,  # Keep it 0 for strict command adherence
                "stream": False
            }

            if IS_CLOUD:
                # GROQ (OpenAI Format)
                response = requests.post(API_URL, json=payload, headers=HEADERS)
                response.raise_for_status()
                response_text = response.json()['choices'][0]['message']['content']
            else:
                # OLLAMA (Local Format)
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                response_text = response.json()['message']['content']

            # --- AGENT LOGIC ---

            # Check for ADD_TASK
            add_match = re.search(r"COMMAND:\s*ADD_TASK\s*\|\s*(.*)", response_text, re.IGNORECASE)

            # Check for LIST_TASKS
            list_match = re.search(r"COMMAND:\s*LIST_TASKS", response_text, re.IGNORECASE)

            if add_match:
                task_content = add_match.group(1).strip()
                add_task(task_content)

                final_msg = f"✅ Added task: **{task_content}**"
                message_placeholder.markdown(final_msg)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"I have added '{task_content}' to your list."
                })

            elif list_match:
                # 1. Fetch data from DB
                tasks_str = get_tasks_as_string()

                # 2. Show in UI
                final_msg = f"📋 **Current Tasks:**\n\n{tasks_str}"
                message_placeholder.markdown(final_msg)

                # 3. Save to history (so the LLM knows what's on the list for follow-up questions)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Here are your current tasks:\n{tasks_str}"
                })

            else:
                # Normal chat response
                message_placeholder.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            message_placeholder.error(f"Error: {e}")