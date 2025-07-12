import streamlit as st
import bcrypt
import json
import os
from PyPDF2 import PdfReader

# -------------------------------
# USER AUTH SYSTEM
# -------------------------------

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
                st.rerun()  # ✅ Updated from experimental
            else:
                st.sidebar.error("Invalid credentials!")

# -------------------------------
# STOP IF USER NOT LOGGED IN
# -------------------------------

if "user" not in st.session_state:
    login_signup()
    st.stop()

# -------------------------------
# MAIN APP STARTS HERE
# -------------------------------

st.title("🔍 AI Career Guidance System")

st.success(f"Hello, {st.session_state['user']}! Let's discover your ideal career path.")

# 🔓 Logout Button
if st.button("Logout"):
    del st.session_state["user"]
    st.success("You have been logged out.")
    st.rerun()  # ✅ Updated from experimental

# -----------------------------------
# SECTION 1: Career Questionnaire
# -----------------------------------

st.header("🚀 Career Guidance Questionnaire")

interests = st.multiselect("What are your interests?", ["Technology", "Science", "Art", "Finance", "Healthcare"])
activities = st.multiselect("Preferred work activities?", ["Working with people", "Analyzing data", "Creating content", "Managing projects"])
strengths = st.multiselect("Your strengths?", ["Communication", "Problem-solving", "Leadership", "Creativity"])
work_values = st.multiselect("What do you value most in a job?", ["Job Security", "High Salary", "Work-Life Balance", "Helping Others"])

# -----------------------------------
# SECTION 2: Personality Quiz
# -----------------------------------

st.header("🧠 Personality Insights")

q1 = st.radio("Do you enjoy leading teams?", ["Yes", "No", "Sometimes"])
q2 = st.radio("Are you more analytical or creative?", ["Analytical", "Creative", "Both"])
q3 = st.radio("Do you like working with technology?", ["Yes", "No", "Neutral"])

# -----------------------------------
# SECTION 3: Career Suggestions
# -----------------------------------

if st.button("Generate Career Recommendation"):
    st.subheader("🎯 Recommended Careers")

    career_suggestions = []

    # From career questions
    if "Technology" in interests and "Problem-solving" in strengths:
        career_suggestions.append("Software Developer")
    if "Finance" in interests and "Analyzing data" in activities:
        career_suggestions.append("Financial Analyst")
    if "Art" in interests and "Creativity" in strengths:
        career_suggestions.append("Graphic Designer")
    if "Helping Others" in work_values and "Communication" in strengths:
        career_suggestions.append("HR Manager")

    # From personality quiz
    if q1 == "Yes" and q2 == "Analytical":
        career_suggestions.append("Project Manager")
    if q2 == "Creative":
        career_suggestions.append("Marketing Strategist")
    if q3 == "Yes":
        career_suggestions.append("IT Consultant")

    if career_suggestions:
        for career in set(career_suggestions):
            st.markdown(f"- **{career}**")
    else:
        st.warning("No clear matches found. Try adjusting your answers.")

# -----------------------------------
# SECTION 4: Resume Upload
# -----------------------------------

st.header("📄 Upload Your Resume (PDF)")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text()
        st.success("Resume uploaded and text extracted!")
        st.text_area("📄 Extracted Resume Text:", resume_text[:2000], height=200)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
