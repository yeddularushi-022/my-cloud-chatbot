import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Global AI Assistant", layout="centered")

# Fetch the AQ key from Streamlit's backend secrets securely
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    api_key = None

with st.sidebar:
    st.title("Settings ⚙️")
    st.write("Configure your global cloud assistant.")
    st.divider()
    
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
                    # Initialize client using the new SDK standard for AQ keys
                    client = genai.Client(api_key=api_key)
                    
                    # Generate content via the production stable model
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_input,
                    )
                    
                    if response.text:
                        assistant_response = response.text
                    else:
                        assistant_response = "I received an empty response. Please verify your Cloud project access."
                    
                    st.write(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"System Authorization Error: {e}")
