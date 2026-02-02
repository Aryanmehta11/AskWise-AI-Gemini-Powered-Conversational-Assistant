from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.getenv("gemini_api_key"))

# Use stable model
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])


# ---------- Gemini function ----------
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)

    full_text = ""
    placeholder = st.empty()  # for live typing

    for chunk in response:
        if chunk.text:
            full_text += chunk.text
            placeholder.markdown(full_text)

    return full_text


# ---------- Streamlit UI ----------
st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.header("Conversational Q&A with Gemini")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask something:")
submit = st.button("Send")


# ---------- On submit ----------
if submit and user_input:

    st.session_state.chat_history.append(("User", user_input))

    answer = get_gemini_response(user_input)

    st.session_state.chat_history.append(("Gemini", answer))


# ---------- Show history ----------
st.subheader("Chat History")

for role, text in st.session_state.chat_history:
    st.write(f"**{role}:** {text}")
