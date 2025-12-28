import streamlit as st
import requests
import json
from utils.auth import require_auth

# 1. Security Check
require_auth()

st.title("💬 Nemotron Chat")
st.caption("Running locally via Ollama with 'nemotron-mini'")

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if prompt := st.chat_input("Ask Nemotron something..."):
    # Add user message to UI state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Call Local LLM (Ollama)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        try:
            # We use the /api/chat endpoint so we can send the full history
            payload = {
                "model": "nemotron-mini",
                "messages": st.session_state.messages,  # Sends context!
                "stream": False
            }

            response = requests.post(
                "http://localhost:11434/api/chat",
                json=payload
            )

            if response.status_code == 200:
                # Parse the response from /api/chat
                response_data = response.json()
                assistant_text = response_data['message']['content']

                # Update UI
                message_placeholder.markdown(assistant_text)

                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": assistant_text})
            else:
                message_placeholder.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            message_placeholder.error(f"Connection failed: {e}. Ensure 'ollama run nemotron-mini' is active.")