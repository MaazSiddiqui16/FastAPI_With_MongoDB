import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL")

# Ensure API_URL is configured to avoid confusing failures
if not API_URL:
    st.error("API_URL is not set. Define it in your environment or .env file.")
    st.stop()

st.set_page_config(page_title="Student Dashboard", page_icon="🎓", layout="wide")

st.title("🎓 Student Management Dashboard")
st.markdown("Manage students using FastAPI + MongoDB")

# Flash message renderer (auto-dismiss toast, then clear state)
flash = st.session_state.get("flash")
if flash:
    icon = "✅" if flash.get("type") == "success" else ("❌" if flash.get("type") == "error" else "ℹ️")
    st.toast(flash.get("msg", ""), icon=icon)
    if "flash" in st.session_state:
        del st.session_state["flash"]

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
tabs = st.tabs(["Add Student", "View Students", "Update Student", "Delete Student"])


def fetch_students():
    try:
        res = requests.get(f"{API_URL}/students", timeout=10)
        if res.ok:
            return res.json()
        st.error(f"Error fetching students: {res.status_code}")
    except requests.RequestException as e:
        st.error(f"Error fetching students: {e}")
    return []

# ================= ADD STUDENT =================
with tabs[0]:
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
            res = requests.post(f"{API_URL}/students", json=data, timeout=10)

            if res.status_code == 200:
                st.session_state["flash"] = {"type": "success", "msg": "✅ Student added successfully!"}
            else:
                st.session_state["flash"] = {"type": "error", "msg": "❌ Failed to add student!"}
            st.session_state["reset_add_form"] = True
            st.rerun()

# ================= VIEW STUDENTS =================
with tabs[1]:
    st.subheader("All Students")
    students = fetch_students()
    if students:
        st.dataframe(students, width="stretch", hide_index=True)
    else:
        st.info("No students found.")

# ================= UPDATE STUDENT =================
with tabs[2]:
    st.subheader("Update Student Details")
    student_id = st.text_input("Enter Student ID to Update", key="upd_id")
    new_name = st.text_input("New Name (leave blank to skip)", key="upd_name")
    new_age = st.number_input("New Age (0 = skip)", min_value=0, max_value=100, key="upd_age")
    new_course = st.text_input("New Course (optional)", key="upd_course")
    new_department = st.text_input("New Department (optional)", key="upd_department")
    new_gpa = st.number_input("New GPA (0 = skip)", min_value=0.0, max_value=4.0, step=0.1, key="upd_gpa")

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
                    res = requests.put(f"{API_URL}/students/{student_id}", json=update_data, timeout=10)
                    if res.ok:
                        st.session_state["flash"] = {"type": "success", "msg": "✅ Student updated successfully!"}
                    else:
                        st.session_state["flash"] = {"type": "error", "msg": "❌ Failed to update student!"}
                except requests.RequestException as e:
                    st.session_state["flash"] = {"type": "error", "msg": f"❌ Failed to update student: {e}"}
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
                res = requests.delete(f"{API_URL}/students/{delete_id}", timeout=10)
                if res.ok:
                    st.session_state["flash"] = {"type": "success", "msg": "🗑️ Student deleted successfully!"}
                else:
                    st.session_state["flash"] = {"type": "error", "msg": "❌ Failed to delete student!"}
            except requests.RequestException as e:
                st.session_state["flash"] = {"type": "error", "msg": f"❌ Failed to delete student: {e}"}
            st.session_state["reset_delete_form"] = True
            st.rerun()
