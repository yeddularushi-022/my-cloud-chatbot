import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Global AI Assistant", layout="centered")

with st.sidebar:
    st.title("Settings ⚙️")
    st.write("Configure your global cloud assistant.")
    st.divider()
    
    api_key_input = st.text_input(
        "Enter Gemini API Key:", 
        type="password",
        placeholder="AQ. or AIzaSy...",
        help="Paste your free key from Google AI Studio."
    )
    
    st.divider()
    if st.button("Clear Conversation 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("Global AI Assistant 🌐")
st.caption("Hosted on the Cloud | Powered by Google Gemini")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Ask a precise question..."):
    if not api_key_input:
        st.error("Please enter your Gemini API Key in the sidebar to begin chatting!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing via Cloud..."):
                try:
                    # Strip any accidental whitespace
                    clean_key = api_key_input.strip()
                    
                    # Direct configuration call
                    genai.configure(api_key=clean_key)
                    
                    # Initialize model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Generate response
                    response = model.generate_content(user_input)
                    
                    if response.text:
                        assistant_response = response.text
                    else:
                        assistant_response = "I received an empty response. Please verify the key has active permissions."
                    
                    st.write(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"API Error: {e}")
