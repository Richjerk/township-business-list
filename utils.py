import cloudinary
import streamlit as st
from pymongo import MongoClient

# Configure Cloudinary settings
def configure_cloudinary():
    cloudinary.config(
        cloud_name=st.secrets["cloudinary"]["cloud_name"],
        api_key=st.secrets["cloudinary"]["api_key"],
        api_secret=st.secrets["cloudinary"]["api_secret"]
    )

# Get MongoDB client using Streamlit secrets
def get_mongo_client():
    mongo_uri = st.secrets.get("MONGO_URI")  # Fetch MongoDB URI from Streamlit secrets
    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in Streamlit secrets!")
    
    client = MongoClient(mongo_uri)  # Return MongoDB client instance
    return client

