import streamlit as st
from utils import get_mongo_client

client = get_mongo_client()
buyers_col = client["township_directory"]["buyers"]

def register_buyer():
    st.subheader("Register as a Buyer")
    name = st.text_input("Your Name")
    email = st.text_input("Email")
    phone = st.text_input("WhatsApp Number")

    if st.button("Register"):
        buyers_col.insert_one({
            "name": name,
            "email": email,
            "phone": phone
        })
        st.success(f"{name}, you've been registered!")
