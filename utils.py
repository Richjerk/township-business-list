import cloudinary
from cloudinary import config
from dotenv import load_dotenv
import os

def configure_cloudinary():
    load_dotenv()

    cloudinary_config = {
        "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME"),
        "api_key": os.getenv("CLOUDINARY_API_KEY"),
        "api_secret": os.getenv("CLOUDINARY_API_SECRET")
    }
    cloudinary.config(
        cloud_name=cloudinary_config["cloud_name"],
        api_key=cloudinary_config["api_key"],
        api_secret=cloudinary_config["api_secret"],
        secure=True
    )
