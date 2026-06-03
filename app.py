import streamlit as st
from openai import OpenAI

# Set webpage browser title and layout
st.set_page_config(page_title="Global AI Assistant", layout="centered")

# --- SIDEBAR INTERFACE ---
with st.sidebar:
    st.title("Settings ⚙️")
    st.write("Configure your global cloud assistant.")
    st.divider()
    
    # Text input for users to provide their own OpenAI API Key securely
    api_key_input = st.text_input(
        "Enter OpenAI API Key:", 
        type="password",
        placeholder="sk-...",
        help="Paste your secret key from the OpenAI developer dashboard."
    )
    
    st.divider()
    if st.button("Clear Conversation 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("Global AI Assistant 🌐")
st.caption("Hosted on the Cloud | Powered by OpenAI GPT-4o-mini")
st.divider()

# Advanced system prompt for premium, precise responses
EXPERT_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are an expert, high-precision AI assistant operating exactly like premium versions of Gemini and ChatGPT. "
        "Adhere to these strict formatting and behavioral rules:\n\n"
        "1. FACTUAL ACCURACY: Do not hallucinate. If you do not know an answer or lack real-time data, state it directly.\n"
        "2. SCANNABILITY & CLARITY: Avoid dense blocks of text. Use clean Markdown headings (##, ###), bolding, and bullet points to ensure clarity at a glance.\n"
        "3. TONALITY: Maintain an authentic, direct, and professional tone. Avoid unnecessary conversational fluff."
    )
}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# User input box
if user_input := st.chat_input("Ask a precise question..."):
    if not api_key_input:
        st.error("Please enter your OpenAI API Key in the sidebar to begin chatting!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Build message payload
        formatted_messages = [EXPERT_SYSTEM_PROMPT] + st.session_state.messages

        # Generate cloud-based assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing via Cloud..."):
                try:
                    # Initialize the OpenAI cloud client with the provided key
                    client = OpenAI(api_key=api_key_input)
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",  # Highly efficient, fast, and cost-effective cloud model
                        messages=formatted_messages,
                        temperature=0.3
                    )
                    assistant_response = response.choices[0].message.content
                    st.write(assistant_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"API Error: Please check your secret key or billing configuration. Details: {e}")