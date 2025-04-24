# chat.py
from huggingface_hub import InferenceClient
from db import get_all_businesses

client = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")  # or your model

def load_chatbot():
    return client

def ask_chatbot_form():
    user_question = st.text_input("Ask about township businesses:")
    if user_question:
        businesses = get_all_businesses()
        context = "\n".join([f"{b['business_name']}: {b['business_description']}" for b in businesses])
        prompt = f"{context}\n\nQ: {user_question}\nA:"

        response = client.text_generation(prompt, max_new_tokens=200)
        st.markdown("### 💬 Response:")
        st.write(response)
