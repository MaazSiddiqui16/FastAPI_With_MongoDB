# 🎓 FastAPI + MongoDB Student Management System

A mini full-stack CRUD application for managing student records using FastAPI backend and Streamlit frontend with MongoDB database.

## 🚀 Features

- **Create** - Add new student records with auto-incrementing IDs
- **Read** - View all students or fetch a specific student by ID
- **Update** - Update student information partially
- **Delete** - Remove student records

## 📋 Prerequisites

- Python 3.8+
- MongoDB installed and running locally (or MongoDB Atlas connection string)
- pip (Python package manager)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MHS-007/FastAPI_With_MongoDB.git
   cd FastAPI_With_MongoDB
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Add your MongoDB connection string:
   You can use **either** a cloud MongoDB Atlas or a local MongoDB instance:

### MongoDB Atlas (Recommended)
```
MONGO_USER=your_atlas_username
MONGO_PASS=your_atlas_password
MONGO_CLUSTER=your_atlas_cluster_url
DATABASE_NAME=your_db_name
API_URL=your_api_url
# Do NOT set MONGODB_URL when using Atlas
```

### Local MongoDB (Alternative)
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=your_db_name
API_URL=your_api_url
# Do NOT set MONGO_USER, MONGO_PASS, or MONGO_CLUSTER when running locally
```

- If both approaches are set, `MONGODB_URL` takes precedence.
- Make sure to restart your backend after changing your .env! 

5. **Start MongoDB**
   - Make sure MongoDB is running either on your local machine or using Atlas.
   - Default connection: `mongodb://localhost:27017/`

## 🚀 Running the Application

### Backend (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

3. The API will be available at: `http://127.0.0.1:8000`
   - API Documentation: `http://127.0.0.1:8000/docs`
   - Alternative Docs: `http://127.0.0.1:8000/redoc`

### Frontend (Streamlit)

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. The frontend will open in your browser at: `http://localhost:8501`

## 📡 API Endpoints

### Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Create a new student |
| GET | `/students` | Get all students |
| GET | `/students/{id}` | Get student by ID |
| PUT | `/students/{id}` | Update student by ID |
| DELETE | `/students/{id}` | Delete student by ID |

## 📝 Example Usage

### Create Student
```bash
POST /students
Content-Type: application/json

{
  "Name": "John Doe",
  "Age": 22,
  "Course": "Database Management System",
  "Department": "Software Engineering",
  "GPA": 3.8
}
```

### Get All Students
```bash
GET /students
```

### Get Student by ID
```bash
GET /students/1
```

### Update Student
```bash
PUT /students/1
Content-Type: application/json

{
  "Name": "Jane Doe",
  "GPA": 3.9
}
```

### Delete Student
```bash
DELETE /students/1
```

## 📂 Project Structure

```
FastAPI_with_MongoDB/
├── backend/
│   └── main.py          # FastAPI backend application
├── frontend/
│   └── app.py           # Streamlit frontend application
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # Project documentation
```

## 🛡️ Technologies Used

- **Backend**: FastAPI, Pydantic, PyMongo
- **Frontend**: Streamlit
- **Database**: MongoDB
- **Python**: 3.8+

## 📝 Notes

- The application uses auto-incrementing IDs implemented with MongoDB counters
- Student IDs start from 1 and increment automatically
- The update endpoint accepts partial updates (only send fields you want to change)
- MongoDB connection string can be configured via environment variables

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.