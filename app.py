import streamlit as st
import matplotlib.pyplot as plt
import time
import random
from wordcloud import WordCloud

from job_roles import job_roles
from resume_parser import extract_text
from skill_matcher import match_skills


# ---------- UI STYLE ----------
st.markdown("""
<style>

[data-testid="stSidebar"] {
background: linear-gradient(180deg,#1f4037,#99f2c8);
color:white;
}

.stApp {
background: linear-gradient(-45deg,#0f2027,#203a43,#2c5364,#00c6ff);
background-size: 400% 400%;
animation: gradient 12s ease infinite;
}

@keyframes gradient {
0% {background-position:0% 50%;}
50% {background-position:100% 50%;}
100% {background-position:0% 50%;}
}

</style>
""", unsafe_allow_html=True)


# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_time" not in st.session_state:
    st.session_state.otp_time = None


# ---------- LOGIN ----------
def login():

    st.title("🔐 AI Career Platform Login")

    email = st.text_input("Enter Email")

    if st.button("Send OTP"):

        if email == "":
            st.warning("Please enter email")

        else:

            otp = random.randint(1000,9999)

            st.session_state.otp = otp
            st.session_state.otp_time = time.time()

            st.success(f"Demo OTP: {otp}")

    entered = st.text_input("Enter OTP")

    if st.button("Verify OTP"):

        if st.session_state.otp is None:
            st.warning("Generate OTP first")

        elif time.time() - st.session_state.otp_time > 120:
            st.error("OTP expired. Generate again")

        elif entered == str(st.session_state.otp):

            st.session_state.logged_in = True
            st.success("Login Successful")

        else:
            st.error("Invalid OTP")


# ---------- HOME ----------
def home_page():

    st.title("🚀 AI Career Platform")

    st.markdown("""
### Welcome 👋

This platform helps students and professionals:

- 📄 Analyze resumes  
- 📊 Check job match percentage  
- 🎓 Get career guidance  
- 💼 Discover job platforms  

Upload your resume and discover how well it matches your dream job.
""")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("AI Job Roles", "15+")

    with col2:
        st.metric("Resume Analysis", "Instant")

    with col3:
        st.metric("Career Domains", "4+")

    st.markdown("---")

    st.subheader("🔥 Popular Tech Career Domains")

    st.write("""
• Artificial Intelligence / Machine Learning  
• Web Development  
• Data Science  
• Cyber Security  
• Cloud Computing  
""")


# ---------- RESUME ANALYZER ----------
def resume_analyzer():

    st.title("📄 AI Resume Analyzer")

    role = st.selectbox("Select Job Role", list(job_roles.keys()))

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file:

        with st.spinner("🤖 AI analyzing resume..."):
            time.sleep(2)

        text = extract_text(uploaded_file)

        required_skills = job_roles[role]

        found, missing, score = match_skills(text, required_skills)

        st.subheader("🎯 Job Match Score")

        c1,c2 = st.columns(2)

        with c1:
            st.metric("Match %",f"{score:.1f}%")

        with c2:
            st.metric("Skills Found",len(found))

        st.progress(int(score))

        col1,col2 = st.columns(2)

        with col1:

            st.subheader("✅ Skills Found")

            for s in found:
                st.success(s)

        with col2:

            st.subheader("❌ Missing Skills")

            for m in missing:
                st.error(m)

        st.subheader("💡 Suggestions")

        for m in missing:
            st.warning(f"Consider adding {m}")

        st.subheader("☁ Resume Word Cloud")

        wc = WordCloud(width=800,height=400,background_color="white").generate(text)

        fig,ax = plt.subplots()

        ax.imshow(wc)

        ax.axis("off")

        st.pyplot(fig)


# ---------- CAREER GUIDANCE ----------
def career_page():

    st.title("🎓 Career Guidance")

    domain = st.selectbox(
        "Choose Domain",
        ["AI / Machine Learning","Web Development","Cyber Security","Data Science"]
    )

    if domain=="AI / Machine Learning":

        st.write("""
AI and Machine Learning focuses on building intelligent systems.

Skills Required
- Python
- Machine Learning
- Deep Learning
- TensorFlow

Job Roles
- AI Engineer
- Machine Learning Engineer
- NLP Engineer
""")

    if domain=="Web Development":

        st.write("""
Web development builds websites and applications.

Skills Required
- HTML
- CSS
- JavaScript
- React
- Node.js

Job Roles
- Frontend Developer
- Backend Developer
- Full Stack Developer
""")

    if domain=="Cyber Security":

        st.write("""
Cyber security protects systems from attacks.

Skills Required
- Network Security
- Ethical Hacking
- Linux
- Cryptography
""")

    if domain=="Data Science":

        st.write("""
Data science analyzes large datasets.

Skills Required
- Python
- Pandas
- SQL
- Statistics
""")


# ---------- JOB PLATFORMS ----------
def jobs_page():

    st.title("💼 Where to Apply Jobs")

    st.markdown("""
### Popular Job Platforms

LinkedIn  
https://www.linkedin.com/jobs

Indeed  
https://www.indeed.com

Glassdoor  
https://www.glassdoor.com

Naukri  
https://www.naukri.com

AngelList  
https://angel.co/jobs
""")


# ---------- APP ----------
if not st.session_state.logged_in:

    login()

else:

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Go to",
        ["Home","Resume Analyzer","Career Guidance","Job Platforms"]
    )

    if page == "Home":
        home_page()

    if page == "Resume Analyzer":
        resume_analyzer()

    if page == "Career Guidance":
        career_page()

    if page == "Job Platforms":
        jobs_page()

    st.sidebar.markdown("---")
    st.sidebar.write("Made by **Vikas Barigidad**")