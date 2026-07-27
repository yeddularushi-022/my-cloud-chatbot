import streamlit as st
from google import genai
from google.genai import types
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Aether AI Pro", page_icon="⚡", layout="centered")

# --- MODERN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; font-family: 'Inter', sans-serif; }
    .title-container { text-align: center; margin-top: 1rem; margin-bottom: 1.5rem; }
    .main-title { font-size: 2.2rem; font-weight: 700; color: #111; }
    .subtitle { color: #666; font-size: 1rem; }
    div.stButton > button {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    div.stButton > button:hover { border-color: #3B82F6 !important; color: #3B82F6 !important; }
    div[data-testid="stChatMessage"] { background: transparent !important; padding: 0.5rem !important; }
    div[data-testid="stChatMessageContent"] { background: #FFFFFF; padding: 1.2rem; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-container'><h1 class='main-title'>Aether AI</h1><p class='subtitle'>Your Advanced Intelligent Assistant</p></div>", unsafe_allow_html=True)

# Fetch API Key from Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"].strip() if "GEMINI_API_KEY" in st.secrets else None

# Initialize GenAI Client
client = genai.Client(api_key=api_key) if api_key else None

# --- STATE INITIALIZATION ---
if "messages" not in st.session_state: st.session_state.messages = []
if "edit_index" not in st.session_state: st.session_state.edit_index = None

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    selected_model = st.selectbox("Choose Model", ["gemini-2.5-flash", "gemini-2.5-pro"], index=0)
    temperature = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.3, 0.1)
    
    st.markdown("---")
    st.markdown("### 💬 Session Actions")
    if st.button("✨ New Chat", use_container_width=True): 
        st.session_state.messages = []
        st.session_state.edit_index = None
        st.rerun()
        
    if st.session_state.messages:
        chat_export = "\n".join([f"{msg['role'].upper()}: {msg['content']}" if isinstance(msg['content'], str) else f"{msg['role'].upper()}: [Image Generated]" for msg in st.session_state.messages])
        st.download_button("📥 Export Chat", chat_export, file_name="aether_chat_history.txt", mime="text/plain", use_container_width=True)

    st.markdown("---")
    st.caption(f"Total Messages: {len(st.session_state.messages)}")

# --- DISPLAY CHAT & IMAGES ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], Image.Image):
            st.image(msg["content"], caption="Generated Image", use_column_width=True)
        else:
            st.write(msg["content"])
            
        if msg["role"] == "user":
            if st.button("✏️ Edit", key=f"edit_btn_{idx}"):
                st.session_state.edit_index = idx
                st.rerun()

# --- HANDLE PROMPT OR IMAGE GENERATION ---
if st.session_state.edit_index is not None:
    idx = st.session_state.edit_index
    old_content = st.session_state.messages[idx]["content"]
    
    st.info(f"Editing prompt...")
    new_prompt = st.text_input("Modify message:", value=str(old_content), key=f"edit_input_{idx}")
    
    col1, col2 = st.columns(2)
    if col1.button("Save & Resend"):
        st.session_state.messages = st.session_state.messages[:idx]
        st.session_state.messages.append({"role": "user", "content": new_prompt})
        
        try:
            if not client:
                raise Exception("Client not initialized")
                
            if any(keyword in new_prompt.lower() for keyword in ["generate image", "draw", "create an image", "picture of"]):
                result = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=new_prompt,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )
                for generated_image in result.generated_images:
                    image = Image.open(BytesIO(generated_image.image.image_bytes))
                    st.session_state.messages.append({"role": "assistant", "content": image})
                    break
                else:
                    st.session_state.messages.append({"role": "assistant", "content": "Could not generate image."})
            else:
                response = client.models.generate_content(
                    model=selected_model,
                    contents=new_prompt,
                    config=types.GenerateContentConfig(temperature=temperature)
                )
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.session_state.messages.append({"role": "assistant", "content": "Error: Check your API key or connection."})
            
        st.session_state.edit_index = None
        st.rerun()
        
    if col2.button("Cancel"):
        st.session_state.edit_index = None
        st.rerun()

else:
    if prompt := st.chat_input("Ask Aether anything or ask to generate an image..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            if not client:
                raise Exception("Client not initialized")
                
            if any(keyword in prompt.lower() for keyword in ["generate image", "draw", "create an image", "picture of"]):
                result = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=prompt,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )
                for generated_image in result.generated_images:
                    image = Image.open(BytesIO(generated_image.image.image_bytes))
                    reply = image
                    break
                else:
                    reply = "Could not generate image."
            else:
                response = client.models.generate_content(
                    model=selected_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=temperature)
                )
                reply = response.text
        except Exception:
            reply = "Check your API key or connection."
            
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
