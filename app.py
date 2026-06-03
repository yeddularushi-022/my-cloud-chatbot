import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Aether AI", page_icon="⚡", layout="centered")

# --- PREMIUM MODERN CSS ---
st.markdown("""
    <style>
    /* Global Styling */
    .stApp { background-color: #FAFAFA; font-family: 'Inter', sans-serif; }
    
    /* Header Styling */
    .title-container { text-align: center; margin-top: 2rem; margin-bottom: 2rem; }
    .main-title { font-size: 2.2rem; font-weight: 700; color: #111; }
    .subtitle { color: #666; font-size: 1rem; }
    
    /* Input Pill Buttons */
    div.stButton > button {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    div.stButton > button:hover { border-color: #3B82F6 !important; color: #3B82F6 !important; }
    
    /* Chat Bubbles */
    div[data-testid="stChatMessage"] { background: transparent !important; padding: 1rem !important; }
    div[data-testid="stChatMessageContent"] { background: #FFFFFF; padding: 1.5rem; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='title-container'><h1 class='main-title'>Aether AI</h1><p class='subtitle'>Your Intelligent Professional Assistant</p></div>", unsafe_allow_html=True)

api_key = st.secrets["GEMINI_API_KEY"].strip() if "GEMINI_API_KEY" in st.secrets else None

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("### 💬 Recent Sessions")
    if st.button("✨ New Chat", use_container_width=True): st.session_state.messages = []

# --- INPUT SELECTORS ---
if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "Text"

c1, c2, c3, c4 = st.columns(4)
if c1.button("💬 Text"): st.session_state.mode = "Text"
if c2.button("🖼️ Photo"): st.session_state.mode = "Photo"
if c3.button("📷 Camera"): st.session_state.mode = "Camera"
if c4.button("🎙️ Voice"): st.session_state.mode = "Voice"

file = None
if st.session_state.mode == "Photo": file = st.file_uploader("", type=["jpg", "png"])
elif st.session_state.mode == "Camera": file = st.camera_input("")
elif st.session_state.mode == "Voice": file = st.audio_input("")

# --- CHAT DISPLAY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# --- ENGINE ---
if prompt := st.chat_input("Ask Aether anything..."):
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
            st.error("Check your API key or connection.")
