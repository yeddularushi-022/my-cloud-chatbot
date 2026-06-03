import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Aether AI", page_icon="⚡", layout="centered")

# --- PREMIUM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0F0F0F; color: white; }
    .main-title { text-align: center; font-size: 2rem; margin-top: 1rem; margin-bottom: 2rem; }
    [data-testid="stSidebar"] { background-color: #161616; }
    .stChatMessage { background-color: #1A1A1A !important; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

api_key = st.secrets["GEMINI_API_KEY"].strip() if "GEMINI_API_KEY" in st.secrets else None

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("⚡ Aether History")
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
    st.divider()
    # List previous interactions briefly
    if "messages" in st.session_state:
        for i, msg in enumerate(st.session_state.messages[::2]):
            st.caption(f"Session {i+1}: {msg['content'][:20]}...")

# --- MAIN AREA ---
st.markdown("<h1 class='main-title'>Aether AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "input_mode" not in st.session_state: st.session_state.input_mode = "Text"

# Input Selectors
cols = st.columns(4)
if cols[0].button("💬 Text"): st.session_state.input_mode = "Text"
if cols[1].button("🖼️ Photo"): st.session_state.input_mode = "Photo"
if cols[2].button("📷 Cam"): st.session_state.input_mode = "Camera"
if cols[3].button("🎙️ Voice"): st.session_state.input_mode = "Voice"

# File Input Logic
file = None
if st.session_state.input_mode == "Photo": file = st.file_uploader("", type=["jpg", "png"])
elif st.session_state.input_mode == "Camera": file = st.camera_input("")
elif st.session_state.input_mode == "Voice": file = st.audio_input("")

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# Chat Input
if prompt := st.chat_input("Message Aether..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        try:
            client = genai.Client(api_key=api_key, http_options={'headers': {'X-Goog-User-Project': 'gen-lang-client-0546112520'}})
            payload = [prompt]
            if file: payload.append(types.Part.from_bytes(data=file.getvalue(), mime_type=file.type if hasattr(file, 'type') else 'image/jpeg'))
            
            resp = client.models.generate_content(model='gemini-2.5-flash', contents=payload)
            st.write(resp.text)
            st.session_state.messages.append({"role": "assistant", "content": resp.text})
        except Exception as e:
            st.error(f"Error: {e}")
