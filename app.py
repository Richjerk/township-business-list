import streamlit as st
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from transformers import pipeline
from PIL import Image
from io import BytesIO
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os
import datetime

# --- Load environment variables ---
load_dotenv()

# --- Page Configuration ---
st.set_page_config(page_title="Township Business Directory", page_icon="📍", layout="wide")

# --- Secrets & Environment Setup ---
# MongoDB URI
mongo_uri = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI")
if not mongo_uri:
    st.error("MongoDB URI is not configured.")
    st.stop()

# Cloudinary credentials
cloudinary_config = st.secrets.get("cloudinary", {})
cloudinary.config(
    cloud_name=cloudinary_config.get("cloud_name") or os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=cloudinary_config.get("api_key") or os.getenv("CLOUDINARY_API_KEY"),
    api_secret=cloudinary_config.get("api_secret") or os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# --- MongoDB Setup ---
client = MongoClient(mongo_uri)
db = client["township_directory"]
businesses = db["businesses"]
users = db["users"]
ads = db["ads"]

# --- Chatbot Setup ---
@st.cache_resource
def load_chatbot():
    return pipeline("text2text-generation", model="google/flan-t5-small")

chatbot = load_chatbot()

# --- Sidebar ---
st.sidebar.title("💼 Township Directory")
st.sidebar.success("Connected to MongoDB")
st.sidebar.markdown("---")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Add Business",
    "📍 View Businesses",
    "🙋‍♂️ Register as Buyer",
    "💬 Chatbot",
    "⭐ Premium Businesses",
    "📢 Upload Advertisement"
])

# --- Show Ads on Home/Landing Page ---
st.markdown("## 📰 Featured Ads")
sort_option = st.selectbox("Sort Ads by", ["Latest", "Most Clicked"])

if sort_option == "Latest":
    ads_data = list(ads.find().sort("created_at", -1))
else:
    ads_data = list(ads.find().sort("clicks", -1))

if ads_data:
    for ad in ads_data:
        st.subheader(ad.get("title", "Untitled"))
        if ad.get("image_url"):
            st.image(ad["image_url"], use_column_width=True)
        if ad.get("advertiser"):
            st.write(f"🧾 Advertiser: {ad['advertiser']}")
        if ad.get("url"):
            st.markdown(f"[🔗 Visit Site]({ad['url']})", unsafe_allow_html=True)
        st.markdown("---")
else:
    st.info("No ads available yet.")

# --- Example of how to access MongoDB URI ---
# Access the MONGO_URI from secrets or environment variables
mongo_uri = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI")
if mongo_uri:
    st.write(f"MongoDB URI: {mongo_uri}")
else:
    st.warning("MongoDB URI is not set.")



