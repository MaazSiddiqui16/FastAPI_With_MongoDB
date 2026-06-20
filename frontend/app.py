import streamlit as st
import os
import requests
from dotenv import load_dotenv
from datetime import date

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL")

# Ensure API_URL is configured to avoid confusing failures
if not API_URL:
    st.error("API_URL is not set. Define it in your environment or .env file.")
    st.stop()

st.set_page_config(page_title="Student Dashboard", page_icon="🎓", layout="wide")

# Initialize session state for auth
if "token" not in st.session_state:
    st.session_state["token"] = None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Flash message renderer (auto-dismiss toast, then clear state)
flash = st.session_state.get("flash")
if flash:
    icon = "✅" if flash.get("type") == "success" else ("❌" if flash.get("type") == "error" else "ℹ️")
    st.toast(flash.get("msg", ""), icon=icon)
    if "flash" in st.session_state:
        del st.session_state["flash"]

# ================= AUTHENTICATION UI =================
if not st.session_state["logged_in"]:
    st.title("🎓 Student Management Dashboard")
    st.markdown("Manage students using FastAPI + MongoDB")
    
    auth_tabs = st.tabs(["Login", "Sign Up"])
    
    with auth_tabs[0]:
        st.subheader("Login")
        login_first_name = st.text_input("First Name", key="login_first")
        login_last_name = st.text_input("Last Name", key="login_last")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if not login_first_name.strip() or not login_last_name.strip() or not login_pass.strip():
                st.warning("Please enter your First Name, Last Name, and Password.")
            else:
                login_username = f"{login_first_name.strip()} {login_last_name.strip()}".lower()
                res = requests.post(
                    f"{API_URL}/login", 
                    data={"username": login_username, "password": login_pass}
                )
                if res.ok:
                    data = res.json()
                    st.session_state["token"] = data["access_token"]
                    st.session_state["first_name"] = data.get("first_name", login_first_name)
                    st.session_state["last_name"] = data.get("last_name", login_last_name)
                    st.session_state["logged_in"] = True
                    st.session_state["flash"] = {"type": "success", "msg": "Logged in successfully!"}
                    st.rerun()
                else:
                    st.error("Invalid credentials (Try creating an account using 'Sign Up')")
                
    with auth_tabs[1]:
        st.subheader("Sign Up")
        
        col1, col2 = st.columns(2)
        with col1:
            signup_first_name = st.text_input("First Name", key="signup_first")
            signup_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="signup_gender")
        with col2:
            signup_last_name = st.text_input("Last Name", key="signup_last")
            signup_dob = st.date_input("Date of Birth", key="signup_dob", min_value=date(1900, 1, 1), max_value=date.today())
            
        signup_pass = st.text_input("New Password", type="password", key="signup_pass")
        
        if st.button("Sign Up"):
            if not signup_first_name.strip() or not signup_last_name.strip() or not signup_pass.strip():
                st.warning("Please provide all required fields correctly.")
            else:
                res = requests.post(
                    f"{API_URL}/signup", 
                    json={
                        "first_name": signup_first_name.strip(),
                        "last_name": signup_last_name.strip(),
                        "gender": signup_gender,
                        "dob": str(signup_dob),
                        "password": signup_pass
                    }
                )
                if res.ok:
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error(res.json().get("detail", "Error creating account"))

    st.stop() # Stop rendering the rest of the app if not logged in

# ================= LOGGED IN APP =================
col1, col2 = st.columns([8, 1])
with col1:
    st.title("🎓 Student Management Dashboard")
    st.markdown("Manage students using FastAPI + MongoDB")
    st.write(f"### Welcome, {st.session_state.get('first_name', '')} {st.session_state.get('last_name', '')} 🎉")
with col2:
    if st.button("Logout", use_container_width=True):
        st.session_state["token"] = None
        st.session_state["logged_in"] = False
        st.session_state["flash"] = {"type": "info", "msg": "Logged out."}
        st.rerun()

def get_headers():
    return {"Authorization": f"Bearer {st.session_state['token']}"}

# Apply pending form resets BEFORE widgets are instantiated
if st.session_state.get("reset_add_form"):
    st.session_state["add_name"] = ""
    st.session_state["add_age"] = 1
    st.session_state["add_course"] = ""
    st.session_state["add_department"] = ""
    st.session_state["add_gpa"] = 0.0
    del st.session_state["reset_add_form"]

if st.session_state.get("reset_update_form"):
    st.session_state["upd_id"] = ""
    st.session_state["upd_name"] = ""
    st.session_state["upd_age"] = 0
    st.session_state["upd_course"] = ""
    st.session_state["upd_department"] = ""
    st.session_state["upd_gpa"] = 0.0
    del st.session_state["reset_update_form"]

