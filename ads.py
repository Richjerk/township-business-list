# ads.py
import streamlit as st
from db import get_ads_collection
from utils import upload_image_to_cloudinary, get_current_utc_time

def upload_ad(title, advertiser, url, image_file):
    ads = get_ads_collection()

    image_url = None
    if image_file:
        image_url = upload_image_to_cloudinary(image_file, "ads")

    ads.insert_one({
        "title": title,
        "advertiser": advertiser,
        "url": url,
        "image_url": image_url,
        "clicks": 0,
        "created_at": get_current_utc_time()
    })

def show_ads():
    ads = get_ads_collection()
    sort_option = st.selectbox("Sort by", ["Latest", "Most Clicks"])
    sort_field = "created_at" if sort_option == "Latest" else "clicks"
    ads_data = list(ads.find().sort(sort_field, -1))
    return ads_data


