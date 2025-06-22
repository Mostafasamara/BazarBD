import streamlit as st
import requests
import streamlit.components.v1 as components
import time
import random

# --- Configuration ---
API_KEY = "9ff8e75f1eaa38d836ec1225036b69d9058bf330526b95801dd087c1324b3fa0"  # Replace with your AYD API key
CHATBOT_ID = "6eda15660c4fdb55d8f7bd32e388af7a"  # Replace with your Chatbot ID
SESSION_API = "https://www.askyourdatabase.com/api/chatbot/v2/session"

# --- Streamlit Setup ---
st.set_page_config(page_title="AYD Chatbot (Live)", layout="wide")
st.title("💬 Bazar Chatbot Demo")

# --- Sidebar Refresh Control ---
st.sidebar.title("🔄 Session Controls")
refresh = st.sidebar.button("♻️ Start New Chat Session")

# --- Create New Session Function ---
def create_chat_session():
    unique_email = f"streamlit_user_{int(time.time())}_{random.randint(1, 9999)}@example.com"
    payload = {
        "chatbotid": CHATBOT_ID,
        "name": "Streamlit User",
        "email": unique_email
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(SESSION_API, headers=headers, json=payload)
    if response.status_code == 200:
        session_url = response.json().get("url")
        return session_url
    else:
        st.error(f"❌ Failed to initiate session\nStatus: {response.status_code}\nMessage: {response.text}")
        return None

# --- Run Chatbot ---
if 'chat_session_url' not in st.session_state or refresh:
    st.session_state.chat_session_url = create_chat_session()

if st.session_state.chat_session_url:
    components.html(
        f"""
        <iframe src="{st.session_state.chat_session_url}" width="100%" height="720"
        style="border:none;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.15);"></iframe>
        """,
        height=740
    )
else:
    st.warning("⚠️ Chatbot failed to load. Please check your API key or chatbot configuration.")
