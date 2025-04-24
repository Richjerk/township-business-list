# db.py
import os
from pymongo import MongoClient
import streamlit as st

def get_db():
    mongo_uri = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client["township_directory"]  # Replace with your actual DB name

def insert_business(data):
    db = get_db()
    return db.businesses.insert_one(data)

def update_business(business_id, update_data):
    db = get_db()
    return db.businesses.update_one({"_id": business_id}, {"$set": update_data})

def get_all_businesses():
    db = get_db()
    return list(db.businesses.find({}))

def search_businesses(keyword):
    db = get_db()
    return list(db.businesses.find({"$text": {"$search": keyword}}))
