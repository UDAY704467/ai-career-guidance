import streamlit as st
import bcrypt
import json
import os
from PyPDF2 import PdfReader

USER_DB = "users.json"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_signup():
    users = load_users()
    option = st.sidebar.selectbox("Login or Sign Up", ["Login", "Sign Up"])

    if option == "Sign Up":
        st.sidebar.subheader("📝 Create an Account")
        new_user = st.sidebar.text_input("Username")
        new_pass = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Register"):
            if new_user in users:
                st.sidebar.warning("User already exists!")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.sidebar.success("Registered! Please log in.")

    elif option == "Login":
        st.sidebar.subheader("🔐 Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if username in users and check_password(password, users[username]):
                st.session_state["user"] = username
                st.sidebar.success(f"Welcome back, {username}!")
                st.experimental_rerun()  # 🔁 Important!
            else:
                st.sidebar.error("Invalid credentials!")

# ----------------------
# STOP if user not logged in
# ----------------------
if "user" not in st.session_state:
    login_signup()
    st.stop()

# ----------------------
# MAIN APP STARTS HERE
# ----------------------

# ✅ This block only runs after login
st.success(f"Hello, {st.session_state['user']}! Let's find your ideal career path.")

st.header("🚀 Career Guidance Questionnaire")

interests = st.multiselect("What are your interests?", ["Technology", "Science", "Art", "Finance", "Healthcare"])
activities = st.multiselect("Preferred work activities?", ["Working with people", "Analyzing data", "Creating content", "Managing projects"])
strengths = st.multiselect("Your strengths?", ["Communication", "Problem-solving", "Leadership", "Creativity"])
work_values = st.multiselect("What do you value most in a job?", ["Job Security", "High Salary", "Work-Life Balance", "Helping Others"])

if st.button("Generate Career Recommendation"):
    st.subheader("🎯 Recommended Careers")
    if "Technology" in interests:
        st.markdown("- **Software Engineer**")
    if "Finance" in interests:
        st.markdown("- **Financial Analyst**")
    if "Art" in interests:
        st.markdown("- **UX Designer**")

# Resume Upload
st.header("📄 Upload Your Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        st.text_area("Extracted Resume Text", text, height=200)
    except Exception as e:
        st.error(f"Could not read PDF: {e}")
