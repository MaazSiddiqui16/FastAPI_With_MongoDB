# 🎓 FastAPI + MongoDB Student Management System

A full-stack CRUD application for managing student records, now featuring a robust JWT authentication system. Built with a FastAPI backend, a Streamlit frontend, and a MongoDB database.

## 🚀 Features

- **Authentication** - Secure JWT token-based login and signup system with password hashing (bcrypt).
- **User Profiles** - Expanded signup tracking First Name, Last Name, Gender, and Date of Birth.
- **Create** - Add new student records with auto-incrementing IDs.
- **Read** - View all students or fetch a specific student by ID.
- **Update** - Update student information partially.
- **Delete** - Remove student records.
- **Protected Routes** - All student management endpoints are protected and require a valid auth token.

## 📋 Prerequisites

- Python 3.8+
- MongoDB installed and running locally (or MongoDB Atlas connection string)
- pip (Python package manager)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MaazSiddiqui16/FastAPI_With_MongoDB.git
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
   - Create a `.env` file in the root directory.
   - Add your connection and security details:

### MongoDB Atlas & Security Config
```env
MONGO_USER=your_atlas_username
MONGO_PASS=your_atlas_password
MONGO_CLUSTER=your_atlas_cluster_url
DATABASE_NAME=your_db_name
API_URL=http://127.0.0.1:8000

# Required for JWT Authentication
SECRET_KEY=your_super_secret_random_string_here
```

### Local MongoDB (Alternative)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=your_db_name
API_URL=http://127.0.0.1:8000
SECRET_KEY=your_super_secret_random_string_here
```

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

### Frontend (Streamlit)

1. Open a new terminal, activate your virtual environment, and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. The frontend will open in your browser at: `http://localhost:8501`

## 📡 API Endpoints

### Auth Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register a new user |
| POST | `/login` | Authenticate and retrieve JWT token |

### Protected CRUD Routes
*Note: All routes below require the `Authorization: Bearer <token>` header.*

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Create a new student |
| GET | `/students` | Get all students |
| GET | `/students/{id}` | Get student by ID |
| PUT | `/students/{id}` | Update student by ID |
| DELETE | `/students/{id}` | Delete student by ID |

## 📂 Project Structure

```text
FastAPI_with_MongoDB/
├── backend/
│   ├── auth.py          # JWT and password hashing logic
│   ├── database.py      # MongoDB connection and configurations
│   ├── main.py          # FastAPI application and route definitions
│   └── models.py        # Pydantic schemas for data validation
├── frontend/
│   └── app.py           # Streamlit frontend with auth state management
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 🛡️ Technologies Used

- **Backend**: FastAPI, Pydantic, PyMongo, passlib[bcrypt], PyJWT
- **Frontend**: Streamlit, Requests
- **Database**: MongoDB
- **Python**: 3.8+

## 📝 Notes

- The application uses auto-incrementing IDs implemented with MongoDB counters for students.
- User authentication uses robust JSON Web Tokens (JWT). Passwords are never stored in plain text.
- The Streamlit UI intelligently renders based on `st.session_state` to ensure an organized flow between unauthenticated users and logged-in dashboard users.
- MongoDB connection strings and security keys are managed securely via environment variables.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.