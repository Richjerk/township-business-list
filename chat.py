import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_chatbot():
    return pipeline("text2text-generation", model="google/flan-t5-small")

def ask_chatbot_form():
    st.header("💬 Ask Our Business Chatbot")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat input form
    user_query = st.text_input("💡 What do you need help with?", key="chat_input")

    col1, col2 = st.columns([1, 1])
    with col1:
        ask_button = st.button("🚀 Ask")
    with col2:
        clear_button = st.button("🧹 Clear History")

    if clear_button:
        st.session_state.chat_history = []
        st.experimental_rerun()

    if ask_button and user_query:
        chatbot = load_chatbot()
        with st.spinner("🤖 Thinking..."):
            response = chatbot(user_query, max_new_tokens=100, do_sample=False)[0]["generated_text"]

        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Bot", response))

    # Display styled chat history
    if st.session_state.chat_history:
        st.subheader("📜 Chat History")
        
        for speaker, message in st.session_state.chat_history:
            if speaker == "You":
                # User messages styled as WhatsApp bubbles aligned to the right
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <div style="background-color: #dcf8c6; padding: 10px 20px; border-radius: 20px; max-width: 80%; word-wrap: break-word;">
                        <strong style="color: #075e54;">You:</strong><br>{message}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Bot messages styled as WhatsApp bubbles aligned to the left
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                    <div style="background-color: #f1f0f0; padding: 10px 20px; border-radius: 20px; max-width: 80%; word-wrap: break-word;">
                        <strong style="color: #128C7E;">Bot:</strong><br>{message}
                    </div>
                </div>
                """, unsafe_allow_html=True)

