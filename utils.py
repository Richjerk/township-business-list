import cloudinary
import streamlit as st
from pymongo import MongoClient

def configure_cloudinary():
    cloudinary.config(
        cloud_name=st.secrets["cloudinary"]["cloud_name"],
        api_key=st.secrets["cloudinary"]["api_key"],
        api_secret=st.secrets["cloudinary"]["api_secret"]
    )

def get_mongo_client():
    uri = st.secrets.get("MONGO_URI")
    return MongoClient(uri)

