from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

# Import from our new modules
from database import collection_students, collection_users, get_next_id
from models import Student, UserSignup
from auth import (
    verify_password, get_password_hash, create_access_token, 
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="🎓 FastAPI + MongoDB Student CRUD")

# ========================
# 🔐 AUTH ROUTES
# ========================
@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup):
    # Create a unique username identifier based on first and last name
    username = f"{user.first_name.strip()} {user.last_name.strip()}".lower()
    
    if collection_users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Account with this name already exists")
    
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "username": username,
        "first_name": user.first_name.strip(),
        "last_name": user.last_name.strip(),
        "gender": user.gender.strip(),
        "dob": str(user.dob),
        "hashed_password": hashed_password
    }
    collection_users.insert_one(user_dict)
    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user by generated username
    user = collection_users.find_one({"username": form_data.username.lower()})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "first_name": user.get("first_name", ""),
        "last_name": user.get("last_name", "")
    }

# ========================
# 🧩 CREATE
# ========================
@app.post("/students")
def add_student(student: Student, current_user: str = Depends(get_current_user)):
    new_id = get_next_id()
    student_dict = student.model_dump()
    student_dict["ID"] = new_id
    collection_students.insert_one(student_dict)
    return {"message": "Student added successfully", "ID": new_id}

# ========================
# 📋 READ ALL
# ========================
@app.get("/students")
def get_all_students(current_user: str = Depends(get_current_user)):
    students = list(collection_students.find({}, {"_id": 0}))
    return students

# ========================
# 🔍 READ ONE (by ID)
# ========================
@app.get("/students/{id}")
def get_student(id: int, current_user: str = Depends(get_current_user)):
    student = collection_students.find_one({"ID": id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ========================
# ✏️ UPDATE (by ID)
# ========================
@app.put("/students/{id}")
def update_student(id: int, updated_data: dict, current_user: str = Depends(get_current_user)):
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
def delete_student(id: int, current_user: str = Depends(get_current_user)):
    result = collection_students.delete_one({"ID": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
