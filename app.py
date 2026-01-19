import streamlit as st
from google import genai
from PIL import Image
import time


# ---------------------------------------
# 1. Performance & Config
# ---------------------------------------
@st.cache_resource
def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)


st.set_page_config(page_title="Gemini AI Partner | Shakeeb", layout="wide", page_icon="🚀")

# ---------------------------------------
# 2. Secure API Key Check
# ---------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    client = get_gemini_client(API_KEY)
except KeyError:
    st.error("Please set GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

MODEL_NAME = "models/gemini-2.5-flash"


# ---------------------------------------
# 3. Helper: Multi-turn streaming with Retry Logic
# ---------------------------------------
def stream_gemini_response(user_text, image_data=None):
    parts = [user_text]
    if image_data:
        parts.append(image_data)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            responses = client.models.generate_content_stream(model=MODEL_NAME, contents=parts)
            for chunk in responses:
                if chunk.text:
                    yield chunk.text
            return
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                yield f"⚠️ Gemini is busy. Please try again in a moment."
                break


# ---------------------------------------
# 4. Session State
# ---------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = [{"name": "First Chat", "id": 1, "messages": []}]
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = 1

active_chat = next(chat for chat in st.session_state.chats if chat["id"] == st.session_state.active_chat_id)

# ---------------------------------------
# 5. Sidebar: Tools, Navigation & Developer Info
# ---------------------------------------
with st.sidebar:
    st.title("⚙️ Control Center")

    # 📖 User Guide
    with st.expander("📖 How to use", expanded=False):
        st.markdown("""
        1. **Chat:** Type in the box below to start.
        2. **Vision:** Upload an image for analysis.
        3. **History:** Switch between chats below.
        """)

    # 🖼️ Image Upload
    st.subheader("🖼️ Image Upload")
    uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "png", "jpeg"])
    img_preview = None
    if uploaded_file:
        img_preview = Image.open(uploaded_file)
        st.image(img_preview, caption="Image Ready!", use_container_width=True)
        if st.button("🗑️ Remove Photo"):
            st.rerun()

    st.divider()

    # 💬 Chat Management
    st.subheader("💬 Conversations")
    if st.button("➕ Start New Chat", use_container_width=True):
        new_id = max([c["id"] for c in st.session_state.chats]) + 1
        st.session_state.chats.append({"name": f"Chat {new_id}", "id": new_id, "messages": []})
        st.session_state.active_chat_id = new_id
        st.rerun()

    for chat_item in st.session_state.chats:
        is_active = chat_item["id"] == st.session_state.active_chat_id
        if st.button(chat_item["name"], key=f"chat_{chat_item['id']}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_chat_id = chat_item["id"]
            st.rerun()

    st.divider()

    # 👨‍💻 Developer Info (Updated)
    st.markdown("### 👨‍💻 Developer")
    st.info("**Shakeeb** \n\n Data Science Enthusiast building AI-driven solutions to simplify everyday tasks.")

    st.link_button("🐙 View My GitHub", "https://github.com/Sadat-Shakeeb", use_container_width=True)

    with st.expander("🛠️ Tech Stack"):
        st.caption("Engine: Gemini 2.5 Flash")
        st.caption("Frontend: Streamlit")
        st.caption("Language: Python 3.12")

# ---------------------------------------
# 6. Main UI: Welcome & Chat
# ---------------------------------------
if not active_chat["messages"]:
    st.title("👋 Welcome to Gemini Partner")
    st.markdown(f"#### Designed by **Shakeeb**")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**👁️ Vision Analysis**\n\nAnalyze datasets, code, or images for instant insights.")
    with col2:
        st.success("**✍️ Creative Content**\n\nDraft documentation or code with high-speed logic.")
    with col3:
        st.warning("**🚀 Optimized Speed**\n\nBuilt with retry logic and cached resources for stability.")
    st.divider()
else:
    st.title(f"💬 {active_chat['name']}")

# Display History
for msg in active_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"], width=400)

# Input
user_input = st.chat_input("Ask Shakeeb's AI anything...")

if user_input:
    user_entry = {"role": "user", "content": user_input}
    if uploaded_file:
        user_entry["image"] = img_preview
    active_chat["messages"].append(user_entry)

    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            st.image(img_preview, width=400)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Shakeeb's AI is thinking..."):
            for token in stream_gemini_response(user_input, img_preview if uploaded_file else None):
                full_res += token
                placeholder.markdown(full_res + "▌")
        placeholder.markdown(full_res)

    active_chat["messages"].append({"role": "assistant", "content": full_res})

# ---------------------------------------
# 7. Global Footer
# ---------------------------------------
st.markdown("---")
cols = st.columns([4, 1])
cols[1].caption("© 2026 Shakeeb")