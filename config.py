import os
from pymongo import MongoClient
from dotenv import load_dotenv
import cloudinary

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MongoDB URI is not configured.")

client = MongoClient(mongo_uri)
db = client["township_directory"]
businesses = db["businesses"]
users = db["users"]
ads = db["ads"]

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