if st.session_state.get("reset_delete_form"):
    st.session_state["del_id"] = ""
    del st.session_state["reset_delete_form"]

# Tabs for better organization
tabs = st.tabs(["View Students", "Add Student", "Update Student", "Delete Student"])

def fetch_students():
    try:
        res = requests.get(f"{API_URL}/students", headers=get_headers(), timeout=10)
        if res.status_code == 401:
            st.session_state["logged_in"] = False
            st.session_state["token"] = None
            st.rerun()
        if res.ok:
            return res.json()
        st.error(f"Error fetching students: {res.status_code}")
    except requests.RequestException as e:
        st.error(f"Error fetching students: {e}")
    return []

# ================= VIEW STUDENTS =================
with tabs[0]:
    st.subheader("All Students")
    students = fetch_students()
    if students:
        st.dataframe(students, width="stretch", hide_index=True)
    else:
        st.info("No students found.")

# ================= ADD STUDENT =================
with tabs[1]:
    st.subheader("Add New Student")
    name = st.text_input("Name", key="add_name")
    age = st.number_input("Age", min_value=1, max_value=100, key="add_age")
    course = st.text_input("Course", key="add_course")
    department = st.text_input("Department", key="add_department")
    gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, step=0.1, key="add_gpa")

    if st.button("Add Student"):
        if not name.strip() or not course.strip() or not department.strip():
            st.warning("Please fill in all fields: Name, Course, and Department are required.")
        else:
            data = {"Name": name, "Age": age, "Course": course, "Department": department, "GPA": gpa}
            res = requests.post(f"{API_URL}/students", json=data, headers=get_headers(), timeout=10)

            if res.status_code == 200:
                st.session_state["flash"] = {"type": "success", "msg": "Student added successfully!"}
            else:
                st.session_state["flash"] = {"type": "error", "msg": "Failed to add student!"}
            st.session_state["reset_add_form"] = True
            st.rerun()

# ================= UPDATE STUDENT =================
with tabs[2]:
    st.subheader("Update Student Details")
    student_id = st.text_input("Student ID (Required)", key="upd_id")
    new_name = st.text_input("Name (leave blank to skip)", key="upd_name")
    new_age = st.number_input("Age (0 = skip)", min_value=0, max_value=100, key="upd_age")
    new_course = st.text_input("Course (optional)", key="upd_course")
    new_department = st.text_input("Department (optional)", key="upd_department")
    new_gpa = st.number_input("GPA (0 = skip)", min_value=0.0, max_value=4.0, step=0.1, key="upd_gpa")

    if st.button("Update Student"):
        if not student_id.strip():
            st.warning("Student ID is required.")
        else:
            update_data = {}
            if new_name:
                update_data["Name"] = new_name
            if new_age > 0:
                update_data["Age"] = new_age
            if new_course:
                update_data["Course"] = new_course
            if new_department:
                update_data["Department"] = new_department
            if new_gpa > 0:
                update_data["GPA"] = new_gpa

            if not update_data:
                st.info("Nothing to update. Provide at least one new value.")
            else:
                try:
                    res = requests.put(f"{API_URL}/students/{student_id}", json=update_data, headers=get_headers(), timeout=10)
                    if res.ok:
                        st.session_state["flash"] = {"type": "success", "msg": "Student updated successfully!"}
                    else:
                        st.session_state["flash"] = {"type": "error", "msg": "Failed to update student!"}
                except requests.RequestException as e:
                    st.session_state["flash"] = {"type": "error", "msg": f"Failed to update student: {e}"}
                st.session_state["reset_update_form"] = True
                st.rerun()

# ================= DELETE STUDENT =================
with tabs[3]:
    st.subheader("Delete Student")
    delete_id = st.text_input("Enter Student ID to Delete", key="del_id")

    if st.button("Delete Student"):
        if not delete_id.strip():
            st.warning("Student ID is required.")
        else:
            try:
                res = requests.delete(f"{API_URL}/students/{delete_id}", headers=get_headers(), timeout=10)
                if res.ok:
                    st.session_state["flash"] = {"type": "success", "msg": "Student deleted successfully!"}
                else:
                    st.session_state["flash"] = {"type": "error", "msg": "Student doesn't exist!"}
            except requests.RequestException as e:
                st.session_state["flash"] = {"type": "error", "msg": f"Failed to delete student: {e}"}
            st.session_state["reset_delete_form"] = True
            st.rerun()
