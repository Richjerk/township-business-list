import os
from dotenv import load_dotenv
import streamlit as st
import cloudinary

load_dotenv()

st.set_option("server.headless", True)
st.set_option("server.fileWatcherType", "none")
st.set_page_config(page_title="Township Business Directory", page_icon="📍", layout="wide")

mongo_uri = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI")
if not mongo_uri:
    st.error("MongoDB URI is not configured.")
    st.stop()

cloudinary_config = st.secrets.get("cloudinary", {})
cloudinary.config(
    cloud_name=cloudinary_config.get("cloud_name") or os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=cloudinary_config.get("api_key") or os.getenv("CLOUDINARY_API_KEY"),
    api_secret=cloudinary_config.get("api_secret") or os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def get_mongo_uri():
    return mongo_uri
