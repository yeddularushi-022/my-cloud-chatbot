import streamlit as st
from google import genai
from google.genai import types
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Aether AI", 
    page_icon="⚡", 
    layout="centered"
)

# --- DARK MODE DESIGN ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .main-title {
        color: #FFFFFF;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    div[data-testid="stChatMessage"] {
        background-color: #1E1E1E !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }
    div.stButton > button {
        border-radius: 20px !important;
        border: 1px solid #444 !important;
        background: #222 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

api_key = st.secrets["GEMINI_API_KEY"].strip() if "GEMINI_API_KEY" in st.secrets else None

# --- UI ---
st.markdown("<h1 class='main-title'>Aether AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input Options
col1, col2, col3, col4 = st.columns(4)
mode = "Text"
if col1.button("💬 Text"): mode = "Text"
if col2.button("🖼️ Photo"): mode = "Photo"
if col3.button("📷 Cam"): mode = "Camera"
if col4.button("🎙️ Voice"): mode = "Voice"

file = None
if mode == "Photo": file = st.file_uploader("Upload", type=["jpg", "png"])
if mode == "Camera": file = st.camera_input("Capture")
if mode == "Voice": file = st.audio_input("Record")

# Chat
if prompt := st.chat_input("Message Aether..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        if file: st.image(file) if mode != "Voice" else st.audio(file)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                client = genai.Client(api_key=api_key, http_options={'headers': {'X-Goog-User-Project': 'gen-lang-client-0546112520'}})
                
                payload = [prompt]
                if file:
                    payload.append(types.Part.from_bytes(data=file.getvalue(), mime_type=file.type if hasattr(file, 'type') else 'image/jpeg'))
                
                resp = client.models.generate_content(model='gemini-2.5-flash', contents=payload)
                st.write(resp.text)
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
            except Exception as e:
                st.error(f"Error: {e}")
