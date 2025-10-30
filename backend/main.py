import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient, ReturnDocument
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================
# 🚀 FastAPI + MongoDB Atlas (Cloud) Connection
# ==========================================

app = FastAPI(title="🎓 FastAPI + MongoDB Student CRUD")

# ✅ Connect to MongoDB
USERNAME = os.getenv("MONGO_USER")             
PASSWORD = quote_plus(os.getenv("MONGO_PASS"))  
CLUSTER = os.getenv("MONGO_CLUSTER")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Build MongoDB connection string (cloud or local)
MONGODB_URL = os.getenv("MONGODB_URL") or f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}/"

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
collection_students = db["students"]
collection_counters = db["counters"]

# ✅ Create Counter Document if not exists
if collection_counters.count_documents({"_id": "studentid"}) == 0:
    collection_counters.insert_one({"_id": "studentid", "sequence_value": 0})

# ✅ Function to get next ID
def get_next_id():
    counter = collection_counters.find_one_and_update(
        {"_id": "studentid"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return int(counter["sequence_value"]) 

# ✅ Student Model
class Student(BaseModel):
    Name: str
    Age: int
    Course: str
    Department: str
    GPA: float

# ========================
# 🧩 CREATE
# ========================
@app.post("/students")
def add_student(student: Student):
    new_id = get_next_id()
    student_dict = student.model_dump()
    student_dict["ID"] = new_id
    collection_students.insert_one(student_dict)
    return {"message": "Student added successfully", "ID": new_id}

# ========================
# 📋 READ ALL
# ========================
@app.get("/students")
def get_all_students():
    students = list(collection_students.find({}, {"_id": 0}))
    return students

# ========================
# 🔍 READ ONE (by ID)
# ========================
@app.get("/students/{id}")
def get_student(id: int):
    student = collection_students.find_one({"ID": id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ========================
# ✏️ UPDATE (by ID)
# ========================
@app.put("/students/{id}")
def update_student(id: int, updated_data: dict):
    # Validate allowed fields
    allowed_fields = {"Name", "Age", "Course", "Department", "GPA"}
    clean_data = {k: v for k, v in updated_data.items() if k in allowed_fields and v not in [None, ""]}
    
    if not clean_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    result = collection_students.update_one({"ID": id}, {"$set": clean_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}

# ========================
# ❌ DELETE (by ID)
# ========================
@app.delete("/students/{id}")
def delete_student(id: int):
    result = collection_students.delete_one({"ID": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
