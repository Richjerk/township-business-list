import streamlit as st
from utils import get_mongo_client

# Initialize MongoDB client and access the ads collection
client = get_mongo_client()
ads_col = client["township_directory"]["ads"]

def show_ads():
    """Fetch and display ads from MongoDB"""
    ads_data = list(ads_col.find())
    return ads_data

def upload_ad_form():
    """Form for uploading advertisements"""
    st.subheader("Upload Advertisement")
    title = st.text_input("Ad Title")
    image_url = st.text_input("Image URL")

    if st.button("Upload Ad"):
        if title and image_url:
            # Insert ad data into MongoDB collection
            ads_col.insert_one({
                "title": title,
                "image_url": image_url
            })
            st.success(f"Ad '{title}' uploaded successfully!")
        else:
            st.error("Please provide both title and image URL.")
