import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(
    page_title="Aether AI - Global Cloud Assistant", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        max-width: 850px;
        margin: 0 auto;
    }
    .main-title {
        font-size: 2.6rem !important;
        font-weight: 800;
        background: linear-gradient(45deg, #FF4B4B, #4A90E2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    div.stButton > button:first-child {
        border-radius: 12px;
        border: 1px solid rgba(151, 151, 151, 0.2);
        transition: all 0.3s ease;
        font-weight: 500;
    }
    div.stButton > button:first-child:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
        box-shadow: 0px 4px 12px rgba(255, 75, 75, 0.1);
    }
    .stChatInput {
        padding-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    api_key = None

with st.sidebar:
    st.markdown("### ⚡ AETHER CLOUD CORE")
    st.caption("Production Instance: Active Layer V2.5")
    st.divider()
    
    with st.container(border=True):
        st.markdown("**🌐 SERVER NETWORK INFRASTRUCTURE**")
        if api_key:
            st.markdown("<span style='color:#2ecc71; font-weight:bold;'>● CLOUD LINK ACTIVE</span>", unsafe_allow_html=True)
            st.caption("Securely bound via Cloud Node: `gen-lang-client-0546112520`")
        else:
            st.markdown("<span style='color:#e74c3c; font-weight:bold;'>● OFFLINE DECOUPLED</span>", unsafe_allow_html=True)
            st.error("Missing Authentication Configuration Box.")
            
    st.divider()
    if st.button("🗑️ Clear Chat Terminal Workspace", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---- MAIN INTERFACE AREA ----
st.markdown("<h1 class='main-title'>Aether AI Assistant ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.1rem; opacity:0.8; margin-top:0px;'>Next-Gen Intelligent Cloud Command Interface</p>", unsafe_allow_html=True)
st.divider()

# MULTIMEDIA CAPTURE OPTIONS (Separated Choosable Tabs)
st.markdown("### 🛠️ Choose Input Type")
tab_text, tab_photo, tab_camera, tab_voice = st.tabs([
    "💬 Text Prompt", 
    "🖼️ Upload Photo", 
    "📷 Take Picture", 
    "🎙️ Record Voice"
])

active_media = None
media_mime = ""
fallback_prompt = ""

with tab_text:
    st.caption("Type your message directly into the chat bar at the bottom.")

with tab_photo:
    uploaded_file = st.file_uploader("Choose a photo from gallery", type=["png", "jpg", "jpeg"], key="photo_input")
    if uploaded_file:
        active_media = uploaded_file.getvalue()
        media_mime = uploaded_file.type
        fallback_prompt = "Analyze this uploaded photo asset."
        st.image(active_media, width=250, caption="Photo staged")

with tab_camera:
    camera_file = st.camera_input("Capture instant camera snapshot", key="camera_input")
    if camera_file:
        active_media = camera_file.getvalue()
        media_mime = "image/jpeg"
        fallback_prompt = "Analyze this captured camera picture snapshot."

with tab_voice:
    voice_file = st.audio_input("Record voice or speech instructions", key="voice_input")
    if voice_file:
        active_media = voice_file.getvalue()
        media_mime = "audio/wav"
        fallback_prompt = "Analyze and process this recorded audio voice message clip."

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar_style = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar_style):
        st.write(message["content"])

# Bottom Input Chat Execution Bar
if user_input := st.chat_input("Ask a precise question or provide instructions..."):
    
    # Use fallback prompt string if user sends media asset without adding any text
    final_text_prompt = user_input if user_input.strip() else fallback_prompt
    if not final_text_prompt and active_media:
        final_text_prompt = fallback_prompt

    if not api_key:
        st.error("Infrastructure Authorization Error: Backend target key string layer is undefined.")
    else:
        st.session_state.messages.append({"role": "user", "content": final_text_prompt})
        with st.chat_message("user", avatar="👤"):
            st.write(final_text_prompt)
            if active_media and "image" in media_mime:
                st.image(active_media, width=300)
            elif active_media and "audio" in media_mime:
                st.audio(active_media)

        with st.chat_message("assistant", avatar="⚡"):
            with st.spinner("Processing cloud request pipelines..."):
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
                    
                    if response.text:
                        assistant_response = response.text
                    else:
                        assistant_response = "Cloud warning: Server node returned an empty execution payload."
                    
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in assistant_response.split(" "):
                        full_response += chunk + " "
                        time.sleep(0.04)
                        message_placeholder.write(full_response + "▌")
                    message_placeholder.write(full_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    st.error(f"Cloud Infrastructure Execution Halt: {e}")
