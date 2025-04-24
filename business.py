import streamlit as st
from utils import get_mongo_client

client = get_mongo_client()
db = client["township_directory"]
businesses_col = db["businesses"]

def add_business_form():
    st.subheader("Add a New Business")
    name = st.text_input("Business Name")
    description = st.text_area("Description")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")
    image_url = st.text_input("Business Logo URL")

    if st.button("Submit Business"):
        businesses_col.insert_one({
            "name": name,
            "description": description,
            "phone": phone,
            "address": address,
            "image_url": image_url,
            "premium": False,
        })
        st.success(f"{name} added successfully!")

def view_businesses_form():
    st.subheader("All Businesses")
    for b in businesses_col.find():
        st.write(b)

def view_premium_businesses():
    st.subheader("⭐ Premium Listings")
    for b in businesses_col.find({"premium": True}):
        st.write(f"{b['name']} - {b['description']}")

def get_businesses():
    return list(businesses_col.find())
