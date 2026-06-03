import streamlit as st
from google import genai
from google.genai import types
import time

# 1. Premium App Configurations & Favicon
st.set_page_config(
    page_title="Nexus AI - Global Cloud Assistant", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Advanced Premium CSS Injector (Gives that polished iOS/SaaS App layout feel)
st.markdown("""
    <style>
    /* Main body background spacing */
    .stApp {
        max-width: 850px;
        margin: 0 auto;
    }
    /* Style the main app title headers */
    .main-title {
        font-size: 2.6rem !important;
        font-weight: 800;
        background: linear-gradient(45deg, #FF4B4B, #4A90E2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    /* Rounded premium buttons styling */
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
    /* Chat inputs positioning alignment */
    .stChatInput {
        padding-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Secure backend setup for credentials
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    api_key = None

# ---- PREMIUM SIDEBAR CONTROL HUB ----
with st.sidebar:
    st.markdown("### ⚡ NEXUS CLOUD CORE")
    st.caption("Production Instance: Active Layer V2.5")
    st.divider()
    
    # Visual Connection Card Status Panel
    with st.container(border=True):
        st.markdown("**🌐 SERVER NETWORK INFRASTRUCTURE**")
        if api_key:
            st.markdown("<span style='color:#2ecc71; font-weight:bold;'>● CLOUD LINK ACTIVE</span>", unsafe_allow_html=True)
            st.caption("Securely bound via Cloud Node: `gen-lang-client-0546112520`")
        else:
            st.markdown("<span style='color:#e74c3c; font-weight:bold;'>● OFFLINE DECOUPLED</span>", unsafe_allow_html=True)
            st.error("Missing Authentication Configuration Box.")
            
    st.divider()
    
    # MULTIMEDIA CAPABILITY HUB (Image Uploader Component)
    st.markdown("### 📸 VISION CAPABILITY")
    uploaded_file = st.file_uploader(
        "Upload an image to analyze with the AI:", 
        type=["png", "jpg", "jpeg"],
        help="Upload a document screenshot, math equation, code error snapshot, or general image to chat directly with it."
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="🎯 Staged Image Ready for Processing", use_container_width=True)
        if st.button("❌ Clear Staged Image", use_container_width=True):
            st.rerun()

    st.divider()
    
    # Workspace Manager Box Dropdown
    with st.expander("🛠️ Workspace System Details"):
        st.write("""
        * **Engine Standard:** Google Gemini 2.5 Flash
        * **Interface Frame:** Streamlit Web Engine Pro
        * **Device Target:** Responsive Screen Adaptive (Mobile Sync Enabled)
        """)
        
    st.divider()
    # Action Button to wipe chat history log clean instantly
    if st.button("🗑️ Clear Chat Terminal Workspace", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---- MAIN PREMIUM APP INTERFACE AREA ----
st.markdown("<h1 class='main-title'>Nexus AI Assistant ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.1rem; opacity:0.8; margin-top:0px;'>Next-Gen Intelligent Cloud Command Interface</p>", unsafe_allow_html=True)
st.divider()

# Session tracking initialization for history variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# If app is completely fresh and empty, generate attractive UI suggestion buttons
if not st.session_state.messages:
    st.markdown("### 💡 Recommended Starter Prompts")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Brainstorm Project Concepts", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Give me 5 unique project concepts integrating Python web services and Machine Learning."})
            st.rerun()
        if st.button("✍️ Refine Document Structure", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Provide a clean, standard executive template design structure for a professional technical project report."})
            st.rerun()
    with col2:
        if st.button("💻 Debug Complex Script Errors", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "How do you systematically isolate and fix memory leak execution compiler bugs in multi-threaded application environments?"})
            st.rerun()
        if st.button("🌍 Translate Global Dialogues", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Create a neat conversational table tracking helpful expressions split between English, Telugu, and German translations."})
            st.rerun()

# Render past history contents with custom avatar layout designs
for message in st.session_state.messages:
    avatar_style = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar_style):
        st.write(message["content"])

# Main Input Capture Field Handler
if user_input := st.chat_input("Enter prompts, scripts, or instructions..."):
    if not api_key:
        st.error("Infrastructure Authorization Error: Backend target key string layer is undefined.")
    else:
        # Save prompt log history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)

        # Trigger live execution interface
        with st.chat_message("assistant", avatar="⚡"):
            with st.spinner("Processing cloud request pipelines..."):
                try:
                    # Construct active pipeline connections
                    client = genai.Client(
                        api_key=api_key,
                        http_options={'headers': {'X-Goog-User-Project': 'gen-lang-client-0546112520'}}
                    )
                    
                    # Package content payloads depending on whether media assets are attached
                    if uploaded_file:
                        # Convert user's uploaded stream into bytes dictionary format for the model API 
                        image_data = uploaded_file.getvalue()
                        contents_payload = [
                            types.Part.from_bytes(data=image_data, mime_type=uploaded_file.type),
                            user_input
                        ]
                    else:
                        contents_payload = user_input
                    
                    # Fetch inference data directly from generation cloud modules
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents_payload,
                    )
                    
                    if response.text:
                        assistant_response = response.text
                    else:
                        assistant_response = "Cloud warning: Server node returned an empty execution payload."
                    
                    # Premium Premium Feature: Premium Real-time Matrix Ticker/Typing simulation feedback loop
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in assistant_response.split(" "):
                        full_response += chunk + " "
                        time.sleep(0.04) # Simulates crisp smooth typewriter streaming action 
                        message_placeholder.write(full_response + "▌")
                    message_placeholder.write(full_response)
                    
                    # Record tracking information strings safely
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    st.error(f"Cloud Infrastructure Execution Halt: {e}")
