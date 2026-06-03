import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Global AI Assistant", layout="centered")

# 1. Fetch the API key securely from Streamlit's backend secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = None

with st.sidebar:
    st.title("Settings ⚙️")
    st.write("Configure your global cloud assistant.")
    st.divider()
    
    # Simple status indicator for your users
    if api_key:
        st.success("Cloud Connection: Active ✅")
    else:
        st.error("Cloud Connection: Missing Key ❌")
    
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
    if not api_key:
        st.error("System Error: API Key is not configured in Streamlit Secrets!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing via Cloud..."):
                try:
                    # Configure using the hidden backend key
                    genai.configure(api_key=api_key.strip())
                    
                    # Initialize production model
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Generate response
                    response = model.generate_content(user_input)
                    
                    if response.text:
                        assistant_response = response.text
                    else:
                        assistant_response = "I received an empty response. Please verify the key parameters."
                    
                    st.write(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"API Error: {e}")
