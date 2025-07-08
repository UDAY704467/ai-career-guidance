import streamlit as st

# ---- PAGE CONFIG ----
st.set_page_config(page_title="AI Career Guidance", layout="centered")

# ---- TITLE ----
st.title("🎓 AI-Enhanced Career Guidance System")
st.markdown("Find your ideal career path through personalized AI-driven suggestions.")

# ---- USER INFO ----
st.header("📋 Step 1: Tell us about yourself")

name = st.text_input("Your Name")
age = st.number_input("Your Age", min_value=13, max_value=60)
education = st.selectbox(
    "Current Education Level",
    ["High School", "Undergraduate", "Postgraduate", "Working Professional"]
)

# ---- APTITUDE & INTEREST ----
aptitude = st.multiselect(
    "What are your strong aptitudes?",
    ["Analytical Thinking", "Creativity", "Problem Solving", "Leadership", "Communication", "Coding", "Design Thinking"]
)

interests = st.text_area("What are your career interests or long-term goals?")
skills = st.text_area("List your top 3 skills (technical or non-technical)")
experience = st.text_area("Mention any work, internship, or project experience")

# ---- LEARNING & FUTURE STYLE ----
learning_style = st.radio(
    "What type of learning do you prefer?",
    ["Hands-on/Practical", "Theoretical", "Visual/Creative", "Collaborative/Team-based"]
)

future_pref = st.selectbox(
    "What kind of future job do you imagine for yourself?",
    ["Corporate Job", "Startup/Freelance", "Government Sector", "Research/Academia", "Entrepreneurship"]
)

# ---- CAREER SUGGESTION LOGIC ----
if st.button("🎯 Get Career Recommendations"):
    st.subheader(f"Hi {name}, here are some personalized suggestions for you:")

    if "Analytical Thinking" in aptitude or "data" in interests.lower():
        st.success("📊 Recommended: Data Analyst, Business Analyst, AI/ML Engineer")
    
    if "Creativity" in aptitude or "design" in interests.lower():
        st.success("🎨 Recommended: UI/UX Designer, Graphic Designer, Creative Director")
    
    if "Leadership" in aptitude or future_pref == "Entrepreneurship":
        st.success("🚀 Recommended: Startup Founder, Product Manager, Business Consultant")
    
    if "Coding" in aptitude or "software" in interests.lower():
        st.success("💻 Recommended: Software Developer, Web Developer, App Developer")
    
    if "Communication" in aptitude or "marketing" in interests.lower():
        st.success("📢 Recommended: Marketing Manager, PR Specialist, Content Creator")
    
    if education == "Postgraduate" and "research" in interests.lower():
        st.success("🔬 Recommended: Research Scientist, Professor, Academic Researcher")

    st.info("✅ Based on your input, we suggest you explore certification platforms like Coursera, LinkedIn Learning, and Internshala to get started.")

    st.caption("Note: These suggestions are based on your responses and simplified logic. An advanced AI version can further enhance personalization.")

