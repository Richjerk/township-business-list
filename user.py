import streamlit as st
import datetime

def register_buyer():
    st.header("🙋 Register as a Buyer")
    username = st.text_input("Your Name")
    email = st.text_input("Your Email")
    whatsapp = st.text_input("WhatsApp Number")

    if st.button("Register"):
        if username and email and whatsapp:
            users.insert_one({
                "username": username,
                "email": email,
                "whatsapp": whatsapp,
                "registered_at": datetime.datetime.utcnow()
            })
            st.success("🎉 Buyer registered successfully!")
        else:
            st.warning("Please complete all fields.")
