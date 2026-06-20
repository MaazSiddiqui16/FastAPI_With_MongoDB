from pydantic import BaseModel, Field
from datetime import date

class Student(BaseModel):
    Name: str
    Age: int
    Course: str
    Department: str
    GPA: float

class UserSignup(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(..., min_length=1, max_length=20)
    dob: date
    password: str = Field(..., min_length=1)
