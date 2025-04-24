from pymongo import MongoClient
from modules.config import get_mongo_uri

client = MongoClient(get_mongo_uri())
db = client["township_directory"]
businesses = db["businesses"]
users = db["users"]
ads = db["ads"]
