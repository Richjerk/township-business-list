import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# ✅ Load environment variables
load_dotenv()

# ⛅ Configure Cloudinary
def configure_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

# 📤 Upload image to Cloudinary
def upload_image_to_cloudinary(file, folder="ads"):
    try:
        result = cloudinary.uploader.upload(file, folder=folder)
        return result.get("secure_url")
    except Exception as e:
        print("❌ Cloudinary upload failed:", e)
        return None
