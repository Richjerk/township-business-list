import datetime
import streamlit as st
from geopy.geocoders import Nominatim
import cloudinary.uploader
from cloudinary import config

def add_business_form():
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

def view_businesses_form():
    st.header("📍 View Registered Businesses")
    all_businesses = list(businesses.find().sort("created_at", -1))

    if all_businesses:
        for biz in all_businesses:
            st.subheader(biz["name"])
            st.write(biz["description"])
            st.write(f"📞 {biz['phone']} | 📍 {biz['address']}")
            if biz.get("image_url"):
                st.image(biz["image_url"], width=400)
            st.markdown("---")
    else:
        st.info("No businesses listed yet.")

def view_premium_businesses():
    st.header("⭐ Premium Businesses")
    premium = list(businesses.find({"premium": True}).sort("created_at", -1))

    if premium:
        for p in premium:
            st.subheader(f"🌟 {p['name']}")
            st.write(p["description"])
            st.write(f"📞 {p['phone']} | 📍 {p['address']}")
            if p.get("image_url"):
                st.image(p["image_url"], width=400)
            st.markdown("---")
    else:
        st.info("No premium businesses yet.")
