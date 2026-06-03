import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(
    page_title="Aether AI - Premium Assistant", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- THEMING & ChatGPT/GEMINI LAYOUT CSS SYSTEM ----
st.markdown("""
    <style>
    /* Global App Container constraints */
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        background-color: transparent;
    }
    
    /* Header layout styling */
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 5px;
        text-align: center;
    }
    .main-subtitle {
        font-size: 1.05rem;
        opacity: 0.6;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Premium Chat Message Blocks Overrides */
    div[data-testid="stChatMessage"] {
        padding: 1.5rem 1rem !important;
        border-radius: 0px !important;
        background-color: transparent !important;
        border-bottom: 1px solid rgba(128, 128, 128, 0.08);
    }
    
    /* Modern minimalist tool pills styling */
    div.stButton > button:first-child {
        background-color: rgba(128, 128, 128, 0.05) !important;
        border: 1px solid rgba(128, 128, 128, 0.1) !important;
        border-radius: 20px !important;
        color: inherit !important;
        font-size: 0.85rem !important;
        padding: 0.25rem 0.75rem !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: rgba(128, 128, 128, 0.12) !important;
        border-color: rgba(128, 128, 128, 0.3) !important;
    }
    
    /* Active State Highlights */
    .active-pill {
        box-shadow: 0 0 0 2px #4A90E2 !important;
    }
    
    /* Hide default borders around input elements to preserve premium look */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    api_key = None

# Sidebar Configuration Workspace Area
with st.sidebar:
    st.markdown("### ⚡ SYSTEM SPECIFICATIONS")
    st.caption("Architecture Node V2.5 Live")
    st.divider()
    if st.button("🗑️ Clear Workspace History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_tool = "Text"
        st.rerun()

# Title Area Setup
st.markdown("<h1 class='main-title'>Aether AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Clean Intelligence Cloud Interface</p>", unsafe_allow_html=True)

# Maintain structural user state sessions
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_tool" not in st.session_state:
    st.session_state.active_tool = "Text"

# Render Conversation Window Stream
for message in st.session_state.messages:
    avatar_style = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar_style):
        st.write(message["content"])

# ---- PRE-INPUT SHORTCUT PILLS AREA ----
st.write("")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("💬 Text Only", use_container_width=True):
        st.session_state.active_tool = "Text"
with col2:
    if st.button("🖼️ Photo File", use_container_width=True):
        st.session_state.active_tool = "Photo"
with col3:
    if st.button("📷 Camera", use_container_width=True):
        st.session_state.active_tool = "Camera"
with col4:
    if st.button("🎙️ Voice Dictation", use_container_width=True):
        st.session_state.active_tool = "Voice"

active_media = None
media_mime = ""
fallback_prompt = ""

# Clean Contextual Drop-in Element Triggers
if st.session_state.active_tool != "Text":
    with st.container(border=True):
        if st.session_state.active_tool == "Photo":
            uploaded_file = st.file_uploader("Upload target asset", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
            if uploaded_file:
                active_media = uploaded_file.getvalue()
                media_mime = uploaded_file.type
                fallback_prompt = "Analyze this attached image file."
                st.image(active_media, width=120)
                
        elif st.session_state.active_tool == "Camera":
            camera_file = st.camera_input("Capture instant snap", label_visibility="collapsed")
            if camera_file:
                active_media = camera_file.getvalue()
                media_mime = "image/jpeg"
                fallback_prompt = "Analyze this camera viewport frame snapshot."
                
        elif st.session_state.active_tool == "Voice":
            voice_file = st.audio_input("Record audio stream instruction", label_visibility="collapsed")
            if voice_file:
                active_media = voice_file.getvalue()
                media_mime = "audio/wav"
                fallback_prompt = "Transcribe and analyze this voice message recording."

# Unified Primary Chat Input Engine Component
if user_input := st.chat_input("Message Aether..."):
    final_text_prompt = user_input if user_input.strip() else fallback_prompt
    if not final_text_prompt and active_media:
        final_text_prompt = fallback_prompt

    if not api_key:
        st.error("Authentication Credential Parameters Empty.")
    else:
        st.session_state.messages.append({"role": "user", "content": final_text_prompt})
        with st.chat_message("user", avatar="👤"):
            st.write(final_text_prompt)
            if active_media and "image" in media_mime:
                st.image(active_media, width=280)
            elif active_media and "audio" in media_mime:
                st.audio(active_media)

        with st.chat_message("assistant", avatar="⚡"):
            with st.spinner(""):
                try:
                    client = genai.Client(
                        api_key=api_key,
                        http_options={'headers': {'X-Goog-User-Project': 'gen-lang-client-0546112520'}}
                    )
                    
                    if active_media:
                        contents_payload = [
                            types.Part.from_bytes(data=active_media, mime_type=media_mime),
                            final_text_prompt
                        ]
                    else:
                        contents_payload = final_text_prompt
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents_payload,
                    )
                    
                    assistant_response = response.text if response.text else "System Node Error: Null context output received."
                    
                    # Smooth real-time character typing response simulator
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in assistant_response.split(" "):
                        full_response += chunk + " "
                        time.sleep(0.03)
                        message_placeholder.write(full_response + "▌")
                    message_placeholder.write(full_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    st.error(f"Execution Error Core Halt: {e}")
