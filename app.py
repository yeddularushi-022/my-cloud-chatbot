import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Global AI Assistant", layout="centered")

with st.sidebar:
    st.title("Settings ⚙️")
    st.write("Configure your global cloud assistant.")
    st.divider()
    
    # Text input for users to provide their Gemini Key securely
    api_key_input = st.text_input(
        "Enter Gemini API Key:", 
        type="password",
        placeholder="AIzaSy...",
        help="Paste your free key from Google AI Studio."
    )
    
    st.divider()
    if st.button("Clear Conversation 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("My AI Assistant 🌐")
st.caption("Hosted on the Cloud | Powered by Google Gemini 1.5 Flash (Free Tier)")
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
                    # Configure Gemini with the provided key
                    genai.configure(api_key=api_key_input)
                    
                    # Set up the high-precision system instructions
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction=(
                            "You are an expert, high-precision AI assistant operating exactly like premium versions of Gemini and ChatGPT. "
                            "Adhere to these strict rules:\n"
                            "1. FACTUAL ACCURACY: Do not hallucinate. If you do not know an answer, state it directly.\n"
                            "2. SCANNABILITY & CLARITY: Avoid dense blocks of text. Use clean Markdown headings, bolding, and bullet points.\n"
                            "3. TONALITY: Maintain an authentic, direct, and professional tone."
                        )
                    )
                    
                    # Format history properly for the Gemini SDK
                    chat_history = []
                    for msg in st.session_state.messages[:-1]:
                        role = "user" if msg["role"] == "user" else "model"
                        chat_history.append({"role": role, "parts": [msg["content"]]})
                    
                    chat = model.start_chat(history=chat_history)
                    response = chat.send_message(user_input)
                    
                    assistant_response = response.text
                    st.write(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"API Error: Please check your key configuration. Details: {e}")
