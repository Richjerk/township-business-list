# db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MongoDB URI is not configured.")
    client = MongoClient(mongo_uri)
    return client

def get_db():
    client = get_mongo_client()
    return client["township_directory"]

def get_businesses_collection():
    db = get_db()
    return db["businesses"]

def get_users_collection():
    db = get_db()
    return db["users"]

def get_ads_collection():
    db = get_db()
    return db["ads"]
