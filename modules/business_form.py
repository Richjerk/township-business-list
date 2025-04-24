import streamlit as st
import datetime
from geopy.geocoders import Nominatim
import cloudinary.uploader
from modules.db import businesses

def add_business_tab():
    st.header("📝 Add a New Business")

    name = st.text_input("Business Name")
    description = st.text_area("Business Description")
    phone = st.text_input("Business Phone")
    address = st.text_input("Business Address")
    image = st.file_uploader("Upload Business Image", type=["jpg", "jpeg", "png"])

    if st.button("Submit Business"):
        if name and description and phone and address:
            geolocator = Nominatim(user_agent="township-directory")
            location = geolocator.geocode(address)
            lat, lon = (location.latitude, location.longitude) if location else (None, None)

            image_url = None
            if image:
                uploaded = cloudinary.uploader.upload(image, folder="businesses")
                image_url = uploaded.get("secure_url")

            businesses.insert_one({
                "name": name,
                "description": description,
                "phone": phone,
                "address": address,
                "location": {"lat": lat, "lon": lon},
                "image_url": image_url,
                "created_at": datetime.datetime.utcnow()
            })

            st.success("✅ Business added successfully!")
        else:
            st.warning("Please fill in all required fields.")
