# chat.py

import os
import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from db import get_all_businesses

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("Hugging Face API key not found. Please set HF_API_KEY in your .env file.")

client = InferenceClient(api_key=HF_API_KEY)

def load_chatbot():
    st.success("🤖 Township Business Assistant loaded successfully!")

def get_context_from_db():
    try:
        businesses = get_all_businesses()
        return "\n".join([f"{b['business_name']}: {b['business_description']}" for b in businesses])
    except Exception as e:
        st.error("Failed to load business context from the database.")
        return "Local businesses include a variety of services and shops."

def ask_chatbot_form():
    st.subheader("💬 Chat with the Township Business Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask about township businesses:")

    if user_question:
        with st.spinner("Thinking..."):
            context = get_context_from_db()
            prompt = f"{context}\n\nQ: {user_question}\nA:"

            try:
                stream = client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=512,
                    stream=True,
                )

                full_response = ""
                response_container = st.empty()

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_container.markdown(full_response)

                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": full_response
                })

            except Exception as e:
                st.error(f"Error talking to chatbot: {e}")

    with st.container():
        st.markdown(
            """
            <style>
            .chat-box {
                height: 300px;
                overflow-y: auto;
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                padding: 1em;
                border-radius: 0.5em;
                font-family: monospace;
            }
            .user-msg {
                color: #444;
                font-weight: bold;
            }
            .bot-msg {
                margin-bottom: 1em;
                color: #222;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for entry in reversed(st.session_state.chat_history):
            st.markdown(f'<div class="user-msg">You: {entry["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-msg">🤖: {entry["answer"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
