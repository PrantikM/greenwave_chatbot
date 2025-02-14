import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="Greenwave Bot",
    page_icon="\U0001F331",
    layout="centered"
)

# Get API Key from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing in Streamlit secrets. Please check your setup.")
    st.stop()

# Initialize Groq client
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# App title
st.title("Greenwave Bot \U0001F331")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Ask Greenwave Bot")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": "You are a helpful assistant knowledgeable about environment-friendly practices."},
        *st.session_state.chat_history
    ]

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages
            )
            assistant_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            with st.chat_message("assistant"):
                st.markdown(assistant_response)

        except Exception as e:
            st.error(f"Error while fetching response from Groq: {e}")