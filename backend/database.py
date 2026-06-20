import os
from pymongo import MongoClient, ReturnDocument
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("MONGO_USER")             
PASSWORD = quote_plus(os.getenv("MONGO_PASS") or "")  
CLUSTER = os.getenv("MONGO_CLUSTER")
DATABASE_NAME = os.getenv("DATABASE_NAME")

MONGODB_URL = os.getenv("MONGODB_URL") or f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}/"

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

collection_students = db["students"]
collection_counters = db["counters"]
collection_users = db["users"]

# ✅ Create Counter Document if not exists
if collection_counters.count_documents({"_id": "studentid"}) == 0:
    collection_counters.insert_one({"_id": "studentid", "sequence_value": 0})

def get_next_id():
    counter = collection_counters.find_one_and_update(
        {"_id": "studentid"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return int(counter["sequence_value"]) 
