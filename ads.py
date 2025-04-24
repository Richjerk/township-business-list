import streamlit as st
from utils import get_mongo_client

client = get_mongo_client()
ads_col = client["township_directory"]["ads"]

def show_ads():
    return list(ads_col.find())

def upload_ad_form():
    st.subheader("Upload Advertisement")
    title = st.text_input("Ad Title")
    image_url = st.text_input("Image URL")
    if st.button("Upload Ad"):
        ads_col.insert_one({
            "title": title,
            "image_url": image_url
        })
        st.success(f"Ad '{title}' uploaded.")
