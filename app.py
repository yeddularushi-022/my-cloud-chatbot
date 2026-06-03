import streamlit as st
from google import genai
from google.genai import types

# Set page to wide mode for a professional look
st.set_page_config(page_title="Aether AI", page_icon="⚡", layout="centered")

# --- PROFESSIONAL LIGHT THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .main-title { color: #202124; text-align: center; font-size: 2.5rem; margin-top: 1rem; }
    
    /* Style Chat Bubbles to be professional/colorful */
    div[data-testid="stChatMessage"] { background-color: #F7F7F8 !important; border-radius: 10px; padding: 15px; margin: 10px 0; }
    
    /* Modern Action Buttons */
    div.stButton > button { 
        background-color: #FFFFFF !important; 
        border: 1px solid #D1D5DB !important; 
        color: #374151 !important;
        border-radius: 8px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #F3F4F6 !important; border-color: #9CA3AF !important; }
    
    /* Fix Chat Input at bottom */
    .stChatInput { background-color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

api_key = st.secrets["GEMINI_API_KEY"].strip() if "GEMINI_API_KEY" in st.secrets else None

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("### ⚡ Aether History")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
    st.divider()

# --- MAIN UI ---
st.markdown("<h1 class='main-title'>Aether AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "input_mode" not in st.session_state: st.session_state.input_mode = "Text"

# Input Selector Pills
cols = st.columns(4)
if cols[0].button("💬 Text"): st.session_state.input_mode = "Text"
if cols[1].button("🖼️ Photo"): st.session_state.input_mode = "Photo"
if cols[2].button("📷 Cam"): st.session_state.input_mode = "Camera"
if cols[3].button("🎙️ Voice"): st.session_state.input_mode = "Voice"

# File Handling
file = None
if st.session_state.input_mode == "Photo": file = st.file_uploader("Upload Image", type=["jpg", "png"])
elif st.session_state.input_mode == "Camera": file = st.camera_input("Capture")
elif st.session_state.input_mode == "Voice": file = st.audio_input("Record Voice")

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# --- CHAT ENGINE ---
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
            st.error("Please ensure your API key is correctly set in the secrets.")
