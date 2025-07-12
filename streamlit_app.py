import streamlit as st
import bcrypt
import json
import os
from PyPDF2 import PdfReader
from datetime import datetime

# -------------------------------
# USER AUTH SYSTEM
# -------------------------------

USER_DB = "users.json"
RESPONSES_DIR = "responses"

if not os.path.exists(RESPONSES_DIR):
    os.makedirs(RESPONSES_DIR)

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
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials!")

if "user" not in st.session_state:
    login_signup()
    st.stop()

# -------------------------------
# MAIN APP UI
# -------------------------------

st.title("🔍 AI Career Guidance System")

st.success(f"Hello, {st.session_state['user']}! Let's explore your ideal career path.")

if st.button("Logout"):
    del st.session_state["user"]
    st.success("You have been logged out.")
    st.rerun()

# -------------------------------
# TABS
# -------------------------------

tab1, tab2, tab3 = st.tabs(["🧠 Career Quiz", "📄 Resume Analysis", "📥 Report & Save"])

# -------------------------------
# TAB 1: CAREER QUIZ
# -------------------------------

with tab1:
    st.header("🚀 Career Guidance Questionnaire")

    interests = st.multiselect("What are your interests?", ["Technology", "Science", "Art", "Finance", "Healthcare"])
    activities = st.multiselect("Preferred work activities?", ["Working with people", "Analyzing data", "Creating content", "Managing projects"])
    strengths = st.multiselect("Your strengths?", ["Communication", "Problem-solving", "Leadership", "Creativity"])
    work_values = st.multiselect("What do you value most in a job?", ["Job Security", "High Salary", "Work-Life Balance", "Helping Others"])

    st.header("🧠 Personality Quiz")
    q1 = st.radio("Do you enjoy leading teams?", ["Yes", "No", "Sometimes"])
    q2 = st.radio("Are you more analytical or creative?", ["Analytical", "Creative", "Both"])
    q3 = st.radio("Do you like working with technology?", ["Yes", "No", "Neutral"])

    st.header("📊 Skill Confidence (Rate 1–10)")
    tech = st.slider("Tech Skills", 1, 10, 5)
    comm = st.slider("Communication", 1, 10, 5)
    lead = st.slider("Leadership", 1, 10, 5)

# -------------------------------
# TAB 2: RESUME UPLOAD & ANALYSIS
# -------------------------------

with tab2:
    st.header("📄 Upload Your Resume (PDF)")

    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    resume_text = ""

    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                resume_text += page.extract_text()
            st.success("Resume uploaded and text extracted!")
            st.text_area("📃 Resume Preview:", resume_text[:2000], height=200)
        except Exception as e:
            st.error(f"Failed to extract text: {e}")

# -------------------------------
# TAB 3: REPORT & RECOMMENDATIONS
# -------------------------------

with tab3:
    st.header("🎯 Career Recommendations")

    career_suggestions = []

    if "Technology" in interests and "Problem-solving" in strengths:
        career_suggestions.append("Software Developer")
    if "Finance" in interests and "Analyzing data" in activities:
        career_suggestions.append("Financial Analyst")
    if "Art" in interests and "Creativity" in strengths:
        career_suggestions.append("Graphic Designer")
    if "Helping Others" in work_values and "Communication" in strengths:
        career_suggestions.append("HR Manager")
    if q1 == "Yes" and q2 == "Analytical":
        career_suggestions.append("Project Manager")
    if q2 == "Creative":
        career_suggestions.append("Marketing Strategist")
    if q3 == "Yes":
        career_suggestions.append("IT Consultant")

    if resume_text:
        if "Python" in resume_text or "Machine Learning" in resume_text:
            career_suggestions.append("Data Scientist")
        if "Sales" in resume_text or "CRM" in resume_text:
            career_suggestions.append("Sales Executive")

    if career_suggestions:
        st.success("We recommend exploring these roles:")
        for career in set(career_suggestions):
            st.markdown(f"- **{career}**")
    else:
        st.warning("No strong matches found. Try adjusting your answers.")

    st.subheader("📥 Download Career Report")

    if st.button("Download Report"):
        report_text = f"""Career Report for {st.session_state['user']}

Interests: {interests}
Activities: {activities}
Strengths: {strengths}
Work Values: {work_values}
Personality: {q1}, {q2}, {q3}
Resume Keywords Found: {', '.join(set(resume_text.split()) & {'Python', 'ML', 'Sales', 'CRM'}) if resume_text else 'None'}

Recommended Careers:
{chr(10).join(['- ' + c for c in set(career_suggestions)])}
"""
        st.download_button("📄 Click to Download", report_text, file_name="career_report.txt")

    st.subheader("💾 Save Response for Later")

    if st.button("Save Progress"):
        user_file = os.path.join(RESPONSES_DIR, f"{st.session_state['user']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        data = {
            "user": st.session_state["user"],
            "interests": interests,
            "activities": activities,
            "strengths": strengths,
            "work_values": work_values,
            "personality": [q1, q2, q3],
            "skills": {"Tech": tech, "Communication": comm, "Leadership": lead},
            "resume_keywords": list(set(resume_text.split()) & {"Python", "ML", "Sales", "CRM"}) if resume_text else [],
            "suggestions": list(set(career_suggestions)),
            "timestamp": datetime.now().isoformat()
        }
        with open(user_file, "w") as f:
            json.dump(data, f, indent=2)
        st.success(f"Responses saved as `{user_file}`")
