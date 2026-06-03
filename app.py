import streamlit as st
from google import genai
from google.genai import types

# Set up page with a custom favicon emoji
st.set_page_config(page_title="Global AI Assistant", page_icon="🌐", layout="centered")

# Custom CSS to polish chat bubbles and spacing
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    div.stButton > button:first-child {
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Fetch the AQ key from Streamlit's backend secrets securely
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    api_key = None

# ---- SIDEBAR INTERFACE ----
with st.sidebar:
    st.markdown("# Control Center ⚙️")
    st.caption("Manage your cloud assistant instance.")
    st.divider()
    
    # System Status Container
    with st.container(border=True):
        st.markdown("**System Health**")
        if api_key:
            st.success("Cloud Core: Connected ✅")
        else:
            st.error("Cloud Core: Disconnected ❌")
            
    st.divider()
    
    # Quick Documentation Dropdown
    with st.expander("ℹ️ About This Assistant"):
        st.write("""
            This is a global-scale AI assistant powered by **Google Gemini 2.5 Flash** and hosted completely on Streamlit Cloud servers. 
            
            It works seamlessly across desktop and mobile devices without requiring any local installations.
        """)
        
    st.divider()
    
    # Clean up conversation button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---- MAIN INTERFACE ----
st.title("Global AI Assistant 🌐")
st.markdown("##### *Your production-ready cloud companion*")
st.divider()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick starter prompt suggestions if chat is empty
if not st.session_state.messages:
    st.markdown("### Try asking one of these:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 Explain Cloud Computing", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Explain Cloud Computing in simple words."})
    with col2:
        if st.button("🚀 Write a Python quicksort code", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Write a clean Python implementation for the quicksort algorithm."})

# Render conversation history with tailored user/assistant icons
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Handle actual text input trigger
if user_input := st.chat_input("Ask a precise question..."):
    if not api_key:
        st.error("System Error: API Key is not configured in Streamlit Secrets!")
    else:
        # Avoid duplicate rendering if suggestion buttons were used
        if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user", avatar="👤"):
                st.write(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Processing queries via Google Cloud..."):
                try:
                    # Initialize client using credentials mapping
                    client = genai.Client(
                        api_key=api_key,
                        http_options={'headers': {'X-Goog-User-Project': 'gen-lang-client-0546112520'}}
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_input,
                    )
                    
                    if response.text:
                        assistant_response = response.text
                    else:
                        assistant_response = "I received an empty response. Please verify your Cloud project parameters."
                    
                    st.write(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"System Authorization Error: {e}")
