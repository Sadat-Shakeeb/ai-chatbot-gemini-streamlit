import streamlit as st
from google import genai
import os

# ---------------------------------------
# Page config
# ---------------------------------------
st.set_page_config(page_title="Gemini Chatbot", layout="wide")




# ---------------------------------------
# Gemini client initialization
# ---------------------------------------
# Use the key you just verified
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Initialize standard client (No v1beta forced)
client = genai.Client(api_key=API_KEY)

# Use the ID that we found in your test script
MODEL_NAME = "models/gemini-2.5-flash"

# Optional: Add a quick check to the UI
if "connection_verified" not in st.session_state:
    try:
        client.models.get(model=MODEL_NAME)
        st.session_state.connection_verified = True
    except Exception as e:
        st.error(f"Failed to connect to {MODEL_NAME}: {e}")
        st.stop()

# ... (the rest of your Streamlit code)

# We force 'v1beta' to ensure the latest models like gemini-1.5-flash are found


# ---------------------------------------
# Session state initialization
# ---------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = [
        {"name": "New Chat", "id": 1, "messages": []}
    ]

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = 1


# ---------------------------------------
# Helper functions
# ---------------------------------------
def get_active_chat():
    return next(
        chat for chat in st.session_state.chats
        if chat["id"] == st.session_state.active_chat_id
    )


def stream_gemini_response(history):
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    # The call remains the same, but MODEL_NAME now has the prefix
    responses = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents
    )

    for chunk in responses:
        if chunk.text:
            yield chunk.text


# ---------------------------------------
# Sidebar – Chat Management
# ---------------------------------------
st.sidebar.title("💬 Chat Sessions")

# Create New Chat
if st.sidebar.button("➕ New Chat", use_container_width=True):
    new_id = max([c["id"] for c in st.session_state.chats]) + 1
    st.session_state.chats.append(
        {"name": f"Chat {new_id}", "id": new_id, "messages": []}
    )
    st.session_state.active_chat_id = new_id
    st.rerun()

st.sidebar.divider()

# List existing chats
for chat in st.session_state.chats:
    is_active = chat["id"] == st.session_state.active_chat_id
    # Use a visually distinct button for the active chat
    if st.sidebar.button(
            chat["name"],
            key=f"chat_{chat['id']}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
    ):
        st.session_state.active_chat_id = chat["id"]
        st.rerun()

st.sidebar.divider()

if st.sidebar.button("🗑️ Delete Current Chat", use_container_width=True):
    if len(st.session_state.chats) > 1:
        st.session_state.chats = [
            c for c in st.session_state.chats
            if c["id"] != st.session_state.active_chat_id
        ]
        st.session_state.active_chat_id = st.session_state.chats[0]["id"]
        st.rerun()
    else:
        st.sidebar.warning("At least one chat must exist")

# ---------------------------------------
# Main Chat UI
# ---------------------------------------
chat = get_active_chat()
st.title(f"Gemini: {chat['name']}")

# Display chat history
for msg in chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # 1. Add user message to state and UI
    chat["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Generate and stream assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # We pass the message history (including the prompt we just added)
        for token in stream_gemini_response(chat["messages"]):
            full_response += token
            placeholder.markdown(full_response)

    # 3. Save assistant response to state
    chat["messages"].append({"role": "assistant", "content": full_response})