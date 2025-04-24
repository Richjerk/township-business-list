from transformers import pipeline

@st.cache_resource
def load_chatbot():
    return pipeline("text2text-generation", model="google/flan-t5-small")

def ask_chatbot_form():
    st.header("💬 Ask Our Business Chatbot")
    user_query = st.text_input("What do you need help with?")
    if st.button("Ask") and user_query:
        with st.spinner("Thinking..."):
            response = chatbot(user_query, max_new_tokens=100, do_sample=False)[0]["generated_text"]
        st.markdown(f"**🤖 Chatbot:** {response}")
