import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import streamlit as st

# ✅ Load environment variables
load_dotenv()

# ⛅ Configure Cloudinary
def configure_cloudinary():
    try:
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True
        )
    except Exception as e:
        print("❌ Cloudinary configuration failed:", e)

# 📤 Upload image to Cloudinary
def upload_image_to_cloudinary(file, folder="ads"):
    try:
        result = cloudinary.uploader.upload(file, folder=folder)
        return result.get("secure_url")
    except Exception as e:
        print("❌ Cloudinary upload failed:", e)
        return None

# 🧾 Render a business card with WhatsApp button
def render_business_card(business: dict):
    phone_number = business.get("business_phone", "")
    whatsapp_link = f"https://wa.me/27{phone_number}" if phone_number else "#"
    logo_url = business.get("logo_url", "")

    st.markdown(f"""
        <div style="
            display: inline-block;
            width: 250px;
            margin: 10px;
            padding: 15px;
            text-align: center;
            border-radius: 16px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            
            <img src="{logo_url}" alt="Logo" style="border-radius: 50%; height: 100px; width: 100px; object-fit: cover;" />
            
            <h4 style="margin-top: 10px;">{business.get('business_name', 'Business Name')}</h4>
            <p style="font-size: 14px;">{business.get('business_description', 'Description')}</p>
            <p style="font-size: 13px; color: gray;">📍 {business.get('business_address', '')}</p>
            <p style="font-size: 13px;">📞 {phone_number}</p>

            <a href="{whatsapp_link}" target="_blank">
                <button style="margin-top:10px; background-color:#25D366; color:white; border:none; padding:8px 16px; border-radius:8px; cursor:pointer;">
                    📲 Chat on WhatsApp
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
