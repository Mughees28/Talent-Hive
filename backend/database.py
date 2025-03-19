from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["talent_hive"]


users_collection = db["users"]
tasks_collection = db["tasks"]
bids_collection = db["bids"]
payments_collection = db["payments"]
reviews_collection = db["reviews"]
notifications_collection = db["notifications"]
